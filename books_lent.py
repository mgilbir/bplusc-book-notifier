#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import sys
import datetime


def parse_ddmmyyyy(field):
    [dd, mm, yyyy] = field.split('-')
    return datetime.date(int(yyyy), int(mm), int(dd))


def convert_times(dictionary, fields):
    for field in fields:
        dictionary[field+"_date"] = parse_ddmmyyyy(dictionary[field])
    return dictionary


def parse_header(chunk):
    headers = map(lambda x: x.text, chunk.find_all('td'))
    return headers


def parse_books(chunk, headers):
    fields = map(lambda x: x.text, chunk.find_all('td')[:-1])
    dictionary = dict(zip(headers, fields))
    dictionary = convert_times(dictionary, ['Uitleendatum', 'Inleverdatum'])
    return dictionary


def main(argv):
    cookies_handling = "?offerCookieTerms=false&acceptedCookieTerms=true"
    initial_url = "https://www.bplusc.nl/home"

    s = requests.Session()
    login_page = s.get(initial_url + cookies_handling)
    parsed_login_page = BeautifulSoup(login_page.text)
    login_form = parsed_login_page.find('form', id='loginForm')
    pecid = login_form.find('input', attrs={'name': '_pecid'})['value']

    fields = {}
    fields["username"] = argv[0]
    fields["password"] = argv[1]
    fields["action"] = "Login"
    fields["remindMe"] = "true"
    fields["_remindMe"] = "on"
    fields["_pecid"] = pecid

    profile_page = s.post(initial_url, data=fields)

    parsed_profile_page = BeautifulSoup(profile_page.text)
    entries = parsed_profile_page.find('article', class_='items-overview')
    books = entries.find_all('tr')

    headers = parse_header(books[0])

    parsed_book_info = map(lambda book: parse_books(book, headers), books[1:])
    print parsed_book_info


if __name__ == "__main__":
    main(sys.argv[1:])
