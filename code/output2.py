# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'code/APP800x480.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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
import res_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
