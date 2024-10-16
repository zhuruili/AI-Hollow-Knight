import sys

from frontend.logWindow import app
from frontend.mainWindow import MainWindow

if __name__ == '__main__':
    # app = QApplication(sys.argv) # 在日志窗口中已经创建了一个app实例
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

    