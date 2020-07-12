import random
import requests
import time
import os
import subprocess
from demo1.mysql_utils import *



def random_ip():  # line:354:def method8():
    OOOOOO0000000000O = random.randint(1, 255)  # line:355:a = random.randint(1, 255)
    O0OOOO0OOO0OO0O0O = random.randint(1, 255)  # line:356:b = random.randint(1, 255)
    O000O00000OOO00OO = random.randint(1, 255)  # line:357:c = random.randint(1, 255)
    O0OOO000OOO0OO0OO = random.randint(1, 255)  # line:358:d = random.randint(1, 255)
    gen_ip = str(OOOOOO0000000000O) + '.' + str(O0OOOO0OOO0OO0O0O) + '.' + str(O000O00000OOO00OO) + '.' + str(
        O0OOO000OOO0OO0OO)
    return gen_ip  # line:359:return str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)


def mget(url):
    rand_time = random.randint(200, 400) / 1000
    time.sleep(rand_time)
    resp = None
    try:
        ip = random_ip()
        headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                   'X-Forwarded-For': ip
                   }
        proxies = {'http': 'http://127.0.0.1:1080'}
        resp = requests.get(url
                            , headers=headers
                            , proxies=proxies
                            # , timeout=10
                            , verify=False)
    except Exception as e:
        print("mget" + e.__str__())
        raise
    return resp


def time_cmp(first_time, second_time):
    return int(time.strftime("%M%S", time.strptime(first_time, "%M:%S"))) - int(
        time.strftime("%M%S", time.strptime(second_time, "%M:%S")))


def getHeader():
    headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
               'X-Forwarded-For': random_ip()
               }
    return headers


def down_u3m8(u3m8, title):
    cmd = "J:/Debug/ffmpeg/bin/ffmpeg.exe -i " + u3m8 + " -n -c copy F:/大文件/avhub/" + title + ".mp4"
    # excuteCommand(cmd)



def excuteCommand(cmd):
    print(cmd)
    p = os.popen(cmd)
    x = p.read()
    print(x)


def down():
    avhub_list = select_url()
    for a in avhub_list:
        down_u3m8(a['m3u8_url'], str(a['title']).replace(" ", ""))


if __name__ == '__main__':
    down()
