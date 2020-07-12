# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import avhubItem
import random
from . import utils
import time
import re
from scrapy.conf import settings

prefix = "http://www.avbs5.xyz"
min_time = '03:00'


class AvhubSpider(scrapy.Spider):
    name = 'avhub'
    allowed_domains = ['www.avbs5.xyz']
    start_urls = ['http://www.avbs5.xyz/china/']
    proxies_ = settings.get('PROXIES')
    cookies = settings.get("COOKIES")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url
                                 , callback=self.parse
                                 , headers=utils.getHeader()
                                 ,meta={'proxy': random.choice(self.proxies_)}
                                 # , cookies=self.cookies
                                 )

    def parse(self, response):
        # print(response.text)
        doc = PyQuery(response.text)
        rows = doc('.video').items()
        for row in rows:
            try:
                item = avhubItem()
                item['time'] = row.find('.badge').text()
                if utils.time_cmp(item['time'], min_time) < 0:
                    continue
                item['title'] = row.find('.video-title').text().replace(" ","")
                item['views'] = row.find('.video-details').text()
                item['img'] = row.find('img').attr('src')

                href = row.find('a').eq(0).attr("href")
                item['cell_url'] = prefix + href
                # $('#player script')[2]
                item['m3u8_url'] = self.get_video_url(prefix + href)
                item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                yield item
            except Exception as e:
                print("parse" + e.__str__())
        p = doc('.prevnext')
        next_href = p.eq(p.length - 1).attr('href')
        if next_href is not None:
            print(prefix + next_href)
            yield scrapy.Request(prefix + next_href
                                 , callback=self.parse
                                 , headers=utils.getHeader()
                                 ,meta={'proxy': random.choice(self.proxies_)}
                                 )

    def get_video_url(self, href):
        mget = utils.mget(href)
        if mget is None:
            return ""
        doc = PyQuery(mget.text)
        m3u8 = doc('#videoBox source').attr('src')
        if m3u8.__len__() > 0:
            return m3u8
        return ""
