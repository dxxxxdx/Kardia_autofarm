
import queue as queue

def label_updater(root,label,queuex):
    text = ""
    if not root.winfo_exists():
        return
    try :
        text = queuex.get_nowait()
    except queue.Empty:
        pass
    if text != "" :
        label.config(text=text)
    else:
        pass
    root.after(50,label_updater,root,label,queuex)

def test_th(root,th,end_func): #th销毁后关闭窗口
    if not root.winfo_exists():
        return
    if not th.is_alive() :
        root.after(50,lambda :end_func())
    else:
        root.after(100, lambda: test_th(root,th,end_func))


import threading
import tkinter as tk


def show_message(text,join= False):
    def show_message_gui():
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        root.geometry(f"500x200+{screen_width - 550}+200")
        root.attributes("-topmost", True)
        root.title("你有问题")

        label = tk.Label(root, text=text, padx=30, pady=30,font=("",15))
        label.pack()

        # 添加关闭按钮
        close_button = tk.Button(root, text="关闭", command=root.destroy, padx=10, pady=5)
        close_button.pack(pady=10)

        # 运行主循环
        root.mainloop()

    # 在单独的线程中运行弹窗函数
    th = threading.Thread(target=show_message_gui)
    th.start()
    if join:
        th.join()
    return th

if __name__ == '__main__':
    show_message("1111")