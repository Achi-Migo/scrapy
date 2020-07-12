import os
from demo1.spiders import utils
from scrapy.conf import settings

cache_path = settings.get('cache_path')
ffmpeg = 'ffmpeg '


def down_m3u8(m3u8, title):
    for f in os.listdir(cache_path):
        if f == title:
            return
    cmd = ffmpeg + " -i " + m3u8 + " -n -c copy " + cache_path + title
    exec(cmd)
    utils.update_already(title, m3u8)


def exec(cmd):
    print(cmd)
    p = os.popen(cmd)
    x = p.read()
    print(x)
    return x


def ffmpeg_down():
    avhub_list = utils.select_url()
    cache_list = []
    for f in os.listdir(cache_path):
        if f.endswith('.mp4') and os.path.getsize(cache_path + f) > 0:
            cache_list.append(f)
    for a in avhub_list:
        title = a['title']
        if not cache_list.__contains__(title):
            down_m3u8(a['m3u8_url'], title)
            pass


if __name__ == '__main__':
    ffmpeg_down()
    # print(platform.system())
