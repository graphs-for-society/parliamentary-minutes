# -*- coding: utf-8 -*-
import json
import os

from graphcommons import GraphCommons, Signal

# import ConfigParser
#
# config = ConfigParser.ConfigParser()
#
# config.read("config.ini")

# api_key = config.get("api", "api_key")
# graph_id = config.get("graph", "graph_id")

api_key = os.environ['API_KEY']
graph_id = os.environ['GRAPH_ID']

class GraphApi():

    def __init__(self, api_key, graph_id):
        # self.api_key = api_key
        if graph_id:
            self.graph_id = graph_id

        self.api = GraphCommons(api_key)

    def create_new_graph(self, graph_name, subtitle, description):

        graph = self.api.new_graph(
                name=graph_name,
                subtitle=subtitle,
                description=subtitle,
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

    @staticmethod
    def get_nodes(graph, node_type):
        return filter(lambda node: node.type == node_type, graph.nodes)

    @staticmethod
    def create_nodetype_dicts(nodes):
        names = [party.name for party in nodes]
        node_dict = dict(zip(names, nodes))
        return node_dict

    def get_paths(self, rep_name, party):
        graph = self.api.graphs(self.graph_id)
        rep_nodes, parties = map(lambda node_type: GraphApi.get_nodes(graph, node_type), ["Milletvekili", "Parti"])
        reps_dict, parties_dict = map(GraphApi.create_nodetype_dicts, [rep_nodes, parties])
        party = unicode(party)
        rep_name = unicode(rep_name)
        party_id = parties_dict[party].id
        rep_id = reps_dict[rep_name].id
        d = {"from": rep_id, "to": party_id, "limit": 30}
        response = self.api.get_path(self.graph_id, d)
        response_nodes = response['nodes']
        to_return = []
        for r in response['paths']:
            d = {}
            # speecher = r['nodes'][0]
            speech_id = r['nodes'][1]
            speech = response_nodes[speech_id]
            d['reference'] = speech['reference']
            d['path_string'] = r['path_string']
            to_return.append(d)

        return to_return

    def upsert_edges(self, signals, chunk_size=100):
        for i in range(0, len(signals) / chunk_size + 1):
            # print signals[i*chunk_size:(i+1)*chunk_size]
            self.api.update_graph(
                    id=self.graph_id,
                    signals=signals[i * chunk_size:(i + 1) * chunk_size]
            )
            print("Updated graph... {} of {}".format(min((i + 1) * chunk_size, len(signals)), len(signals)))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--version", nargs="?")
    parser.add_argument("input_filename")
    parser.add_argument("--graph_id", nargs="?")
    args = parser.parse_args()

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

    # push_changes(args.input_filename)
