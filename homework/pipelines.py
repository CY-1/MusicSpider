# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import requests
from homework.settings import my_headers
class HomeworkPipeline(object):
    i=0
    def process_item(self, item, spider):

        if item["songLink"]!="":
            with open(str(self.i)+item["songName"]+".mp3","wb") as f:
                f.write(requests.get(url=item["songLink"],headers=my_headers).content)
            f.close()
            self.i+=1
        return item
