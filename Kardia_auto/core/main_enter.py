
import tkinter as tk
import core.op
import core.recongnize_process as rp
import core.sub_enter

def main_enter():

    root = tk.Tk()
    root.attributes("-topmost", True)
    label1 = tk.Label(root, text="欢迎使用游戏自动脚本\n\n", font=("", 24))
    label2 = tk.Label(root,text='将程序挂在农场里即可开始！\n需要检测到屏幕上有模拟器窗口的农场\n',font=("", 18))
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+100")
    label1.pack()
    label2.pack()

    def close_enter():
        root.destroy()
        rp.close_all_process()
    def jump_to_sub_enter():
        root.destroy()
        core.sub_enter.sub_enter()
    def jump_to_fight_enter():
        root.destroy()

    rp.wait_for(root,"testxx",jump_to_sub_enter)
    root.protocol("WM_DELETE_WINDOW", close_enter)
    root.mainloop()









