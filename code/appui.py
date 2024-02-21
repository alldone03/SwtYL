
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import cv2
import torch


class Camera(QThread):
    frameCaptured = pyqtSignal(QImage) # create signal
    def __init__(self):
        super().__init__()
        self.capture = cv2.VideoCapture(0) # capture video from camera
        self.isRunning = True # set running flag
        
    __images = None # private variable
    
    def run(self):
        while True:
            ret, frame = self.capture.read() # read frame from camera
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert frame to RGB
                h, w, ch = frame.shape # get frame shape
                bytesPerLine = ch * w # get bytes per line
                convert_to_qt_format = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888) # convert frame to QImage
                p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio) # scale image
                self.frameCaptured.emit(p) # emit signal
                
                

    def inference_yolo(self):
        pass
    def readImage(self):
        frame = cv2.imread('/home/alldone/Desktop/sawit-yolo/image/sawit.jpg')
        cv2.resize(frame, (256, 192))
        return frame

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1022, 643)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1021, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Camera = QtWidgets.QLabel(self.centralwidget)
        self.Camera.setGeometry(QtCore.QRect(10, 100, 640, 480))
        self.Camera.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Camera.setFont(font)
        self.Camera.setObjectName("Camera")
        self.Capture = QtWidgets.QPushButton(self.centralwidget)
        self.Capture.setGeometry(QtCore.QRect(700, 310, 299, 61))
        self.Capture.setObjectName("Capture")
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(700, 370, 299, 31))
        self.label_3.setObjectName("label_3")
        self.input_buah_jatuh = QtWidgets.QSpinBox(self.centralwidget)
        self.input_buah_jatuh.setGeometry(QtCore.QRect(700, 410, 299, 26))
        self.input_buah_jatuh.setObjectName("input_buah_jatuh")
        self.btn_Input_buah_jatuh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Input_buah_jatuh.setGeometry(QtCore.QRect(700, 450, 299, 61))
        self.btn_Input_buah_jatuh.setObjectName("btn_Input_buah_jatuh")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(700, 520, 297, 41))
        self.label_2.setObjectName("label_2")
        self.Camera_2 = QtWidgets.QLabel(self.centralwidget)
        self.Camera_2.setGeometry(QtCore.QRect(720, 100, 256, 192))
        self.Camera_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Camera_2.setFont(font)
        self.Camera_2.setObjectName("Camera_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1022, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow) # translate UI
        QtCore.QMetaObject.connectSlotsByName(MainWindow) # connect slot to signal
        
        self.Capture.clicked.connect(self.capture_image) # connect signal to slot
        self.camera = Camera() # create camera object
        self.camera.frameCaptured.connect(self.update_image) # connect signal to slot
        self.camera.start()
        
    saved_frame = None
    def showToUI(self,frame, label):
        pixmap = QPixmap.fromImage(frame)
        pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        
    
    def update_image(self, frame):
        self.saved_frame = frame
        self.showToUI(frame,self.Camera)
        
    # def load_image(self):
    #     frame = self.camera.readCamera()
    #     qImg = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
    #     pixmap = QPixmap.fromImage(qImg)
    #     pixmap = pixmap.scaled(self.Camera.size(), Qt.KeepAspectRatio)
    #     self.Camera.setPixmap(pixmap)
        
    def capture_image(self):
        # print("hello")
        self.showToUI(self.saved_frame,self.Camera_2)
        
        
        
        pass
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Harvesting Sickle"))
        self.label.setText(_translate("MainWindow", "Harvesting Sickle"))
        self.Camera.setText(_translate("MainWindow", "Camera"))
        self.Capture.setText(_translate("MainWindow", "Capture"))
        self.label_3.setText(_translate("MainWindow", "Input Buah Jatuh"))
        self.btn_Input_buah_jatuh.setText(_translate("MainWindow", "Input"))
        self.label_2.setText(_translate("MainWindow", "Result"))
        self.Camera_2.setText(_translate("MainWindow", "Camera"))
        
        
def main() -> None:
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # ui.load_image()
    MainWindow.show()
    sys.exit(app.exec_())
            
if __name__ == "__main__":
    main()
