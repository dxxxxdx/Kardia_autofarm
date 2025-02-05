import time
from time import sleep

import keyboard
from mylib import func
import tkinter as tk
import multiprocessing as mp
import mylib.process_manager as pm
import gui_enter
from queue import Empty
import mylib.imgtest as imgtest
global working

import  pyautogui
import  random
def eggauto_gui():
    # 创建gui
    root = tk.Tk()
    label1 = tk.Label(root, text="自动孵蛋中", font=("", 24))
    label0 = tk.Label(root, text="当前状态", font=("", 18))
    label = tk.Label(root, text='进行中', fg="blue",font=("", 24))
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x500+{screen_width - 550}+0")
    label1.pack()
    label0.pack()
    label.pack()
    queue = mp.Queue()
    process = pm.create_process(eggauto_guiprocess, args=(queue,))
    root.after(100,pm.loop_test_process_window_and_do,process,root,gui_enter.gui_enter)
    root.after(1000,func.label_updater,root, label, queue)
    def on_closing():
        root.destroy()
        gui_enter.gui_enter()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()




def eggauto_guiprocess(queue):
    # 进入孵蛋室
    func.find_click(func.fpth('eggroom_enter'))
    time.sleep(0.3)

    def workingset ():
        global working
        working = 0
    keyboard.on_press_key("shift", lambda e: workingset())
    times = 0
    global working
    working = 1
    while True:
        working += imgtest.non_eggroom_test()
        if working != 1 :
            func.find_click(func.fpth('farm_enter'))
            break
        elif func.is_exist(func.fpth('egg_finished'))or func.is_exist(func.fpth('egg_empty')):
            print('孵好了，开拐')
            queue.put('孵好了，开拐')
            time.sleep(0.5)
            func.find_click(func.fpth('sell'))
            time.sleep(0.5)
            func.find_click(func.fpth('confirm'))
            time.sleep(0.5)
            print('自动装填，请确定蛋种类')
            queue.put('自动装填，请确定蛋种类')
            func.find_click(func.fpth('fill'))
            time.sleep(0.5)
            func.find_click(func.fpth('sort_by_class'))
            time.sleep(0.5)
            # 待拓展
            func.find_click(func.fpth('egg1'))
            time.sleep(0.5)
        else:
            print('未发现可操作步骤,按shift结束')
            queue.put(f'正在孵蛋\n按shift结束\n已经经过{times}秒')
            times +=1
            func.find_click(func.fpth('eggroom_place'))
            pyautogui.drag(xOffset= 0, yOffset= random.randint(-30,30),duration=0.5,button='left')



if __name__ == "__main__":
    eggauto_gui()
