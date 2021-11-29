import sys
from treelib import Node, Tree

from rubybridge import RubySession


def get_node_tree(graph):
    node_tree = Tree()
    parent_node_set = False

    for edge in graph.edges():
        parent_node_id, node_id = [node.id() for node in edge.nodes()]
        if not parent_node_set:
            node_tree.create_node(parent_node_id, parent_node_id)
            parent_node_set = True
        node_tree.create_node(node_id, node_id, parent=parent_node_id)

    for node_id, node in graph.nodes().items():
        node_tree[node_id].tag = node.props()['label']

    return node_tree


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

        node_tree = get_node_tree(graph)
        node_tree.show()


        # for x in new_tree:
        #     print(x)

        # print("###")
        # # print("GRAPH_HEADER:", graph_header)
        # print("NAME:", name)
        # print("GRAPH:", graph)
        # # print("PROPS:", graph.props())
        # # print("NODES:", graph.nodes())
        # print("NODE LABELS:")
        # for node in graph.nodes().values():
        #     print(node.props()['label'])
        # print("EDGES:", graph.edges())
        # print("BLOCKS:", graph.blocks())
        # print("###")


if __name__ == "__main__":
    main(sys.argv)

