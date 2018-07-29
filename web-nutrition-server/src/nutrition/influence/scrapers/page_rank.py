#! usr/bin/env python
# *--coding : utf-8 --*
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import math
import requests
import sys
from bs4 import BeautifulSoup as bs
import urllib.request

from pandas._libs import json

from nutrition.structure.environment import OPEN_PAGE_RANK_API_URL, OPEN_PAGE_RANK_API_KEY
from wnserver.response import SubFeatureError, SubFeature


class PageRank(object):
    def __init__(self):
        pass

    QUOTE_PAGE = 'https://www.checkpagerank.net/'

    def get_alexa_rank(self, domain):
        try:
            input_url = PageRank.QUOTE_PAGE
            payload = {'name': domain}
            r = requests.post(input_url, payload)
            if r.status_code == requests.codes.ok:
                page = r.text
                soup = bs(page, 'html.parser')
                text_pr = soup.get_text('|', strip=True)
                text_pr_list = text_pr.split('|')
                for i in text_pr_list:
                    if i.startswith('Global Rank:'):
                        alexa_rank = float(i.split(':')[1])
                        score = min(100, (1 / (math.log((alexa_rank) ** 0.0001) + 0.01)))
                        return SubFeature('Alexa Rank', alexa_rank, score,
                                          tooltip="How much traffic on this website")
            else:
                raise Exception('Unable to retrieve ')
        except:
            pass

        return SubFeatureError('Alexa Rank')

    def get_page_rank(self, domain_to_query):
        try:
            params = urlencode({'domains[]': domain_to_query})
            req = Request(OPEN_PAGE_RANK_API_URL + "?" + params)
            print(OPEN_PAGE_RANK_API_URL + "?" + params)
            req.add_header('API-OPR', OPEN_PAGE_RANK_API_KEY)
            result = json.loads(urlopen(req).read())['response'][0]['page_rank_decimal'] * 10
            return SubFeature('Page Rank', result, result,
                              tooltip='Domain ranking based on links from and to external sources')

        except:
            return SubFeatureError('Page Rank')


if __name__ == '__main__':
    print(PageRank().get_page_rank('bbc.com'))
    print(PageRank().get_alexa_rank('bbc.com'))
