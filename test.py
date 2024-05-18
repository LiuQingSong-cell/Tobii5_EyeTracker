from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget  
from PyQt5.QtGui import QPainter, QColor 
from PyQt5.QtCore import Qt, QPoint


  
class DotLabel(QLabel):  
    def __init__(self, x, y, parent=None):  
        super().__init__(parent)  
        self.x = x  
        self.y = y  
  
    def paintEvent(self, event):  
        super().paintEvent(event)  
  
        painter = QPainter(self)  
        painter.setRenderHint(QPainter.Antialiasing)  
  
        # 设置画笔颜色和样式  
        painter.setPen()  # 红色  
        # painter.setBrush(QColor(255, 0, 0))  # 红色画刷  
  
        # 在指定位置绘制点  
        painter.drawPoint(self.x, self.y)  
  
class MainWindow(QMainWindow):  
    def __init__(self):  
        super().__init__()  
  
        self.initUI()  
  
    def initUI(self):  
        self.setWindowTitle('QLabel Drawing Example')  
        self.setGeometry(300, 300, 280, 170)  
  
        # 创建 QLabel 并设置其位置和大小  
        dot_label = DotLabel(100, 100)  
        dot_label.setFixedSize(200, 200)  
  
        # 使用 QVBoxLayout 将 QLabel 添加到窗口中  
        layout = QVBoxLayout()  
        layout.addWidget(dot_label)  
  
        container = QWidget()  
        container.setLayout(layout)  
        self.setCentralWidget(container)  
  
if __name__ == '__main__':  
    app = QApplication([])  
  
    window = MainWindow()  
    window.show()  
  
    app.exec_()