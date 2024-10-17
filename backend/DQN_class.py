"""
搭建DQN模型
"""

import random
import numpy as np
from collections import deque

import torch
import torch.nn as nn
import torch.nn.init as init
import torch.optim as optim
import torch.nn.functional as F

from frontend.logWindow import log

# 部分超参数设置
REPLAY_SIZE = 2000
INITIAL_EPSILON = 0.4
FINAL_EPSILON = 0.01
BATCH_SIZE = 16
GAMMA = 0.9

class NET(nn.Module):
    """
    网络架构：
    输入层：输入为图像，图像大小为[ob_height, ob_width]，通道数为1（灰度图）
    输出层：输出为动作空间的维度
    """
    def __init__(self, ob_height, ob_width, action_space):
        super(NET, self).__init__()
        self.state_w = ob_width
        self.state_h = ob_height
        self.state_dim =self.state_w * self.state_h
        self.action_dim = action_space

        self.relu = nn.ReLU()
        self.net = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=[5, 5], stride=1, padding='same'),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=[3, 3], stride=1, padding='same'),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.fc1 = nn.Linear(int((self.state_w/4) * (self.state_h/4) * 64), 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, self.action_dim)

    def forward(self, x):
        """前向传播"""
        x = self.net(x)
        x = x.view(-1, int((self.state_w/4) * (self.state_h/4) * 64))
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
class DQN(object):
    """DQN类"""
    def __init__(self, ob_height, ob_width, action_space, model_path=None):
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # 选择设备
        log.appendLog(f"使用设备：{self.device}", "INFO")
        self.target_net = NET(ob_height, ob_width, action_space).to(self.device)
        self.eval_net = NET(ob_height, ob_width, action_space).to(self.device)
        self.replay_buffer = deque(maxlen=REPLAY_SIZE) # 经验池
        self.epsilon = INITIAL_EPSILON
        self.optimizer = optim.Adam(self.eval_net.parameters(), lr=1e-3) # 优化器, 虽然很想把lr设置置顶，但是似乎大部分时候给的参考代码都是1e-3
        self.loss = nn.MSELoss()
        self.action_dim = action_space

    def choose_action(self, state):
        """选择动作"""
        # ε-贪婪策略
        if np.random.uniform(0, 1) <= self.epsilon:
            action = np.random.randint(0, self.action_dim) 
        else:
            Q_value = self.eval_net(state)
            action = torch.argmax(Q_value)
        # ε衰减
        self.epsilon = max(FINAL_EPSILON, self.epsilon - (INITIAL_EPSILON - FINAL_EPSILON) / 10000)
        
        return action
    
    def store_transition(self, state, action, reward, next_state, done):
        """存储经验"""
        one_hot_action = np.zeros(self.action_dim)
        one_hot_action[action] = 1 # one-hot编码
        self.replay_buffer.append((state, one_hot_action, reward, next_state, done))

    def train(self):
        """训练"""
        self.target_net.to(self.device)
        minibatch = random.sample(self.replay_buffer, BATCH_SIZE)
        state_batch = torch.stack([data[0] for data in minibatch])
        action_batch = [data[1] for data in minibatch]
        reward_batch = [data[2] for data in minibatch]
        next_state_batch = torch.stack([data[3] for data in minibatch])
        # 使用 target_net 进行前向传播
        Q_value_batch = self.target_net(next_state_batch)

        y_batch = []
        for i in range(0, BATCH_SIZE):
            done = minibatch[i][4]
            if done:
                y_batch.append(reward_batch[i])
            else:
                y_batch.append(reward_batch[i] + GAMMA * torch.max(Q_value_batch[i]))

        action_batch = torch.tensor(np.array(action_batch), dtype=torch.float32).to(self.device)
        Q_eval = self.eval_net(state_batch)
        Q_action = torch.sum(torch.mul(Q_eval, action_batch), dim=1)
        y_batch = torch.tensor(y_batch, dtype=torch.float32).to(self.device)
        loss = self.loss(Q_action, y_batch)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def save_model(self):
        """保存模型"""
        torch.save(self.target_net.state_dict(), self.model_path)
        log.appendLog(f"模型已保存至{self.model_path}", "INFO")

    def load_model(self, existed_model_path=None):
        """加载模型"""
        self.target_net.load_state_dict(torch.load(existed_model_path))
        log.appendLog(f"模型已加载自{existed_model_path}", "INFO")

    def update_target_net(self):
        """更新目标网络"""
        self.target_net.load_state_dict(self.eval_net.state_dict())
        log.appendLog("目标网络已更新", "INFO")
