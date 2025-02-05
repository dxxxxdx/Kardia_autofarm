import time
import types
from ctypes.wintypes import tagMSG
from time import sleep
import keyboard
from mylib import func
import tkinter as tk
import multiprocessing as mp
import mylib.process_manager as pm
import gui_enter
import pyautogui
from queue import Empty

def miningauto_gui():
    manager = mp.Manager()
    with_bread = manager.Value('i', 0)
    working = manager.Value('i', 0)
    types = manager.Value('i', 1)
    queue = manager.Queue()

    root = tk.Tk()
    label1 = tk.Label(root, text="自动战斗系统", font=("", 24))
    label0 = tk.Label(root, text="请把页面挂在矿洞里面\n当前状态：", font=("", 18))
    label = tk.Label(root, text='初始化ing', fg="blue", font=("", 24))
    button = tk.Button(root, text="开始刷副本", font=("", 18), command=lambda: start_process())
    button2 = tk.Button(root, text="按当前未使用面包续航", font=("", 18), command=lambda: set_with_bread(button2))
    button_select = tk.Button(root,text="风矿",fg="green",command=lambda: type_select())
    def type_select():
        types.value = types.get() + 1
        cry = types.get() % 4
        if cry == 1 :
            button_select.config(text="风矿",fg="green")
            types.value = 1
        elif cry == 2:
            button_select.config(text="水矿",fg="blue")
            types.value = 2
        elif cry == 3 :
            button_select.config(text="地矿",fg="brown")
            types.value = 3
        else:
            button_select.config(text="火矿",fg="red")
            types.value = 4

    def set_with_bread(buttonx):
        with_bread.value = 1
        buttonx.config(text='正在使用面包续航 ')

    def start_process():
        if working.value == 0:
            working.value = 1
            process = pm.create_process(miningauto_guiprocess, (queue, with_bread, types))
            root.after(100, pm.loop_test_process_window_when_arg_and_do, process, root, working ,gui_enter.gui_enter)
            return process

    button.pack(pady=20)
    button2.pack(pady=20)
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+0")
    label1.pack()
    label0.pack()
    label.pack()
    button_select.pack(pady=40)
    root.after(100, func.label_updater, root, label, queue)
    def on_closing():
        root.destroy()
        gui_enter.gui_enter()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def miningauto_guiprocess(queue, with_bread, mine_types):
    while True:
        time.sleep(1)
        if not func.is_exist(func.fpth('mine_feature')):
            func.show_popup("你掉线了，请挂到矿洞")
            break
        mine_type = mine_types.get()
        roll_level = 0
        def rolling ():
            func.find_click("mine_feature")

            pyautogui.scroll(100)
        if mine_type == 1:
            while func.find_click(func.fpth('mine2')):
                func.find_click(func.fpth('mine2'))
                rolling()
                time.sleep(0.3)
        elif  mine_type == 2:
            while func.find_click(func.fpth('mine1')):
                func.find_click(func.fpth('mine1'))
                rolling()
                time.sleep(0.3)
        elif mine_type == 3:
            while func.find_click(func.fpth('mine3')):
                func.find_click(func.fpth('mine3'))
                rolling()
                time.sleep(0.3)
        elif mine_type == 4:
            while func.find_click(func.fpth('mine4')):
                func.find_click(func.fpth('mine4'))
                rolling()
                time.sleep(0.3)
        else:
            func.show_popup("你到底要挖什么？")
            break
        func.find_click(func.fpth('start_mine'))
        queue.put('搜索中')
        if func.is_exist(func.fpth('accident_event')):
            sleep(0.5)
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
            if func.is_exist(func.fpth('non_auto_fight')):
                func.find_click(func.fpth('non_auto_fight'))
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
    miningauto_gui()
