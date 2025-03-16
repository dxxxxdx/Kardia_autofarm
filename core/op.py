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
    tarpath = path.join(base_path, "lib", name + filetype)
    if not path.exists(path.dirname(tarpath)):
        makedirs(path.dirname(tarpath))
    return tarpath


import cv2
import numpy as np
from os import path

def find_img(tarpath, threshold=0.8, single_find=True, ingray=True, min_distance=10, color_tolerance=30):
    """
    图像识别函数，返回匹配到的目标坐标，并可选择检测颜色。
    """
    # 检查截图文件是否存在
    scr_shot_path = fpth("screenshot")
    if not path.exists(scr_shot_path):
        print(f"Error: Screenshot file does not exist at {scr_shot_path}")
        return []

    # 检查目标文件是否存在
    tar_img_path = tarpath
    if not path.exists(tar_img_path):
        print(f"Error: Target image file does not exist at {tar_img_path}")
        return []

    # 加载图像
    scr_shot = cv2.imread(scr_shot_path)
    if scr_shot is None:
        print(f"Error: Failed to read screenshot from {scr_shot_path}")
        return []

    tar_img = cv2.imread(tar_img_path)
    if tar_img is None:
        print(f"Error: Failed to read target image from {tar_img_path}")
        return []


    scr_shot_gray = cv2.cvtColor(scr_shot, cv2.COLOR_BGR2GRAY)
    tar_img_gray = cv2.cvtColor(tar_img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(scr_shot_gray, tar_img_gray, cv2.TM_CCOEFF_NORMED)

    locations = np.where(result >= threshold)
    centers = []

    # 遍历匹配结果，计算中心坐标
    if locations[0].size > 0:
        for loc in zip(*locations[::-1]):
            center_x = loc[0] + tar_img.shape[1] // 2
            center_y = loc[1] + tar_img.shape[0] // 2
            if not ingray:
                is_color_match = check_color(scr_shot, tar_img, (center_x, center_y), tolerance=color_tolerance)
                if not is_color_match:
                    continue  # 跳过颜色不匹配的目标
            centers.append((center_x, center_y))
            # 如果设置为单次匹配，立即返回第一个结果
            if single_find:
                return centers
    else:
        print("未找到目标")
        return []

    filtered_centers = filter_close_points(centers, min_distance)
    print("找到了目标", tar_img_path, "个数：", len(filtered_centers), "位置：", filtered_centers)
    return filtered_centers

def check_color(scr_shot, tar_img, center, size=5, tolerance=50):
    """
    检测截图中目标区域的颜色是否与模板相似。
    :param scr_shot: 截图图像
    :param tar_img: 模板图像
    :param center: 匹配中心点
    :param size: 区域大小，默认5x5
    :param tolerance: 颜色接近的容忍度
    :return: True 如果颜色匹配，False 如果颜色差异较大
    """
    x, y = center
    half_size = size // 2


    # 提取模板图像和截图中目标区域的5x5区域
    target_region = tar_img[tar_img.shape[0]//2-half_size:tar_img.shape[0]//2+half_size+1,
                            tar_img.shape[1]//2-half_size:tar_img.shape[1]//2+half_size+1]

    matched_region = scr_shot[y-half_size:y+half_size+1, x-half_size:x+half_size+1]

    if target_region.size == 0 or matched_region.size == 0:
        print(f"Error: Region around {center} is out of bounds.")
        return False

    # 计算目标区域和匹配区域的平均颜色
    target_color = np.mean(target_region, axis=(0, 1))
    matched_color = np.mean(matched_region, axis=(0, 1))

    # 比较颜色差异
    color_distance = np.linalg.norm(target_color - matched_color)
    return color_distance <= tolerance




def filter_close_points(points, min_distance):
    """
    过滤掉距离过近的点，移除多余的邻近匹配结果。
    :param points: 原始匹配点列表 [(x1, y1), (x2, y2), ...]
    :param min_distance: 最小允许距离
    :return: 去重后的点列表
    """
    filtered_points = []
    for point in points:
        # 检查当前点是否与已保留点的距离足够远
        if all(abs(point[0] - fp[0]) > min_distance or abs(point[1] - fp[1]) > min_distance for fp in filtered_points):
            filtered_points.append(point)
    return filtered_points



if __name__ == '__main__':
    pass
    find_img(fpth("test"),ingray=False)
