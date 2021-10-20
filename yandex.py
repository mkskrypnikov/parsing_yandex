import geo
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import time
import datetime
import os

today = datetime.datetime.now()
today = today.strftime("%Y%m%d")

pages = [i for i in range(1,3)]

name = today + '.csv'
report_name = os.getcwd()+'\\data\\'+name
cities = geo.yandex_geo

def gen_url(keyword):
    return 'https://yandex.ru/search/ads?text='+keyword.replace(' ', '%20')+'&lr=213&p='


def get_html(url):
    UserAgent().chrome
    response = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    html = response.text
    return BeautifulSoup(html)

def gen_key():
    keywords = {}
    keys =  open('key.txt', 'r', encoding='utf-8')
    while True:
        line = keys.readline()
        if not line:
            break
        keywords[line.strip().split(';')[0]] = line.strip().split(';')[1]
    keys.close
    return  keywords


def parsing():
    keywords = gen_key()
    contents = []
    test = []
    for city in cities:
        for keyword in keywords:
            try:
                print(cities[city], '||', keyword)
                x = 0
                for page in pages:
                    url = gen_url(keyword)+str(page)
                    soup = get_html(url)
                    content = soup.findAll('li', {'class': 'serp-item desktop-card'})
                    for ads in content:
                        title = ads.find('div', {'class': 'OrganicTitle-LinkText organic__url-text'}).text
                        url = ads.find('div', {'class': 'Path Organic-Path path organic__path'}).text
                        ad = ads.find('span', {'class': 'OrganicTextContentSpan'}).text
                        if 'Реклама' in ad and keyword + url+str(city) not in test:
                            test.append(keyword+url+str(city))
                            x += 1
                            contents.append({'city' : cities[city], 'keywords' : keyword, 'keyword_type' : keywords[keyword], 'title' : title, 'url' : url, 'ad': ad, 'position' : x})
                        else:
                            continue
                time.sleep(0.5)
            except:
                continue
    df = pd.DataFrame(contents)
    df_new = df.url.str.split('›', 0, expand=True)
    df['url_mini'] = df_new[0]
    df_new = df.ad.str.split('·', 0, expand=True)
    df['ad'] = df_new[1]
    df['type'] = df_new[0]
    df['date'] = today
    df.to_csv(report_name, index=False, header=True, sep=';', encoding='utf-8')












