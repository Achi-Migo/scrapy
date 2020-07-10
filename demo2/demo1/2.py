import time
import re


def time_cmp(first_time, second_time):
    print(first_time)
    print(second_time)
    return int(time.strftime("%M%S", first_time)) - int(time.strftime("%M%S", second_time))


if __name__ == '__main__':
    # cmp = time_cmp(time.strptime('00:58', "%M:%S"), time.strptime("02:00", "%M:%S"))
    # print(cmp)
    m3u8 = '''<script type="text/javascript">
var vHLSurl = "https://play.bo159159.com/20191101/OaBwHMcP/index.m3u8";
</script>'''
    match = re.findall("http.*m3u8", m3u8)
    print(match)
