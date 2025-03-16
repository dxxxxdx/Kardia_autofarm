import tkinter as tk
import stages.main_enter
import stages.egg_process as ep
import stages.fight_enter

def sub_enter():
    root = tk.Tk()
    root.attributes("-topmost", True)
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+100")
    label1 = tk.Label(root,text="已经检测到你的农场\n\n",font=("", 24))
    label1.pack()
    def jump_to_egg_process():
        root.after(50, root.destroy)
        ep.egg_process()
    def jump_to_main_enter():
        root.after(50, root.destroy)
        stages.main_enter.main_enter()
    def jump_to_fight_gui():
        root.after(50, root.destroy)
        stages.fight_enter.fight_enter()
    b1 = tk.Button(root,text="自动孵蛋",command=jump_to_egg_process,padx=25,pady=25)
    b1.pack()
    b2 = tk.Button(root,text="自动打架",command=jump_to_fight_gui,padx=25,pady=25)
    b2.pack()
    root.protocol("WM_DELETE_WINDOW", jump_to_main_enter)
    root.mainloop()

if __name__ == '__main__':
    sub_enter()


