import os
import sys
import urllib2
import StringIO
import zipfile
import threading
import time
from urllib2 import Request, urlopen
from urllib import urlretrieve
from bs4 import BeautifulSoup
import shutil
SKIP_LIST = ['Name', 'modified', 'Size', 'Description', 'Parent']
def get_years_amos_urls(url = 'http://amosweb.cse.wustl.edu/zipfiles/'):
    url = url.replace(" ","%20")
    req = Request(url)
    a = urlopen(req).read()
    soup = BeautifulSoup(a, 'html.parser')
    x = (soup.find_all('a'))
    years = []
    for i in x:
        file_name = i.extract().get_text()
        url_new = url + file_name
        url_new = url_new.replace(" ","%20")
        if 'zipfiles/20' in url_new:
            years.append(url_new)
    return years
        #print(url_new)
def get_next_level_urls_from_years_amos_url(url = 'http://amosweb.cse.wustl.edu/zipfiles/2017/',
                                            SKIP_LIST = SKIP_LIST):
    url = url.replace(" ","%20")
    req = Request(url)
    a = urlopen(req).read()
    soup = BeautifulSoup(a, 'html.parser')
    x = (soup.find_all('a'))
    out = []
    for i in x:
        file_name = i.extract().get_text()
        url_new = url + file_name
        url_new = url_new.replace(" ","%20")
        SKIP = False
        for s in SKIP_LIST:
            if s in url_new:
                SKIP = True
                break
        if SKIP:
            continue
        out.append(url_new)
        #print url_new
        #if 'zipfiles/20' in url_new:
        #    years.append(url_new)
    return out
        #print(url_new)
years = get_years_amos_urls('http://amosweb.cse.wustl.edu/zipfiles/')
full_url_list = []
for y_url in years:
    urls_level1 = get_next_level_urls_from_years_amos_url(y_url)
    for l1 in urls_level1:
        print l1
        urls_level2 = get_next_level_urls_from_years_amos_url(l1)
        for l2 in urls_level2:
            print l2
            urls_level3 = get_next_level_urls_from_years_amos_url(l2)
            for l3 in urls_level3:
                print l3
                zip_urls = get_next_level_urls_from_years_amos_url(l3)
                for z in zip_urls:
                    full_url_list.append(z)
        from shutil import copyfile
        copyfile('current_amos_urls.txt', 'current_amos_urls.txt_backup')
        with open('current_amos_urls.txt', 'wb') as file_handler:
            for item in full_url_list:
                file_handler.write("{}\n".format(item))