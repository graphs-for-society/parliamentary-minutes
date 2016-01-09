
from bs4 import BeautifulSoup
import requests
import re, json
import time

import datetime

starting_url = "https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.liste"

def get_milletvekili_listesi():
    '''

    :return: i.e. [[u'26', u'7244', u'CHP', u'Ayd\xfdn USLUPEHL\xddVAN', u'https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi?p_donem=26&p_sicil=7244']]
    '''
    response = requests.get(starting_url)
    if not response: # TODO: make other checks.
        print "ERROR in request"
        return
    text = response.text
    soup = BeautifulSoup(text, "html.parser")

    #rows = soup.find_all("tr", attrs={'bgcolor': '#FFFFFF'})
    rows = soup.select('tr[bgcolor="#FFFFFF"]')

    result = []

    print rows
    for row in rows:
        cell1 = row.select('td > a')[0]
        m = re.match("https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi\?p_donem=(\d+)&p_sicil=(\d+)",
                     cell1.attrs['href'])
        if m:
            term_id = m.group(1)
            representative_id = m.group(2)
            representative_name = cell1.text

            cell2 = row.select('td:nth-of-type(3)')[0]
            representative_party = cell2.text

            result.append({"term_id": term_id,
                           "representative_id": representative_id,
                           "representative_party": representative_party,
                           "representative_name": representative_name,
                           "profile_url": cell1.attrs['href']
                           })
        else:
            print cell1.attrs['href']

    return result


def get_rep_general_assembly_talk(talk_id, rep_id, term_id):
    talk_url = "https://www.tbmm.gov.tr/develop/owa/genel_kurul.cl_getir?pEid={}".format(talk_id)

    headers = {"Referer": "https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi?p_donem={}&p_sicil={}".format(term_id, rep_id),
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

    exp_backoff = 1
    finish = False
    while not finish:
        try:
            response = requests.get(talk_url, headers=headers)
            finish = True
        except requests.exceptions.ConnectionError, e:
            print e
            time.sleep(exp_backoff)
            exp_backoff *= 2
    if not response:
        return ""
    soup = BeautifulSoup(response.text)
    table = soup.select("table:nth-of-type(2)")[0]
    return table.text


def is_in_interval(session_date, interval):
    if not interval:
        return True

    if session_date > interval[0] and session_date < interval[1]:
        return True
    else:
        return False

def get_rep_general_assembly_talks(rep_row, interval=None):
    rep_id = rep_row['representative_id']
    term_id = rep_row['term_id']

    headers = {"Referer": "https://www.tbmm.gov.tr/develop/owa/genel_kurul.konusmaci_tutanak?pkonusmacisicil={}&pdonem={}".format(rep_id, term_id),
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

    exp_backoff = 1
    url = "https://www.tbmm.gov.tr/develop/owa/genel_kurul.konusmaci_tutanak?pkonusmacisicil={}&pdonem={}".format(rep_id, term_id)
    finish = False
    while not finish:
        try:
            response = requests.get(url, headers=headers)
            finish = True
        except requests.exceptions.ConnectionError, e:
            print e
            time.sleep(exp_backoff)
            exp_backoff *= 2
    time.sleep(1)
    if not response:
        return []

    result = []
    soup = BeautifulSoup(response.text)
    rows = soup.select("tr")
    first_row = 0
    for row in rows:
        if first_row < 2:
            first_row += 1
            continue
        legislation_term = row.select("td:nth-of-type(1)")[0].text
        session_id = row.select("td:nth-of-type(2)")[0].text
        session_date = datetime.datetime.strptime(row.select("td:nth-of-type(3)")[0].text, "%d/%m/%Y")
        talk_subject_el = row.select("td:nth-of-type(4) a")[0]
        talk_subject = talk_subject_el.text
        m = re.match("https://www.tbmm.gov.tr/develop/owa/genel_kurul.cl_getir\?pEid=(\d+)",
                           talk_subject_el.attrs['href'])
        if m:
            talk_id = m.group(1)
        else:
            talk_id = -1



        if not is_in_interval(session_date, interval):
            continue
        talk_text = get_rep_general_assembly_talk(talk_id, rep_row['representative_id'], rep_row['term_id'])
        print("Retrieved Talk Id: {}".format(talk_id))
        time.sleep(1)
        print("Rep. name: {} Talk Id: {}, Session Date: {}".format(rep_row['representative_name'].encode('utf-8'),
                                                                   talk_id,
                                                                   session_date))

        result.append({'rep_name': rep_row['representative_name'],
                 'rep_id': rep_row['representative_id'],
                 "representative_party": rep_row['representative_party'],
                 "term_id": rep_row['term_id'],
                 "legislation_term": legislation_term,
                 "session_id": session_id,
                 "session_date": session_date.strftime("%Y%m%d"),
                 "talk_subject": talk_subject,
                 "talk_id": talk_id,
                 "talk_script": talk_text
                 })
    return result

def run(start_date=None, end_date=None):
    rep_list = get_milletvekili_listesi()
    print("Retrieved representative list..")

    if start_date and end_date:
        interval = [datetime.datetime.strptime(start_date, "%d/%m/%Y"),
                    datetime.datetime.strptime(start_date, "%d/%m/%Y")]
    else:
        interval = None

    done_dict = dict()
    try:
        done_list = open("done-representatives.lst", "r")
        lines = done_list.readlines()
        for line in lines:
            done_dict[line.strip()] = 1
        done_list.close()
    except IOError, e:
        print e

    done_list = open("done-representatives.lst", "a")

    for rep_row in rep_list:
        if rep_row['representative_id'] in done_dict:
            print("PASSED Rep. name: {}".format(rep_row['representative_name'].encode('utf-8')))
        else:
            print("Rep. name: {}".format(rep_row['representative_name'].encode('utf-8')))
            talks = get_rep_general_assembly_talks(rep_row, interval)
            for talk in talks:
                f = open("representative-talks-rep_id-{}-date-{}.json".format(rep_row['representative_id'],
                                                                              talk['session_date']), "a")
                f.write(json.dumps(talk) + "\n")
                done_list.write(rep_row['representative_id'].encode('utf-8') + "\n")
                print(json.dumps(talk))
                f.close()

    done_list.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--start_date", nargs="?")
    parser.add_argument("--end_date", nargs="?")
    args = parser.parse_args()
    run(args.start_date, args.end_date)
