import os
from demo1.mysql_utils import select_already
from scrapy.conf import settings

base_url = "http://zakza.top:81/"
cache_path = settings.get('cache_path')
down_url_path = cache_path + "down_list.txt"


def gen():
    l = []
    for f in os.listdir(cache_path):
        path_f = cache_path + f
        if os.path.exists(path_f) and f.endswith(".mp4"):
            if os.path.getsize(path_f) > 0:
                l.append(base_url + f)
            else:
                os.remove(path_f)
    with open(down_url_path, 'w')as f:
        f.writelines(l)
        f.close()
    pass


def remove(names):
    for name in names:
        if name.endswith(".mp4") and os.path.exists(cache_path + name):
            os.remove(cache_path + name)


def rename():
    subfix = "_2.mp4"
    for f in os.listdir(cache_path):
        path_f = cache_path + f
        if f.endswith(subfix):
            replace = f.replace(subfix, '.mp4')
            if os.path.exists(cache_path + replace):
                os.remove(path_f)
            else:
                os.rename(path_f, cache_path + replace)


if __name__ == '__main__':
    # already = select_already()
    gen()
    # remove(already)
    # rename()
