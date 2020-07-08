# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
import random
from pyquery import PyQuery
from ..items import a91Item
import execjs
import time
import requests

error_list = []
error_ip = set()
retry_url = []
try_times = 0
prefix = 'http://www.91porn.com/v.php'
min_time = "03:00"


class A91Spider(scrapy.Spider):
    name = '91'
    allowed_domains = ['www.91porn.com']
    # start_urls = ['https://www.google.com/']
    start_urls = ['http://www.91porn.com/v.php?next=watch']

    proxies_ = settings.get('PROXIES')
    max_page = 4698
    cookies = settings.get("COOKIES")

    #
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={'proxy': random.choice(self.proxies_)}, cookies=self.cookies)

    def parse(self, response):
        print(response.text)
        doc = PyQuery(response.text)
        rows = doc('.videos-text-align').items()
        for row in rows:
            try:
                print(row.text())

                split = row.text().strip()
                item = a91Item()
                r1 = split.split("积分:")
                item['score'] = r1[1]
                r2 = r1[0].split("留言:")
                item['msg'] = r2[1]
                r3 = r2[0].split("收藏:")
                item['favorite'] = r3[1]
                r4 = r3[0].split("查看:")
                item["views"] = r4[1]
                r5 = r4[0].split("作者:")
                item['author'] = r5[1]
                r6 = r5[0].split("添加时间:")
                item['add_time'] = r6[1].strip()
                r7 = r6[0].split(" ")
                if r6[0].lower().startswith("hd"):
                    item['time'] = r6[0][3:8]
                    item['title'] = r6[0][8:]
                else:
                    item['time'] = r6[0][0:5]
                    item['title'] = r6[0][5:]
                if self.time_cmp(item['time'], min_time) < 0:
                    continue
                img = row.find(".img-responsive")
                if img is not None:
                    item['img'] = img.attr('src')
                else:
                    item['img'] = None
                href = doc('.videos-text-align a').eq(0).attr("href")
                item['cell_url'] = href
                item['video_url'] = self.get_video_url(href)
                yield item
            except Exception as e:
                text = doc('span.pagingnav').text()
                error_list.append(text)
                print(e)
        navs = doc(".pagingnav a")
        navs_eq = navs.eq(navs.length - 1)
        if navs_eq.text() == "»" and navs_eq.attr("href") is not None:
            print(prefix + navs_eq.attr("href"))
            yield scrapy.Request(prefix + navs_eq.attr("href"), callback=self.parse,
                                 meta={'proxy': random.choice(self.proxies_)}, cookies=self.cookies)

    def get_video_url(self, href):
        mget = self.mget(href)
        doc = PyQuery(mget.text)
        split = doc('#player_one script').eq(0).text().replace("\"", "").split("(")[2].split(",")
        with open("D:\develop\Python\scrapy\demo1\demo1\spiders\md5.js", "r") as f:
            data_func = f.read()  # 读取js文件
        tk = execjs.compile(data_func)  # 编译执行js代码
        a = "NS0tQCoqBCQKMg0AWjwoUwFaEGcTPzUBIRNBPCcAUi14AmRpIgwfS3QjETYLDVw7BigDKARRIQgLLXJ3N2x6MjALMEIaZR4NOy1nLhgEO3AqYiExCBNzHy0Obj8/A389KnA+R1AcORw8GihrIggYAiswMk00CSoFDX5hUhUjB3dydQ8BFX8UIzsdaUIrJgAd"
        b = "eec6NrNNPaOz9QejKhxWwwt7mjyDhT5X5h1Xnfx28IzNGteOelRRH+lqFG7Fz/OFSOamyVO4nh1lV5KCd7UzlF5fxcWneh5syBp44ecplNmZlbM2dtQ4zMokD63gvdRN8FUqO8BUw/X5"
        '''strencode()'''
        tk = tk.call('strencode', split[0], split[1])  # 调用函数 token为js里面的函数  a为传的参数
        # tk = tk.call('strencode', a, b)  # 调用函数 token为js里面的函数  a为传的参数
        tk = str(tk).split('src=\'')[1].split("'")[0]
        print('tk', tk)
        return tk

    def random_ip(self):  # line:354:def method8():
        OOOOOO0000000000O = random.randint(1, 255)  # line:355:a = random.randint(1, 255)
        O0OOOO0OOO0OO0O0O = random.randint(1, 255)  # line:356:b = random.randint(1, 255)
        O000O00000OOO00OO = random.randint(1, 255)  # line:357:c = random.randint(1, 255)
        O0OOO000OOO0OO0OO = random.randint(1, 255)  # line:358:d = random.randint(1, 255)
        gen_ip = str(OOOOOO0000000000O) + '.' + str(O0OOOO0OOO0OO0O0O) + '.' + str(O000O00000OOO00OO) + '.' + str(
            O0OOO000OOO0OO0OO)
        return gen_ip  # line:359:return str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)

    def mget(self, url):
        rand_time = random.randint(300, 500) / 1000
        time.sleep(rand_time)
        resp = None
        try:
            ip = self.random_ip()
            headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                       'X-Forwarded-For': ip
                       }
            proxies = {'http': 'http://127.0.0.1:1080'}
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=10, verify=False)
        except Exception:
            error_ip.add(ip)
            raise
        return resp

    def time_cmp(self, first_time, second_time):
        print(first_time)
        print(second_time)
        return int(time.strftime("%M%S", time.strptime(first_time, "%M:%S"))) - int(
            time.strftime("%M%S", time.strptime(second_time, "%M:%S")))
