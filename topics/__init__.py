'''
#HOST=193.140.196.97
#HOST=spotlight.sztaki.hu
HOST=localhost
read QUERY
curl http://$HOST:2222/rest/annotate --data-urlencode "text=$QUERY" --data "confidence=0.0" --data "support=0"

'''

import requests

def annotate(text):
    pass