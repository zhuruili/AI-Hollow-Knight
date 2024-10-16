# coding:utf-8
"""
游戏窗口（基本上是空窗，用来放游戏画面）
本窗口自带重置游戏窗口布局按钮
"""
import sys

from PySide6.QtWidgets import (QApplication, 
                               QWidget, 
                               QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import Qt
from qfluentwidgets import (LargeTitleLabel, TitleLabel, 
                            PushButton,
                            setTheme, Theme)
from qfluentwidgets import FluentIcon as FIF

from backend.init import initialize


class GameWindow(QWidget):

    def __init__(self):
        super().__init__()

        # setTheme(Theme.DARK)

        self.sizerate = 0.8 # 放缩比例

        self.resize(1280*self.sizerate, 720*self.sizerate)

        # 垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setSpacing(20)

        # 水平布局
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addStretch(1) # 左侧空白
        self.hBoxLayout.addWidget(LargeTitleLabel('游戏画面放置处'))
        self.hBoxLayout.addStretch(1) # 右侧空白

        self.vBoxLayout.addLayout(self.hBoxLayout) # 添加水平布局到垂直布局

        self.LayoutRefreshButton = PushButton(FIF.LAYOUT, '重置游戏窗口布局', self)
        self.LayoutRefreshButton.setFixedSize(200, 50)
        self.LayoutRefreshButton.clicked.connect(initialize) # 点击按钮重置游戏窗口布局
        self.vBoxLayout.addWidget(self.LayoutRefreshButton)
        self.vBoxLayout.setAlignment(self.LayoutRefreshButton,Qt.AlignCenter)

        TipLabel = TitleLabel('推荐分辨率：1280*720')
        self.vBoxLayout.addWidget(TipLabel) 
        self.vBoxLayout.setAlignment(TipLabel, Qt.AlignCenter)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GameWindow()
    w.show()
    app.exec()