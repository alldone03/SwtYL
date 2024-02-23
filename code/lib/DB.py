import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class Database:
    def __init__(self) -> None:
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('logging.db')
        db.open()
        query = QSqlQuery()
        query.exec_("""CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        numbertree INTERGER,
                        matang INTEGER,
                        mentah INTEGER,
                        busuk INTEGER,
                        buahjatuh INTEGER,
                        keputusan TEXT
                    )""")
        pass
    def add_record(self, numbertree, matang, mentah, busuk, buahjatuh, keputusan) -> None:
        query = QSqlQuery()
        query.prepare("INSERT INTO employees (numbertree, matang, mentah, busuk, buahjatuh, keputusan) VALUES (?, ?, ?, ?, ?, ?)")
        query.addBindValue(numbertree)
        query.addBindValue(matang)
        query.addBindValue(mentah)
        query.addBindValue(busuk)
        query.addBindValue(buahjatuh)
        query.addBindValue(keputusan)
        query.exec_()
        pass
    def view_records(self) -> None:
        query = QSqlQuery()
        query.exec_("SELECT * FROM employees")
        while query.next():
            print(query.value(0), query.value(1), query.value(2), query.value(3), query.value(4), query.value(5), query.value(6))
        pass
    def delete_record(self, numbertree) -> None:
        query = QSqlQuery()
        query.prepare("DELETE FROM employees WHERE numbertree = ?")
        query.addBindValue(numbertree)
        query.exec_()
        pass
    def update_table(self,function)->None:
        
        # function()
        pass
    
# db = Database()
# db.add_record(1, 2, 1, 1, 1, "matang")
# db.view_records()
