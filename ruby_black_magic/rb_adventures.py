import sys

from rubybridge import RubySession


def main(argv: [str]):
    rb = RubySession()
    rb.require_relative('bgv_parser.rb')
    BGV_PARSER_CLASS = rb.const('BGVParser')

    bgv_parser = BGV_PARSER_CLASS(argv[1])
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


if __name__ == "__main__":
    main(sys.argv)

