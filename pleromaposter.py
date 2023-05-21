#!/usr/bin/env python3

""" DOCSTRING PLACEHOLDER """

import configparser
import requests
from requests.structures import CaseInsensitiveDict


configParser = configparser.RawConfigParser()
CONFIG_FILE_PATH = r'/home/rubin/pleromaposter/config.cfg'
configParser.read(CONFIG_FILE_PATH)


url = configParser['pleroma']['instance'] + "/api/v1/statuses"
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = 'Bearer ' + configParser['pleroma']['access_token']
headers["Content-Type"] = "application/json"


def getstats():
    """ DOCSTRING PLACEHOLDER """
    data = requests.get(configParser['ge']['apiendpoint'], timeout = 30).json()
    stats = {
        "feeds": data["stats"]["feedCountTotal"],
        "totalep": data["stats"]["episodeCountTotal"],
        "timestamp": data["as-of"],
        "last3days": data["stats"]["NewEpisodes3days"],
        "last10days": data["stats"]["NewEpisodes10days"],
        "last30days": data["stats"]["NewEpisodes30days"],
        "last90days": data["stats"]["NewEpisodes90days"]
    }
    return stats


def post():
    """ DOCSTRING PLACEHOLDER """
    data = getstats()
    payload = {"status":  data['timestamp'] + "\n" + str(data['feeds']) + \
        " подкаста са публикували " + str(data['totalep']) + " епизода на български език.\n" + \
        "За последните три дена: " + str(data['last3days']) + " епизода.\n" + \
        "За последните десет дена: " + str(data['last10days']) + " епизода.\n" + \
        "За последните тридесет дена: " + str(data['last30days']) + " епизода.\n" + \
        "За последните деветдесет дена: " + str(data['last90days']) + \
        " епизода.\nhttps://podcastalot.com\n#podcasts #stat"}
    response = requests.post(url, json=payload, headers=headers, timeout = 30)
    return response.status_code

if __name__ == '__main__':
    post()
