import mylib.func as func
import time
import multiprocessing
# 用这里面的函数创建进程，进程会进行检测，检测完毕进程结束

def farm_test():
    print('将程序挂在农场里即可开始！')
    while True:
        running = func.is_exist(func.fpth('farm_feature'))
        time.sleep(0.8)
        if running:
            break
    print('已经匹配到你的农场！')

def non_farm_test():
    print('检测不到农场就结束')
    while True :
        if func.is_exist(func.fpth('farm_feature'))!= 1: break
        time.sleep(0.8)
    print('已经掉线！')
    return 1
def non_eggroom_test():
    if not func.is_exist(func.fpth('sell')):
        print('已经掉线！')
        return 1
    else:
        return 0
def non_selarm_test():
    while True :
        if not func.is_exist(func.fpth('selarm_feature')):
            print('已经掉线！')
            return 1
