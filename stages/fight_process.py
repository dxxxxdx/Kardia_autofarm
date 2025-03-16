import time
import tkinter as tk
import stages.fight_enter
import threading as th
import core.recongnize_process as rp
import core.gui_tools as gt
import stages.main_enter
import queue
import core.often_operate

def fight_process(target_map):
    root = tk.Tk()
    root.attributes("-topmost", True)
    label1 = tk.Label(root, text=f"自动战斗系统\n\n{stages.fight_enter.fight_dic_inv.get(target_map)}\n", font=("", 24))
    label0 = tk.Label(root, text="请把页面挂在副本入口\n当前状态：", font=("", 18))
    labelx = tk.Label(root, text='初始化ing', fg="blue", font=("", 24))
    bread = [0]
    fight_t = None
    queuex = queue.Queue()
    def set_with_bread(buttonx):
        nonlocal bread
        bread = [1]
        buttonx.config(text="正在使用面包续航")

    def start ():
        nonlocal fight_t
        fight_t = th.Thread(target=fighting,args=(target_map,bread,queuex,))
        fight_t.start()
        root.after(100, lambda: gt.test_th(root, fight_t, back))

    def back():
        root.destroy()
        stages.main_enter.main_enter()

    button = tk.Button(root, text="开始刷副本", font=("", 18), command=lambda: start())
    button2 = tk.Button(root, text="当前未使用面包续航", font=("", 18), command=lambda: set_with_bread(button2))
    button.pack(pady=20)
    button2.pack(pady=20)
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+100")
    label1.pack()
    label0.pack()
    labelx.pack()
    root.after(100,lambda :gt.label_updater(root,labelx,queuex))
    root.mainloop()




def fighting(target_map,bread,queuex):
    rp.operate("update","e")
    if not rp.operate(target_map,"e"):
        gt.show_message("公主请把脚本挂在副本里",join=True)
        return
    fight_times = 0
    while True:
        rp.operate(target_map,"c",multi_click=2)
        queuex.put(f"搜索中\n已刷{fight_times}次")
        time.sleep(1)
        if rp.operate('accident_event',"e"):
            time.sleep(0.1)
            rp.operate('confirm2',"c")
            time.sleep(0.8)
            rp.operate('get_item',"c",try_times=3)
            time.sleep(0.8)
            fight_times += 1
            continue
        time.sleep(0.1)
        if rp.operate('no_stamina',"e"):
            if bread[0] == 1 :
                queuex.put('来口面包')
                rp.operate("confirm","c")
                time.sleep(0.8)
                a = core.often_operate.eat_bread()
                if not a :
                    return
            else :
                gt.show_message("你没有面包还没体力\n真心刷不动")
                return
        time.sleep(0.5)
        if rp.operate('ap',"e"):
            queuex.put(f"打着呢\n已刷{fight_times}次")
            time.sleep(0.8)
            rp.operate('fight_confirm',"c",multi_click=3)
            while True:
                time.sleep(0.5)
                if rp.operate('winning',"e"):
                    rp.operate('winning',"c",multi_click=2)
                    time.sleep(0.8)
                    rp.operate('get_item',"c")
                    time.sleep(2.8)
                    fight_times += 1
                    break
                time.sleep(0.5)
                if rp.operate('escape', "e"):
                    gt.show_message("你怎么跑了？？")
                    break







