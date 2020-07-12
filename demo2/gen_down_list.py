import os

base_url = "http://zakza.top:81/"
cache_path = "F:/大文件/avhub_idm/"
already_path = cache_path + "already.txt"
down_url_path = cache_path + "down_list.txt"


def gen():
    if True:
        return
    l = []
    with open(already_path, "a")as ap:
        for f in os.listdir(cache_path):
            path_f = cache_path + f
            if os.path.exists(path_f) and f.endswith(".mp4"):
                if os.path.getsize(path_f) > 0:
                    ap.write(f + "\n")
                    l.append(base_url + f)
                else:
                    os.remove(path_f)
        ap.close()

    l.__len__().__str__()
    # with open(down_url_path, "w")as f:
    #     f.writelines(l)
    #     f.close()
    pass


def remove():
    with open(already_path, 'r')as file:
        readlines = file.readlines()
        readlines_ = [x.replace("\n", "") for x in readlines]
        print(readlines_)
        for f in readlines:
            f = f.replace('\n', '')
            if f.endswith(".mp4"):
                os.remove(cache_path + f)


def rename():
    subfix = "_2.mp4"
    for f in os.listdir(cache_path):
        path_f = cache_path + f
        if f.endswith(subfix):
            replace = f.replace(subfix, '.mp4')
            if os.path.exists(cache_path+replace):
                os.remove(path_f)
            else:
                os.rename(path_f, cache_path + replace)


if __name__ == '__main__':
    gen()
    # rename()
