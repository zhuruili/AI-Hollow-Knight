# -*- coding: utf-8 -*-
"""
@file: init.py
1. 初始化
2. 检查是否以管理员权限运行（可选，针对具体游戏而异）
3. 将窗口移动至左上角
4. 输出窗口大小、缩放因子、游戏分辨率等信息
"""
import os
import re
import sys
import time
import ctypes
from ctypes import windll
import win32gui
from win32con import SWP_NOMOVE, SWP_NOSIZE, HWND_TOPMOST

from multiprocessing import current_process

from frontend.logWindow import log # 引入日志模块

class_name = None # 不是没有，而是不知道
window_title = "Hollow Knight" # ‘空洞骑士’窗口句柄名称

hwnd = win32gui.FindWindow(class_name, window_title) # 获取窗口句柄

def wait_exit():
    """退出"""
    log.appendLog("程序将在3秒后退出", "INFO")
    time.sleep(3)
    sys.exit(0)

def is_admin():
    """判断当前是否为管理员权限"""
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    
def get_scale_factor():
    """获取放缩因子"""
    try:
        windll.shcore.SetProcessDpiAwareness(1)  # 设置进程的 DPI 感知
        scale_factor = windll.shcore.GetScaleFactorForDevice(
            0
        )  # 获取主显示器的缩放因子
        return scale_factor / 100  # 返回百分比形式的缩放因子
    except Exception as e:
        print("Error:", e)
        return None

def initialize():
    """初始化"""
    # 输出进程信息
    process = current_process()
    log.appendLog(f"进程ID: {process.pid}", "INFO")
    log.appendLog(f"进程名称: {process.name}", "INFO")

    # 检测是否以管理员权限运行
    if not is_admin():
        log.appendLog("如有需要请以管理员权限运行", "WARNING")
        # wait_exit()
        # 对于特定游戏，可能需要管理员权限，而有些不需要，因此这里不直接退出程序

    # constant
    global hwnd # 全局变量声明，initialize函数将会修改该全局变量的值
    hwnd = win32gui.FindWindow(class_name, window_title)
    if hwnd == 0:
        log.appendLog("未找到窗口，请检查是否已启动游戏", "ERROR")
    else:
        log.appendLog("已找到目标窗口", "INFO")
        left, top, right, bot = win32gui.GetClientRect(hwnd)
        w = right - left
        h = bot - top

        scale_factor = get_scale_factor()

        width_ratio = w / 1920 * scale_factor
        height_ratio = h / 1080 * scale_factor
        real_w = int(w * width_ratio)
        real_h = int(h * height_ratio)
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 判断 root_path 中是否包含中文或特殊字符
        special_chars_pattern = r"[\u4e00-\u9fa5\!\@\#\$\%\^\&\*\(\)]"
        if bool(re.search(special_chars_pattern, root_path)):
            log.appendLog("请将项目路径移动到纯英文路径下", "ERROR")
            wait_exit()

        # 输出基本信息日志
        log.appendLog(f"窗口大小：{w}x{h} 当前屏幕缩放：{scale_factor} 游戏分辨率：{real_w}x{real_h}", "INFO")
        log.appendLog(f"项目路径：{root_path}", "INFO")

        log.appendLog("将游戏窗口移动至左上角并固定上层显示", "OP")

        rect = win32gui.GetWindowRect(hwnd)  # 获取窗口区域
        win32gui.MoveWindow(
            hwnd, 0, 0, rect[2] - rect[0], rect[3] - rect[1], True
        )  # 设置窗口位置为0,0
        win32gui.SetForegroundWindow(hwnd)  # 窗口置顶
        # 设置游戏画面位于上层
        win32gui.SetWindowPos(hwnd, # 游戏窗口句柄
                            HWND_TOPMOST,  # 置顶
                            0, 0, 0, 0,  # 窗口位置
                            SWP_NOMOVE | SWP_NOSIZE  # 窗口大小不变
                            )
