import json

api_key = "sk_0G2yPCzKrGLbUz0ODA32rA"

graph_id = "801746fa-e5bf-4c0b-9b8a-7d300f63cb88"

from graphcommons import GraphCommons
graphcommons = GraphCommons(api_key)

from graphcommons import Signal

def upsert_edges(signals):
    graphcommons.update_graph(
        id=graph_id,
        signals=signals
    )

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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--version", nargs="?")
    parser.add_argument("--input_filename", nargs="?")
    args = parser.parse_args()

    print graphcommons.status()

    signals = create_signals(args.input_filename)
    upsert_edges(signals)

    #push_changes(args.input_filename)