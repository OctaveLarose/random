import itertools
import sys
from treelib import Node, Tree
from itertools import count

from rubybridge import RubySession


def are_subtrees_equal(subtree1, subtree2) -> bool:
    # Probably wrong-ish, pretty sure it would return True for subtrees with the same nodes but differing hierarchies
    for a, b in zip(subtree1.nodes.items(), subtree2.nodes.items()):
        if a[1].tag != b[1].tag:
            return False
    return True


# Dubious moral choice right there, but who's judging
Tree.__eq__ = are_subtrees_equal


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


def print_recurring_node_groups(supernode_occurrences):
    for supernode, nbr_found in supernode_occurrences.items():
        print("{} found:".format(nbr_found))
        print(supernode)
    pass


def add_supernode_occurrence(supernode_occurrences: dict, new_supernode):
    for supernode in supernode_occurrences:
        if supernode == new_supernode:
            supernode_occurrences[supernode] += 1
            return

    supernode_occurrences[new_supernode] = 1


def main(argv: [str]):
    rb = RubySession()
    rb.require_relative('bgv_parser.rb')
    BGV_PARSER_CLASS = rb.const('BGVParser')

    graph_index = int(argv[2]) if len(argv) >= 3 else None

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

        if graph_index is not None and graph_index != index[0]:
            continue

        node_tree = get_node_tree(graph)
        # node_tree.show()

        all_subtrees = []
        for n in node_tree.expand_tree(mode=Tree.DEPTH):
            if len(node_tree.subtree(n).nodes) != 1:  # Dumping single node subtrees
                all_subtrees.append(node_tree.subtree(n))

        permutations = itertools.permutations(all_subtrees, 2)

        supernode_occurrences = {}
        for a, b in permutations:
            if a == b:
                add_supernode_occurrence(supernode_occurrences, a)

        print_recurring_node_groups(supernode_occurrences)

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

