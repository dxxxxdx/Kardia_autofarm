import time
from ctypes.wintypes import tagMSG
from time import sleep
import keyboard
from mylib import func
import tkinter as tk
import multiprocessing as mp
import mylib.process_manager as pm
import gui_enter
from queue import Empty

def fightauto_gui():
    manager = mp.Manager()
    with_bread = manager.Value('i', 0)
    working = manager.Value('i', 0)
    queue = manager.Queue()

    root = tk.Tk()
    label1 = tk.Label(root, text="自动战斗系统", font=("", 24))
    label0 = tk.Label(root, text="请把页面挂在副本入口\n当前状态：", font=("", 18))
    label = tk.Label(root, text='初始化ing', fg="blue", font=("", 24))
    button = tk.Button(root, text="开始刷副本", font=("", 18), command=lambda: start_process())
    button2 = tk.Button(root, text="按当前未使用面包续航", font=("", 18), command=lambda: set_with_bread(button2))

    def set_with_bread(button3):
        with_bread.value = 1
        button3.config(text='正在使用面包续航')

    def start_process():
        if working.value == 0:
            working.value = 1
            process = pm.create_process(fightauto_guiprocess, (queue, with_bread, working))
            root.after(100, pm.loop_test_process_window_when_arg_and_do, process, root, working ,gui_enter.gui_enter)
            return process

    button.pack(pady=20)
    button2.pack(pady=20)
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x500+{screen_width - 550}+0")
    label1.pack()
    label0.pack()
    label.pack()
    root.after(100, func.label_updater, root, label, queue)
    def on_closing():
        root.destroy()
        gui_enter.gui_enter()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def fightauto_guiprocess(queue, with_bread, working):
    while True:
        time.sleep(1)
        func.find_click(func.fpth("fight3"))
        time.sleep(0.3)
        func.find_click(func.fpth('fight3'))
        time.sleep(1)
        func.find_click(func.fpth('fight_confirm'))
        queue.put('搜索中')
        if func.is_exist(func.fpth('accident_event')):
            time.sleep(0.5)
            func.find_click(func.fpth('confirm2'))
            sleep(0.5)
            func.find_click(func.fpth('get_item'))
            sleep(0.5)
            continue
        elif func.is_exist(func.fpth('no_stamina')):
            if with_bread.value == 1:
                func.find_click(func.fpth('confirm'))
                sleep(0.5)
                with_bread.value = func.eat_bread()
            else:
                queue.put('没体力')
                func.find_click(func.fpth('confirm'))
                func.popup("你没有面包还没体力\n真心刷不动")
                break
        elif func.is_exist(func.fpth('ap')):
            # 已经进入战斗了
            #if func.is_exist(func.fpth('non_auto_fight')):
            #    func.find_click(func.fpth('non_auto_fight'))
            queue.put('打着呢')
            while True:
                time.sleep(0.5)
                if func.is_exist(func.fpth('winning')):
                    time.sleep(0.5)
                    func.find_click(func.fpth('winning'))
                    sleep(0.5)
                    func.find_click(func.fpth('get_item'))
                    time.sleep(3)
                    break
                elif func.is_exist(func.fpth('escape')):
                    func.popup("你怎么跑了？？？")
                    break

if __name__ == '__main__':
    fightauto_gui()
