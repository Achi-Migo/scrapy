import os
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import datetime
from queue import Queue
import threading
from threading import Lock

fixed = 60
# fixed = 5
cache_path = "/root/down/scrapy/demo2/cache/"
already_path = "/root/down/scrapy/demo2/already.txt"
dist_path = "/home/sync/cache"
block_queue = Queue()
lock = Lock()


def schedule():
    scheduler = BlockingScheduler()
    scheduler.add_job(run, 'interval', seconds=fixed, next_run_time=datetime.datetime.now())

    scheduler.start()
    print("init" + time.localtime().__str__())
    pass


def work():
    f = block_queue.get()
    path_f = cache_path + f
    sync(path_f)
    lock.acquire()
    with open(already_path, 'a')as already:
        already.write(f + "\n")
        already.close()
    remove(path_f)
    lock.release()


def multi_sync():
    num = block_queue.qsize()
    # 根据数量来开线程数，每五个元素一个线程
    # 最大开到50个
    print("下载任务开始")
    if num > 2:
        t_num = num // 2
    else:
        t_num = 1
    if t_num > 10:
        t_num = 10
    # print(s,concatfile)
    threads = []
    for i in range(t_num):
        t = threading.Thread(target=work, name='th-' + str(i))
        t.setDaemon(True)
        threads.append(t)
    for t in threads:
        time.sleep(0.4)
        t.start()
        t.join()


def run():
    print("start:" + time.localtime().__str__())
    # time.sleep(16)
    wait_sync = []
    with open(already_path, 'a+')as already:
        read_lines = already.readlines()

        for f in os.listdir(cache_path):
            path_f = cache_path + f
            if os.path.exists(path_f) and os.path.getsize(path_f) == 0:
                os.remove(f)
            if not read_lines.__contains__(f):
                block_queue.put(path_f)
        already.close()
    multi_sync()

    print("end:" + time.localtime().__str__())
    print("finish")
    pass


def remove(f):
    if os.path.exists(f):
        os.remove(f)
    pass


def sync(f):
    # cmd = "scp -r -P1122 " + f + "   root@zakza.top:/home/sync"
    cmd = "rsync -avuz -e 'ssh -p 1122' " + f + " root@zakza.top:" + dist_path
    print(cmd)
    p = os.popen(cmd)
    x = p.read()
    print(x)
    pass


def check():
    pass


if __name__ == '__main__':
    # schedule()
    import requests
    from demo1.spiders import utils
    get = requests.get("http://www.avbs5.xyz/china/",headers=utils.getHeader())
    text = get.text
    print(text)
