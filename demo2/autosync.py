import os
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import datetime

fixed = 60
# fixed = 5
cache_path = "~/down/scrapy/demo2/cache/"
already_path = "~/down/scrapy/demo2/already.txt"
dist_path = "/home/sync/cache"


def schedule():
    scheduler = BlockingScheduler()
    scheduler.add_job(run, 'interval', seconds=fixed, next_run_time=datetime.datetime.now())

    scheduler.start()
    print("init" + time.localtime().__str__())
    pass


def run():
    print("start:" + time.localtime().__str__())
    # time.sleep(16)
    wait_sync = []
    with open(already_path, 'a+')as already:
        read_lines = already.readlines()

        for f in os.listdir(cache_path):
            path_f = cache_path + f
            if os.path.exists(path_f) and os.path.getsize(path_f) == 0:
                os.remove(path_f)
            if not read_lines.__contains__(f):
                sync(path_f)
                already.write(f + "\n")
                remove(path_f)
        already.close()
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
    schedule()
