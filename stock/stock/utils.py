import random
import requests
import time


def random_ip():  # line:354:def method8():
    OOOOOO0000000000O = random.randint(1, 255)  # line:355:a = random.randint(1, 255)
    O0OOOO0OOO0OO0O0O = random.randint(1, 255)  # line:356:b = random.randint(1, 255)
    O000O00000OOO00OO = random.randint(1, 255)  # line:357:c = random.randint(1, 255)
    O0OOO000OOO0OO0OO = random.randint(1, 255)  # line:358:d = random.randint(1, 255)
    gen_ip = str(OOOOOO0000000000O) + '.' + str(O0OOOO0OOO0OO0O0O) + '.' + str(O000O00000OOO00OO) + '.' + str(
        O0OOO000OOO0OO0OO)
    return gen_ip  # line:359:return str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)


def random_ua():
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Dalvik/1.6.0 (Linux; U; Android 4.2.1; 2013022 MIUI/JHACNBL30.0)",
        "Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; HUAWEI MT7-TL00 Build/HuaweiMT7-TL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "AndroidDownloadManager",
        "Apache-HttpClient/UNAVAILABLE (java 1.4)",
        "Dalvik/1.6.0 (Linux; U; Android 4.3; SM-N7508V Build/JLS36C)",
        "Android50-AndroidPhone-8000-76-0-Statistics-wifi",
        "Dalvik/1.6.0 (Linux; U; Android 4.4.4; MI 3 MIUI/V7.2.1.0.KXCCNDA)",
        "Dalvik/1.6.0 (Linux; U; Android 4.4.2; Lenovo A3800-d Build/LenovoA3800-d)",
        "Lite 1.0 ( http://litesuits.com )",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
        "Mozilla/5.0 (Linux; U; Android 4.1.1; zh-cn; HTC T528t Build/JRO03H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30; 360browser(securitypay,securityinstalled); 360(android,uppayplugin); 360 Aphone Browser (2.0.4)",
    ]
    return random.choice(USER_AGENT_LIST)


def mget(url):
    rand_time = random.randint(200, 300) / 1000
    time.sleep(rand_time)
    resp = None
    try:
        headers = random_header()
        proxies = {'http': 'http://127.0.0.1:1080'}
        resp = requests.get(url, headers=headers, proxies=proxies, timeout=10, verify=False)
    except Exception as e:
        print("mget" + e.__str__())
        raise
    return resp


def time_cmp(first_time, second_time):
    return int(time.strftime("%M%S", time.strptime(first_time, "%M:%S"))) - int(
        time.strftime("%M%S", time.strptime(second_time, "%M:%S")))


def random_header():
    ip = random_ip()
    headers = {'Accept-Language': 'zh-CN,zh;q=0.9',
               'User-Agent': random_ua(),
               'X-Forwarded-For': random_ip()
               }
    return headers;
