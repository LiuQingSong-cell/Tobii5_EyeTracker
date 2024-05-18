from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

from WelcomWindow import WelcomWindow

from EyeTracker import InitEyeTracker, CheckEyeTracker



about_text = """欢迎使用本眼动信息采集系统。
在接下来的配置页面请选择要采集眼动信息图片的路径以及每张图片的采集时间(1~100s),最后请选择要将眼动数据保存在哪一个位置。\n
使用操作：方向键左右可控制图片的前后切换，空格键可开始对当前图片进行眼动信息采集
            """



if __name__ == '__main__':
    app = QApplication(sys.argv)

    if CheckEyeTracker() == -1:
        QMessageBox.critical(None, "错误", "未找到眼动追踪设备！")
        sys.exit(-1)
    else:
        InitEyeTracker()
        
        win = WelcomWindow()
        win.show()
        QMessageBox.about(None, "眼动采集系统介绍", about_text)
        
    sys.exit(app.exec_())
    