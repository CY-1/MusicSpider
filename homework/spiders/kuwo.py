# -*- coding: utf-8 -*-
import scrapy
from homework.items import HomeworkItem
import requests
class KuwoSpider(scrapy.Spider):
    name = 'kuwo'
    allowed_domains = ['www.kuwo.cn']
    start_urls = ['http://www.kuwo.cn/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
        'csrf': 'RUJ53PGJ4ZD',
        'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1577029678,1577034191,1577034210,1577076651; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1577080777; kw_token=RUJ53PGJ4ZD'
    }

    def handle(self, The_input, Number):

        for x in range(1, Number + 1):

            url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}&rn=30&reqId=615ae920-2d21-11ea-b560-73e04c9f8018".format(
                The_input, Number)

            response = requests.get(url, headers=self.headers).json()

            return response['data']['list']

    def download_music(self,rid, name):
        url = 'http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1582894271662&reqId=ff4d2920-5a28-11ea-a40f-c96cc7a8aad1'.format(
            rid)

        response = requests.get(url, headers=self.headers).json()

        return response['url']
    def parse(self, response):
        data = self.handle("薛之谦", 1)

        for i in data:
            a = HomeworkItem()
            rid = i.get('rid')
            name = i.get('name')
            a["songLink"] = self.download_music(rid, name)
            a["songName"] = name
            yield  a