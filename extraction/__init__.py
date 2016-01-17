# -*- coding: utf-8 -*-
import sys
import re
import ujson
import codecs
from collections import defaultdict as dd

import datetime
import time


def convert_datetime_to_unix(d):
    '''
    :param d: datetime object
    :return: unix time conversion in miliseconds
    '''
    return int(time.mktime(d.timetuple())*1000)

TURKISH_ALPHABET_UPPER = "[A-ZÇĞİÖÜŞ]"
TURKISH_ALPHABET = "[a-zçğıöüş]"

NODES = dd(set)

name_surname = r"(((%s+ ){2,})\(\w+\))" % TURKISH_ALPHABET_UPPER

PARTIES = {u"AK PARTİ", "CHP", "HDP", "MHP"}
reaction_regex = ur"\(((.*) sıralarından (\w+))\)"

# regex = re.compile("BURCU KÖKSAL \([^\)]*\) ")
# print '\n'.join(element[0] for element in re.findall(name_surname, text))
#regex = re.compile("(BURCU KÖKSAL \(\w+\).*(?=({})))".format(name_surname))


def create_node_types():
    outputs = []

    # Create Milletvekili nodetype
    d = dict()
    d["action"] = "nodetype_create"
    d["name"] = "Milletvekili"
    d["image_as_icon"] = False
    outputs.append(d)

    # Create Parti nodetype
    d = dict()
    d["action"] = "nodetype_create"
    d["name"] = "Parti"
    # d["image_as_icon"] = False
    outputs.append(d)

    # Create Konuşma nodetype
    d = dict()
    d["action"] = "nodetype_create"
    d["name"] = "Konuşma"
    outputs.append(d)

    return outputs

def get_party_names(party_text):
    matched_parties = []
    party_text = party_text.upper()
    for party in PARTIES:
        if party in party_text:
            matched_parties.append(party)
    return matched_parties


def reps_convs(representative, lines):
    conversation = []
    paragraph = ""
    is_representative_talking = True
    for line in lines:
        line = line.strip()
        match = re.search(name_surname, line, flags=re.UNICODE)
        if match is not None:
            current_representative = match.group(2).strip()
            if current_representative != representative:
                if paragraph != "":
                    conversation.append(paragraph)
                    paragraph = ""
                is_representative_talking = False
            else:
                is_representative_talking = True
                paragraph = "%s %s" % (paragraph, line)
        elif is_representative_talking:
            paragraph = "%s %s" % (paragraph, line)

    if paragraph != "" and is_representative_talking:
        conversation.append(paragraph)

    return conversation


def create_reactions_data(input_file):
    records = read_scrape_data(input_file)
    outputs = create_node_types()
    rep_names = {}
    for record in records:
        # Read representative properties
        representative = record["rep_name"]
        rep_names[representative] = 1
        representative_party = record["representative_party"]
        if representative_party == "AK Parti":
            representative_party = "AK PARTİ"
        rep_profile_url = record.get("rep_profile_url", "")
        rep_profile_image_url = record.get("rep_profile_image_url", "")

        # Read talk properties
        text = record["talk_script"]
        talk_id = record["talk_id"]
        talk_subject = record["talk_subject"]
        talk_name = "%s (ID: %s)" % (talk_subject, talk_id)
        talk_date = record["session_date"]
        talk_url = record.get("talk_url", "")
        term_id = record['term_id']
        matches = re.findall(reaction_regex, text, flags=re.U)

        if len(matches) > 0:
            # Create party node if it doesn't exist
            if representative_party not in NODES['Parti']:
                NODES['Parti'].add(representative_party)
                d = dict()
                d["action"] = "node_create"
                d["name"] = representative_party
                d["type"] = "Parti"
                # TODO: Party Image Link
                outputs.append(d)

            # Create representative node if it doesn't exist
            if representative not in NODES['Milletvekili']:
                NODES['Milletvekili'].add(representative)
                d = dict()
                d["action"] = "node_create"
                d["name"] = representative
                d["type"] = "Milletvekili"
                d["reference"] = rep_profile_url
                d["image"] = rep_profile_image_url
                d['properties'] = {"is member of": representative_party}
                outputs.append(d)

                # Party to representative edge (is member of)
                # d = dict()
                # d["action"] = "edge_create"
                # d["from_name"] = representative_party
                # d["from_type"] = "Parti"
                # d["name"] = "ÜYESİ"
                # d["to_name"] = representative
                # d["to_type"] = "Milletvekili"
                # outputs.append(d)

            # Create talk node
            d = dict()
            d["action"] = "node_create"
            d["name"] = talk_name
            d["type"] = "Konuşma"
            d["properties"] = {"talk_date": talk_date, "talk_summary": "%s ..." % text[:100], "term_id": term_id}
            d["reference"] = talk_url
            outputs.append(d)

            # Create an edge from representative to the talk
            d = dict()
            d["action"] = "edge_create"
            d["from_name"] = representative
            d["from_type"] = "Milletvekili"
            d["name"] = "KONUŞTU"
            d["to_name"] = talk_name
            d["to_type"] = "Konuşma"
            outputs.append(d)

        for match in matches:

            _, party_text, reaction = match
            parties = get_party_names(party_text)
            for party in parties:
                d = dict()
                d["action"] = "edge_create"
                d["from_name"] = party
                d["from_type"] = "Parti"
                d["name"] = reaction.upper()
                d["to_name"] = talk_name
                d["to_type"] = "Konuşma"
                #d['properties'] = {"speech_date": date, "speech_url": "www.buralar_yesillenecek.com",
                #                  "term": term_id}
                outputs.append(d)

    create_output("data/rep_names.json", [{'rep_name': rep_name} for rep_name in sorted(rep_names.keys())], enclosed_in_array=True)
    create_output("data/extraction_output-{}.json".format(convert_datetime_to_unix(datetime.datetime.now())), outputs)


def read_scrape_data(filename):
    records = []
    for line in codecs.open(filename, encoding='utf-8'):
        records.append(ujson.loads(line))

    return records


def create_output(filename, outputs, enclosed_in_array=False):
    f = codecs.open(filename, 'w')
    delimiter = "\n"
    if enclosed_in_array:
        f.write("[\n")
        delimiter = ",\n"
    first = True
    for output in outputs:
        if first:
            f.write("%s" % (ujson.dumps(output)))
            first = False
        else:
            f.write("%s%s" % (delimiter, ujson.dumps(output)))
    if enclosed_in_array:
        f.write("]\n")


def main():
    '''
    Run as
    (first ensure that there is a directory named data in the current directory)
    python crawl/__init__.py --input data/all-talks-combined.json --function create_reactions_data
    :return:
    '''
    import argparse
    parser = argparse.ArgumentParser(description='Extract information from Parliamentary minutes.')
    parser.add_argument("--input", required=True)
    parser.add_argument("--function", required=True, help="The function which is used for information extraction")
    args = parser.parse_args()

    function_name = args.function
    input_file = args.input
    print >> sys.stderr, "Function: %s\nInput: %s" % (function_name, input_file)
    globals()[function_name](input_file)


def my_analysis():
    pass


if __name__ == '__main__':
    main()
