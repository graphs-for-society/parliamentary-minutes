# -*- coding: utf-8 -*-
import sys
import re
import ujson
import codecs

TURKISH_ALPHABET_UPPER = "[A-ZÇĞİÖÜŞ]"
TURKISH_ALPHABET = "[a-zçğıöüş]"


name_surname = r"(((%s+ ){2,})\(\w+\))" % TURKISH_ALPHABET_UPPER

PARTIES = set([u"AK PARTİ", "CHP", "HDP", "MHP"])
reaction_regex = ur"\(((.*) sıralarndan (\w+))\)"

# regex = re.compile("BURCU KÖKSAL \([^\)]*\) ")
# print '\n'.join(element[0] for element in re.findall(name_surname, text))
#regex = re.compile("(BURCU KÖKSAL \(\w+\).*(?=({})))".format(name_surname))


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
    data = read_scrape_data(input_file)
    text = data["talk_script"]
    representative = data["rep_name"]
    representative_party = data["representative_party"]
    talk_id = data["talk_id"]
    date = data["session_date"]
    matches = re.findall(reaction_regex, text, flags=re.U)
    print >> sys.stderr, matches
    reactions = []
    for match in matches:
        _, party_text, reaction = match
        parties = get_party_names(party_text)
        for party in parties:
            d = dict()
            d["action"] = "edge_create"
            d["from_name"] = party
            d["from_type"] = "Parti"
            d["name"] = reaction.upper()
            d["to_name"] = talk_id
            d["to_type"] = "Konuşma"
            reactions.append(d)

    if len(reactions) > 0:
        d = dict()
        d["action"] = "edge_create"
        d["from_name"] = representative
        d["from_type"] = "MV"
        d["name"] = "KONUŞTU"
        d["to_name"] = talk_id
        d["to_type"] = "Konuşma"
        reactions.append(d)

        d = dict()
        d["action"] = "edge_create"
        d["from_name"] = representative_party
        d["from_type"] = "MV"
        d["name"] = "ÜYESİ"
        d["to_name"] = representative
        d["to_type"] = "MV"
        reactions.append(d)

    create_output("sample_out.json", reactions)


def read_scrape_data(filename):
    return ujson.load(codecs.open(filename, encoding='utf-8'))


def create_output(filename, output):
    ujson.dump(output, codecs.open(filename, 'w'))


def main():
    function_name = sys.argv[1]
    input_file = sys.argv[2]
    globals()[function_name](input_file)


def my_analysis():
    pass


if __name__ == '__main__':
    main()
