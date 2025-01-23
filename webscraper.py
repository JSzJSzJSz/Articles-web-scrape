# -*- coding: utf-8 -*-
"""
Created on Tue May 21 19:59:47 2024

@author: Huawei
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:24:55 2024

@author: Huawei
"""


import requests 
import json
from bs4 import BeautifulSoup
import re
import time
#https://wiadomosci.wp.pl/rss.xml
#https://wiadomosci.onet.pl/.feed

class scraper:
  
    def __init__(self, rss_url, folder_path, site="ON", last_id = "" ):
        self.articles = []
        self.rss_url = rss_url
        self.site = site
        self.last_article_id = last_id
        self.folder_path = folder_path
        
    def get_new_links(self):
        rss = requests.get(self.rss_url)
        soup = BeautifulSoup(rss.text,features="xml")
        #print(soup)
        if self.site=="WP":
            items = soup.findAll("item")
            #print(items)
            for i,item in enumerate(items):
                link_clean = item.link.text
                #print(item.guid.text)
                if item.guid.text!=self.last_article_id:
                    lead = item.description.text
                    clean_lead = re.sub("<img.{2,}>","",lead)
                    self.articles.append(article(url = link_clean, 
                                            date = item.pubDate.text.replace(":","-").replace(" ",""),
                                            title = item.title.text,
                                            lead = clean_lead,
                                            id_ = item.guid.text,
                                            site = self.site))
                else:
                    break
                
            if len(self.articles)>0:
                print(f"downloaded {i} new articles")
                return True
            else:
                return False
            #self.last_article_url = new_links[0] #tymczasowo do testow

        if self.site=="ON":
            items = soup.findAll("entry")
            for i,item in enumerate(items):
                link_clean = item.link["href"]
                if item.id.text!=self.last_article_id:
                    lead = item.summary.text
                    clean_lead = re.sub("<img.{2,}>","",lead)
                    self.articles.append(article(url = link_clean, 
                                            date = item.published.text.replace(":","-"),
                                            title = item.title.text,
                                            lead = clean_lead,
                                            id_ = item.id.text,
                                            site = self.site))
                else:
                    break
                
            if len(self.articles)>0:
                print(f"downloaded {i} new articles")
                return True
            else:
                return False
        
        
    
    def get_articles(self):
        
        for art in self.articles:
            art_html = requests.get(art.url)
            soup = BeautifulSoup(art_html.text,"html")
            if self.site=='WP':
                art_html = soup.find_all("p", attrs={"class": None})
            else:
                art_html = soup.find_all("p")
            try:
                art_text = [x.text for x in art_html]
                art_text = "".join(art_text)
            except:
                pass #można dopisac zapisywanie bledu
            art.text = art_text
    def update_last_url(self):
        self.last_article_id = self.articles[0].id_
        
    def save_new_articles(self):
        for art in self.articles:
            
            with open(self.folder_path + art.site + art.id_.replace(":","-")+ ".json", "w") as outfile:
                json.dump(art.to_json(), outfile)
                
        self.update_last_url()
        self.articles = []
        
        
class article:
    def __init__(self, url = None, date = None, title = None, lead = None, text = None, site = None, id_ = None):
        self.url = url
        self.id_ = id_
        self.date = date
        self.title = title
        self.lead = lead
        self.text = text
        self.site = site
    
    def to_json(self):
        art_dict = {
            "url" : self.url,
            "id_" : self.id_,
            "date" : self.date,
            "title" : self.title,
            "lead" : self.lead,
            "text" : self.text
            }
        return art_dict
           
        
        
        
        
        
        
        
        
        
        
        
        
        