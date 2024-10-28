# Auto Hollow-Knight

![language](https://img.shields.io/badge/language-Python-blue)
![license](https://img.shields.io/badge/License-MIT-red)
![pytorch](https://img.shields.io/badge/Framework-Pytorch-orange)

>使用‘强化学习’知识训练模型操纵游戏‘空洞骑士’中的小骑士与BOSS战斗

**注意事项**：若要调试程序，请以管理员身份启动VSC

---

> [!Important]
> 本程序中强化学习的奖励机制依赖检测**小骑士的生命值与BOSS生命值的变化**来推进。为此您需要安装显示**BOSS血条**的Mod并且您的小骑士皮肤Mod所显示的小骑士的生命需要接近白色！

## 网络架构

最初的网络架构比较简单粗暴，网络结构的变更日志如下（配置参考：RTX3050-GPU-LAPTOP）：

- 2024-10-12：缩水版AlexNet
- 2024-10-24：在前代架构下缩减了参数量

>Tip：由于个人能力有限，我目前使用的网络架构效率可能仍较为低下，如果有更优的方案欢迎讨论。

## 日志

### [万神殿-格鲁兹之母-调谐级] 2024-10-17

小骑士于2024/10/17晚的第30轮（合计约为60轮）训练左右偶尔能够击败BOSS，并于第40轮（合计约为70轮）训练左右能够经常性击败BOSS

虽然它学会的只是‘莽夫流’--“骄傲快劈，天下无敌”。
但需要考虑到程序的诸多限制与不足（后文会提到），再加上其奖励曲线确实有不小的进步，个人认为这个ai小骑士还是有在不断前进的。只是我的个人能力问题导致训练结果看起来不太聪明=_=

reward变化图（实际为30~70轮训练的reward）：
![alt text](backend/rsc/images/3rd_try_2024_10_17/reward_40.png)

---

## 限制与不足

- 当前的代码对小骑士操作的多线程适配并不完全（相当于你在用一到两根手指头打游戏）
- 以我个人的程序效率与算力支持，程序的实际每秒接收帧数可能只有6~8帧
- 奖励机制的设置较为简单粗暴

---

## 参考资料

- [DQN-Sekiro](https://github.com/analoganddigital/DQN_play_sekiro/blob/main/README.md): 蓝魔digital, DQN只狼实战教程, Github, 2021.
- [DQN-Sekiro（Pytorch）](https://github.com/Skaiyin/DQN_play_blood):Skaiyin, torch form, Github, 2024.
