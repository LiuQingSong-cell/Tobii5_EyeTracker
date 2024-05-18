from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import tifffile as tif
import sys

from PyQt5.QtWidgets import QWidget

# 可以绘制点数据的标签
class DotLabel(QLabel):
    def __init__(self, gaze_points: tuple | list, parent=None):
        super().__init__(parent)
        self.gaze_points = gaze_points
    
    def paintEvent(self, evt: QPaintEvent | None) -> None:
        super().paintEvent(evt)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  
        painter.setPen(QPen(QColor('yellow'), 5))
        painter.setBrush(QColor('yellow'))

        for gaze in self.gaze_points:
            # painter.drawPoint(int(gaze[0]), int(gaze[1]))
            painter.drawEllipse(QPoint(int(gaze[0]), int(gaze[1])), 1, 1)

class ShowGazeWindow(QWidget):
    def __init__(self, show_image_path: str, gaze_tuple: tuple, parent: QWidget=None) -> None:
        super().__init__(parent)
        self.show_image_path = show_image_path
        self.gaze_points = gaze_tuple
        self.setWindowTitle("眼动轨迹点可视化")

        try:
            image = tif.imread(self.show_image_path)
            self.qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_RGB888)
        except Exception as e:
            self.qimage = QImage(self.show_image_path)

        self.left_margin = (1920 - self.qimage.width()) / 2
        self.up_margin = (1080 - self.qimage.height()) / 2

        self.initUI()


    def initUI(self):
        gaze = []
        for p in self.gaze_points:
            x, y = p[0] * 1920, p[1] * 1080
            if x >= self.left_margin and x <= 1920 - self.left_margin and y >= self.up_margin and y <= 1080 - self.up_margin:
                # self.drawer.drawPoint(int(x - self.left_margin), int(y - self.up_margin))
                gaze.append((int(x - self.left_margin), int(y - self.up_margin)))

        self.image_label = DotLabel(gaze, self)
        self.image_label.setPixmap(QPixmap.fromImage(self.qimage))
        self.setFixedSize(self.qimage.size())




if __name__ == '__main__':

    app = QApplication([])
    win = DotLabel(((1, 1), (10, 10), (30, 10), ))
    win.resize(50, 50)
    win.show()
    sys.exit(app.exec_())