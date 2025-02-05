import time
import cv2
import numpy as np
import pyautogui
from os import path
import tkinter as tk
import multiprocessing as mp
import  os
import  random
from queue import Empty
from PIL import Image, ImageGrab
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True



def get_project_folder():
    return path.dirname(path.abspath(__file__))

def scr_process():
    while True:
        time.sleep(0.8)
        project_folder = get_project_folder()
        piclib_folder = path.join(project_folder, 'piclib')
        screenshot_path= path.join(piclib_folder, 'screenshot.png')
        tempscrshot = pyautogui.screenshot()
        can_open = True
        """
        try:
            with Image.open(fpth("screenshot")) as img:
                img.verify()  # 验证文件是否损坏
        except Exception as e:
            print(f"截图文件损坏：{e}")
            can_open = False
            tempscrshot.save(fpth("error.png"))
        """
        if can_open:
            tempscrshot.save(screenshot_path)
            time.sleep(0.1)



def scr_func():
    tempscrshot = pyautogui.screenshot()
    return tempscrshot


def find_subimage_center(parent_image_path, sub_image_path,threshold=0.8):

    # 检查路径是否存在
    if not parent_image_path or not sub_image_path:
        print("Error: Image path is None")
        return None
    if not os.path.exists(parent_image_path):
        print(f"Error: Parent image file does not exist at {parent_image_path}")
        return None
    if not os.path.exists(sub_image_path):
        print(f"Error: Sub image file does not exist at {sub_image_path}")
        return None
    def safe_read_convert(pathx):
        img = cv2.imread(pathx)
        if img is None:
            imgx = scr_func()
            return np.array(imgx)
        return img
    parent_image = safe_read_convert(parent_image_path)
    sub_image = safe_read_convert(sub_image_path)

    if parent_image is None:
        print(f"Error: Failed to read parent image from {parent_image_path}")
        return None
    if sub_image is None:
        print(f"Error: Failed to read sub image from {sub_image_path}")
        return None

    # 转换为灰度图
    parent_gray = cv2.cvtColor(parent_image, cv2.COLOR_BGR2GRAY)
    sub_gray = cv2.cvtColor(sub_image, cv2.COLOR_BGR2GRAY)

    # 检查子图像尺寸
    if sub_gray.shape[0] > parent_gray.shape[0] or sub_gray.shape[1] > parent_gray.shape[1]:
        print("Error: Sub image is larger than parent image")
        return None

    # 模板匹配
    result = cv2.matchTemplate(parent_gray, sub_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 检查匹配结果
    if max_val >= threshold:
        sub_height, sub_width = sub_gray.shape
        center_x = max_loc[0] + sub_width // 2
        center_y = max_loc[1] + sub_height // 2
        print("找到了", center_x, center_y, "位置的目标")
        return (center_x, center_y)
    else:
        print("未找到匹配的子图片")
        return None

def find_click (img_path):
    scr_path = fpth("screenshot")
    clickarea = find_subimage_center(scr_path,img_path )

    if clickarea is not None:
        pyautogui.moveTo(clickarea[0]+ random.randint(-10,10), clickarea[1]+ random.randint(-10,10))
        pyautogui.click()
        return 1
    else :
        return 0

def is_exist (img_path):
    scr_path = fpth("screenshot")
    bol1 = find_subimage_center(scr_path,img_path)
    if bol1 is not None: return 1
    else: return 0

def fpth(filename):
    return r"{}".format(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'piclib', filename +  '.png'))



def popup(text):
    # 创建弹窗
    popup_root = tk.Tk()
    popup_root.title("提示")
    screen_width = popup_root.winfo_screenwidth()
    popup_root.geometry(f"500x300+{screen_width - 550}+300")
    label = tk.Label(popup_root, text=text, font=("", 18))
    label.pack(pady=20)
    def on_close():
        print("弹窗已关闭")
        popup_root.destroy()
    button = tk.Button(popup_root, text="关闭", font=("", 18), command=on_close)
    button.pack(pady=20)
    popup_root.mainloop()
def show_popup(text):
    popup_process = mp.Process(target=popup,args=(text,))
    popup_process.start()

def label_updater(window,label,queue):
    try:
        text = queue.get_nowait()
        label.configure(text=text)
    except Empty:
        pass
    window.after(100,label_updater,window,label,queue,)

    return 1


def eat_bread():
    print('吃口面包')
    find_click(fpth('bag_enter'))
    time.sleep(0.5)
    find_click(fpth('item_can_use'))
    if is_exist(fpth('bread')):
        find_click(fpth('bread'))
        time.sleep(0.5)
        find_click(fpth('use'))
        time.sleep(0.5)
        find_click(fpth('confirm2'))
        time.sleep(0.5)
        find_click(fpth('get_item'))
        time.sleep(0.5)
        find_click(fpth('return'))
        time.sleep(0.5)
        return 1
    else:
        show_popup("你没有面包了！")
        return 0


def rolling_find_click(upper_roll,lower_roll,tarimg,):
    positon = 0
    for upper_roll in range(upper_roll):
        pyautogui.moveTo(1280,720)
        pyautogui.scroll(-100)
        find_click(fpth(tarimg))
    for lower_roll in range(lower_roll):
        pyautogui.moveTo(1280,720)
        pyautogui.scroll(100)
        find_click(fpth(tarimg))





if __name__ == '__main__':
    scr_process()