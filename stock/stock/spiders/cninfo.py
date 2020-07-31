# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq
from scrapy.http import Request, Response


class CninfoSpider(scrapy.Spider):
    name = 'cninfo'
    allowed_domains = ['www.cninfo.com.cn']
    start_urls = ['http://www.cninfo.com.cn/']

    def parse(self, response: Response):
        text = response.text
        doc = pq(text)
        pass
