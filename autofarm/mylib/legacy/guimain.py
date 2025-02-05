"""""



import multiprocessing
import tkinter as tk
from multiprocessing import Process, active_children, Queue
import signal
import os
import keyboard
import mylib.func as func
import eggauto
from eggauto import eggauto_gui
import time
from queue import Empty

working = False

def bind_farm(queue):
    while True:
        binding = func.is_exist(func.fpth('farm_feature'))
        time.sleep(1)
        if (binding != 1):
            queue.put("stop")

def out_bind(queue, p):
    global working
    try:
        if queue.get_nowait() == "stop" and working == False:
            root.destroy()
            p.terminate()
            print("离开了农场")
    except Empty:
        pass
    root.after(100, out_bind, queue, p)

def f2():
    while True:
        print("Function f2 is running")

def f3():
    while True:
        print("Function f3 is running")

# 创建进程并禁用按钮
def create_process(target, buttons):
    for button in buttons:
        button.config(state=tk.DISABLED)
    p = Process(target=target)
    global working
    working = True
    p.start()

# 关闭窗口时终止所有进程
def on_closing():
    for p in active_children():
        os.kill(p.pid, signal.SIGTERM)
    root.after_cancel(out_bind)  # 取消所有计划的 out_bind 调用
    root.destroy()

# 主函数
def guimain():
    global root
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+0")

    root.title("Process Launcher")

    buttons = []

    button1 = tk.Button(root, text="自动孵蛋", command=lambda: create_process(eggauto_gui, buttons), width=20, height=3)
    button1.pack(pady=10)
    buttons.append(button1)

    button2 = tk.Button(root, text="自动挖矿", command=lambda: create_process(f2, buttons), width=20, height=3)
    button2.pack(pady=10)
    buttons.append(button2)

    button3 = tk.Button(root, text="挖矿吃面包", command=lambda: create_process(f3, buttons), width=20, height=3)
    button3.pack(pady=10)
    buttons.append(button3)

    # 绑定窗口关闭事件
    root.protocol("WM_DELETE_WINDOW", on_closing)
    queue = multiprocessing.Queue()
    p = Process(target=bind_farm, args=(queue,))
    p.start()
    root.after(100, out_bind, queue, p)

    def stopwork():
        global working
        working = False

    keyboard.on_press_key("shift", lambda e: stopwork())
    root.mainloop()
    return 1

if __name__ == "__main__":
    guimain()



"""