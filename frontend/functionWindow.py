"""
功能窗口，自动战斗选项
"""

import sys

from PySide6.QtWidgets import (QApplication,
                                 QWidget, QStackedWidget, QLabel,
                                 QGroupBox,
                                 QVBoxLayout, QHBoxLayout,
                                 )
from PySide6.QtCore import Qt
from qfluentwidgets import (SegmentedToggleToolWidget, 
                            PushButton, TableWidget, CheckBox, 
                            )
from qfluentwidgets import FluentIcon as FIF

from backend.DQN_main import TrainingStart
from backend.utils import (Slash, restart, 
                           screen_grab_test, BloodDetectTest_K, BloodDetectTest_B, 
)

class editInterface(QWidget):
    """编辑调试界面"""
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout(self) # 总体布局（垂直）
        mainLayout.setContentsMargins(30, 10, 30, 30)

        self.TrainStartButton = PushButton(FIF.PLAY_SOLID, 'Training Start', self) # 训练开始按钮
        self.TrainStartButton.clicked.connect(lambda: TrainingStart(use_existed_model=True))
        self.TrainPauseButton = PushButton(FIF.PAUSE, 'Training Pause', self) # 训练暂停按钮
        self.TrainContinueButton = PushButton(FIF.PLAY, 'Training Continue', self) # 训练继续按钮
        pause_and_continue_hbox = QHBoxLayout()
        pause_and_continue_hbox.addWidget(self.TrainPauseButton)
        pause_and_continue_hbox.addWidget(self.TrainContinueButton)
        self.TrainExitButton = PushButton(FIF.POWER_BUTTON, 'Training Stop', self) # 训练停止按钮
        
        self.RestartButton = PushButton(FIF.ACCEPT, '重开测试', self)
        self.RestartButton.clicked.connect(lambda: restart())

        self.TakePhotoButton = PushButton(FIF.CAMERA, '截图测试', self) # 截图按钮
        self.TakePhotoButton.clicked.connect(lambda: screen_grab_test())
        self.Knight_HP_Button = PushButton(FIF.HEART, 'HP检测-小骑士')
        self.Knight_HP_Button.clicked.connect(lambda: BloodDetectTest_K())
        self.Boss_HP_Button = PushButton(FIF.HEART, 'HP检测-BOSS')
        self.Boss_HP_Button.clicked.connect(lambda: BloodDetectTest_B())
        HP_hbox = QHBoxLayout()
        HP_hbox.addWidget(self.Knight_HP_Button)
        HP_hbox.addWidget(self.Boss_HP_Button)
        

        group_box_train = QGroupBox("Training Test")
        train_box_layout = QVBoxLayout() # 训练调试布局（垂直）
        train_box_layout.addWidget(self.TrainStartButton)
        train_box_layout.addSpacing(10)
        train_box_layout.addLayout(pause_and_continue_hbox)
        train_box_layout.addSpacing(10)
        train_box_layout.addWidget(self.TrainExitButton)
        train_box_layout.addSpacing(20)
        group_box_train.setLayout(train_box_layout)

        group_box_operation = QGroupBox("Operation Test")
        operation_box_layout = QVBoxLayout() # 操作测试布局（垂直）
        operation_box_layout.addWidget(self.RestartButton)
        group_box_operation.setLayout(operation_box_layout)

        group_box_cv = QGroupBox("Computer Vision Test")
        cv_box_layout = QVBoxLayout() # CV布局（垂直）
        cv_box_layout.addWidget(self.TakePhotoButton)
        cv_box_layout.addLayout(HP_hbox)
        group_box_cv.setLayout(cv_box_layout)

        mainLayout.addWidget(group_box_train)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(group_box_operation)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(group_box_cv)

class gameInterface(QWidget):
    """自动战斗功能界面"""
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout(self) # 总体布局（垂直）
        mainLayout.setContentsMargins(30, 10, 30, 30)

        # 按键测试按钮
        self.FightRepeatButton = PushButton(FIF.PLAY, '按键测试', self)
        self.FightRepeatButton.clicked.connect(Slash)

        RewardLayout = QHBoxLayout() # 水平布局
        
        # 奖励按钮
        self.daily_rewardButton = PushButton(FIF.BOOK_SHELF, '领取每日奖励', self)
        self.daily_rewardButton.clicked.connect(None)
        self.passportButton = PushButton(FIF.ALBUM, '领取通行证奖励', self)
        self.passportButton.clicked.connect(None)

        RewardLayout.addWidget(self.daily_rewardButton)
        RewardLayout.addWidget(self.passportButton)

        mainLayout.addWidget(self.FightRepeatButton)
        mainLayout.addLayout(RewardLayout)
        
class aiInterface(QWidget):
    """AI战斗界面"""
    pass


class FunctionWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""background-color: #333333;  /* 设置背景颜色 */
                           border: 1px solid #00FFEF;  /* 设置边框 */
                           border-radius: 10px; /* 设置边框圆角半径 */
                           """)

        mainLayout = QVBoxLayout(self) # 总体布局（垂直）

        self.pivot = SegmentedToggleToolWidget(self) # 选项卡
        self.stackedWidget = QStackedWidget(self) # 子界面

        self.hBoxLayout = QHBoxLayout()

        # 下面三个是临时子页面
        self.editInterface = editInterface()
        self.gameInterface = gameInterface()
        self.aiInterface = QLabel('没做', self)

        # add items to pivot
        self.addSubInterface(self.editInterface, 'editInterface', FIF.EDIT)
        self.addSubInterface(self.gameInterface, 'gameInterface', FIF.GAME)
        self.addSubInterface(self.aiInterface, 'aiInterface', FIF.ROBOT)

        self.hBoxLayout.addWidget(self.pivot, 0, Qt.AlignCenter)
        mainLayout.addLayout(self.hBoxLayout)
        mainLayout.addWidget(self.stackedWidget)
        mainLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.setCurrentWidget(self.gameInterface) # 默认显示游戏界面
        self.pivot.setCurrentItem(self.gameInterface.objectName()) # 默认选中游戏界面
        self.pivot.currentItemChanged.connect(
            lambda k:  self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k)))

    def addSubInterface(self, widget: QWidget, objectName, icon):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, icon=icon)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = FunctionWindow()
    w.show()
    app.exec()