import os
from demo1.spiders import utils
from scrapy.conf import settings
from demo1.settings import *
from queue import Queue

ffmpeg = 'ffmpeg '
q = Queue()


def down_m3u8():
    get = q.get()
    title = get['title']
    m3u8 = get['m3u8_url']
    for f in os.listdir(cache_path):
        if f == title:
            return
    cmd = ffmpeg + " -i " + m3u8 + " -n -c copy " + cache_path + title
    x = exec(cmd)
    if str(x).__contains__('HTTP error 404 Not Found'):
        utils.update_already(title, m3u8, 404)
    else:
        utils.update_already(title, m3u8)


def exec(cmd):
    print(cmd)
    p = os.popen(cmd)
    x = p.read()
    print(x)
    return x


def ffmpeg_down():
    avhub_list = utils.select_url()
    # while True:
    # if avhub_list.__len__() == 0:
    #     break

    cache_list = []
    for f in os.listdir(cache_path):
        f = f.replace(" ", "")
        if f.endswith('.mp4') and os.path.getsize(cache_path + f) > 0:
            cache_list.append(f)
    # avhub_list = utils.select_url()

    for a in avhub_list:
        title = a['title']
        if not cache_list.__contains__(title):
            # down_m3u8(a['m3u8_url'], title)
            q.put(a)
            # break


from threading import Thread
import time


def multi_work():
    t = []
    t_num = q.qsize() // 2
    if q.qsize() > 10:
        t_num = 10
    for i in range(t_num):
        thread = Thread(target=down_m3u8, name='th-' + str(i))
        thread.setDaemon(True)
        t.append(thread)
    for i in t:
        i.start()
        time.sleep(0.5)
        i.join()
    print('muti work finish')
    pass


if __name__ == '__main__':
    ffmpeg_down()
    multi_work()
    # print(platform.system())
