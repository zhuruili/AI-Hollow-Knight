# -*- coding: utf-8 -*-
"""
@file: control.py
控制鼠标键盘进行操作
"""
import time
import win32gui
import win32con
import win32api
import pyautogui
from typing import Union

from .init import hwnd # 窗口句柄

from frontend.logWindow import log

pyautogui.PAUSE = 0.05 # 设置每次按键后的自动间隔时间

class Control:
    """模拟一般键鼠输入"""

    def __init__(self, hwnd: int):
        self.hwnd = hwnd # 控制的窗口句柄

    # 前台鼠标点击
    def click_login(self, x: Union[int, float] = 0, y: Union[int, float] = 0, specified_hwnd=None):
        """让游戏窗口位于前台，在操作角色之前完成"""
        current_hwnd = self.hwnd if specified_hwnd is None else specified_hwnd
        x = x if isinstance(x, int) else int(x)
        y = y if isinstance(y, int) else int(y)
        # 登录窗口置顶
        win32gui.SetWindowPos(current_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        time.sleep(0.2)
        pt = win32gui.ClientToScreen(current_hwnd, (x, y))
        win32api.SetCursorPos([pt[0], pt[1]])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pt[0], pt[1], 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pt[0], pt[1], 0, 0)
        time.sleep(0.2)

    def tap(self, key: Union[str, int]):
        """按下指定的键"""
        if isinstance(key, str):
            key = ord(key.upper()) # 转换为ascii码
        pyautogui.press(chr(key))
        time.sleep(0.005)

    def tap_long(self, key: Union[str, int], duration: float):
        """长按指定的键"""
        if isinstance(key, str):
            key = ord(key.upper()) # 转换为ascii码  
        pyautogui.keyDown(chr(key))
        time.sleep(duration)
        pyautogui.keyUp(chr(key))

    def esc(self):
        """ESC"""
        win32gui.PostMessage(self.hwnd, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0)
        print("ESC DOWN")
        time.sleep(0.2)
        win32gui.PostMessage(self.hwnd, win32con.WM_KEYUP, win32con.VK_ESCAPE, 0)
        print("ESC UP")


control = Control(hwnd) # 实例化控制类
log.appendLog("操作控制类实例化完成", "INFO")



"""
BUG: win32gui 模拟键盘输入故障
    具体表现为：模拟键盘按下操作后无法正常释放（仅在游戏‘空洞骑士’中失效，但在游戏‘鸣潮’中测试成功）
    原因：未知
    解决方案：使用 pyautogui 模拟键盘输入
"""