import multiprocessing as mp
import queue
import time
import uuid
import  pyautogui as pg
from numpy.f2py.auxfuncs import throw_error
import core.op as op
import threading as th


global_queue = [mp.Queue(),mp.Queue()]

#出于性能考虑，开一个单独进程进行图像识别

def recongnize_process( ):
    #初始化
    img_input = mp.Queue()
    img_output = mp.Queue()
    p = mp.Process(target=recongnize_func,name="recongnize",args=(img_input,img_output,))
    global global_queue
    global_queue = (img_input, img_output)
    p.start()
    return img_input, img_output


def recongnize_func(img_input,img_output):

    #进程内部

    while img_input is not None:
        time.sleep(0.01)
        print("有"+ str(img_input.qsize())+"任务排队")
        op.capture_screenshot_func()
        img_op = ImgOperation
        try:
            img_op = img_input.get()
        except queue.Empty as e:
            pass
        if img_op is not None and img_op.name != "":
            path = op.fpth(img_op.name)
            print("尝试寻找"+img_op.name)

        elif img_op.name == "update":
            #update作为特殊参数传入后会尝试更新截图
            op.capture_screenshot_func()
            continue
        else:
            continue

        center = op.find_img(path,single_find=img_op.single_find)
        if center is None:
            img_output.put(ImgResult(img_op.name,-1,img_op.uuid))
            continue
        while center == [] and img_op.try_times > 1:
            center = op.find_img(path, single_find=img_op.single_find)
            print(f"find retry:{img_op.try_times}")
            img_op.try_times -= 1
            time.sleep(0.03)
            op.capture_screenshot_func()


        success = False
        while not success:

            #几种操作，点击，移动，寻找

            if img_op.operation == "c" :
                i = 0
                for tar_area in center:
                    for j in range(img_op.multi_click):
                        pg.click(tar_area)
                        time.sleep(0.01)
                    i += 1
                img_output.put(ImgResult(img_op.name,i,img_op.uuid))
                success = True

            elif img_op.operation == "m" :
                i = 0
                for tar_area in center:
                    pg.moveTo(tar_area)
                    time.sleep(0.01)
                    i += 1
                img_output.put(ImgResult(img_op.name,i,img_op.uuid))
                success = True

            elif img_op.operation == "e" :
                i = 0
                for tar_area in center:
                    i += 1
                img_output.put(ImgResult(img_op.name,i,img_op.uuid))
                success = True
            else :
                throw_error(ValueError)




def get_recongnize_process():

    for p in mp.active_children():
        if p.name == "recongnize":
            return p


class ImgOperation :
    #识别类，将目标打包送给识别进程
    def __init__(self, name, operation, single_find=True, try_times=1, multi_click=1):
        self.name = name
        self.operation = operation
        self.single_find = single_find
        self.try_times = try_times
        self.uuid = str(uuid.uuid1())
        self.multi_click = multi_click
    name = ""
    operation = ""
    single_find = True
    try_times = False
    uuid = ""
    multi_click = 0



class ImgResult :
    #识别结果
    def __init__(self, name , times, uuidx):
        self.name = name
        self.times : int =  times
        self.uuid = uuidx
    name = ""
    times = 0
    uuid = ""


def operate (name,operation,single_find=True,try_times =1,multi_click=1):

    #最常用的识别，任务多时可能会被阻塞

    starttime = time.time()
    img = ImgOperation(name,operation,single_find,try_times,multi_click)
    uuidx = img.uuid
    global global_queue
    img_input, img_output = global_queue
    img_input.put(img)
    res = ImgResult
    while True:
        try :
            res = img_output.get()
            if res.uuid !=  uuidx :
                img_output.put(res)
                continue
            break
        except queue.Empty :
            continue
    endtime = time.time()
    print(f"op消耗{endtime-starttime:.2f}")
    if res.times == -1  :
        throw_error(ValueError)
        return 0
    return int(res.times)





def wait_for(root,tarimg,end_func):

    #窗口调用后，不断识别是否有目标，识别到会执行endfunc

    t = th.Thread(target=wait_for_thread,args=(root,tarimg,end_func))
    t.start()
    return t

def wait_for_thread(root,tarimg,end_func):
    while True:
        if tarimg == "testxx":
            time.sleep(1)
            root.after(10, end_func)
            return
        if not root.winfo_exists():
            return
        res = operate(tarimg,"e")
        if res:
            root.after(10,end_func)
            return
        else:
            time.sleep(0.3)
            continue



def close_all_process():
    #清理进程，准备关闭
    print("即将关闭")
    for p in mp.active_children():
        p.terminate()
        p.join()








