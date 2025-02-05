"""
import tkinter as tk
import mylib.farm_test
import multiprocessing as mp


def update_label():
    if not queue.empty():
        result = queue.get()
        if result == 1 :
            label2.config(text="wei")
        elif result == 0 :
            label2.config(text="nie")
    else :
        root.after(500, update_label)


root = tk.Tk()
root.title= ("羊油自动脚本")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"500x800+{screen_width-550}+0")
label1 = tk.Label(root,text="羊油自动脚本\n余胜军徒儿开发",font=("", 24))
label1.pack()
label2 = tk.Label(root,text="牧场检测")
label2.pack()

#运行状态
queue = mp.Queue()
farmtestprocess = mp.Process(target=mylib.farm_test.farm_test,args=(queue,))
farmtestprocess.start()
#检测是否进入牧场状态
root.after(500, update_label)


"""





