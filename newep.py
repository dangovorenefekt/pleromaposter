#!/usr/bin/env python3

""" DOCSTRING PLACEHOLDER """

import configparser
import sqlite3
import logging
from sqlite3 import Error
import requests
from requests.structures import CaseInsensitiveDict


logging.basicConfig(filename='/home/rubin/pleromaposter/newep.log',
    format='%(asctime)s-%(process)d-%(levelname)s: %(message)s',
    level=logging.DEBUG)
config_parser = configparser.RawConfigParser()
CONFIG_FILE_PATH = r'/home/rubin/pleromaposter/config.cfg'
config_parser.read(CONFIG_FILE_PATH)
DATA_BASE = config_parser['database']['path']
url = config_parser['pleroma']['instance'] + "/api/v1/statuses"
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = 'Bearer ' + config_parser['pleroma']['access_token']
headers["Content-Type"] = "application/json"
GET_EPISODES = """
    SELECT pods.title, 
        episodes.title, 
        episodes.audio 
    FROM episodes
    JOIN pods 
    ON episodes.podcast_id = pods.podcast_id 
    WHERE strftime('%Y-%m-%d', isodate) is date('now','-1 day');
"""

def create_connection(db_file):
    """ DOCSTRING PLACEHOLDER """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as error_message:
        print(error_message)
    return conn


def post():
    """ DOCSTRING PLACEHOLDER """
    conn = create_connection(DATA_BASE)
    cur = conn.cursor()
    rows = cur.execute(GET_EPISODES).fetchall()
    if len(rows) < 1:
        return
    for i in range(0, len(rows), 5):
        status_body = ''
        for podcast_title, episode_title, audio_link in rows[i:i+5]:
            status_body += "Подкаст: " + podcast_title + ", Епизод: " + \
            episode_title + ", Audio: " + audio_link +"\n\n"
        payload = { "status": "" + \
            status_body + "#PodcastDaily #bulgarian #ПодкастДневник #български"}
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        logging.info('%s', response.status_code)
    return

if __name__ == '__main__':
    post()
