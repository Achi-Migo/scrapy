from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def step1():
    content = '''02:41
高考前的放松 后入双马尾JK
添加时间: 1 天 前
作者: forbear
查看: 74047  收藏: 311
留言: 8  积分: 2000'''
    split = content.strip().split('\n')
    for i in range(split.__len__()):
        print(i.__str__()+":"+split[i])


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('avhub')  # 你需要将此处的spider_name替换为你自己的爬虫名称
    process.start()
    # step1()
