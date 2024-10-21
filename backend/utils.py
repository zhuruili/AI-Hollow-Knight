"""
实用工具，常规操作等
"""
import os
import time
import threading

import cv2
import numpy as np
import pyautogui

from .blood_detect import blood_detect_Knight, blood_detect_Boss
from .control import control
from frontend.logWindow import log

def Slash():
    """普通攻击：挥砍"""
    control.tap_long("j",0.08)
    # log.appendLog("挥砍", "OP")

def Dash():
    """冲刺"""
    control.tap("l")
    # log.appendLog("冲刺", "OP")

def Left():
    """向左移动小段距离"""
    control.tap_long("a", 0.08)
    
def Right():
    """向右移动小段距离"""
    control.tap_long("d", 0.08)

def Jump():
    """跳跃"""
    control.tap_long("k", 0.25)
    # log.appendLog("跳跃", "OP")

def UpSlash():
    """上劈"""
    control.click_login()
    pyautogui.hotkey("w", "j")

def WaveAttack():
    """黑波"""
    control.tap("i")

def take_action(actions):
    """
    执行动作
    @param actions: 动作编号（列表）
    """
    def execute_action(action):
        if action == 0:
            Slash()
        elif action == 1:
            Dash()
        elif action == 2:
            Left()
        elif action == 3:
            Right()
        elif action == 4:
            Jump()
        elif action == 5:
            pass
        else: 
        #     log.appendLog(f"未知动作：{action}", "WARNING") # 不能在此处调用log.appendLog，否则会导致多线程下的日志混乱
            print(f"未知动作：{action}") # DEBUG
        
    threads = []
    for action in actions:
        t = threading.Thread(target=lambda a=action: execute_action(a))
        threads.append(t)
        t.start()
    for t in threads:
        t.join() # 等待所有线程结束

def action_judge(boss_health, next_boss_health, knight_health, next_knight_health, stop, HealDownCount):
    """
    action reward judge
    @param boss_health: BOSS当前生命值
    @param next_boss_health: 下一帧BOSS生命值
    @param knight_health: 小骑士当前生命值
    @param next_knight_health: 下一帧小骑士生命值
    @param stop: 是否停止扣分
    @param HealDownCount: 血量下降次数
    """
        
    temp_HDC = HealDownCount

    self_blood_reward = 0
    boss_blood_reward = 0

    if next_knight_health < knight_health and temp_HDC < 9: # 小骑士受伤
        if stop == 0:
            temp_HDC += 1
            self_blood_reward = -10*temp_HDC
            stop = 1 # 防止连续取帧时重复扣分
            log.appendLog(f"小骑士受伤，扣{self_blood_reward}分，累计受伤扣分次数：{temp_HDC}", "INFO")
    else:
        stop = 0

    if next_boss_health < boss_health and boss_health - next_boss_health <50: # BOSS受伤且受伤值不超过50
        damage = boss_health - next_boss_health
        if damage > 10:
            boss_blood_reward = damage*1.8
            log.appendLog(f"击伤BOSS，奖励{boss_blood_reward:.2f}分", "INFO")
        else:
            boss_blood_reward = damage*0.1
            log.appendLog(f"生存时间奖励：{boss_blood_reward:.2f}分", "INFO")
    
    reward = self_blood_reward + boss_blood_reward
    done = 0

    return reward, done, stop, temp_HDC

def screen_grab(x=0, y=0, w=1288, h=757):
    """
    截取屏幕指定区域
    @param x: 左上角x坐标
    @param y: 左上角y坐标
    @param w: 宽度
    @param h: 高度
    """
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    frame = np.array(screenshot) # 转换为numpy数组, 以便OpenCV处理
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # 转换为OpenCV的RGB格式
    
    return frame

def screen_grab_test():
    """测试screen_grab"""
    x, y, w, h = 0, 0, 1288, 757
    log.appendLog(f"截屏测试，区域：x={x}, y={y}, w={w}, h={h}", "INFO")

    capyured_img = screen_grab(x, y, w, h)

    cv2.imshow("Captured Image", capyured_img)
    log.appendLog("触摸任意键以继续", "INFO")
    cv2.waitKey(5000) # 以毫秒为单位
    cv2.destroyAllWindows() # 销毁所有由cs2.imshow产生的窗口
    
    log.appendLog("截屏测试结束", "INFO")

def BloodDetectTest_K():
    """小骑士血量检测-测试"""

    img = screen_grab()

    Health = blood_detect_Knight(img)

    log.appendLog(f"小骑士当前生命值：{Health}", 'INFO')

    return Health

def BloodDetectTest_B():
    """BOSS血量检测-测试"""

    img = screen_grab()

    Health = blood_detect_Boss(img)

    log.appendLog(f"Boss当前生命值：{Health}", 'INFO')

    return Health

def take_screenshots(duration=20.0, interval=0.5, path="D:\helloworld_python\Rookie\Programs\Auto\Hollow Knight\Temp"):
    """
    连续截图
    @param duration: 持续时间
    @param interval: 截图间隔
    @param path: 截图保存路径
    """
    # 确保文件夹存在
    if not os.path.exists(path):
        os.makedirs(path)
        log.appendLog(f"{path}文件夹不存在，已自动创建", "WARNING")
    else:
        log.appendLog(f"截图开始，持续时间：{duration}秒，间隔：{interval}秒", "INFO")
        log.appendLog(f"截图保存路径：{path}", "INFO")
    # 截图
    end_time = time.time() + duration
    while time.time() < end_time:
        screenshot = pyautogui.screenshot(region=(0, 0, 1280, 720))
        screenshot.save(f"{path}\\{time.time()}.png")
        time.sleep(interval)
    log.appendLog("截图结束", "INFO")
    
def restart():
    """死亡或击杀BOSS后重进副本开始新一轮战斗/训练"""
    time.sleep(8)
    Jump() # 小骑士起身
    log.appendLog("小骑士起身", "INFO")
    time.sleep(5)
    control.tap_long("w",0.3) # 与BOSS神像交互
    log.appendLog("与神像交互", "INFO")
    time.sleep(2)
    Jump() # 确认进入副本
    log.appendLog("确认进入副本", "INFO")
    time.sleep(4) # 等待进入副本
    log.appendLog("开始新一轮战斗", "INFO")