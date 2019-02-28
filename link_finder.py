#link_finder.py
# By Ian Campbell
# This program maps out a website by finding and visiting
# all of the links that can be found in the html
# It then categorizes them as working or broken
# This is heavily inspired by my previous works email_parser.py
# version 1.0.0 02/28/19

import getopt
import re
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque

#opening message
print('Welcome to link_finder.py\n')

#hardcoded website
start = "http://krukafdafampbell.com/"

# data structures
new_urls = deque([start])
processed_urls = set()

#main while loop
while len(new_urls):
    url = new_urls.popleft()
    processed_urls.add(url)

    parts = urlsplit(url)
    #setup url
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    if parts.scheme != 'mailto' and parts.scheme != '#':
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url
    else:
        continue
    
    #determine if it works or is broken
    try:
        response = requests.get(url)
        print (url + " is alive")
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        print( url + " is Broken\n")
        continue

    #create a BSOBJ to scan the html for links
    soup = BeautifulSoup(response.text, 'lxml')

    #determine which lnks are valid from the html
    for anchor in soup.find_all("a"):
        link = anchor.attrs["href"] if "href" in anchor.attrs and anchor.attrs["href"].find("mailto") == -1 and anchor.attrs["href"].find("tel") == -1 and anchor.attrs["href"].find("#") == -1 else ''
        #append good links back to the url queue. 
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link
        if not link in new_urls and not link in processed_urls and not link.find(start) == -1:
            new_urls.append(link)

