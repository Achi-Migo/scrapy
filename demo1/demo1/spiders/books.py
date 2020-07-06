import scrapy

from ..items import BookItem


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for sel in response.css('article.product_pod'):
            book = BookItem()
            book['name'] = sel.xpath('./h3/a/@title').extract_first()
            book['price'] = sel.css('p.price_color::text').extract_first()
            yield book
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
            # 如果找到下一页的URL，得到绝对路径，构造新的Request 对象
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
