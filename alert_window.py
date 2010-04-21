from PyQt4.QtCore import QTimer
from PyQt4.QtGui import *

ALERT_WIDTH = 350
ALERT_HEIGHT = 200

class AlertWindow(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setWindowIcon(QIcon("icon.png"))
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(ALERT_WIDTH, ALERT_HEIGHT)
        self.move((screen.width()-ALERT_WIDTH-10), 20)
        self.setWindowOpacity(0.8)
        layout = QVBoxLayout(self)
        QTimer.singleShot(10000, self.end)
        
    def end(self):
        self.close()
        self.destroy()
        
    def setup(self, title, text):
        self.setWindowTitle(title)
        layout = self.layout()
        scroll = QScrollArea()
        scroll.setWidget(QLabel(text))
        layout.addWidget(scroll)
