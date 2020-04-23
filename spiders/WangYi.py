# -*- coding: utf-8 -*-
import scrapy
from Crypto.Cipher import AES
import requests
import base64
import os
import codecs
import json
from pypinyin import  lazy_pinyin
from homework.items import HomeworkItem
from urllib.request import urlretrieve

class WangyiSpider(scrapy.Spider):
    name = 'WangYi'
    # allowed_domains = ['https://music.163.com/']
    start_urls = ["https://music.163.com/#/album?id=80003734"]
    # 后三个参数和i的值（随机的十六位字符串）
    b = '010001'
    c = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    d = '0CoJUm6Qyw8W8jud'
    numbers=0
    song_list=[]
    # 随机的十六位字符串
    def createSecretKey(self,size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]

    # AES加密算法
    def AES_encrypt(self,text, key, iv):
        pad = 16 - len(text) % 16
        if type(text) == type(b''):
            text = str(text, encoding='utf-8')
        text = text + str(pad * chr(pad))
        encryptor = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
        encrypt_text = encryptor.encrypt(text.encode("utf8"))
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    # 得到第一个加密参数
    def Getparams(self,a, SecretKey):
        # 0102030405060708是偏移量，固定值
        iv = '0102030405060708'
        h_encText = self.AES_encrypt(a, self.d, iv)
        h_encText = self.AES_encrypt(h_encText, SecretKey, iv)
        return h_encText

    # 得到第二个加密参数
    def GetSecKey(self,text, pubKey, modulus):
        # 因为JS做了一次逆序操作
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    # 得到表单的两个参数
    def GetFormData(self,a):
        SecretKey = self.createSecretKey(16)
        params = self.Getparams(a, SecretKey)
        enSecKey = self.GetSecKey(SecretKey, self.b, self.c)
        data = {
            "params": str(params, encoding='utf-8'),
            "encSecKey": enSecKey
        }
        return data

    def getOnePatam(self):
        # 查询id的url
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        # 伪装头部
        head = {
            'Host': 'music.163.com',
            'Origin': 'https://music.163.com',
            'Referer': 'https://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        song_name = "薛之谦"
        # 第一个参数
        song_name = ''.join(lazy_pinyin(song_name))
        key = '{hlpretag:"",hlposttag:"</span>",s:"' + song_name + '",type:"1",csrf_token:"",limit:"100",total:"true",offset:"0"}'
        FormData = self.GetFormData(key)
        html = requests.post(url, headers=head, data=FormData)
        result = json.loads(html.text)
        return result['result']['songs']

    # 下载器：
    def download(self,name, id):
        # 获取歌曲的url的路径
        song_url = "https://music.163.com/weapi/song/enhance/player/url?csrf_token="
        # 伪装头部
        headers = {
            'Host': 'music.163.com',
            'Origin': 'https://music.163.com',
            'Referer': 'https://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        # 把上个页面查询到的id放到第二个页面的第一个参数上
        a = str({'ids': "[" + str(id) + "]", 'br': 320000, 'csrf_token': ""})
        FormData = self.GetFormData(a)
        response = requests.post(song_url, data=FormData, headers=headers)
        json_dict = json.loads(response.content)
        song_url = json_dict['data'][0]['url']
        return song_url
    def parse(self, response):
        print(self.numbers)
        if self.numbers==0:
            self.song_list = self.getOnePatam()
            # for i in song_list:
            #     id = i['id']
            #     a=HomeworkItem()
            #     a["songName"]=i['name']
            #     print(a["songName"])
            #     a["songLink"]=self.download(a["songName"], id)
            self.numbers += 1
            print(self.download(self.song_list[0]["name"],self.song_list[0]["id"]))
            yield scrapy.Request(
                url=self.download(self.song_list[0]["name"],self.song_list[0]["id"]),
                callback=self.parse
            )
        else:

            with open(self.song_list[self.numbers]['name']+".mp3","wb") as f:
                f.write(response.body)
                f.close()
            self.numbers += 1
            yield scrapy.Request(
                url=self.download(self.song_list[self.numbers]["name"],self.song_list[self.numbers]["id"]),
                callback=self.parse
            )






