
import time
import tkinter as tk
from tkinter import ttk
import pyautogui as pya
from numpy.random import random_integers

import threading as th
import core.recongnize_process as rp
import core.gui_tools as gt
import stages.main_enter
import queue
import core.often_operate
from core.op  import fpth



gem_dic = {
    "":"请选择",
    "red_small":"火碎片",
    "yellow_small": "地碎片",
    "green_small":"风碎片",
    "blue_small": "水碎片",
    "red_big": "红宝石",
    "yellow_big":"黄宝石",
    "green_big":"风宝石",
    "blue_big": "水宝石",
    "red_mid": "火结晶（不建议）",
    "yellow_mid":"地结晶（不建议）",
    "green_mid":"风结晶（不建议）",
    "blue_mid": "水结晶（不建议）",
}
inverse_gem_dic = {
    "请选择": "",
    "火碎片": "red_small",
    "地碎片": "yellow_small",
    "风碎片": "green_small",
    "水碎片": "blue_small",
    "红宝石": "red_big",
    "黄宝石": "yellow_big",
    "风宝石": "green_big",
    "水宝石": "blue_big",
    "火结晶（不建议）": "red_mid",
    "地结晶（不建议）": "yellow_mid",
    "风结晶（不建议）": "green_mid",
    "水结晶（不建议）": "blue_mid"
}

def mine_process():
    root = tk.Tk()
    root.attributes("-topmost", True)
    label1 = tk.Label(root, text=f"自动战斗系统\n\n ", font=("", 24))
    labelgem = tk.Label(root,text="",font=("",24))
    label0 = tk.Label(root, text="请把页面挂在副本入口\n当前状态：", font=("", 18))
    labelx = tk.Label(root, text='初始化ing', fg="blue", font=("", 24))
    bread = [0]
    queuex = queue.Queue()
    gem_type = []
    mine_t = None

    def set_with_bread(buttonx):
        nonlocal bread
        bread = [1]
        buttonx.config(text="正在使用面包续航 ")

    def start():
        nonlocal mine_t
        mine_t = th.Thread(target=mining, args=(gem_type, bread, queuex,))
        mine_t.start()
        root.after(100, lambda: gt.test_th(root, mine_t, back))

    def back():
        root.destroy()
        stages.main_enter.main_enter()

    def set_gem_type(event):
        nonlocal gem_type
        gem_type = [inverse_gem_dic.get( combobox.get(),None)]
        label1.config(text=gem_dic.get(gem_type[0],"请选择"), fg="blue")


    button = tk.Button(root, text="开始刷副本", font=("", 18), command=lambda: start())
    button2 = tk.Button(root, text="当前未使用面包续航", font=("", 18), command=lambda: set_with_bread(button2))
    combobox = ttk.Combobox(root, values=list(gem_dic.values()))
    combobox.current(0)
    combobox.pack(pady=30)
    combobox.bind("<<ComboboxSelected>>",set_gem_type)
    button.pack(pady=20)
    button2.pack(pady=20)
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+100")
    label1.pack()
    labelgem.pack()
    label0.pack()
    labelx.pack()
    root.after(100, lambda: gt.label_updater(root, labelx, queuex))

    root.mainloop()

def fighting(target_map, bread, queuex):
    if not rp.operate(fpth(target_map), "e"):
        gt.show_message("公主请把脚本挂在副本里", join=True)
        return
    while True:
        rp.operate(fpth(target_map), "c", multi_click=2, try_times=5)
        #还没写完
        queuex.put("搜索中")
        time.sleep(1)
        if rp.operate(fpth('no_stamina') , "e"):
            if bread[0] == 1:
                queuex.put('来口面包')
                rp.operate(fpth("confirm"), "c")
                time.sleep(0.7 )
                a = core.often_operate.eat_bread()
                if not a:
                    return
            else:
                gt.show_message("你没有面包还没体力\n真心刷不动")
                return
        time.sleep(0.5)
        if rp.operate(fpth('ap'), "e"):
            queuex.put("打着呢")
            time.sleep(0.8)
            while True:
                time.sleep(0.5)
                if rp.operate(fpth('winning'), "e"):
                    rp.operate(fpth('winning'), "c", multi_click=2)
                    time.sleep(0.8)
                    rp.operate(fpth('get_item'), "c")
                    time.sleep(2.8)
                    break
                time.sleep(0.5)
                if rp.operate(fpth('escape'), "e"):
                    gt.show_message("你怎么跑了？？")
                    break


def mining (gem_type, bread, queuex):
    if not rp.operate(fpth("mine_feature"), "e",try_times= 6):
        gt.show_message("公主请把脚本挂在矿洞里", join=True)
        return
    while True:
        while not rp.operate(fpth(gem_type), "e", multi_click=2, try_times=2):
            scroll_level = 0
            queuex.put("搜索中")
            time.sleep(1)
            if rp.operate(fpth('mine_buttom'), "e"):
                scroll_level = 1
                time.sleep(0.8)
            if rp.operate(fpth('mine_top'), "e"):
                scroll_level = 0
                time.sleep(0.8)
            if scroll_level == 0:
                pya.scroll(clicks=3)
            elif scroll_level == 1:
                pya.scroll(clicks=-3)
            else:
                pya.scroll(clicks=random_integers(low = -5,high= 5))
        rp.operate(fpth(gem_type), "e", multi_click=2, try_times=2)
        








