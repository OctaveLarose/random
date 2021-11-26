import subprocess, time, sys, os, inspect, atexit, re
from pprint import pprint

import msgpack, mprpc


class RubyObject():
    session = None

    @staticmethod
    def cast(obj):
        if isinstance(obj, msgpack.ExtType):
            assert obj.code == 40
            rb_class, obj_id = msgpack.unpackb(obj.data, raw=False)
            return RubyObject(rb_class, obj_id)
        elif isinstance(obj, list):
            return [RubyObject.cast(x) for x in obj]
        elif isinstance(obj, dict):
            return {k: RubyObject.cast(v) for k, v in obj.items()}
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        else:
            return obj

    def __init__(self, rb_class, obj_id):
        self.rb_class = rb_class
        self.obj_id = obj_id

    def __del__(self):
        if self.session:
            self.session.del_object(self.obj_id)

    def __eq__(self, other):
        return self.send('==', other)

    def __dir__(self):
        return self.send('public_methods')

    def __iter__(self):
        return self.send("each")

    def __str__(self):
        return self.send('to_s')

    def __repr__(self):
        return self.send('inspect')

    def __len__(self):
        return self.send("size")

    def __getattr__(self, attr):
        def _method_missing(*args, **kwargs):
            return self.send(attr, *args, **kwargs)

        return _method_missing

    def __getitem__(self, index):
        return self.send('[]', index)

    def send(self, method, *args, **kwargs):
        try:
            obj = self.session.client.call('send_method', self.obj_id, method, args, kwargs)
            return self.cast(obj)
        except mprpc.exceptions.RPCError as ex:
            # data may contain space, single-quote('), double-quote(")
            matched = re.match(r'ExtType\(code=40, data=b(.+)\)', ex.args[0])
            if matched:
                e = msgpack.ExtType(40, eval('b' + matched.group(1)))
                arg = RubyObject.cast(e)
                raise RubyException(arg.message(), arg) from None
            else:
                raise

    # msgpack-rpc-python uses `to_msgpack` method
    def to_msgpack(self):
        return msgpack.ExtType(40, msgpack.packb([self.rb_class, self.obj_id]))

    def __next__(self):
        try:
            return self.send("next")
        except RubyException as ex:
            if ex.rb_exception.rb_class == 'StopIteration':
                raise StopIteration()
            else:
                raise

    def __call__(self, *args, **kwargs):
        if self.rb_class == 'Class':
            return self.send('new', *args, **kwargs)
        else:
            return self.send('call', *args, **kwargs)


class RubyException(Exception):
    def __init__(self, message, rb_exception):
        self.args = (message,)
        self.rb_exception = rb_exception


class RubySession:

    def __init__(self):
        server_rb = os.path.abspath(os.path.join(os.path.dirname(__file__), 'rb_call_server.rb'))

        def setpgrp():
            os.setpgrp()

        self.proc = subprocess.Popen(['bundle', 'exec', 'ruby', server_rb], stdout=subprocess.PIPE, preexec_fn=setpgrp)

        def cleanup():
            RubyObject.session = None
            self.proc.terminate()

        atexit.register(cleanup)
        port = int(self.proc.stdout.readline())
        self.proc.stdout.close()

        def default(obj):
            return obj.to_msgpack()

        self.client = mprpc.RPCClient('localhost', port, pack_encoding=None, unpack_encoding=None,
                                      pack_params={"default": default}, unpack_params={"raw": False})
        RubyObject.session = self
        self.kernel = RubyObject.cast(self.client.call('get_kernel'))

    def del_object(self, obj_id):
        return self.client.call('del_object', obj_id)

    def send_kernel(self, method, *args, **kwargs):
        return self.kernel.send(method, *args, **kwargs)

    def require(self, arg):
        return self.send_kernel('require', arg)

    def require_relative(self, arg):
        caller_path = inspect.stack()[1][1]
        abspath = os.path.abspath(os.path.join(os.path.dirname(caller_path), arg))
        return self.send_kernel('require_relative', abspath)

    def const(self, const_name):
        obj = self.send_kernel("const_get", const_name)
        return RubyObject.cast(obj)


if __name__ == "__main__":
    rb = RubySession()
    rb.require_relative('bgv_parser.rb')
    BGV_PARSER_CLASS = rb.const('BGVParser')

    FILENAME = sys.argv[1]
    bgv_parser = BGV_PARSER_CLASS(FILENAME)
    bgv_parser.read_file_header()
    bgv_parser.skip_document_props()

    while True:
        index = bgv_parser.read_graph_preheader()

        if not index:
            break

        graph_header = bgv_parser.read_graph_header()
        name = bgv_parser.graph_name(graph_header)
        graph = bgv_parser.read_graph()

        print("###")
        # print("GRAPH_HEADER:", graph_header)
        print("NAME:", name)
        print("GRAPH:", graph)
        # print("PROPS:", graph.props())
        # print("NODES:", graph.nodes())
        print("NODE LABELS:")
        for node in graph.nodes().values():
            print(node.props()['label'])
        print("EDGES:", graph.edges())
        print("BLOCKS:", graph.blocks())
        print("###")
