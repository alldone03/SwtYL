import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 QtSQL CRUD Example")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        self.age_label = QLabel("Age:")
        layout.addWidget(self.age_label)
        self.age_input = QLineEdit()
        layout.addWidget(self.age_input)

        self.add_button = QPushButton("Add Record")
        self.add_button.clicked.connect(self.add_record)
        layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Record")
        self.delete_button.clicked.connect(self.delete_record)
        layout.addWidget(self.delete_button)

        self.view_button = QPushButton("View Records")
        self.view_button.clicked.connect(self.view_records)
        layout.addWidget(self.view_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect to SQLite database
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("example.db")
        if not self.db.open():
            QMessageBox.critical(None, "Database Error", "Failed to connect to database.")
            sys.exit(1)

        # Create table if not exists
        query = QSqlQuery()
        query.exec_("""CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        age INTEGER
                    )""")

    def add_record(self):
        name = self.name_input.text()
        age = self.age_input.text()
        if name and age:
            query = QSqlQuery()
            query.prepare("INSERT INTO employees (name, age) VALUES (?, ?)")
            query.bindValue(0, name)
            query.bindValue(1, int(age))
            if query.exec_():
                QMessageBox.information(None, "Success", "Record added successfully.")
                self.name_input.clear()
                self.age_input.clear()
            else:
                QMessageBox.critical(None, "Error", "Failed to add record.")

    def delete_record(self):
        name = self.name_input.text()
        if name:
            query = QSqlQuery()
            query.prepare("DELETE FROM employees WHERE name = ?")
            query.bindValue(0, name)
            if query.exec_():
                QMessageBox.information(None, "Success", "Record deleted successfully.")
                self.name_input.clear()
                self.age_input.clear()
            else:
                QMessageBox.critical(None, "Error", "Failed to delete record.")

    def view_records(self):
        query = QSqlQuery("SELECT * FROM employees")
        records = []
        while query.next():
            id = query.value(0)
            name = query.value(1)
            age = query.value(2)
            records.append(f"ID: {id}, Name: {name}, Age: {age}")
        QMessageBox.information(None, "Records", "\n".join(records))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())