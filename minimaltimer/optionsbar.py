from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton

class OptionsBar(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self) -> None:
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(QPushButton('Option'))
