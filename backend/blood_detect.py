"""
@file blood_detect.py
检测小骑士与BOSS的血量
状态：测试成功但存在一定BUG
BUG：血量检测时，如果出现小骑士死亡或者BOSS死亡，白屏结算时会返回错误的血量结果
"""

import numpy as np

def blood_detect_Knight(image):
    """根据传入的图片检测小骑士生命值"""
    health_start_x = 200 # 小骑士血量条侦测点起始x坐标
    health_start_y = 117 # 小骑士血量条侦测点起始y坐标
    health_step_x = 39 # 小骑士每一格血量间的x坐标间隔
    max_health = 9 # 小骑士最大血量

    remaining_health = 0

    for i in range(max_health):
        x = health_start_x + i * health_step_x
        y = health_start_y
        # 获取当前血量格的颜色
        color = image[y, x]
        # 假设白色为满血，黑色为空血
        if np.all(color > 180):  # 白色
            remaining_health += 1

    deducted_health = max_health - remaining_health
    return remaining_health


def blood_detect_Boss(image):
    """检测BOSS生命值"""
    health_start_x = 330  # BOSS血量条侦测点起始x坐标
    health_start_y = 735  # BOSS血量条侦测点起始y坐标
    health_step_x = 1     # BOSS每一格血量间的x坐标间隔
    max_health = 967      # BOSS最大血量处的x坐标

    remaining_health = 0

    for i in range(max_health - health_start_x):
        x = health_start_x + i * health_step_x
        y = health_start_y
        # 获取当前血量格的颜色
        color = image[y, x]
        # 假设红色为满血，黑色为空血
        if color[2] <100 and color[2] > 50 and color[0] < 32 and color[1] < 32:  # 红色
            remaining_health += 1

    deducted_health = max_health - remaining_health
    return remaining_health

# 截图范围约（1285，760）