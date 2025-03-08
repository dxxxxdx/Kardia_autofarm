import numpy as np
import pyautogui as pg
import cv2
import time
from os import path, makedirs

#operation 仅在此处使用opencv，并且做了一些函数便于调用


def capture_screenshot():
    while True:
        screenshot = pg.screenshot()
        save_path = fpth("screenshot")
        screenshot.save(save_path)
        #print(f"Screenshot saved to {save_path}")
        time.sleep(0.6)

def capture_screenshot_func():
    screenshot = pg.screenshot()
    save_path = fpth("screenshot")
    try :
        screenshot.save(save_path)
#偶尔会因为运行时间长报错
    except PermissionError as e:
        print(e)
    except Exception as e :
        print(e)
    return 1


def fpth(name,filetype= ".png"):
    #找路径常用
    base_path = path.dirname(path.abspath(__file__))
    tarpath = path.join(base_path, "lib", name , filetype)
    if not path.exists(path.dirname(tarpath)):
        makedirs(path.dirname(tarpath))
    return tarpath

def find_img(tarpath, threshold=0.8,single_find=True):
    #图像识别函数，返回坐标
    #time_start = time.time()
    scr_shot_path = fpth("screenshot")
    if not path.exists(scr_shot_path):
        print(f"Error: Screenshot file does not exist at {scr_shot_path}")
        return None

    tar_img_path = tarpath
    if not path.exists(tar_img_path):
        print(f"Error: Target image file does not exist at {tar_img_path}")
        return None

    scr_shot = cv2.imread(scr_shot_path)
    if scr_shot is None:
        print(f"Error: Failed to read screenshot from {scr_shot_path}")
        return None

    tar_img = cv2.imread(tar_img_path)
    if tar_img is None:
        print(f"Error: Failed to read target image from {tar_img_path}")
        return None

    scr_gray = cv2.cvtColor(scr_shot, cv2.COLOR_BGR2GRAY)
    tar_gray = cv2.cvtColor(tar_img, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(scr_gray, tar_gray, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    centers = []
    #time_end = time.time()
    #elapsed_time = time_end - time_start
    #print(f"函数运行时间：{elapsed_time:.4f} 秒")
    if locations[0].size > 0:
        for loc in zip(*locations[::-1]):
            center_x = loc[0] + tar_gray.shape[1] // 2
            center_y = loc[1] + tar_gray.shape[0] // 2
            centers.append((center_x, center_y))
            print("找到了", center_x, center_y, "位置的目标",tar_img_path)
            if single_find:
                print("单个目标")
                return centers
    else:
        print("未找到目标")
        return centers




if __name__ == '__main__':
    time.sleep(1)
