"""
主窗口

布局：
    1. 左侧上半部分：放置游戏窗口的空白区
    2. 左侧下半部分：输出操作日志
    3. 右侧为控制区域

基于PySide6实现
"""
import sys

from .gameWindow import GameWindow
from .logWindow import log
from .functionWindow import FunctionWindow

from PySide6.QtWidgets import (QApplication,
                               QWidget,
                               QVBoxLayout, QHBoxLayout)
from PySide6.QtGui import QIcon

from qfluentwidgets import Theme, setTheme

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        setTheme(Theme.DARK) # 设置主题

        # 主窗口设置
        self.title = 'AutoHollowKnight'
        self.size = (1525, 800)
        self.icoPath = 'frontend\\assets\icos\mainWindow.ico'

        self.setWindowTitle(self.title)
        self.resize(*self.size)
        self.setWindowIcon(QIcon(self.icoPath))

        # 初始化ui
        self.init_ui()
    
    def init_ui(self):
        # 创建子窗口实例
        self.game_window = GameWindow() # 游戏窗口
        self.log_window = log # 日志窗口
        self.function_window = FunctionWindow() # 功能窗口

        # 设置窗口大小
        self.game_window.setFixedSize(1280*0.8, 720*0.8)
        self.log_window.setFixedSize(1280*0.8, 800-720*0.8)
        self.function_window.setFixedSize(1500-1280*0.8, 800)


        # 总布局（水平布局）
        self.MainLayout = QHBoxLayout(self)

        # 左侧布局（垂直布局）
        self.LeftLayout = QVBoxLayout()
        self.LeftLayout.addWidget(self.game_window)
        self.LeftLayout.addWidget(self.log_window)

        # 右侧布局（垂直布局）
        self.RightLayout = QVBoxLayout()
        self.RightLayout.addWidget(self.function_window)

        # 添加左右布局到总布局
        self.MainLayout.addLayout(self.LeftLayout)
        self.MainLayout.addLayout(self.RightLayout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())