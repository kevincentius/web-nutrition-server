#! usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs


def get_rank(domain_to_query):
    url = "http://www.mywot.com/scorecard/" + domain_to_query
    score = {}
    page = requests.get(url)
    if page.status_code == requests.codes.ok:
        soup = bs(page.text, 'html.parser')
        text_pr = soup.get_text('|', strip=True)
        text_pr_list = text_pr.split('|')
        for i in text_pr_list:
            if i == 'Trustworthiness':
                if str(text_pr_list[text_pr_list.index(i) + 1]) == 'No Data':
                    score['WOT Score'] = '0/100'
                else:
                    score['WOT Score'] = str(text_pr_list[text_pr_list.index(i) + 1])+'/100'
    else:
        score['WOT Score'] = '0/100'
    return score


