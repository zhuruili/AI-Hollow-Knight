"""
DQN训练主程序
"""

import cv2
import time
import numpy as np
import matplotlib.pyplot as plt

import torch

from frontend.logWindow import log
from .control import control
from .utils import *
from .DQN_class import DQN
from .blood_detect import blood_detect_Knight, blood_detect_Boss


# 超参数设置
HEIGHT = 72
WIDTH = 128
epochs = 2000 # 训练轮数
big_BATCH_SIZE = 16 # 大批量大小
UPDATE_STEP = 48 # 更新步数
num_step = 0 
target_step = 0
pause = False

DQN_model_path = 'D:\helloworld_python\Rookie\Programs\AI\AI-Hollow-Knight\\backend\\rsc\models\dqn_model.pth'
existed_model_path = 'D:\helloworld_python\Rookie\Programs\AI\AI-Hollow-Knight\\backend\\rsc\models\existed_model\model_20241017_30.pth'

action_space = 6 # 动作空间维度
"""
动作空间：
0 - Slash: 攻击(J)
1 - Dash: 冲刺(L)
2 - Left: 左移(A)
3 - Right: 右移(D)
4 - Jump: 跳跃(K)
5 - Idle: 无操作
"""

def TrainingStart(use_existed_model=False):
    """
    开始训练
    @param use_existed_model: 是否使用已有模型
    """

    agent = DQN(ob_height=HEIGHT, ob_width=WIDTH, action_space=action_space, model_path=DQN_model_path)
    if use_existed_model:
        agent.load_model(existed_model_path)
    else:
        log.appendLog("未指定预训练模型，将创建新模型用于训练", "INFO")

    control.click_login() # 使游戏窗口获得焦点
    log.appendLog("开始训练", "INFO")

    reward_list = [] # 记录每轮奖励

    for episode in range(epochs):
        # 初始化环境
        global target_step, num_step, pause
        target_step = 0 # used to update target network
        done = 0
        total_reward = 0

        stop = 0 # 防止连续取帧重复计算扣血
        HealDownCount = 0 # 防止图标闪烁误判死亡导致重复扣分

        screen_RGB = screen_grab()
        screen_gray = cv2.cvtColor(screen_RGB, cv2.COLOR_BGR2GRAY)

        state = cv2.resize(screen_gray, (WIDTH, HEIGHT)) # 将截图缩放为模型输入尺寸
        boss_blood = blood_detect_Boss(screen_RGB)
        self_blood = blood_detect_Knight(screen_RGB)

        last_time = time.time() 
        
        while not done:
            state = torch.from_numpy(state).to(dtype=torch.float).to(agent.device)
            state = state.reshape(-1, 1, HEIGHT, WIDTH)[0] # 将状态转换为模型输入格式
            target_step += 1
            
            # print(state.dtype) # DEBUG

            action = agent.choose_action(state) # 选择动作
            take_action(action) # 执行动作

            # 获取下一状态
            screen_RGB = screen_grab()
            screen_gray = cv2.cvtColor(screen_RGB, cv2.COLOR_BGR2GRAY)
            next_state = cv2.resize(screen_gray, (WIDTH, HEIGHT))
            next_state = np.array(next_state).reshape(-1, 1, HEIGHT, WIDTH)[0]
            next_state_torch = torch.from_numpy(next_state).to(dtype=torch.float).to(agent.device)
            next_boss_blood = blood_detect_Boss(screen_RGB)
            next_self_blood = blood_detect_Knight(screen_RGB)
            reward, done, stop, HealDownCount = action_judge(boss_health=boss_blood, next_boss_health=next_boss_blood,
                                                               knight_health=self_blood, next_knight_health=next_self_blood,
                                                               stop=stop, HealDownCount=HealDownCount,
                                                               )
            # 存储经验
            agent.store_transition(state, action, reward, next_state_torch, done)
            # 如果经验池积累到一定程度，训练一轮, 更新网络
            if len(agent.replay_buffer) > big_BATCH_SIZE:
                num_step += 1
                agent.train()
            # 更新状态
            state = next_state
            self_blood = next_self_blood
            boss_blood = next_boss_blood
            # 更新总奖励
            total_reward += reward
            # 更新目标网络
            if target_step % UPDATE_STEP == 0:
                agent.update_target_net()
            # 暂停
            while pause:
                time.sleep(10)
                log.appendLog("已暂停", "INFO")
                if not pause:
                    break
            # 如果屏幕基本全白，说明游戏已结束，done置1
            if np.mean(screen_gray) > 250:
               log.appendLog("检测到白屏，游戏结束", "INFO")
               done = 1      
            # DONE
            if done == 1:
                log.appendLog("Done", "INFO")
                break
        # 记录每轮奖励
        reward_list.append(total_reward)
        # 每10轮保存一次模型与奖励信息图
        if episode % 10 == 0:
            agent.save_model()
            plt.clf() # 清空图像
            plt.plot(reward_list) # 绘制奖励曲线
            plt.savefig(f"D:\helloworld_python\Rookie\Programs\AI\AI-Hollow-Knight\\backend\\rsc\images\\reward_{episode}.png")
            log.appendLog("已保存模型与奖励信息", "INFO") 
            plt.close() # 关闭图像, 释放内存
        # 输出训练信息
        log.appendLog(f"Episode: {episode}, Total Reward: {total_reward}", "INFO")
        log.appendLog(f"Time: {time.time() - last_time}", "INFO")
        last_time = time.time()
        
        restart() # 进行下一轮训练
