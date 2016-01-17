# -*- coding: utf-8 -*-

from graphcommons import GraphCommons

graph_id = "de6e0fd9-e5a6-42ac-86ad-b98c5a5d15ed"
api = GraphCommons('sk_ZHtDXwgI2yvT4EcALt-rVg')


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

    return d

if __name__ == "__main__":
    print get_paths("Deniz BAYKAL", u"AK PARTİ")

#d = {"fromtype": "Milletvekili", "via": "KONUŞTU,ALKIŞLAR", "totype":"Parti", "limit":30, "strict": True}
#print api.get_path(graph_id, d)


