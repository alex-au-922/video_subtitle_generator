from PyQt5.QtWidgets import QApplication
import sys
from view.ui import MainWindow
from controller.control import Controller

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    Controller(window)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()