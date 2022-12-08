#!/usr/bin/env python3

import configparser
import json
import requests
from requests.structures import CaseInsensitiveDict


configParser = configparser.RawConfigParser()   
configFilePath = r'/home/rubin/pleromaposter/config.cfg'
configParser.read(configFilePath)


url = configParser['pleroma']['instance'] + "/api/v1/statuses"
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = 'Bearer ' + configParser['pleroma']['access_token']
headers["Content-Type"] = "application/json"


def getstats():
  r = requests.get(configParser['ge']['apiendpoint'])
  return r.json()

def main():
  data = getstats()
  feeds = data["stats"]["feedCountTotal"]
  totalep = data["stats"]["episodeCountTotal"]
  timestamp = data["as-of"]

  payload = {"status":  timestamp + "\n" + str(feeds) + " подкаста са публикували " + str(totalep) + " епизода на български език.\nhttps://podcastalot.com\n#podcasts #stat"}
  response = requests.post(url, json=payload, headers=headers)
  return response.status_code

if __name__ == '__main__':
	main()

