import mylib.func
import multiprocessing as mp
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
import mylib.imgtest as imgtest
from mylib.func import find_click
from mylib.process_manager import loop_test_process_window


def selarmauto():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+0")
    button = tk.Button(root,text="building",command=selarm_building(root))
    button2 = tk.Button(root,text="parkour",command=selarm_parkour(root))

    p1 = pm.create_process(imgtest.non_selarm_test,)
    button3 = tk.Button(root,text="hitmouse",command=selarm_hitmouse(root,p1))
    button.pack(pady=20)
    button2.pack(pady=20)
    button3.pack(pady=20)
    pm.loop_test_process_window(p1,root)
    root.mainloop()


def selarm_hitmouse(root,p):

    func.find_click("hitmouse_enter")
    time.sleep(1)
    onclosing(root,p)
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+0")
    label = tk.Label(root,text="正在打地鼠")
    label.pack(pady=20)
    p = pm.create_process(selarm_hitmouse_process)
    pm.loop_test_process_window(p,root)
    root.mainloop()

def selarm_hitmouse_process():
    while True:
        time.sleep(0.01)
        func.find_click("hitmouse_enter")
        if func.is_exist("game_over"):
            break


def selarm_parkour(root):
    return 1

def selarm_building(root):
    return 1

def onclosing(root,p):
    p.terminate()
    root.destroy()














