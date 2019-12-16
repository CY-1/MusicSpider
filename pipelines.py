# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import requests
from homework.settings import my_headers
class HomeworkPipeline(object):
    def process_item(self, item, spider):
        if item["songLink"]!="":
            with open(item["songName"]+".mp3","wb") as f:
                f.write(requests.get(url=item["songLink"],headers=my_headers).content)
            f.close()
        return item
