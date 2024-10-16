"""
日志窗口，输出操作日志
"""

import sys

from PySide6.QtWidgets import (QApplication,
                                QWidget,QTextBrowser,
                                QVBoxLayout,
                                )
from PySide6.QtCore import QDateTime

MAX_LOG_NUM = 100 # 最大日志数量

class LogWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(1280*0.8, 180)

        self.vBoxLayout = QVBoxLayout(self)

        self.textBrowser = QTextBrowser()
        self.vBoxLayout.addWidget(self.textBrowser)

        self.appendLog('日志窗口已启动', 'INFO')
        self.appendLog('日志最大数量：100 ，当超过最大限额将清空当前日志列表', 'WARNING')


    def appendLog(self, log, kind='OP'):
        """
        添加日志，日志格式：时间（橙色） 日志类型（绿/红/黄/蓝） 日志内容（白色）
        @param log: 日志内容
        @param kind: 日志类型
        """
        if self.textBrowser.document().blockCount() > MAX_LOG_NUM: # 超过最大日志数量，清空日志
            self.textBrowser.clear()

        time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss") # 获取当前时间
        time = time[11:] # 仅保留时分秒
        if kind == 'INFO':
            self.textBrowser.append(f'<p style="font-size: 16px; line-height: 0.6;"><font color="orange">{time}</font> <font color="green">[INFO]</font> <font color="white">{log}</font></p>')
        elif kind == 'OP':
            self.textBrowser.append(f'<p style="font-size: 16px; line-height: 0.6;"><font color="orange">{time}</font> <font color="#ADD8E6">[OP]</font> <font color="white">{log}</font></p>')
        elif kind == 'ERROR':
            self.textBrowser.append(f'<p style="font-size: 16px; line-height: 0.6;"><font color="orange">{time}</font> <font color="red">[ERROR]</font> <font color="white">{log}</font></p>')
        elif kind == 'WARNING':
            self.textBrowser.append(f'<p style="font-size: 16px; line-height: 0.6;"><font color="orange">{time}</font> <font color="yellow">[WARNING]</font> <font color="white">{log}</font></p>')

        self.textBrowser.repaint() # 刷新
        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum()) # 滚动到底部

app = QApplication(sys.argv) # 创建应用
log = LogWindow()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = LogWindow()
    w.show()
    app.exec()