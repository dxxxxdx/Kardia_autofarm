import sys
import time
import tkinter as tk

import eggauto
import fightauto
from mylib.imgtest import farm_test,non_farm_test
import multiprocessing as mp
import mylib.func as func
import mylib.process_manager as pm

def gui_enter():

    print('欢迎使用自动脚本')
    root = tk.Tk()
    label1 = tk.Label(root, text="欢迎使用游戏自动脚本", font=("", 24))
    label2 = tk.Label(root, text='将程序挂在农场里即可开始！\n需要检测到屏幕上有模拟器窗口\n\n\n余胜军徒儿制作\n\n感谢python之父的支持', font=("", 18))
    img_pth = tk.PhotoImage(file=func.fpth("sponsor"))
    label3 = tk.Label(root, image=img_pth)
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+0")
    label1.pack()
    label2.pack()
    label3.pack()
    #创建与窗口绑定的进程
    process = pm.create_process(farm_test)
    root.after(100,pm.loop_test_process_window_and_do, process,root,sub_gui_enter)
    def on_closing():
        process.terminate()
        process.join()
        root.destroy()
        pm.close_all_mp_processes(1)


    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()



def sub_gui_enter():
    print("进入子页面")
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+0")
    def loop_process(tarfunc,root1):
        #进入子页面的窗口
        pm.create_process(tarfunc)
        root1.destroy()
        farm_test_process.terminate()
        farm_test_process.join()
    label1= tk.Label(root,text="已经检测到你的农场\n 请不要离开\n", font=("", 24))
    button1 = tk.Button(root, text="自动孵蛋", font=("", 18), command=lambda: loop_process(eggauto.eggauto_gui,root))
    button2 = tk.Button(root, text="自动刷本", font=("", 18), command=lambda: loop_process(fightauto.fightauto_gui,root))
    button3 = tk.Button(root, text="正在开发", font=("", 18), command=lambda: print("按钮3被点击"))
    label1.pack(pady=20)
    button1.pack(pady=20)
    button2.pack(pady=20)
    button3.pack(pady=20)
    farm_test_process = pm.create_process(non_farm_test)
    root.after(100, loop_test_process_window_override, farm_test_process, root)
    def on_closing():
        farm_test_process.terminate()
        farm_test_process.join()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def loop_test_process_window_override (process,window):
    #重载了一遍，确保掉线后返回gui主页面
    if process.is_alive():
         window.after(100, loop_test_process_window_override, process, window)
    else:
         time.sleep(0.5)
         window.destroy()
         func.show_popup("你掉线了！请重新进入农场")
         gui_enter()




if __name__ == "__main__":
        gui_enter()
