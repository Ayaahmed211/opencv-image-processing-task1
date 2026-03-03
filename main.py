import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLocale  # <--- 1. Import QLocale
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    

    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()