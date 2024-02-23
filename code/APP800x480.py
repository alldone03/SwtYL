
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import cv2
import torch
from keyboard.number_pad import numberPopup
import numpy as np
import res_rc


class Camera(QThread):
    frameCaptured = pyqtSignal(QImage) # create signal
    saved_frame = None
    model = None
    datajumlahterdeteksi = [0,0,0]
    model = torch.hub.load(r'../../yolo', 'custom', path='/home/alldone/Desktop/sawit-yolo/model/content/yolov5/runs/train/exp5/weights/best.pt', source='local',
                       force_reload=True, device='cpu')
    def __init__(self):
        super().__init__()
        self.capture = cv2.VideoCapture(0) # capture video from camera
        
        self.model.conf = 0.7
        self.model.line_thickness = 1
        self.isRunning = True # set running flag
        
    _images = None # private variable
    
    # load images from camera
    def run(self):
        # print("running")
        while True:
            ret, frame = self.capture.read() # read frame from camera
            self.saved_frame = frame.copy()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert frame to RGB
                h, w, ch = frame.shape # get frame shape
                bytesPerLine = ch * w # get bytes per line
                convert_to_qt_format = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888) # convert frame to QImage
                p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio) # scale image
                self.frameCaptured.emit(p) # emit signal
    
    # yolo inference function
    def inference_yolo(self):
        cv2.resize(self.saved_frame, (640, 480))
        self.results = self.model(self.saved_frame)
        self.tag = self.results.names
        # print(self.tag)
        cv_img = np.squeeze(self.results.render())
        # pass
        return cv_img
    
    # test read static image
    def readImage(self):
        frame = cv2.imread('/home/alldone/Desktop/sawit-yolo/image/sawit.jpg')
        cv2.resize(frame, (256, 192))
        return frame

class Ui_MainWindow(object):
    camera = Camera() # create camera object
    value_nomorpohon = 0
    value_buahjatuh = 0
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Capture = QtWidgets.QPushButton(self.centralwidget)
        self.Capture.setGeometry(QtCore.QRect(700, 270, 91, 81))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Capture.setFont(font)
        self.Capture.setObjectName("Capture")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(570, 280, 91, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.btn_buahjatuh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_buahjatuh.setGeometry(QtCore.QRect(440, 280, 91, 71))
        self.btn_buahjatuh.setObjectName("btn_buahjatuh")
        self.val_buahjatuh = QtWidgets.QLabel(self.centralwidget)
        self.val_buahjatuh.setGeometry(QtCore.QRect(440, 370, 91, 41))
        self.val_buahjatuh.setAlignment(QtCore.Qt.AlignCenter)
        self.val_buahjatuh.setObjectName("val_buahjatuh")
        self.btn_nomorPohon = QtWidgets.QPushButton(self.centralwidget)
        self.btn_nomorPohon.setGeometry(QtCore.QRect(180, 280, 91, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_nomorPohon.sizePolicy().hasHeightForWidth())
        self.btn_nomorPohon.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.btn_nomorPohon.setFont(font)
        self.btn_nomorPohon.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_nomorPohon.setCheckable(False)
        self.btn_nomorPohon.setAutoRepeat(False)
        self.btn_nomorPohon.setObjectName("btn_nomorPohon")
        self.val_nomorpohon = QtWidgets.QLabel(self.centralwidget)
        self.val_nomorpohon.setGeometry(QtCore.QRect(180, 370, 91, 41))
        self.val_nomorpohon.setAlignment(QtCore.Qt.AlignCenter)
        self.val_nomorpohon.setObjectName("val_nomorpohon")
        self.btn_processdecision = QtWidgets.QPushButton(self.centralwidget)
        self.btn_processdecision.setGeometry(QtCore.QRect(580, 380, 91, 41))
        self.btn_processdecision.setObjectName("btn_processdecision")
        self.btn_showtableresult_2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_showtableresult_2.setGeometry(QtCore.QRect(700, 360, 91, 71))
        self.btn_showtableresult_2.setObjectName("btn_showtableresult_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(430, 270, 111, 161))
        self.label_7.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(170, 270, 111, 161))
        self.label_8.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.resultdecision = QtWidgets.QLabel(self.centralwidget)
        self.resultdecision.setGeometry(QtCore.QRect(560, 330, 121, 31))
        self.resultdecision.setAlignment(QtCore.Qt.AlignCenter)
        self.resultdecision.setWordWrap(False)
        self.resultdecision.setObjectName("resultdecision")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(550, 270, 141, 161))
        self.label_9.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 781, 251))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Camera = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.Camera.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Camera.setFont(font)
        self.Camera.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.Camera.setAlignment(QtCore.Qt.AlignCenter)
        self.Camera.setObjectName("Camera")
        self.horizontalLayout.addWidget(self.Camera)
        self.Camera_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
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
        self.horizontalLayout.addWidget(self.Camera_2)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(290, 270, 131, 161))
        self.label_10.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(300, 280, 111, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 310, 141, 91))
        self.widget.setStyleSheet("background-position: center;\n"
"                background-repeat: no-repeat;\n"
"                background-attachment: fixed;\n"
"                background-clip: border;\n"
"                border-image: url(:/ITS LOGO/logo-its-biru-transparan.png) 20 20 20 20 stretch stretch;\n"
"                border-radius: 20px;")
        self.widget.setObjectName("widget")
        self.label_9.raise_()
        self.label_8.raise_()
        self.label_7.raise_()
        self.Capture.raise_()
        self.label_2.raise_()
        self.btn_buahjatuh.raise_()
        self.val_buahjatuh.raise_()
        self.btn_nomorPohon.raise_()
        self.val_nomorpohon.raise_()
        self.btn_processdecision.raise_()
        self.btn_showtableresult_2.raise_()
        self.resultdecision.raise_()
        self.horizontalLayoutWidget.raise_()
        self.label_10.raise_()
        self.verticalLayoutWidget.raise_()
        self.widget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
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
        self.Capture.setText(_translate("MainWindow", "Capture"))
        self.label_2.setText(_translate("MainWindow", "Decision"))
        self.btn_buahjatuh.setText(_translate("MainWindow", "Input \n"
"Fruit \n"
"Drop"))
        self.val_buahjatuh.setText(_translate("MainWindow", "0"))
        self.btn_nomorPohon.setText(_translate("MainWindow", "Input \n"
"Number \n"
"of Tree"))
        self.val_nomorpohon.setText(_translate("MainWindow", "0"))
        self.btn_processdecision.setText(_translate("MainWindow", "Submit"))
        self.btn_showtableresult_2.setText(_translate("MainWindow", "Show Table"))
        self.resultdecision.setText(_translate("MainWindow", "Result Decision"))
        self.Camera.setText(_translate("MainWindow", "Camera"))
        self.Camera_2.setText(_translate("MainWindow", "Result Detection"))
        self.label.setText(_translate("MainWindow", "Matang : "))
        self.label_3.setText(_translate("MainWindow", "Mentah :"))
        self.label_4.setText(_translate("MainWindow", "Busuk    :"))


        #action is clicked
        self.btn_nomorPohon.clicked.connect(self.nomorpohon_push_button_clicked)
        self.btn_buahjatuh.clicked.connect(self.buahjatuh_push_button_clicked)
        self.Capture.clicked.connect(self.capture_image) # connect signal to slot
        
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
        
    
    
    
    #function show UI
    def showToUI(self,frame, label):
        pixmap = QPixmap.fromImage(frame)
        pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
    def update_image(self, frame):
        self.showToUI(frame,self.Camera)
    def capture_image(self):
        image = self.camera.inference_yolo()
        # print(image)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert frame to RGB
        h, w, ch = frame.shape # get frame shape
        bytesPerLine = ch * w
        convert_to_qt_format = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888) # convert frame to QImage
        p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio) # scale image
        
        self.showToUI(p,self.Camera_2)
        

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
