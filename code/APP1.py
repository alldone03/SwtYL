
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import cv2
import torch
from keyboard.number_pad import numberPopup


class Camera(QThread):
    frameCaptured = pyqtSignal(QImage) # create signal
    def __init__(self):
        super().__init__()
        self.capture = cv2.VideoCapture(0) # capture video from camera
        self.isRunning = True # set running flag
        
    __images = None # private variable
    
    # load images from camera
    def run(self):
        print("running")
        while True:
            
            ret, frame = self.capture.read() # read frame from camera``
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert frame to RGB
                h, w, ch = frame.shape # get frame shape
                bytesPerLine = ch * w # get bytes per line
                convert_to_qt_format = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888) # convert frame to QImage
                p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio) # scale image
                self.frameCaptured.emit(p) # emit signal
    
    # yolo inference function
    def inference_yolo(self):
        pass
    
    # test read static image
    def readImage(self):
        frame = cv2.imread('/home/alldone/Desktop/sawit-yolo/image/sawit.jpg')
        cv2.resize(frame, (256, 192))
        return frame

class Ui_MainWindow(object):
    value_nomorpohon = 0
    value_buahjatuh = 0
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Camera = QtWidgets.QLabel(self.centralwidget)
        self.Camera.setGeometry(QtCore.QRect(30, 100, 480, 360))
        self.Camera.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Camera.setFont(font)
        self.Camera.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.Camera.setAlignment(QtCore.Qt.AlignCenter)
        self.Camera.setObjectName("Camera")
        self.Capture = QtWidgets.QPushButton(self.centralwidget)
        self.Capture.setGeometry(QtCore.QRect(530, 410, 221, 51))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Capture.setFont(font)
        self.Capture.setObjectName("Capture")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(430, 480, 299, 31))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(920, 480, 171, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.Camera_2 = QtWidgets.QLabel(self.centralwidget)
        self.Camera_2.setGeometry(QtCore.QRect(770, 100, 480, 360))
        self.Camera_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Camera_2.setFont(font)
        self.Camera_2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.Camera_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Camera_2.setLineWidth(20)
        self.Camera_2.setTextFormat(QtCore.Qt.AutoText)
        self.Camera_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Camera_2.setObjectName("Camera_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 20, 1019, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(120, 70, 299, 31))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(870, 70, 299, 31))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.btn_buahjatuh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_buahjatuh.setGeometry(QtCore.QRect(430, 530, 299, 61))
        self.btn_buahjatuh.setObjectName("btn_buahjatuh")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(460, 610, 101, 41))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.val_buahjatuh = QtWidgets.QLabel(self.centralwidget)
        self.val_buahjatuh.setGeometry(QtCore.QRect(580, 610, 101, 41))
        self.val_buahjatuh.setAlignment(QtCore.Qt.AlignCenter)
        self.val_buahjatuh.setObjectName("val_buahjatuh")
        self.btn_nomorPohon = QtWidgets.QPushButton(self.centralwidget)
        self.btn_nomorPohon.setGeometry(QtCore.QRect(60, 530, 299, 61))
        self.btn_nomorPohon.setObjectName("btn_nomorPohon")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(60, 480, 299, 31))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.val_nomorpohon = QtWidgets.QLabel(self.centralwidget)
        self.val_nomorpohon.setGeometry(QtCore.QRect(190, 610, 101, 41))
        self.val_nomorpohon.setAlignment(QtCore.Qt.AlignCenter)
        self.val_nomorpohon.setObjectName("val_nomorpohon")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(70, 610, 101, 41))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(920, 500, 171, 141))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.btn_processdecision = QtWidgets.QPushButton(self.centralwidget)
        self.btn_processdecision.setGeometry(QtCore.QRect(790, 490, 111, 151))
        self.btn_processdecision.setObjectName("btn_processdecision")
        self.btn_showtableresult_2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_showtableresult_2.setGeometry(QtCore.QRect(1120, 470, 131, 191))
        self.btn_showtableresult_2.setObjectName("btn_showtableresult_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(30, 470, 361, 191))
        self.label_7.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(400, 470, 361, 191))
        self.label_9.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(770, 470, 341, 191))
        self.label_12.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.label_12.raise_()
        self.label_9.raise_()
        self.label_7.raise_()
        self.Camera.raise_()
        self.Capture.raise_()
        self.label_3.raise_()
        self.label_2.raise_()
        self.Camera_2.raise_()
        self.label.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.btn_buahjatuh.raise_()
        self.label_6.raise_()
        self.val_buahjatuh.raise_()
        self.btn_nomorPohon.raise_()
        self.label_8.raise_()
        self.val_nomorpohon.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.btn_processdecision.raise_()
        self.btn_showtableresult_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Camera.setText(_translate("MainWindow", "Camera"))
        self.Capture.setText(_translate("MainWindow", "Capture"))
        self.label_3.setText(_translate("MainWindow", "Input Fruit Drop "))
        self.label_2.setText(_translate("MainWindow", "Decision"))
        self.Camera_2.setText(_translate("MainWindow", "Result Detection"))
        self.label.setText(_translate("MainWindow", "Harvesting Sickle"))
        self.label_4.setText(_translate("MainWindow", "Camera"))
        self.label_5.setText(_translate("MainWindow", "Captured"))
        self.btn_buahjatuh.setText(_translate("MainWindow", "Input"))
        self.label_6.setText(_translate("MainWindow", "Result Input"))
        self.val_buahjatuh.setText(_translate("MainWindow", "0"))
        self.btn_nomorPohon.setText(_translate("MainWindow", "Input"))
        self.label_8.setText(_translate("MainWindow", "Input Number Tree"))
        self.val_nomorpohon.setText(_translate("MainWindow", "0"))
        self.label_10.setText(_translate("MainWindow", "Result Input"))
        self.label_11.setText(_translate("MainWindow", "Result"))
        self.btn_processdecision.setText(_translate("MainWindow", "Input"))
        self.btn_showtableresult_2.setText(_translate("MainWindow", "Show Table Result"))
    

        #action is clicked
        self.btn_nomorPohon.clicked.connect(self.nomorpohon_push_button_clicked)
        self.btn_buahjatuh.clicked.connect(self.buahjatuh_push_button_clicked)
        self.Capture.clicked.connect(self.capture_image) # connect signal to slot
        self.camera = Camera() # create camera object
        self.camera.frameCaptured.connect(self.update_image) # connect signal to slot
        self.camera.start()
        
    # event show keyboard to nomor pohon
    def nomorpohon_push_button_clicked(self):
        self.MainWindow.setEnabled(False)
        self.exPopup = numberPopup(self.MainWindow,self.val_nomorpohon, "", self.nomorpohon_callBackOnSubmit, "Argument 1", "Argument 2")
        self.exPopup.setGeometry(130, 320,400, 300)
        self.exPopup.show()
    def nomorpohon_onClick(self,e):
        self.MainWindow.setEnabled(True)
    def nomorpohon_callBackOnSubmit(self, arg1, arg2,data):
        value_nomorpohon = data
    # event show keyboard to buah jatuh
    def buahjatuh_push_button_clicked(self):
        self.MainWindow.setEnabled(False)
        self.exPopup = numberPopup(self.MainWindow,self.val_buahjatuh, "", self.buahjatuh_callBackOnSubmit, "Argument 1", "Argument 2")
        self.exPopup.setGeometry(130, 320,400, 300)
        self.exPopup.show()
    def buahjatuh_onClick(self,e):
        self.MainWindow.setEnabled(True)
    def buahjatuh_callBackOnSubmit(self, arg1, arg2,data):
        value_buahjatuh = data
        
    
    
    saved_frame = None
    #function show UI
    def showToUI(self,frame, label):
        pixmap = QPixmap.fromImage(frame)
        pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
    def update_image(self, frame):
        self.saved_frame = frame
        self.showToUI(frame,self.Camera)
    def capture_image(self):
        self.showToUI(self.saved_frame,self.Camera_2)
        pass

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
