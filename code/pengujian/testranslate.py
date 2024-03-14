import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QTranslator, QLocale

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Aplikasi Multi Bahasa")

        self.button = QPushButton('Ubah Bahasa', self)
        self.button.move(50, 50)
        self.button.clicked.connect(self.toggleLanguage)

    def toggleLanguage(self):
        # Periksa bahasa yang sedang aktif
        current_language = QLocale.system().name()
        new_language = 'en' if current_language == 'id' else 'id'

        # Muat file terjemahan baru
        translator = QTranslator()
        translator.load(f'aplikasi_{new_language}')
        app.installTranslator(translator)

        # Restart aplikasi agar perubahan bahasa terlihat
        app.removeTranslator(self.translator)
        self.translator = translator
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load translation file based on system locale
    locale = QLocale.system().name()
    translator = QTranslator()
    translator.load(f'aplikasi_{locale}')
    app.installTranslator(translator)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
