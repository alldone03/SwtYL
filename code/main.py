# Mengimpor kelas Ui_MainWindow dari modul egrekdigitalv2
from egrekdigitalv2 import Ui_MainWindow

# Mengimpor modul QtWidgets dari PyQt5
from PyQt5 import QtWidgets  

# Mengimpor kelas QTableWidgetItem dari modul QtWidgets di PyQt5
from PyQt5.QtWidgets import QTableWidgetItem 

# Mengimpor kelas QImage dan QPixmap dari modul QtGui di PyQt5
from PyQt5.QtGui import QImage, QPixmap 

# Mengimpor kelas QThread, pyqtSignal, dan Qt dari modul QtCore di PyQt5
from PyQt5.QtCore import QThread, pyqtSignal, Qt ,QTranslator ,QCoreApplication

# Mengimpor kelas QLocale dari modul QtCore di PyQt5
from PyQt5 import QtCore

# Mengimpor pustaka numpy dan menamainya sebagai np
import numpy as np 

# Mengimpor fungsi load_dotenv dari pustaka dotenv
from dotenv import load_dotenv 

# Mengimpor modul sqlite3 untuk berinteraksi dengan database SQLite
import sqlite3 

# Mengimpor modul os untuk berinteraksi dengan sistem operasi
import os 

# Mengimpor pustaka OpenCV (cv2) untuk pengolahan gambar
import cv2 

# Mengimpor pustaka PyTorch untuk komputasi tensor dan pembelajaran mesin
import torch 

# Mengimpor modul math untuk fungsi-fungsi matematika dasar
import math 

# Mengimpor kelas numberPopup dari modul number_pad
from lib.number_pad import numberPopup


import time


# Memuat variabel lingkungan dari file .env yang terletak di /home/alldone/Desktop/sawit-yolo/.env
load_dotenv("./.env")

# show no image
no_image = cv2.imread("./image/No_Image.png")
ModelYolo = os.getenv("MODEL_YOLO")
PathYolo = os.getenv("PATH_YOLO")
CameraRealtime = os.getenv("CAMERA_YOLO")
print("Use Model: " + str(ModelYolo)+"\nYolo Path: "+str(PathYolo)+"\nID Camera: "+str(CameraRealtime))

class Database:
    def __init__(self) -> None:
        """
        Inisialisasi objek Database.
        
        - Membuat koneksi ke database SQLite dengan nama 'logging.db'.
        - Membuat cursor untuk eksekusi perintah SQL.
        - Membuat tabel 'tb_data' jika belum ada.
        """
        self.conn = sqlite3.connect('logging.db')  # Membuat koneksi ke database
        self.cursor = self.conn.cursor()  # Membuat cursor untuk eksekusi perintah SQL
        
        # Membuat tabel 'tb_data' jika belum ada
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tb_data (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                numtree INTEGER,
                                overripe INTEGER,
                                ripe INTEGER,
                                underripe INTEGER,
                                brondolan INTEGER,
                                decision TEXT
                            )''')
        self.conn.commit()  # Melakukan commit perubahan ke database

    def add_record(self, numtree, brondolan, decision, overripe=0, ripe=0, underripe=0) -> None:
        """
        Menambahkan record baru ke tabel 'tb_data'.
        
        Args:
            numtree (int): Jumlah pohon.
            brondolan (int): Jumlah brondolan.
            decision (str): Keputusan terkait.
            overripe (int): Jumlah buah yang terlalu matang (default 0).
            ripe (int): Jumlah buah yang matang (default 0).
            underripe (int): Jumlah buah yang belum matang (default 0).
        """
        # Menjalankan perintah SQL untuk menambahkan record baru
        self.cursor.execute("INSERT INTO tb_data (numtree, overripe, ripe, underripe, brondolan, decision) VALUES (?, ?, ?, ?, ?, ?)",
                            (numtree, overripe, ripe, underripe, brondolan, decision))
        self.conn.commit()  # Melakukan commit perubahan ke database

    def view_records(self, array) -> None:
        """
        Melihat semua record yang ada dalam tabel 'tb_data' dan menyimpannya ke dalam array.
        
        Args:
            array (list): Array untuk menyimpan record-record.
        """
        # Menjalankan perintah SQL untuk mengambil semua record
        self.cursor.execute("SELECT numtree, overripe, ripe, underripe, brondolan, decision FROM tb_data ORDER BY id DESC")
        rows = self.cursor.fetchall()  # Mendapatkan semua hasil
        for row in rows:
            array.append(row)  # Menambahkan record ke dalam array

    def delete_record(self, numtree) -> None:
        """
        Menghapus record dari tabel 'tb_data' berdasarkan 'numtree'.
        
        Args:
            numtree (int): Jumlah pohon yang terkait dengan record yang ingin dihapus.
        """
        # Menjalankan perintah SQL untuk menghapus record berdasarkan numtree
        self.cursor.execute("DELETE FROM tb_data WHERE numtree = ?", (numtree,))
        self.conn.commit()  # Melakukan commit perubahan ke database
        
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
            
            # ret, frame = True,cv2.imread("/home/alldone/Desktop/sawit-yolo/image/palmoil_oilpalm_palmoil.webp")
            # ret, frame = True,cv2.imread("/home/alldone/Desktop/sawit-yolo/image/sawit.jpg")
            # ret, frame = True,cv2.imread("/home/alldone/Desktop/sawit-yolo/image/sawit2.jpg")
            # ret, frame = True,cv2.imread("/home/alldone/Desktop/sawit-yolo/image/sawit3.jpg")
            # ret, frame = True,cv2.imread("/home/alldone/Desktop/sawit-yolo/image/sawit4.jpg")
            # ret, frame = True,cv2.imread("/home/alldone/Desktop/sawit-yolo/image/sawit6.png")
            # ret, frame = True,cv2.imread("/home/alldone/Desktop/sawit-yolo/image/sawit.webp")
            # ret, frame = True,cv2.imread("/home/alldone/Desktop/sawit-yolo/image/sawit.jpg")
            ret, frame = self.cam.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert frame to RGB 
            self.image = frame
            self.frameCaptured.emit(frame)

class Inference:
    datajumlahterdeteksi = [0, 0, 0]
    def __init__(self):
        """
        Inisialisasi objek Inference.
        
        Args:
            ModelYolo (str): Path ke model YOLOv5 yang akan digunakan.
        """
        # Memuat model YOLOv5 dari path yang diberikan
        self.model = torch.hub.load(r'../yolov5', 'custom', path=str(ModelYolo), source='local', force_reload=True, device='cpu')
        
        # Mengatur threshold confidence model YOLOv5
        self.model.conf = 0.8
        
        # Mengatur ketebalan garis untuk bingkai objek yang terdeteksi
        self.model.line_thickness = 1

    def inference_yolo(self, frame) -> None:
        """
        Melakukan inferensi dengan model YOLOv5 pada frame gambar.
        
        Args:
            frame (numpy.ndarray): Frame gambar input untuk dilakukan inferensi.
            
        Returns:
            numpy.ndarray: Frame gambar dengan objek yang terdeteksi diberi bingkai.
        """
        start_time = time.time()
        # Mengubah ukuran frame gambar menjadi 640x480
        cv2.resize(frame, (640, 480))
        
        # Melakukan inferensi dengan model YOLOv5 pada frame gambar
        self.results = self.model(frame)
        
        # Mendapatkan label kelas dari model YOLOv5
        self.tag = self.results.names
        
        # Inisialisasi variabel jumlah terdeteksi untuk setiap kelas
        self.datajumlahterdeteksi = [0, 0, 0]
        
        # Inisialisasi variabel untuk menyimpan indeks bounding box terbesar
        initial_biggest_bbox = 0
        find_index_biggest_bbox = 0
        
        # Iterasi melalui setiap bounding box yang terdeteksi
        for num, i in enumerate(self.results.xyxy[0]):
            # Mencari bounding box terbesar dengan menggunakan Euclidean Distance
            if initial_biggest_bbox < math.sqrt((i[2]-i[0])**2 + (i[3]-i[1])**2):
                initial_biggest_bbox = math.sqrt((i[2]-i[0])**2 + (i[3]-i[1])**2)
                find_index_biggest_bbox = num
        
        # Menambahkan jumlah terdeteksi untuk kelas yang sesuai dengan bounding box terbesar
        try:
            self.datajumlahterdeteksi[int(self.results.xyxy[0][find_index_biggest_bbox][5])] += 1
            x1, y1, x2, y2 = int(self.results.xyxy[0][find_index_biggest_bbox][0]), int(self.results.xyxy[0][find_index_biggest_bbox][1]), int(self.results.xyxy[0][find_index_biggest_bbox][2]), int(self.results.xyxy[0][find_index_biggest_bbox][3])
        except:
            x1, y1, x2, y2 = 0, 0, 0, 0
        
        # Membuat salinan frame gambar dengan objek yang terdeteksi diberi bingkai
        cv_img = np.squeeze(self.results.render())
        cv2.line(cv_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        print("Inference Time: ", (time.time()-start_time)* 10**3,"ms")
        return cv_img

class MainWindowUI(QtWidgets.QMainWindow, Ui_MainWindow):
    camera = Camera() # create camera object
    Inference = Inference() # create inference object
    Database = Database() # create database object
    # numpad = numberPopup()
    __lbl_take = 1
    
    
    def setupUi(self):
        super().setupUi(self)
        self.retranslateUi(self)
        
        
    # isi array kedepannya memiliki kategori overripe,ripe,underripe,captured
    __result_captured_detection = [no_image,no_image,no_image,no_image]
    __result_camera_detection = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    def __set_lbl_take(self, value):
        
        self.lbl_resultdetection.setText(
            "Terlalu Matang :%s  \n" "Matang :%s \n" "Belum Matang :%s"%(self.__result_camera_detection[value-1][0],self.__result_camera_detection[value-1][1],self.__result_camera_detection[value-1][2]) if self.select_language.currentIndex() == 1 else "OverRipe :%s  \n" "Ripe :%s \n" "UnderRipe :%s"%(self.__result_camera_detection[value-1][0],self.__result_camera_detection[value-1][1],self.__result_camera_detection[value-1][2])
            )
        self.__lbl_take = value
        self.lbl_take.setText(("Take " if self.select_language.currentIndex() != 1 else "Ambil ")+str(value))
        self.__show_image(self.__result_captured_detection[value-1],self.disp_result)
        
    
        
    def __show_image(self, frame,window):
        h, w, ch = frame.shape # get frame shape
        bytesPerLine = ch * w # get bytes per line
        convert_to_qt_format = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888) # convert frame to QImage
        p = convert_to_qt_format.scaled(299, 269, Qt.KeepAspectRatio) # scale image
        pixmap = QPixmap.fromImage(p) # set image to pixmap
        window.setPixmap(pixmap) # set pixmap to label
        
    # inisialisasi semua variabel
    def __init__(self,MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        self.setupUi()
        self.tbl_data.horizontalHeader().setVisible(True)
        self.lbl_resultdetection.setText(
            "Terlalu Matang :%s  \n" "Matang :%s \n" "Belum Matang :%s"%(self.__result_camera_detection[self.__lbl_take-1][0],self.__result_camera_detection[self.__lbl_take-1][1],self.__result_camera_detection[self.__lbl_take-1][2]) if self.select_language.currentIndex() == 1 else "OverRipe :%s  \n" "Ripe :%s \n" "UnderRipe :%s"%(self.__result_camera_detection[self.__lbl_take-1][0],self.__result_camera_detection[self.__lbl_take-1][1],self.__result_camera_detection[self.__lbl_take-1][2])
            )
        self.btn_submittodecision.clicked.connect(self.make_decision)
        self.btn_shut_1.clicked.connect(lambda: self.__set_lbl_take(1))
        self.btn_shut_2.clicked.connect(lambda: self.__set_lbl_take(2))
        self.btn_shut_3.clicked.connect(lambda: self.__set_lbl_take(3))
        self.btn_shut_4.clicked.connect(lambda: self.__set_lbl_take(4))
        self.btn_nextpage1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_back2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_back3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_backtodetection.clicked.connect(lambda: self.reset_all_detection())
        self.select_language.currentIndexChanged.connect(lambda: self.change_language())
        self.btn_showtable.clicked.connect(lambda: self.show_table())
        self.btn_capture.clicked.connect(self.btn_capture_clicked)
        self.camera.frameCaptured.connect(lambda: self.__show_image(self.camera.image,self.disp_camera))
        self.camera.start()
        self.btn_shownumpad_numtree.clicked.connect(lambda: self.show_numpad_numbertree())
        self.btn_shownumpad_inputbrondolan.clicked.connect(lambda: self.show_numpad_brondolan())
    
    #show Numpad 
    def show_numpad_numbertree(self):
        self.MainWindow.setEnabled(False)
        self.exPopup = numberPopup(self.MainWindow,0, "", self.callBackOnSubmit_numbertree , "Argument 1", "Argument 2")
        self.exPopup.setGeometry(0, 0,400, 300)
        self.exPopup.show()
        pass
    def show_numpad_brondolan(self):
        self.MainWindow.setEnabled(False)
        self.exPopup = numberPopup(self.MainWindow,0, "", self.callBackOnSubmit_brondolan , "Argument 1", "Argument 2")
        self.exPopup.setGeometry(0, 0,400, 300)
        self.exPopup.show()
        pass
    def callBackOnSubmit_numbertree(self, arg1, arg2,data)->None:
        self.sbox_inputnumbertree.setValue(int(0 if data == 0 else data))
        
    def callBackOnSubmit_brondolan(self, arg1, arg2,data)->None:
        self.sbox_inputbrondolan.setValue(int(0 if data == 0 else data))
    
    #change language
    def change_language(self):
        self.reset_all_detection()
        self.retranslateUi(self)
        
    #reset all detection
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
        self.lbl_resultdetection.setText(
            "Terlalu Matang :%s  \n" "Matang :%s \n" "Belum Matang :%s"%(self.__result_camera_detection[self.__lbl_take-1][0],self.__result_camera_detection[self.__lbl_take-1][1],self.__result_camera_detection[self.__lbl_take-1][2]) if self.select_language.currentIndex() == 1 else "OverRipe :%s  \n" "Ripe :%s \n" "UnderRipe :%s"%(self.__result_camera_detection[self.__lbl_take-1][0],self.__result_camera_detection[self.__lbl_take-1][1],self.__result_camera_detection[self.__lbl_take-1][2])
            )
        self.lbl_resultdetection_3.setText(
            "Terlalu Matang :%s  \n" "Matang :%s \n" "Belum Matang :%s"%(self.resultalldetection[0],self.resultalldetection[1],self.resultalldetection[2]) if self.select_language.currentIndex() == 1 else "OverRipe :%s  \n" "Ripe :%s \n" "UnderRipe :%s"%(self.resultalldetection[0],self.resultalldetection[1],self.resultalldetection[2])
            )
        self.stackedWidget.setCurrentIndex(0)
        
    # plot data to table
    def show_table(self):
        
        mytbl = []
        self.Database.view_records(mytbl)
        try:
            self.tbl_data.setColumnCount(len(mytbl[0]))
            self.tbl_data.setRowCount(len(mytbl))
            
            for i, row in enumerate(mytbl):
                for j, item in enumerate(row):
                    if j == 5:
                        self.tbl_data.setItem(i, j, QTableWidgetItem(str(item if self.select_language.currentIndex() == 1 else "Ready" if item == "Siap Panen" else "Unready")))
                    else:
                        self.tbl_data.setItem(i, j, QTableWidgetItem(str(item)))
        except:
            pass
                
        self.stackedWidget.setCurrentIndex(2)
    
    
    def make_decision(self) -> None:
        #kalsifikasi hasil panen
        #cek apakah hasil deteksi ada atau tidak
        if (self.resultalldetection == [0, 0, 0] or self.sbox_inputbrondolan.value() == 0):
            self.value_keputusan = "NoFruit"
        else:
            # mengambil nilai tertinggi dari hasil deteksi
            max_index = self.resultalldetection.index(max(self.resultalldetection))
            if self.buahjatuh_classification(self.sbox_inputbrondolan.value()) <= 1 and max_index <= 1:
                self.value_keputusan = "Siap Panen"
            elif self.buahjatuh_classification(self.sbox_inputbrondolan.value()) == 2 and max_index == 2:
                self.value_keputusan = "Tunda Panen"
            else:  
                self.value_keputusan = "Tunda Panen"    
        #menampilkan hasil keputusan
        if self.value_keputusan == "Tunda Panen":
            self.lbl_resultdecision.setStyleSheet("background-color: red;")
            self.Database.add_record(self.sbox_inputnumbertree.value(), self.sbox_inputbrondolan.value(), self.value_keputusan, self.resultalldetection[0], self.resultalldetection[1], self.resultalldetection[2])
        elif self.value_keputusan == "Siap Panen":
            self.lbl_resultdecision.setStyleSheet("background-color: green;")
            self.Database.add_record(self.sbox_inputnumbertree.value(), self.sbox_inputbrondolan.value(), self.value_keputusan, self.resultalldetection[0], self.resultalldetection[1], self.resultalldetection[2])
        else:
            self.lbl_resultdecision.setStyleSheet("background-color: white;")
        
        self.lbl_resultdecision.setText(self.value_keputusan if self.select_language.currentIndex() == 1 else "Ready" if self.value_keputusan == "Siap Panen" else "NoFruit" if self.value_keputusan == "NoFruit" else "Unready")
    
    # klasifikasi buah jatuh
    def buahjatuh_classification(self,data) -> None:
        # keterangan index keputusan = 0 : terlalu matang, 1 : matang, 2 : belum matang, 3 : tidak ada buah
        keputusan = None
        if int(data) > 10:
            keputusan = 0
        elif int(data) == 10:
            keputusan = 1
        elif int(data) == 0:
            keputusan = 2
        elif int(data) < 10:
            keputusan = 3
        return keputusan
          
          
    
    resultalldetection = [0,0,0]  
    save_captured_from_inference = None   
    # capture image from camera   
    def btn_capture_clicked(self):
        self.save_captured_from_inference = self.Inference.inference_yolo(self.camera.image)
        self.__show_image(self.save_captured_from_inference,self.disp_result)
        # save index from category
        self.lbl_resultdetection.setText(
            "Terlalu Matang :%s  \n" "Matang :%s \n" "Belum Matang :%s"%(self.Inference.datajumlahterdeteksi[0],self.Inference.datajumlahterdeteksi[1],self.Inference.datajumlahterdeteksi[2]) if self.select_language.currentIndex() == 1 else "OverRipe :%s  \n" "Ripe :%s \n" "UnderRipe :%s"%(self.Inference.datajumlahterdeteksi[0],self.Inference.datajumlahterdeteksi[1],self.Inference.datajumlahterdeteksi[2])
            )
        self.__result_captured_detection[self.__lbl_take-1] = self.save_captured_from_inference
        # save result detection
        self.__result_camera_detection[self.__lbl_take-1] = self.Inference.datajumlahterdeteksi
        #sum all detection
        self.resultalldetection = np.sum(self.__result_camera_detection, axis=0).tolist()
        
        self.lbl_resultdetection_3.setText(
            "Terlalu Matang :%s  \n" "Matang :%s \n" "Belum Matang :%s"%(self.resultalldetection[0],self.resultalldetection[1],self.resultalldetection[2]) if self.select_language.currentIndex() == 1 else "OverRipe :%s  \n" "Ripe :%s \n" "UnderRipe :%s"%(self.resultalldetection[0],self.resultalldetection[1],self.resultalldetection[2])
        )
    
    # translate all text
    def retranslateUi(self, MainWindow):
        super().retranslateUi(self)
        if (self.select_language.currentIndex() == 1):
            self.save_captured_from_inference = None
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "Egrek Digital"))
            self.label_2.setText(_translate("MainWindow", "Ambil"))
            self.btn_shut_1.setText(_translate("MainWindow", "1"))
            self.btn_shut_2.setText(_translate("MainWindow", "2"))
            self.btn_shut_3.setText(_translate("MainWindow", "3"))
            self.btn_shut_4.setText(_translate("MainWindow", "4"))
            self.btn_capture.setText(_translate("MainWindow", "AMBIL"))
            self.btn_nextpage1.setText(_translate("MainWindow", "Halaman Berikutnya"))
            self.label.setText(_translate("MainWindow", "Hasil Deteksi Kamera"))
            self.lbl_take.setText(_translate("MainWindow", "Ambil %s"%(self.__lbl_take)))
            
            self.lbl_resultdetection.setText(
                "Terlalu Matang :%s  \n" "Matang :%s \n" "Belum Matang :%s"%(0,0,0) if self.select_language.currentIndex() == 1 else "OverRipe :%s  \n" "Ripe :%s \n" "UnderRipe :%s"%(0,0,0)
                )
            
            (self.disp_result.setText(_translate("MainWindow", "Hasil")) if self.select_language.currentIndex() == 1 else self.disp_result.setText(_translate("MainWindow", "Result"))) if self.save_captured_from_inference is None else self.__show_image(self.save_captured_from_inference,self.disp_result)
            
            self.disp_camera.setText(_translate("MainWindow", "KAMERA"))
            self.select_language.setItemText(0, _translate("MainWindow", "Inggris"))
            self.select_language.setItemText(1, _translate("MainWindow", "Indonesia"))
            self.label_3.setText(_translate("MainWindow", "Hasil Semua Deteksi Kamera"))
            self.lbl_resultdetection_3.setText(
            "Terlalu Matang :%s  \n" "Matang :%s \n" "Belum Matang :%s"%(self.resultalldetection[0],self.resultalldetection[1],self.resultalldetection[2]) if self.select_language.currentIndex() == 1 else "OverRipe :%s  \n" "Ripe :%s \n" "UnderRipe :%s"%(self.resultalldetection[0],self.resultalldetection[1],self.resultalldetection[2]))
            
            self.btn_back2.setText(_translate("MainWindow", "KEMBALI"))
            self.btn_showtable.setText(_translate("MainWindow", "TAMPILKAN \n" "TABEL"))
            self.btn_submittodecision.setText(_translate("MainWindow", "Kirim"))
            self.label_4.setText(_translate("MainWindow", "Keputusan"))
            self.lbl_resultdecision.setText(_translate("MainWindow", "-"))
            self.label_6.setText(_translate("MainWindow", "Input Buah Jatuh"))
            self.btn_shownumpad_inputbrondolan.setText(_translate("MainWindow", "Numpad"))
            self.label_7.setText(_translate("MainWindow", "Input Nomor Pohon"))
            self.btn_shownumpad_numtree.setText(_translate("MainWindow", "Numpad"))
            self.btn_back3.setText(_translate("MainWindow", "KEMBALI"))
            self.tbl_data.setSortingEnabled(False)
            item = self.tbl_data.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Nomor Pohon"))
            item = self.tbl_data.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Terlalu Matang"))
            item = self.tbl_data.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Matang"))
            item = self.tbl_data.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Belum Matang"))
            item = self.tbl_data.horizontalHeaderItem(4)
            item.setText(_translate("MainWindow", "Buah Jatuh"))
            item = self.tbl_data.horizontalHeaderItem(5)
            item.setText(_translate("MainWindow", "Keputusan"))
            self.btn_backtodetection.setText(_translate("MainWindow", "RESET \n" "KEMBALI \n" "KE \n" "DETEKSI"))
            pass
        
def main() -> None:
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    myui = MainWindowUI(MainWindow)
    print(ModelYolo)
    if ModelYolo != "/home/alldone/Desktop/sawit-yolo/model/content/yolov5/runs/train/exp5/weights/best.pt":
        MainWindow.showMaximized()
    myui.show()
    sys.exit(app.exec_())
            
if __name__ == "__main__":
    main()