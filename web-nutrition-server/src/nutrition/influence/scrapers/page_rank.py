#! usr/bin/env python
# *--coding : utf-8 --*

import requests
import sys
from bs4 import BeautifulSoup as bs


class PageRank(object):
    def __init__(self):
        pass

    QUOTE_PAGE = 'https://www.checkpagerank.net/'

    def get_rank(self, domain_to_query):
        input_url = PageRank.QUOTE_PAGE
        payload = {'name': domain_to_query}
        r = requests.post(input_url, payload)
        scores = {}
        if r.status_code == requests.codes.ok:
            page = r.text
            soup = bs(page, 'html.parser')
            text_pr = soup.get_text('|', strip=True)
            text_pr_list = text_pr.split('|')
            for i in text_pr_list:
                if i == 'Google PageRank:':
                    scores['Google PageRank'] = text_pr_list[text_pr_list.index(i) + 1]
                if i == 'cPR Score:':
                    scores['cPR Score'] = text_pr_list[text_pr_list.index(i)+1]
                if i.startswith('Global Rank:'):
                    scores['Alexa Rank'] = i.split(':')[1]
                if i.startswith('External Backlinks:'):
                    scores['Backlinks'] = i.split(':')[1]
                if i.startswith('Citation Flow:'):
                    scores['Citations'] = i.split(':')[1]
        else:
            scores = {'Google PageRank' : 0, 'cPR Score': 0, 'Alexa Rank': 0, 'Backlinks': 0, 'Citations': 0}
        return scores


def main():
    pr = PageRank()
    print(pr.get_rank(sys.argv[1]))


if __name__ == '__main__':
    main()
