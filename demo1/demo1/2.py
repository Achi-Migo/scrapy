import time

def time_cmp(first_time, second_time):
    print(first_time)
    print(second_time)
    return int(time.strftime("%M%S", first_time)) - int(time.strftime("%M%S", second_time))

if __name__ == '__main__':
    cmp = time_cmp(time.strptime('09:59', "%M:%S"), time.strptime("03:00", "%M:%S"))
    print(cmp)
