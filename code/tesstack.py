import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout(centralWidget)

        self.stackedWidget = QStackedWidget()
        layout.addWidget(self.stackedWidget)

        # Create three widgets
        widget1 = QWidget()
        label1 = QLabel("Widget 1")
        layout1 = QVBoxLayout(widget1)
        layout1.addWidget(label1)

        widget2 = QWidget()
        label2 = QLabel("Widget 2")
        layout2 = QVBoxLayout(widget2)
        layout2.addWidget(label2)

        widget3 = QWidget()
        label3 = QLabel("Widget 3")
        layout3 = QVBoxLayout(widget3)
        layout3.addWidget(label3)

        # Add widgets to the stacked widget
        self.stackedWidget.addWidget(widget1)
        self.stackedWidget.addWidget(widget2)
        self.stackedWidget.addWidget(widget3)

        # Create buttons to switch between widgets
        button1 = QPushButton("Widget 1")
        button2 = QPushButton("Widget 2")
        button3 = QPushButton("Widget 3")

        button1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        button2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        button3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(button1)
        buttonLayout.addWidget(button2)
        buttonLayout.addWidget(button3)
        layout.addLayout(buttonLayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())