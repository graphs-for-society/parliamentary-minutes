import datetime
import glob
import json
import re
import shutil
import tempfile
import time
import requests
import sys
from bs4 import BeautifulSoup

starting_url = "https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.liste"

def convert_datetime_to_unix(d):
    '''
    :param d: datetime object
    :return: unix time conversion in miliseconds
    '''
    return int(time.mktime(d.timetuple())*1000)

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
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
            print e
            time.sleep(exp_backoff)
            exp_backoff *= 2
    if not response:
        return ""
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.select("table:nth-of-type(2)")[0]
    return table.text


def is_in_interval(session_date, interval):
    if not interval:
        return True

    if interval[0] <= session_date <= interval[1]:
        return True
    else:
        return False


def generate_talk_url(talk_id):
    return "https://www.tbmm.gov.tr/develop/owa/genel_kurul.cl_getir?pEid={}".format(talk_id)


def generate_representative_profile_url(rep_id, term_id):
    return "https://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi?p_donem={}&p_sicil={}".format(term_id,
                                                                                                     rep_id)


def generate_representative_profile_image_url(rep_id):
    return "https://www.tbmm.gov.tr/mv_resim/{}.jpg".format(rep_id)

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
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
            print e
            time.sleep(exp_backoff)
            exp_backoff *= 2
    time.sleep(1)
    if not response:
        return []

    result = []
    soup = BeautifulSoup(response.text, "html.parser")
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

        result.append({"rep_name": rep_row['representative_name'],
                 "rep_id": rep_row['representative_id'],
                 "rep_profile_url": generate_representative_profile_url(rep_id, term_id),
                 "rep_profile_image_url": generate_representative_profile_image_url(rep_id),
                 "representative_party": rep_row['representative_party'],
                 "term_id": rep_row['term_id'],
                 "legislation_term": legislation_term,
                 "session_id": session_id,
                 "session_date": convert_datetime_to_unix(session_date),
                 "talk_subject": talk_subject,
                 "talk_id": talk_id,
                 "talk_script": talk_text,
                 "talk_url": generate_talk_url(talk_id)
                 })
    return result

def run(start_date=None, end_date=None):
    rep_list = get_milletvekili_listesi()
    print("Retrieved representative list..")

    if start_date and end_date:
        interval = [datetime.datetime.strptime(start_date, "%d/%m/%Y"),
                    datetime.datetime.strptime(end_date, "%d/%m/%Y")]
    else:
        interval = None

    done_dict = dict()
    fn = 'crawl/done-representatives.lst'
    try:
        done_list = open(fn, "r")
        lines = done_list.readlines()
        for line in lines:
            done_dict[line.strip()] = 1
        done_list.close()
    except IOError, e:
        print >> sys.stderr, "We couldn't find {}. Creating a new one.".format(fn)

    temp_dir_pathname = tempfile.mkdtemp()

    done_list = open("crawl/done-representatives.lst", "a+")  # create a brand new if it doesn't exist.

    for (index, rep_row) in zip(range(len(rep_list)), rep_list):
        if rep_row['representative_id'] in done_dict:
            print("{} of {} PASSED Rep. name: {}".format(index, len(rep_list), rep_row['representative_name'].encode('utf-8')))
        else:
            print("{} of {} Rep. name: {}".format(index, len(rep_list), rep_row['representative_name'].encode('utf-8')))
            talks = get_rep_general_assembly_talks(rep_row, interval)
            for talk in talks:
                f = open("{}/representative-talks-rep_id-{}-date-{}.json".format(temp_dir_pathname, rep_row['representative_id'],
                                                                              talk['session_date']), "a")
                f.write(json.dumps(talk) + "\n")
                done_list.write(rep_row['representative_id'].encode('utf-8') + "\n")
                print(json.dumps(talk))
                f.close()

    done_list.close()

    f = open("data/all-talks-combined-{}-{}-{}.json".
             format(datetime.datetime.strftime(interval[0], "%Y%m%d"), datetime.datetime.strftime(interval[1], "%Y%m%d"),
                    convert_datetime_to_unix(datetime.datetime.now())), "w+")
    for filename in glob.glob("{}/representative-talks-rep_id-*-date-*.json".format(temp_dir_pathname)):
        with open(filename, "r") as talk_file:
            lines = talk_file.readlines()
            for line in lines:
                f.write(line)
    f.close()

    # removing the temporary directory
    shutil.rmtree(temp_dir_pathname)


if __name__ == "__main__":
    """
    Run as
    python crawl/__init__.py --start_date 11/01/2016 --end_date 13/01/2016
    """
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--start_date", nargs="?")
    parser.add_argument("--end_date", nargs="?")
    args = parser.parse_args()
    run(args.start_date, args.end_date)
