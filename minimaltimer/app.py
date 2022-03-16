import sys
from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QIcon
from minimaltimer.mainwindow import MainWindow
from minimaltimer import resources_rc

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/resources/icon.png"))
    
    win = MainWindow()
    win.show()
    app.exec_()
