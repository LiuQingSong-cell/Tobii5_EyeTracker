from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
import sys

from EyeTrackerWindow import EyeTrackerWindow

class WelcomWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # 定义配置变量
        self.file_path = ""
        self.collect_time = -1
        self.save_path = ""

        self.setFixedSize(700, 450)
        self.setWindowIcon(QIcon("./images/eye.png"))
        self.setWindowTitle("配置界面")
        self.initUi() 

        with open("./Style.qss", "r", encoding='utf-8') as f:
            self.setStyleSheet(f.read())
        
        platte = QPalette()
        platte.setBrush(self.backgroundRole(), QBrush(QPixmap("./images/background.png").scaled(self.size(),
                                                                    Qt.IgnoreAspectRatio,
                                                                    Qt.SmoothTransformation)))
        self.setPalette(platte)

    def initUi(self):
        # 设置文件选择按钮和显示标签
        self.vboxLayout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.vboxLayout.addLayout(self.form_layout)
        self.vboxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fileBtn = QPushButton("选择图片文件夹")
        self.fileBtn.clicked.connect(self.selectFile_slot)
        self.filePathLabel = QLabel()
        # self.filePathLabel.setStyleSheet("font-size: 22px;")
        self.form_layout.addRow(self.fileBtn, self.filePathLabel)
        
        # 设置每张图片的采集时间
        self.timer_label = QLabel()
        self.timer_label.setText("图片采集时间")
        self.spinbox = QSpinBox()  
        self.spinbox.setValue(8)  # 设置初始值  
        self.spinbox.setMinimum(1)  # 设置最小值  
        self.spinbox.setMaximum(100)  # 设置最大值 
        self.spinbox.setSuffix("秒/张") 
        self.form_layout.addRow(self.timer_label, self.spinbox)
        self.collect_time = self.spinbox.value() # 首先获取初始值
        self.spinbox.valueChanged.connect(self.getCollectTime_slot) # 每次改动更新采集时间

        # 设置最后眼动数据文件保存的路径
        self.saveFile_btn = QPushButton("选择保存路径")
        self.saveFile_btn.clicked.connect(self.saveFile_slot)
        self.saveFile_label = QLabel()
        self.form_layout.addRow(self.saveFile_btn, self.saveFile_label)

        self.start_btn = QPushButton("开始采集")
        self.vboxLayout.addWidget(self.start_btn)
        self.start_btn.clicked.connect(self.startCollect_slot)

        self.setLayout(self.vboxLayout)

    
    def selectFile_slot(self):
        self.file_path = QFileDialog.getExistingDirectory(self, "选择图片所在的文件夹", r"C:\pythons\project\VisualGaze\Kvasir-SEG")
        self.filePathLabel.setText(self.file_path)
        self.filePathLabel.adjustSize()

    def getCollectTime_slot(self, value):
        self.collect_time = value

    def saveFile_slot(self):
        self.save_path = QFileDialog.getExistingDirectory(self, "选择保存路径")
        self.saveFile_label.setText(self.save_path)
    
    def startCollect_slot(self):
        self.collect_window = EyeTrackerWindow(self.file_path, self.collect_time, self.save_path)
        self.collect_window.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = WelcomWindow()
    
    

    win.show()

    sys.exit(app.exec_())