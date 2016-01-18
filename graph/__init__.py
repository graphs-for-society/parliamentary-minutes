# -*- coding: utf-8 -*-
import json
import os

from graphcommons import GraphCommons, Signal


class GraphApi(object):

    def __init__(self, api_key, graph_id):
        if graph_id:
            self.graph_id = graph_id

        self.api = GraphCommons(api_key)
        self.graph = None

    def create_new_graph(self, graph_name, subtitle, description):

        graph = self.api.new_graph(
                name=graph_name,
                subtitle=subtitle,
                description=description,
                signals=[]
        )
        print("Created a graph with id {}".format(graph['id']))
        self.graph_id = graph['id']
        return self.graph_id

    @staticmethod
    def create_signals(input_filename):
        result = []
        f = open(input_filename, "r")
        line = f.readline()
        while line:
            line = line.strip()
            obj = json.loads(line)
            result.append(Signal(**obj))
            line = f.readline()
        f.close()
        return result

    def get_nodes_by_node_type(self, node_type):
        graph = self.get_graph()
        return filter(lambda node: node.type == node_type, graph.nodes)

    @staticmethod
    def create_nodetype_dicts(nodes):
        names = [node.name for node in nodes]
        node_dict = dict(zip(names, nodes))
        return node_dict

    def get_graph(self, refresh=False):
        if self.graph is None or refresh:
            graph = self.api.graphs(self.graph_id)
            self.graph = graph
        return self.graph

    def get_all_node_types(self):
        graph = self.get_graph()
        node_types = [t.name for t in graph._node_types.values()]
        return dict((t, self.get_nodes_by_node_type(t)) for t in node_types)

    def get_node_ids_types_names(self):
        types = self.get_all_node_types()
        for t, nodes in types.iteritems():
            for node in nodes:
                yield node.name, node.id, t

    def get_paths(self, from_id, to_id, **kwargs):

        d = {"from": from_id, "to": to_id}
        d.update(kwargs)  # add other key-value pairs.

        paths = self.api.paths(self.graph_id, d)
        to_return = []
        for p in paths:
            speech = p['nodes'][1]
            to_return.append(dict(reference=speech.reference, path_string=p['path_string']))

        return to_return

    def upsert_edges(self, signals, chunk_size=100):
        for i in range(0, len(signals) / chunk_size + 1):
            # print signals[i*chunk_size:(i+1)*chunk_size]
            self.api.update_graph(
                    id=self.graph_id,
                    signals=signals[i * chunk_size:(i + 1) * chunk_size]
            )
            print("Updated graph... {} of {}".format(min((i + 1) * chunk_size, len(signals)), len(signals)))


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("input_filename")

    parser.add_argument("--version", nargs="?")
    parser.add_argument("--graph-id", nargs="?")
    parser.add_argument("--api-key", required=False, default=None)
    args = parser.parse_args()
    return args


def test():
    args = parse_arguments()
    api = GraphApi(args.api_key, args.graph_id)
    nodes = api.get_node_ids_types_names()
    print list(nodes)


def main():
    args = parse_arguments()
    if args.api_key is not None:
        api_key = args.api_key
    else:
        api_key = os.environ['API_KEY']

    assert api_key is not None, "please either set API_KEY Environment Variable or provide --api-key while running."

    if args.graph_id:
        graph_id = args.graph_id
        graph = GraphApi(api_key, graph_id)
        print graph.api.status()
        signals = graph.create_signals(args.input_filename)
    else:
        new_graph_info = {
            "graph_name": "Meclis Konuşmaları",
            "subtitle": "Meclis genel kurul konuşmalarındaki parti ve milletvekili etkileşimleri günlük olarak haritalanıyor.",
            "description": "Meclis genel kurul konuşmalarındaki parti ve milletvekili etkileşimleri günlük olarak haritalanıyor."
        }
        graph = GraphApi(api_key, None)
        graph_id = graph.create_new_graph(**new_graph_info)

    f = open("graph-id.txt", "w")
    f.write(graph_id + "\n")
    f.close()

    graph.upsert_edges(signals)

if __name__ == "__main__":
    test()

