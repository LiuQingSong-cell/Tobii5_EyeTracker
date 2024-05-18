from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
import tifffile as tif

import csv

from EyeTracker import get_eye_points
from ShowEyeGazeWindow import ShowGazeWindow


class EyeTrackerWindow(QWidget):
    def __init__(self, image_path: str, collect_time: int, save_path: str, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.image_path = image_path
        self.collect_time = collect_time
        self.save_path = save_path
        self.isCollecting = False

        self.images = os.listdir(self.image_path)
        self.images_num = len(self.images)


        self.player = QMediaPlayer(self)
        self.player.setMedia(QMediaContent(QUrl("./done.wav")))
        self.drawer = QPainter(self)
        self.drawer.setPen(QColor("red"))

        self.setWindowIcon(QIcon("./images/eye.png"))
        self.setWindowTitle("EyeTracker Window")
        self.setStyleSheet("background-color: black;")

        self.initUI()
    
    def initUI(self):  
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)  
        
        self.label = QLabel()
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.tip_label = QLabel(self)
        self.tip_label.move(10, 0)
        self.tip_label.setStyleSheet("color: red; font-size: 20px")
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.current_image = 0  
        self.__showImage()
    
    def __showImage(self):
        """
            支持常规图像格式(如jpg, png等)以及tif格式的图片资源
            3D或者特殊格式的图像暂不支持 可自行扩展
        """
        try:
            image = tif.imread(self.image_path + '/' + self.images[self.current_image])
            qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_RGB888)
        except Exception as e:
            qimage = QImage(self.image_path + '/' + self.images[self.current_image])

        self.label.setPixmap(QPixmap.fromImage(qimage))
  
    def showNextImage(self):  
        self.tip_label.clear()
        self.current_image = (self.current_image + 1) % self.images_num 
        self.__showImage()
         
    
    def showPreImage(self):
        self.tip_label.clear()
        self.current_image = (self.current_image - 1) % self.images_num
        self.__showImage()
    

    def save_gaze2csv(self, gaze: tuple):
        image_name = self.images[self.current_image].split('.')[0]

        output_file_name = self.save_path + '/' + image_name + '.csv'

        with open(output_file_name, 'w', newline="") as f:
            writer = csv.writer(f)
            for row in gaze:
                writer.writerow(row)

    
    def keyPressEvent(self, evt: QKeyEvent | None) -> None:
        if evt.key() == Qt.Key.Key_Escape and not self.isCollecting:
            self.showNormal()
        elif evt.key() == Qt.Key.Key_Right and not self.isCollecting:
            self.showNextImage()
        elif evt.key() == Qt.Key.Key_Left and not self.isCollecting:
            self.showPreImage()
        elif evt.key() == Qt.Key.Key_Space and not self.isCollecting:
            self.isCollecting = True
            self.tip_label.setText("采集中...")
            QApplication.processEvents()

            self.gaze_tuple = get_eye_points(self.collect_time)
            self.save_gaze2csv(self.gaze_tuple)
            self.player.play() 
            self.tip_label.setText("眼动数据保存成功!")
            self.tip_label.adjustSize()
            
            self.gaze_window = ShowGazeWindow(self.image_path + '/' + self.images[self.current_image], 
                                              self.gaze_tuple)

            self.isCollecting = False

            self.gaze_window.show()
