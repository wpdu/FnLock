import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from FnLock import Main

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    demo = Main()
    demo.show()
    sys.exit(app.exec_())