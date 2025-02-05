import multiprocessing
import time
import os
import mylib.func as func

def create_process(tarfunc,args=()):
    process = multiprocessing.Process(target=tarfunc,args=args)
    process.start()
    return process

def loop_test_process(process):
    #函数接口
    if process.is_alive():
         time.sleep(0.1)
    else:
         return 0

def loop_test_process_window(process,window):
    #窗口接口
    #进程结束后，销毁窗口
    if process.is_alive():
        window.after(100,loop_test_process_window,process,window)
    else:
        time.sleep(0.5)
        window.destroy()

def loop_test_process_window_and_do(process,window,do):
    if process.is_alive():
        window.after(100,loop_test_process_window_and_do,process,window,do)
    else:
        time.sleep(0.5)
        window.destroy()
        do()
def loop_test_process_window_when_arg_and_do(process,window,arg,do):
    if process.is_alive():
        window.after(100,loop_test_process_window_when_arg_and_do,process,window,arg,do)
    elif not arg:
        window.after(100, loop_test_process_window_when_arg_and_do, process, window, arg,do)
    else:
        time.sleep(0.5)
        window.destroy()
        do()
def close_all_mp_processes( withscr ):
    # 获取当前主进程的 PID
    main_pid = os.getpid()
    # 遍历所有活动进程
    for process in multiprocessing.active_children():
        # 确保不终止主进程
        if process.pid != main_pid:
            process.terminate()  # 终止进程
            process.join()       # 等待进程结束
    if withscr : create_process(func.scr_process)

