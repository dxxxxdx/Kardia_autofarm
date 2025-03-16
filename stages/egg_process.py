import threading
import time
import core.recongnize_process as rp
import tkinter as tk
import queue
import core.gui_tools as gt
import keyboard
import stages.main_enter

def egg_process():
    root = tk.Tk()
    root.attributes("-topmost", True)
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+100")
    label = tk.Label(root, text="自动孵蛋系统",font=("",24))
    label.pack()
    egg_queue = queue.Queue()
    label2 = tk.Label(root,text="当前状态：")
    labelx = tk.Label(root,text="初始化中",fg="blue")
    label2.pack()
    labelx.pack()
    eggt = None
    def start ():
        nonlocal eggt
        eggt = threading.Thread(target=egging,args=(egg_queue,))
        eggt.start()
    def back():
        root.destroy()
        stages.main_enter.main_enter()
    root.after(100,start)
    root.after(100, lambda:gt.label_updater(root,labelx,egg_queue))
    root.after(100, lambda: gt.test_th(root, eggt,back))
    root.mainloop()




def egging(queuex):
    stopflag = 0
    def stop(event):
        if event.name == "shift" :
            nonlocal stopflag
            stopflag = 1
    keyboard.on_press(stop)
    # 初始化移动到孵蛋房间
    while not rp.operate("eggroom_feature","e"):
        if stopflag:break
        rp.operate("eggroom_enter","c")
        time.sleep(1)
    i = 0
    while True :
        time.sleep(1)
        if stopflag:break
        i += 1
        queuex.put(f"正在运行，时间已过{i}秒")
        if  rp.operate("egg_finish","e") or  rp.operate("egg_empty","e"):
            queuex.put("孵好了开拐")
            rp.operate("sell","c")
            time.sleep(1)
            rp.operate("confirm","c")
            time.sleep(1)
            rp.operate("fill","c")
            time.sleep(1)
            rp.operate("sort_by_class","c")
            time.sleep(1)
            rp.operate("egg1","c")
            time.sleep(1)
        else:
            pass


























