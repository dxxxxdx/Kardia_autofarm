import tkinter as tk
from tkinter import ttk
import core.mine_process
import core.sub_enter
import core.fight_process
fight_dic = {
    "普通本完全":"normal3",
    "普通本深入":"normal2",
    "普通本初步":"normal1",
    "矿洞":"mine",
    "地区威胁":"weekend",
    "冥界boss":"7map_side1_boss",
    "雨林boss":"8map_side1_boss",
}
fight_dic_inv = {
    "normal3": "普通本完全",
    "normal2": "普通本深入",
    "normal1": "普通本初步",
    "mine": "矿洞",
    "weekend": "地区威胁",
    "7map_side1_boss": "冥界boss",
    "8map_side1_boss": "雨林boss"
}

def fight_enter():
    root = tk.Tk()
    root.attributes("-topmost", True)
    screen_width = root.winfo_screenwidth()
    root.geometry(f"500x800+{screen_width - 550}+100")

    label1 = tk.Label(root,text="你要打什么本？\n\n",font=("",24))
    label1.pack()
    combobox = ttk.Combobox(root, values=list(fight_dic.keys()))
    combobox.pack(padx=30, pady=30)
    combobox.current(0)
    fight_target = None

    def start_fight():
        nonlocal fight_target
        fight_target = fight_dic.get(combobox.get(), None)
        root.after(1000, root.destroy)
        print(fight_target)
        if fight_target is None:
            core.sub_enter.sub_enter()
        elif fight_target == "mine":
            core.mine_process.mine_process()
        else:
            core.fight_process.fight_process(fight_target)


    button = tk.Button(root,text="开始",padx=20,pady=20,command=lambda: start_fight())
    button.pack(padx=20, pady=20)
    root.mainloop()



















