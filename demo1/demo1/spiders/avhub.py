# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import avhubItem
import random
from . import utils
import time
import re

prefix = "http://www.avbs5.xyz/"
min_time = '03:00'


class AvhubSpider(scrapy.Spider):
    name = 'avhub'
    allowed_domains = ['www.avbs5.xyz']
    start_urls = ['https://www.avbs5.xyz/china/']

    def parse(self, response):
        # print(response.text)
        doc = PyQuery(response.text)
        rows = doc('.video').items()
        for row in rows:
            try:
                item = avhubItem()
                item['time'] = row.find('.badge').text()
                if self.time_cmp(item['time'], min_time) < 0:
                    continue
                item['title'] = row.find('.video-title').text()
                item['views'] = row.find('.video-details').text()
                item['img'] = row.find('img').attr('src')

                href = doc('a').eq(0).attr("href")
                item['cell_url'] = href
                # $('#player script')[2]
                item['m3u8_url'] = self.get_video_url(href)
                item['create_time'] = time.localtime()
                yield item
            except Exception as e:
                print("parse" + e.__str__())
        next_href = doc('.prevnext').eq(0).attr('href')
        if next_href is not None:
            print(prefix + next_href)
            yield scrapy.Request(prefix + next_href, callback=self.parse,
                                 meta={'proxy': random.choice(self.proxies_)}, cookies=self.cookies)

    def get_video_url(self, href):
        mget = utils.mget(href)
        if mget is None:
            return ""
        doc = PyQuery(mget.text)
        m3u8 = doc('#player script').eq(2).text()
        match = re.findall("http.*m3u8", m3u8)
        if match.__len__() > 0:
            return match[0]
        return ""
