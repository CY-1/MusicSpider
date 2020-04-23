# -*- coding: utf-8 -*-
import scrapy
import requests
import re
from homework.settings import my_headers
from homework.items import HomeworkItem
import time
class MusicSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['music.taihe.com']
    start_urls = ["http://music.taihe.com/data/user/getsongs?start=0&size=15&ting_uid=2517"]
    i=0
    def parse(self, response):
        mp3_url = "http://play.taihe.com/data/music/songlink"
        a=re.findall('''data-songid=\\\\\"(\d+)\\\\\"''',response.text,re.S)#需要二次转义、、、、、
        a=list(set(a))
        print(a,end=" ")
        print()
        my_data = {
            'songIds': ",".join(a),
            'hq': '0',
            'type': 'm4a,mp3',
            'rate': "",
            'pt': '0',
            'flag': '-1',
            's2p': '-1',
            'prerate': '-1',
            'bwt': '-1',
            'dur': '-1',
            'bat': '-1',
            'bp': '-1',
            'pos': '-1',
            'auto': '-1'
        }
        response2 = requests.post(url=mp3_url, headers=my_headers, data=my_data)
        music_infos = response2.json()['data']['songList']
        for music_info in music_infos:
            a=HomeworkItem()
            a["songLink"] = music_info["songLink"]
            a["songName"]= music_info["songName"]
            yield a
        self.i+=15
        url = "http://music.taihe.com/data/user/getsongs?start=" + str(self.i) + "&size=15&ting_uid=2517"
        res=requests.get(url=url, headers=my_headers)
        errorCode=re.findall('''"errorCode":(\d+),"''',response.text,re.S)
        if errorCode[0]!="22001":
            yield scrapy.Request(
                "http://music.taihe.com/data/user/getsongs?start=" + str(self.i) + "&size=15&ting_uid=2517",
                callback=self.parse
            )



