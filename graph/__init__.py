# -*- coding: utf-8 -*-
import json

import ConfigParser

config = ConfigParser.ConfigParser()

config.read("config.ini")

api_key = config.get("api", "api_key")

graph_id = "801746fa-e5bf-4c0b-9b8a-7d300f63cb88"

from graphcommons import GraphCommons
graphcommons = GraphCommons(api_key)

from graphcommons import Signal

def upsert_edges(signals, chunk_size=100):
    for i in range(0, len(signals)/chunk_size + 1):
        #print signals[i*chunk_size:(i+1)*chunk_size]
        graphcommons.update_graph(
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

def get_paths(a, b, c):
    return [1, 2, 3]


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

    graph = graphcommons.new_graph(
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

    print graphcommons.status()

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