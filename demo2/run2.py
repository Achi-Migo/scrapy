import os
from demo1.spiders import utils

# cache_path = "/var/www/html/"
cache_path = 'F:/大文件/cache/'
ffmpeg = 'ffmpeg '
dist_path = "/home/sync/cache/"


# already_path = cache_path + "already.txt"


def down_u3m8(u3m8, title):
    for f in os.listdir(cache_path):
        if f == title:
            return
    cmd = ffmpeg + " -i " + u3m8 + " -n -c copy " + cache_path + title
    exec(cmd)


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
            down_u3m8(a['m3u8_url'], title)
            pass


if __name__ == '__main__':
    # name = input('请输入视频名称：')
    # url = input('请输入视频链接：').strip()
    # 测试用链接：https://yiyi.55zuiday.com/ppvod/70B5A6E3A150A99882E28EC793CAF519.m3u8
    # 链接电影：地球最后的夜晚
    # init("https://video.huishenghuo888888.com/putong/20200628/QvaSnzU6/500kb/hls/index.m3u8", "lanse")
    # merge(cache_path+"s.txt","lanse")
    # remove()
    ffmpeg_down()
