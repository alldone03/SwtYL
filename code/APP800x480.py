
from PyQt5 import QtCore, QtGui ,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import cv2
import torch
from lib.number_pad import numberPopup
import numpy as np
import res_rc
import time
import sqlite3

import os
from dotenv import load_dotenv
load_dotenv()
ModelYolo = os.getenv("MODEL_YOLO")
PathYolo = os.getenv("PATH_YOLO")
CameraRealtime = os.getenv("CAMERA_YOLO")
print("Use Model: " + ModelYolo+"\nYolo Path: "+PathYolo+"\nID Camera: "+CameraRealtime)

class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('logging.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tb_data (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                numbertree INTEGER,
                                matang INTEGER,
                                mentah INTEGER,
                                busuk INTEGER,
                                buahjatuh INTEGER,
                                keputusan TEXT
                            )''')
        self.conn.commit()

    def add_record(self, numbertree, buahjatuh, keputusan, matang=0, mentah=0, busuk=0) -> None:
        self.cursor.execute("INSERT INTO tb_data (numbertree, matang, mentah, busuk, buahjatuh, keputusan) VALUES (?, ?, ?, ?, ?, ?)",
                            (numbertree, matang, mentah, busuk, buahjatuh, keputusan))
        self.conn.commit()

    def view_records(self, array) -> None:
        self.cursor.execute("SELECT * FROM tb_data ORDER BY id DESC")
        rows = self.cursor.fetchall()
        for row in rows:
            array.append(row)

    def delete_record(self, numbertree) -> None:
        self.cursor.execute("DELETE FROM tb_data WHERE numbertree = ?", (numbertree,))
        self.conn.commit()


class Camera(QThread):
    frameCaptured = pyqtSignal(QImage) # create signal
    saved_frame = None # create saved frame
    model = None # create model
    datajumlahterdeteksi = [0,0,0] # create data jumlah terdeteksi
    model = torch.hub.load(PathYolo, 'custom', path=ModelYolo, source='local',
                       force_reload=True, device='cpu')
    def __init__(self) -> None:
        super().__init__()
        self.capture = cv2.VideoCapture(int(CameraRealtime)) # capture video from camera
        # self.capture = cv2.VideoCapture(0) # capture video from camera
        
        self.model.conf = 0.7
        self.model.line_thickness = 1
        self.isRunning = True # set running flag
    
    # load images from camera
    def run(self)->None:
        while True:
            # ret, frame = self.capture.read() # read frame from camera
            ret, frame = True,cv2.imread("/home/alldone/Desktop/sawit-yolo/image/sawit.jpg")
            self.saved_frame = frame.copy()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert frame to RGB 
                h, w, ch = frame.shape # get frame shape
                bytesPerLine = ch * w # get bytes per line
                convert_to_qt_format = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888) # convert frame to QImage
                p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio) # scale image
                self.frameCaptured.emit(p) # emit signal
    
    # yolo inference function
    def inference_yolo(self) -> None:
        cv2.resize(self.saved_frame, (640, 480))
        self.results = self.model(self.saved_frame)
        self.tag = self.results.names
        self.datajumlahterdeteksi = [0,0,0]
        for i in self.results.xyxy[0]:
            self.datajumlahterdeteksi[int(i[5])] = self.datajumlahterdeteksi[int(i[5])] + 1
        cv_img = np.squeeze(self.results.render())
        # pass
        return cv_img
    
    # test read static image
    def readImage(self) -> None:
        frame = cv2.imread('/home/alldone/Desktop/sawit-yolo/image/sawit.jpg')
        cv2.resize(frame, (256, 192))
        return frame

class Ui_MainWindow(object):
    camera = Camera() # create camera object
    mydb = Database() # create database object
    value_nomorpohon = 0 # value nomor pohon
    value_buahjatuh = 0 # value buah jatuh
    value_keputusan = "-" # value keputusan
    def setupUi(self, MainWindow) -> None:
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 438)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 10, 800, 480))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.Camera = QtWidgets.QLabel(self.page)
        self.Camera.setGeometry(QtCore.QRect(10, 0, 331, 211))
        self.Camera.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Camera.setFont(font)
        self.Camera.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.Camera.setAlignment(QtCore.Qt.AlignCenter)
        self.Camera.setObjectName("Camera")
        self.Camera_2 = QtWidgets.QLabel(self.page)
        self.Camera_2.setGeometry(QtCore.QRect(450, 0, 331, 211))
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
        self.label_9 = QtWidgets.QLabel(self.page)
        self.label_9.setGeometry(QtCore.QRect(540, 220, 141, 161))
        self.label_9.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.widget = QtWidgets.QWidget(self.page)
        self.widget.setGeometry(QtCore.QRect(10, 250, 141, 91))
        self.widget.setStyleSheet("background-position: center;\n"
"                background-repeat: no-repeat;\n"
"                background-attachment: fixed;\n"
"                background-clip: border;\n"
"                border-image: url(:/ITS LOGO/logo-its-biru-transparan.png) 20 20 20 20 stretch stretch;\n"
"                border-radius: 20px;")
        self.widget.setObjectName("widget")
        self.btn_processdecision = QtWidgets.QPushButton(self.page)
        self.btn_processdecision.setGeometry(QtCore.QRect(570, 330, 91, 41))
        self.btn_processdecision.setObjectName("btn_processdecision")
        self.val_nomorpohon = QtWidgets.QLabel(self.page)
        self.val_nomorpohon.setGeometry(QtCore.QRect(170, 320, 91, 41))
        self.val_nomorpohon.setAlignment(QtCore.Qt.AlignCenter)
        self.val_nomorpohon.setObjectName("val_nomorpohon")
        self.val_buahjatuh = QtWidgets.QLabel(self.page)
        self.val_buahjatuh.setGeometry(QtCore.QRect(430, 320, 91, 41))
        self.val_buahjatuh.setAlignment(QtCore.Qt.AlignCenter)
        self.val_buahjatuh.setObjectName("val_buahjatuh")
        self.label_8 = QtWidgets.QLabel(self.page)
        self.label_8.setGeometry(QtCore.QRect(160, 220, 111, 161))
        self.label_8.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.page)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(290, 230, 111, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_matang_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_matang_2.setObjectName("lbl_matang_2")
        self.verticalLayout_2.addWidget(self.lbl_matang_2)
        self.lbl_mentah_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_mentah_2.setObjectName("lbl_mentah_2")
        self.verticalLayout_2.addWidget(self.lbl_mentah_2)
        self.lbl_busuk_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_busuk_2.setObjectName("lbl_busuk_2")
        self.verticalLayout_2.addWidget(self.lbl_busuk_2)
        self.btn_showtableresult_2 = QtWidgets.QPushButton(self.page)
        self.btn_showtableresult_2.setGeometry(QtCore.QRect(690, 310, 91, 71))
        self.btn_showtableresult_2.setObjectName("btn_showtableresult_2")
        self.label_10 = QtWidgets.QLabel(self.page)
        self.label_10.setGeometry(QtCore.QRect(280, 220, 131, 161))
        self.label_10.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.resultdecision = QtWidgets.QLabel(self.page)
        self.resultdecision.setGeometry(QtCore.QRect(550, 280, 121, 31))
        self.resultdecision.setAlignment(QtCore.Qt.AlignCenter)
        self.resultdecision.setWordWrap(False)
        self.resultdecision.setObjectName("resultdecision")
        self.Capture = QtWidgets.QPushButton(self.page)
        self.Capture.setGeometry(QtCore.QRect(690, 220, 91, 81))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.Capture.setFont(font)
        self.Capture.setObjectName("Capture")
        self.label_7 = QtWidgets.QLabel(self.page)
        self.label_7.setGeometry(QtCore.QRect(420, 220, 111, 161))
        self.label_7.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.btn_nomorPohon = QtWidgets.QPushButton(self.page)
        self.btn_nomorPohon.setGeometry(QtCore.QRect(170, 230, 91, 81))
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
        self.label_2 = QtWidgets.QLabel(self.page)
        self.label_2.setGeometry(QtCore.QRect(560, 230, 91, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.btn_buahjatuh = QtWidgets.QPushButton(self.page)
        self.btn_buahjatuh.setEnabled(True)
        self.btn_buahjatuh.setGeometry(QtCore.QRect(430, 230, 91, 81))
        self.btn_buahjatuh.setCheckable(True)
        self.btn_buahjatuh.setObjectName("btn_buahjatuh")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.tableWidget = QtWidgets.QTableWidget(self.page_2)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 701, 361))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.btn_hidetableresult = QtWidgets.QPushButton(self.page_2)
        self.btn_hidetableresult.setGeometry(QtCore.QRect(720, 290, 71, 71))
        self.btn_hidetableresult.setObjectName("btn_hidetableresult")
        self.stackedWidget.addWidget(self.page_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Harvesting Sickle"))
        self.Camera.setText(_translate("MainWindow", "Camera"))
        self.Camera_2.setText(_translate("MainWindow", "Result Detection"))
        self.btn_processdecision.setText(_translate("MainWindow", "Submit"))
        self.val_nomorpohon.setText(_translate("MainWindow", "0"))
        self.val_buahjatuh.setText(_translate("MainWindow", "0"))
        self.lbl_matang_2.setText(_translate("MainWindow", "Matang : "))
        self.lbl_mentah_2.setText(_translate("MainWindow", "Mentah :"))
        self.lbl_busuk_2.setText(_translate("MainWindow", "Busuk    :"))
        self.btn_showtableresult_2.setText(_translate("MainWindow", "Show Table"))
        self.resultdecision.setText(_translate("MainWindow", "Result Decision"))
        self.Capture.setText(_translate("MainWindow", "Capture"))
        self.btn_nomorPohon.setText(_translate("MainWindow", "Input \n"
"Number \n"
"of Tree"))
        self.label_2.setText(_translate("MainWindow", "Decision"))
        self.btn_buahjatuh.setText(_translate("MainWindow", "Input \n"
"Fruit \n"
"Drop\n"
"(Brondolan)"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Number Tree"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Matang"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Mentah"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Busuk"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Buah Jatuh"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Keputusan"))
        self.btn_hidetableresult.setText(_translate("MainWindow", "Hide \n"
"Table"))
        
        
        
        
        #action is clicked
        
        self.btn_processdecision.clicked.connect(self.makeDecision)
        self.btn_showtableresult_2.clicked.connect(self.changetotable)
        self.btn_hidetableresult.clicked.connect(self.changetomain)
        self.btn_nomorPohon.clicked.connect(self.nomorpohon_push_button_clicked)
        self.btn_buahjatuh.clicked.connect(self.buahjatuh_push_button_clicked)
        self.Capture.clicked.connect(self.capture_image) # connect signal to slot
        
        self.camera.frameCaptured.connect(self.update_image) # connect signal to slot
        self.camera.start()
        
    # event show numpad to nomor pohon
    def nomorpohon_push_button_clicked(self) -> None:
        self.MainWindow.setEnabled(False)
        self.exPopup = numberPopup(self.MainWindow,self.val_nomorpohon, "", self.nomorpohon_callBackOnSubmit, "Argument 1", "Argument 2")
        self.exPopup.setGeometry(0, 0,400, 300)
        self.exPopup.show()
    def nomorpohon_onClick(self,e) -> None:
        self.MainWindow.setEnabled(True)
    def nomorpohon_callBackOnSubmit(self, arg1, arg2,data)->None:
        self.value_nomorpohon = data
    # event show numpad to buah jatuh
    def buahjatuh_push_button_clicked(self) -> None:
        self.MainWindow.setEnabled(False)
        self.exPopup = numberPopup(self.MainWindow,self.val_buahjatuh, "", self.buahjatuh_callBackOnSubmit, "Argument 1", "Argument 2")
        self.exPopup.setGeometry(0, 0,400, 300)
        self.exPopup.show()
    def buahjatuh_onClick(self,e) -> None:
        self.MainWindow.setEnabled(True)
    def buahjatuh_callBackOnSubmit(self, arg1, arg2,data) -> None:
        self.value_buahjatuh = data
        self.buahjatuh_classification(data)
    
    #clasification kematangan
    def buahjatuh_classification(self,data) -> None:
        if int(data) >= 10:
            self.value_keputusan = "matang"
        elif int(data) < 10:
            self.value_keputusan = "mentah"
  
    # Show UI to Image
    def showToUI(self,frame, label) -> None:
        pixmap = QPixmap.fromImage(frame)
        pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
    #Update Image Realtime from Camera to UI
    def update_image(self, frame) -> None:
        self.showToUI(frame,self.Camera)
    # Function Event Onclick
    def capture_image(self) -> None:
        image = self.camera.inference_yolo()
        self.showResultDetection()
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert frame to RGB
        h, w, ch = frame.shape # get frame shape
        bytesPerLine = ch * w
        convert_to_qt_format = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888) # convert frame to QImage
        p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio) # scale image
        self.showToUI(p,self.Camera_2)
    # Show Result Detection to Label
    def showResultDetection(self)->None:
        # busuk 0, matang 1, mentah 2
        self.lbl_busuk_2.setText("Busuk    : "+str(self.camera.datajumlahterdeteksi[0]))
        self.lbl_matang_2.setText("Matang : "+str(self.camera.datajumlahterdeteksi[1]))
        self.lbl_mentah_2.setText("Mentah : "+str(self.camera.datajumlahterdeteksi[2]))
        pass
    
    def changetotable(self)->None:
        self.stackedWidget.setCurrentIndex(1)
    def changetomain(self)->None:
        self.stackedWidget.setCurrentIndex(0)
        
    # sumbit decision
    def makeDecision(self) -> None:
        keputusankamera = ""
        #mencari nilai tertinggi di array data jumlah terdeteksi
        max_value = max(self.camera.datajumlahterdeteksi)
        #mencari index nilai tertinggi di array data jumlah terdeteksi
        max_index = self.camera.datajumlahterdeteksi.index(max_value)
        #mencari data keputusan
        if max_index == 0:
            keputusankamera = "busuk"
        elif max_index == 1:
            keputusankamera = "matang"
        elif max_index == 2:
            keputusankamera = "mentah"
            
        if keputusankamera == self.value_keputusan:
            self.value_keputusan = "Siap Panen"
        else:
            self.value_keputusan = "Tidak Siap Panen"
        self.resultdecision.setText(self.value_keputusan)
            
        self.mydb.add_record(numbertree=self.value_nomorpohon,matang= self.camera.datajumlahterdeteksi[1], mentah=self.camera.datajumlahterdeteksi[2], busuk=self.camera.datajumlahterdeteksi[0], buahjatuh=self.value_buahjatuh, keputusan=self.value_keputusan)
        array = []
        self.mydb.view_records(array)
        self.tableWidget.setColumnCount(len(array[0]))
        self.tableWidget.setRowCount(len(array))
        for i, row in enumerate(array):
            for j, item in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))
        self.camera.datajumlahterdeteksi = [0,0,0]
        self.value_buahjatuh = self.value_nomorpohon = 0
        self.value_keputusan = "-"
        self.lbl_busuk_2.setText("Busuk    : 0")
        self.lbl_matang_2.setText("Matang : 0")
        self.lbl_mentah_2.setText("Mentah : 0")
        self.val_nomorpohon.setText("0")
        self.val_buahjatuh.setText("0")
        # self.resultdecision.setText("Result Decision")
        pass

def main() -> None:
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    
    # MainWindow.showMaximized()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
            
if __name__ == "__main__":
    main()
    

