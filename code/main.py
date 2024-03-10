from egrekdigitalv2 import Ui_MainWindow
from PyQt5 import QtWidgets 

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import numpy as np
from dotenv import load_dotenv
import sqlite3
import os
import cv2
import torch
load_dotenv("/home/alldone/Desktop/sawit-yolo/.env")

# show no image
no_image = cv2.imread("/home/alldone/Desktop/sawit-yolo/image/No_Image.png")
ModelYolo = os.getenv("MODEL_YOLO")
PathYolo = os.getenv("PATH_YOLO")
CameraRealtime = os.getenv("CAMERA_YOLO")
print("Use Model: " + str(ModelYolo)+"\nYolo Path: "+str(PathYolo)+"\nID Camera: "+str(CameraRealtime))

class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('logging.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tb_data (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                numtree INTEGER,
                                overripe INTEGER,
                                ripe INTEGER,
                                underripe INTEGER,
                                brondolan INTEGER,
                                decision TEXT
                            )''')
        self.conn.commit()

    def add_record(self, numtree, brondolan, decision, overripe=0, ripe=0, underripe=0) -> None:
        self.cursor.execute("INSERT INTO tb_data (numtree, overripe, ripe, underripe, brondolan, decision) VALUES (?, ?, ?, ?, ?, ?)",
                            (numtree, overripe, ripe, underripe, brondolan, decision))
        self.conn.commit()

    def view_records(self, array) -> None:
        self.cursor.execute("SELECT * FROM tb_data ORDER BY id DESC")
        rows = self.cursor.fetchall()
        for row in rows:
            array.append(row)

    def delete_record(self, numtree) -> None:
        self.cursor.execute("DELETE FROM tb_data WHERE numtree = ?", (numtree,))
        self.conn.commit()
        
class Camera(QThread):
    frameCaptured = pyqtSignal(np.ndarray)
    image = None
    def __init__(self)->None:
        super().__init__()
        # self.cam = cv2.VideoCapture(int(CameraRealtime))
        self.cam = cv2.VideoCapture(0)
        
        pass
    
    def run(self)->None:
        while True:
            
            ret, frame = self.cam.read()
            # ret, frame = True,cv2.imread("/home/alldone/Desktop/sawit-yolo/image/palmoil_oilpalm_palmoil.webp")
            # ret, frame = True,cv2.imread("/home/alldone/Desktop/sawit-yolo/image/sawit.jpg")
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert frame to RGB 
            self.image = frame
            self.frameCaptured.emit(frame)

class Inference:
    def __init__(self):
        
        self.model = torch.hub.load(r'../yolov5', 'custom', path=ModelYolo, source='local',
                        force_reload=True, device='cpu')
        self.model.conf = 0.7
        self.model.line_thickness = 1
    def inference_yolo(self,frame) -> None:
        cv2.resize(frame, (640, 480))
        self.results = self.model(frame)
        self.tag = self.results.names
        self.datajumlahterdeteksi = [0,0,0]
        for i in self.results.xyxy[0]:
            self.datajumlahterdeteksi[int(i[5])] = self.datajumlahterdeteksi[int(i[5])] + 1
        cv_img = np.squeeze(self.results.render())
        return cv_img
    pass

class Mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    camera = Camera() # create camera object
    Inference = Inference() # create inference object
    Database = Database() # create database object
    __lbl_take = 1
    
    # isi array kedepannya memiliki kategori overripe,ripe,underripe,captured
    __result_captured_detection = [no_image,no_image,no_image,no_image]
    __result_camera_detection = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    def __set_lbl_take(self, value):
        
        self.lbl_resultdetection.setText("OverRipe :  "+str(self.__result_camera_detection[value-1][0])+
"\nRipe : "+ str(self.__result_camera_detection[value-1][1])+
"\nUnderRipe :"+ str(self.__result_camera_detection[value-1][2]))
        self.__lbl_take = value
        self.lbl_take.setText("Take "+str(value))
        self.__show_image(self.__result_captured_detection[value-1],self.disp_result)
        
    
        
    def __show_image(self, frame,window):
        h, w, ch = frame.shape # get frame shape
        bytesPerLine = ch * w # get bytes per line
        convert_to_qt_format = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888) # convert frame to QImage
        p = convert_to_qt_format.scaled(299, 269, Qt.KeepAspectRatio) # scale image
        pixmap = QPixmap.fromImage(p) # set image to pixmap
        window.setPixmap(pixmap)
        
    
    def __init__(self):
        super(Mywindow, self).__init__()
        self.setupUi(self)
        self.tbl_data.horizontalHeader().setVisible(True)
        self.lbl_resultdetection.setText("OverRipe :  "+str(self.__result_camera_detection[self.__lbl_take-1][0])+
"\nRipe : "+ str(self.__result_camera_detection[self.__lbl_take-1][1])+
"\nUnderRipe :"+ str(self.__result_camera_detection[self.__lbl_take-1][2]))
        self.btn_submittodecision.clicked.connect(self.make_decision)
        self.btn_shut_1.clicked.connect(lambda: self.__set_lbl_take(1))
        self.btn_shut_2.clicked.connect(lambda: self.__set_lbl_take(2))
        self.btn_shut_4.clicked.connect(lambda: self.__set_lbl_take(4))
        self.btn_shut_3.clicked.connect(lambda: self.__set_lbl_take(3))
        self.btn_nextpage1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_back2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_back3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_backtodetection.clicked.connect(lambda: self.reset_all_detection())
        self.btn_showtable.clicked.connect(lambda: self.show_table())
        self.btn_capture.clicked.connect(self.btn_capture_clicked)
        self.camera.frameCaptured.connect(lambda: self.__show_image(self.camera.image,self.disp_camera))
        self.camera.start()
    def reset_all_detection(self):
        self.value_keputusan = ""
        self.lbl_resultdecision.setText("")
        
        self.lbl_resultdecision.setStyleSheet("background-color: white;")
        self.lbl_resultdecision.setText("")
        self.sbox_inputbrondolan.setValue(0)
        self.sbox_inputnumbertree.setValue(0)
        self.__result_captured_detection = [no_image,no_image,no_image,no_image]
        self.__result_camera_detection = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.resultalldetection = [0,0,0]
        self.__lbl_take = 1
        self.lbl_take.setText("Take "+str(self.__lbl_take))
        self.__show_image(self.__result_captured_detection[self.__lbl_take-1],self.disp_result)
        self.lbl_resultdetection.setText("OverRipe :  "+str(self.__result_camera_detection[self.__lbl_take-1][0])+
"\nRipe : "+ str(self.__result_camera_detection[self.__lbl_take-1][1])+
"\nUnderRipe :"+ str(self.__result_camera_detection[self.__lbl_take-1][2]))
        
        self.lbl_resultdetection_3.setText("OverRipe :  "+str(self.resultalldetection[0])+
"\nRipe : "+str(self.resultalldetection[1])+
"\nUnderRipe :"+str(self.resultalldetection[2]))
        self.stackedWidget.setCurrentIndex(0)
        
        
    def show_table(self):
        mytbl = []
        self.Database.view_records(mytbl)
        self.tbl_data.setColumnCount(len(mytbl[0]))
        self.tbl_data.setRowCount(len(mytbl))
        
        for i, row in enumerate(mytbl):
            for j, item in enumerate(row):
                self.tbl_data.setItem(i, j, QTableWidgetItem(str(item)))
        self.stackedWidget.setCurrentIndex(2)
        
    
    def make_decision(self) -> None:
        #kalsifikasi hasil panen
        keaadaan_buah = ["OverRipe", "Ripe", "UnderRipe", "NoFruit","input brondolan tidak boleh 0"]
        self.buahjatuh_classification(self.sbox_inputbrondolan.value())
        keputusan_panen = self.value_keputusan
        # print(self.resultalldetection)
        if (self.resultalldetection == [0, 0, 0]):
            self.value_keputusan = "NoFruit"
        else:
            # mengambil nilai tertinggi dari hasil deteksi
            max_index = self.resultalldetection.index(max(self.resultalldetection))
            
            if keaadaan_buah.index(keputusan_panen) <= 1 and max_index <= 1:
                self.value_keputusan = "Siap Panen"
            elif keaadaan_buah.index(keputusan_panen) == 2 and max_index == 2:
                self.value_keputusan = "Tunda Panen"
            else:  
                self.value_keputusan = "Tunda Panen"    
        
        if self.value_keputusan == "Tunda Panen":
            self.lbl_resultdecision.setStyleSheet("background-color: red;")
            self.Database.add_record(self.sbox_inputnumbertree.value(), self.sbox_inputbrondolan.value(), self.value_keputusan, self.resultalldetection[0], self.resultalldetection[1], self.resultalldetection[2])
        elif self.value_keputusan == "Siap Panen":
            self.lbl_resultdecision.setStyleSheet("background-color: green;")
            self.Database.add_record(self.sbox_inputnumbertree.value(), self.sbox_inputbrondolan.value(), self.value_keputusan, self.resultalldetection[0], self.resultalldetection[1], self.resultalldetection[2])
        else:
            self.lbl_resultdecision.setStyleSheet("background-color: white;")
        
        self.lbl_resultdecision.setText(self.value_keputusan)
        
    def buahjatuh_classification(self,data) -> None:
        if int(data) > 10:
            self.value_keputusan = "OverRipe"
        elif int(data) == 10:
            self.value_keputusan = "Ripe"
        elif int(data) == 0:
            self.value_keputusan = "input brondolan tidak boleh 0"
        elif int(data) < 10:
            self.value_keputusan = "UnderRipe"
            
    resultalldetection = [0,0,0]        
        
    def btn_capture_clicked(self):
        save_captured_from_inference = self.Inference.inference_yolo(self.camera.image)
        self.__show_image(save_captured_from_inference,self.disp_result)
        # save index from category
        
        self.lbl_resultdetection.setText("OverRipe :  "+ str(self.Inference.datajumlahterdeteksi[0])+
"\nRipe : "+ str(self.Inference.datajumlahterdeteksi[1])+
"\nUnderRipe :"+ str(self.Inference.datajumlahterdeteksi[2]))
        self.__result_captured_detection[self.__lbl_take-1] = save_captured_from_inference
        # save result detection
        self.__result_camera_detection[self.__lbl_take-1] = self.Inference.datajumlahterdeteksi
        #sum all detection
        self.resultalldetection = np.sum(self.__result_camera_detection, axis=0).tolist()
        
        self.lbl_resultdetection_3.setText("OverRipe :  "+ str(self.resultalldetection[0])+
"\nRipe : "+str(self.resultalldetection[1])+
"\nUnderRipe :"+str(self.resultalldetection[2]))


def main() -> None:
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Mywindow()
    MainWindow.show()
    sys.exit(app.exec_())
            
if __name__ == "__main__":
    main()