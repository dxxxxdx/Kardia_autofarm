import pyautogui

import core.op as op
from os import path,makedirs
import os
import re

def fpth_selarm(name, filetype=".png", sub_path=None):
    """
    构建文件路径，支持子目录和文件夹定位。
    :param name: 文件名或文件夹名
    :param filetype: 文件后缀，默认为 ".png"
    :param sub_path: 子目录路径，默认为 None
    :return: 构造后的完整路径
    """
    base_path = path.dirname(path.abspath(__file__))
    if sub_path:
        base_path = path.join(base_path, sub_path)
    if filetype:  # 如果有文件后缀，说明是文件
        tarpath = path.join(base_path, name + filetype)
    else:  # 如果没有文件后缀，说明是文件夹
        tarpath = path.join(base_path, name)
    tarpath = tarpath.rstrip("\\/")
    if not path.exists(tarpath):
        makedirs(tarpath)
    return tarpath

def find_folder(folder_name, base_path=None):
    """
    在项目内查找指定文件夹的位置
    :param folder_name: 要查找的文件夹名称
    :param base_path: 起始路径，默认为项目根目录
    :return: 文件夹的完整路径（如果找到），否则返回 None
    """
    # 如果没有提供起始路径，默认为当前文件的项目根目录
    if base_path is None:
        base_path = path.dirname(path.abspath(__file__))
    # 遍历目录结构
    for root, dirs, _ in os.walk(base_path):
        if folder_name in dirs:
            return path.join(root, folder_name)
    # 如果未找到文件夹，返回 None
    return None


def list_files_in_directory(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:

            file_path = os.path.join(root, file_name)
            file_paths.append(file_path)
    return file_paths



def match_grid(center, max_tuple):
    x = center[0]
    y = center[1]
    #使用第四象限
    # 对 x 进行匹配
    if abs(x - max_tuple[0]) < 50:
        resultx = 0
    elif abs(x - max_tuple[2]) < 50:
        resultx = 3
    elif abs(x - max_tuple[0]) < abs(x - max_tuple[2]):
        resultx = 1
    else:
        resultx = 2
    # 对 y 进行匹配
    if abs(y - max_tuple[1]) < 50:
        resulty = 0
    elif abs(y - max_tuple[3]) < 50:
        resulty = 3
    elif abs(y - max_tuple[1]) < abs(y - max_tuple[3]):
        resulty = 1
    else:
        resulty = 2

    return (resultx, resulty)




def drag_at(center, direction):
    pyautogui.moveTo(center[0], center[1])
    if direction == "RIGHT":
        pyautogui.dragRel(30,0,duration=0.3)
    elif direction == "LEFT":
        pyautogui.dragRel(-30,0,duration=0.3)
    elif direction == "DOWN":
        pyautogui.dragRel(0,30,duration=0.3)
    elif direction == "UP":
        pyautogui.dragRel(0,-30,duration=0.3)
    else:
        return -1
    return 1















