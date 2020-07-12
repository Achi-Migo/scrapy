from demo1.mysql_utils import select_already
import os
import platform

if platform.system().lower().startswith('win'):
    cache_path = 'F:/大文件/cache/'
else:
    cache_path = "/var/www/html/"


def remove():
    already = select_already()
    for name in already:
        if os.path.exists(cache_path + name):
            os.remove(cache_path + name)


if __name__ == '__main__':
    remove()
