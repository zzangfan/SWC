# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvas
#qt5모듈을 위한 matplotlib라이브러리의 Backed
#이것을 사용하면 matplotlib에서 사용하는 형식을 qt5모듈에 사용이 가능해진다.
from matplotlib.figure import Figure


class MplWidget(QWidget):
    #그래프가 그려지는 위젯 클래스
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure(figsize=(10,20)))


        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        #화면의 축을 생성




        self.setLayout(vertical_layout)
