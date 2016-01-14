# -*- coding: utf-8 -*-
import json

import ConfigParser

config = ConfigParser.ConfigParser()

config.read("config.ini")

api_key = config.get("api", "api_key")
graph_id = config.get("graph", "graph_id")

from graphcommons import GraphCommons
api = GraphCommons(api_key)

from graphcommons import Signal

def get_nodes(graph, node_type):
    return filter(lambda node: node.type == node_type, graph.nodes)

def create_nodetype_dicts(nodes):
    names = [party.name for party in nodes]
    node_dict = dict(zip(names, nodes))
    return node_dict

def get_paths(rep_name, party):
    graph = api.graphs(graph_id)
    rep_nodes, parties = map(lambda node_type: get_nodes(graph, node_type), ["Milletvekili", "Parti"])
    reps_dict, parties_dict = map(create_nodetype_dicts, [rep_nodes, parties])
    party = unicode(party)
    rep_name = unicode(rep_name)
    party_id = parties_dict[party].id
    rep_id = reps_dict[rep_name].id
    d = {"from": rep_id, "to": party_id, "limit": 30}
    response = api.get_path(graph_id, d)
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

def upsert_edges(signals, chunk_size=100):
    for i in range(0, len(signals)/chunk_size + 1):
        #print signals[i*chunk_size:(i+1)*chunk_size]
        api.update_graph(
            id=graph_id,
            signals=signals[i*chunk_size:(i+1)*chunk_size]
        )
        print("Updated graph... {} of {}".format(min((i+1)*chunk_size, len(signals)), len(signals)))

'''
{
  "action": "edge_create",
  "from_name": "Yahoo",
  "from_type": "Company",
  "name": "ACQUIRED",
  "to_name": "Tumblr",
  "to_type": "Company",
  "properties": {
    "cost": "$1b",
    "year_of_acquisition": 2013
  }
}
'''


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

def create_new_graph(graph_name, subtitle, description):

    graph = api.new_graph(
        name=graph_name,
        subtitle=subtitle,
        description=subtitle,
        signals=[]
    )
    print("Created a graph with id {}".format(graph['id']))
    return graph['id']

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--version", nargs="?")
    parser.add_argument("input_filename")
    parser.add_argument("--graph_id", nargs="?")
    args = parser.parse_args()

    print api.status()

    if args.input_filename:
        signals = create_signals(args.input_filename)

        if args.graph_id:
            graph_id = args.graph_id
        else:
            graph_id = create_new_graph("Meclis Konuşmaları",
                                        "Meclis genel kurul konuşmalarındaki parti ve milletvekili etkileşimleri günlük olarak haritalanıyor.",
                                        "Meclis genel kurul konuşmalarındaki parti ve milletvekili etkileşimleri günlük olarak haritalanıyor.")

        f = open("graph-id.txt", "w")
        f.write(graph_id+"\n")
        f.close()

        upsert_edges(signals)

    #push_changes(args.input_filename)