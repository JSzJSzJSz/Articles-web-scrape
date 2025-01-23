# -*- coding: utf-8 -*-
"""
Created on Tue May 14 16:02:38 2024

@author: Huawei
"""

#w srodowisku jest wczytany scraper
import time
import requests 
import json
from bs4 import BeautifulSoup
import re
import os 
import mouse

from  webscraper import scraper,article

cwd = os.getcwd()+"\\z_radomia"
try:
    os.makedirs(cwd+"\\WP")
    os.makedirs(cwd+"\\ON")
    
except:
    pass

scrWP = scraper("https://wiadomosci.wp.pl/rss.xml",cwd+"\\WP\\",site="WP")
scrON = scraper("https://wiadomosci.onet.pl/.feed",cwd+"\\ON\\",site="ON")


for i in range(24):
    print(f"numer {i}")
    if scrWP.get_new_links():
        scrWP.get_articles()
        scrWP.save_new_articles()
    print("WP done")    
    if scrON.get_new_links():
        scrON.get_articles()
        scrON.save_new_articles()
    print("ON done")
    
    for i in range(3):
        mouse.move(1000,600) #żeby komputer sie nie wylaczal
        mouse.click("left")
        time.sleep(10*60) #co godzinę sprawdza nowe artykuły