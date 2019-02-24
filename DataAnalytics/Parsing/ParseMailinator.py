#!/usr/bin/env python3

import json
from pprint import pprint
from bs4 import BeautifulSoup

from collections import abc

def read_from_file(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)
    return data

class Mailinator(object):
    def __init__(self, json):
        self.data = json['data']

        self.from_address = self.data['fromfull']
        self.from_name = self.data['from']
        self.subject = self.data['subject']

        self.headers = self.data['headers']
        self.date = self.headers['date']
        self.to = self.headers['to']
        self.recieved_smtp = self.headers['received']
        self.parts = self.data['parts']

        self.body_plain = self.get_mail_body(self.parts, 'text/plain')
        self.body_html = self.get_mail_body(self.parts, 'text/html')

    
    def get_mail_body(self, parts, content_type):
        for part in parts:
            if content_type in part['headers']['content-type']:
                return part['body']

        return ""
    



## EXAMPLE USAGE
data = read_from_file('sample.json')
m = Mailinator(data)
body_html = m.body_html

soup = BeautifulSoup(body_html, 'html.parser')
text_of_email = soup.get_text()
image_count = len(soup.find_all('img'))

print(image_count)
# for a in soup.find_all('img'):
#     print(a.get('src'))
#     print("\n")

link_count = len(soup.find_all('a'))
# for a in soup.find_all('a'):
#     print(a.get('href'))