# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import json







def download_music(rid,name):

    url = 'http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1582894271662&reqId=ff4d2920-5a28-11ea-a40f-c96cc7a8aad1'.format(rid)

    response = requests.get(url, headers = headers).json()

    text = response['url']

    with open("酷我音乐{}.mp3".format(name),'wb') as abc:

        print("正在下载:{}".format(name))

        download = requests.get(text)

        abc.write(download.content)

        print("下载完成...")



def mian(The_input,Number):

    for x in range(1, Number + 1):

        url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}&rn=30&reqId=615ae920-2d21-11ea-b560-73e04c9f8018".format(The_input, Number)

        response = requests.get(url, headers = headers).json()

        data = response['data']['list']

        for i in data:

            rid = i.get('rid')

            name = i.get('name')

            download_music(rid,name)

def run():

    The_input = str(input('请输入要下载歌手:'))

    Number = int(input('请输入要下载的页数:'))

    mian(The_input,Number)



if __name__ == '__main__':

    run()

    download_music_one = Thread(target=download_music)

    mian_one = Thread(target=mian)

    download_music_one.start()
    mian_one.start()
