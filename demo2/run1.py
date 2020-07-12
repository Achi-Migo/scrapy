from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.conf import settings
import requests
from demo1.spiders import utils


def step1():
    get = requests.get(url="https://play.520520bo.com/20200425/kM800nDJ/index.m3u8", headers=utils.getHeader())
    text = get.text
    print(text)


import datetime
import os
import re
import threading
import time
import requests
from queue import Queue

proxies = {'http': 'http://127.0.0.1:1080'}
mer = False
requests.packages.urllib3.disable_warnings()
request = requests.Session()
request.proxies = proxies
request.headers = utils.getHeader()
request.verify = False

# cache_path = 'F:/大文件/cache/'
cache_path = 'F:/大文件/avhub_idm/'
# ffmpeg = 'J:/Debug/ffmpeg/bin/ffmpeg.exe'

# cache_path = "~/down/scrapy/demo2/cache/"
ffmpeg = 'ffmpeg '
dist_path = "/home/sync/cache/"


# timeout=15


# 预下载，获取m3u8文件，读出ts链接，并写入文档
def down(url, base_url):
    # 当ts文件链接不完整时，需拼凑
    resp = request.get(url, timeout=20)
    m3u8_text = resp.text
    for line in m3u8_text.split("\n"):
        if ".m3u8" in line:
            m3u8_url = base_url
            if 'http' in line:
                m3u8_url = line
            else:
                m3u8_url = base_url + line
            m3u8_text = request.get(url=m3u8_url, timeout=20).text
            break
    # print(m3u8_text)
    # 按行拆分m3u8文档
    ts_queue = Queue(10000)
    lines = m3u8_text.split('\n')
    s = len(lines)
    # 找到文档中含有ts字段的行
    concatfile = cache_path + "s" + '.txt'
    for i, line in enumerate(lines):
        if '.ts' in line:
            if 'http' in line:
                # print("ts>>", line)
                ts_queue.put(line)
            else:
                line = base_url + line
                ts_queue.put(line)
                # print('ts>>',line)
            filename = re.search('([a-zA-Z0-9-_]+.ts)', line).group(1).strip()
            # 一定要先写文件，因为线程的下载是无序的，文件无法按照
            # 123456。。。去顺序排序，而文件中的命名也无法保证是按顺序的
            # 这会导致下载的ts文件无序，合并时，就会顺序错误，导致视频有问题。
            open(concatfile, 'a+').write("file %s\n" % filename)
            print("\r", '文件写入中', i, "/", s, end="", flush=True)
    return ts_queue, concatfile


# 线程模式，执行线程下载
def run(ts_queue, headers):
    while not ts_queue.empty():
        url = ts_queue.get()
        filename = re.search('([a-zA-Z0-9-_]+.ts)', url).group(1).strip()
        try:
            r = request.get(url, timeout=20)
            with open(cache_path + filename, 'wb') as fp:
                fp.write(r.content)
                fp.close()
            print("\r", '任务文件 ', filename, ' 下载成功', end="", flush=True)

        except Exception as e:
            print("down ts file")
            print(e)
            print('任务文件 ', filename, ' 下载失败')
            ts_queue.put(url)


def exec(cmd):
    print(cmd)
    p = os.popen(cmd)
    x = p.read()
    print(x)
    return x


# 视频合并方法，使用ffmpeg
def merge(concatfile, name):
    global mer
    try:
        path = cache_path + name
        # command = 'ffmpeg -y -f concat -i %s -crf 18 -ar 48000 -vcodec libx264 -c:a aac -r 25 -g 25 -keyint_min 25 -strict -2 %s' % (concatfile, path)
        command = ffmpeg + ' -y -f concat -safe 0 -i %s -c copy %s' % (concatfile, path)
        # command = 'J:/Debug/ffmpeg/bin/ffmpeg.exe -y -f concat -i %s -bsf:a aac_adtstoasc -c copy %s' % (concatfile, path)
        exec(command)
        print('视频合并完成')
        mer = True
    except:
        print('合并失败')


def remove():
    global mer
    s = cache_path + 's.txt'
    try:
        if os.path.exists(s):
            for line in open(s):
                line = re.search('file (.*?ts)', line).group(1).strip()
                # print(line)
                cache_path_line = cache_path + line
                if os.path.exists(cache_path_line):
                    os.remove(cache_path_line)
            print("ts文件全部删除")
            os.remove(s)
            print('文件删除成功')
            mer = False
    except:
        print('文件删除失败')


def init(url, name: str):
    if not name.endswith(".mp4"):
        name = name + '.mp4'

    playlist = "playlist.m3u8"
    if str(url).endswith(playlist):
        base_url = str(url).replace(playlist, "")
    else:
        base_url = re.findall("https?://[^/]*/", url, re.I)[0]
    start = datetime.datetime.now().replace(microsecond=0)
    print("文件开始写入")
    s, concatfile = down(url, base_url)
    print('\n')
    print("文件写入结束")
    # 获取队列元素数量
    num = s.qsize()
    # 根据数量来开线程数，每五个元素一个线程
    # 最大开到50个
    print("下载任务开始")
    if num > 5:
        t_num = num // 5
    else:
        t_num = 1
    if t_num > 50:
        t_num = 50
    # print(s,concatfile)
    threads = []
    for i in range(t_num):
        t = threading.Thread(target=run, name='th-' + str(i), kwargs={'ts_queue': s, 'headers': utils.getHeader()})
        t.setDaemon(True)
        threads.append(t)
    for t in threads:
        time.sleep(0.4)
        t.start()
    for t in threads:
        t.join()
    print('\n')
    print("下载任务结束")
    end = datetime.datetime.now().replace(microsecond=0)
    print('写文件及下载耗时：' + str(end - start))
    merge(concatfile, name)
    remove()
    utils.update_already(title, url)
    over = datetime.datetime.now().replace(microsecond=0)
    print('合并及删除文件耗时：' + str(over - end))
    print("所有任务结束")
    print('任务总时长：', over - start)


from demo1.spiders import utils


def down_ts():
    url = "https://cdn.com-ml-zyw.com/20200622/kF79cwc8/index.m3u8"
    filename = "性欲旺盛的美女少妇老公出差寂寞难耐和网友酒店私会,说最喜欢用香蕉插,不停的拍打逼逼求操"
    playlist = "playlist.m3u8"
    if str(url).endswith(playlist):
        base_url = str(url).replace(playlist, "")
    else:
        base_url = re.findall("https?://[^/]*/", url, re.I)[0]
    resp = request.get(url, timeout=20)
    m3u8_text = resp.text
    for line in m3u8_text.split("\n"):
        if ".m3u8" in line:
            i_ = re.findall("/[^/]*m3u8", line, re.I)[0]
            line = line.replace(i_, "")
            base_url = base_url + line

    cache_list = []
    for f in os.listdir(cache_path):
        cache_list.append(f)
    with open(cache_path + "s.txt")as f:
        readlines = f.readlines()
        for l in readlines:
            l = l.replace("\n", "").replace("file ", "")
            if not cache_list.__contains__(l):
                r = request.get(base_url + l, timeout=20)
                with open(cache_path + l, 'wb') as fp:
                    fp.write(r.content)
                    fp.close()
                print("\r", '任务文件 ', l, ' 下载成功', end="", flush=True)


def down_m3u8(m3u8, title):
    cmd = ffmpeg + " -i " + m3u8 + " -n -c copy " + cache_path + title
    exec(cmd)
    utils.update_already(title, m3u8)


def exec(cmd):
    print(cmd)
    p = os.popen(cmd)
    x = p.read()
    print(x)
    return x


if __name__ == '__main__':
    # down_m3u8("https://video.huishenghuo888888.com/putong/20200425/GxJ93Kvb/index.m3u8","esu")
    # name = input('请输入视频名称：')
    # url = input('请输入视频链接：').strip()
    # 测试用链接：https://yiyi.55zuiday.com/ppvod/70B5A6E3A150A99882E28EC793CAF519.m3u8
    # 链接电影：地球最后的夜晚
    # init("https://video.huishenghuo888888.com/putong/20200425/GxJ93Kvb/index.m3u8", "esu")
    # merge(cache_path+"s.txt","esu")
    # remove()

    avhub_list = utils.select_url()
    while True:
        if avhub_list.__len__() == 0:
            break

        cache_list = []
        for f in os.listdir(cache_path):
            f = f.replace(" ", "")
            if f.endswith('.mp4') and os.path.getsize(cache_path + f) > 0:
                cache_list.append(f)
        avhub_list = utils.select_url()
        for a in avhub_list:
            title = a['title']
            if not cache_list.__contains__(title):
                down_m3u8(a['m3u8_url'], title)
                break

# down_ts()
