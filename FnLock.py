from PyQt5.QtWidgets import QWidget, QApplication, QSystemTrayIcon, QMenu, QAction, qApp
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, Qt, pyqtSignal
import sys
from PyQt5.QtGui import QIcon
from system_hotkey import SystemHotkey
from FnLock_ui import Ui_FnLock
from my_key_map_util import remap_keys, remove_remap_keys
# from key_remap_util import remap_keys, remove_remap_keys


class Main(QWidget, Ui_FnLock):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('fnlock.ico'))
        self.tray = Tray(self)
        self.hotKey = HotKeyThread(self)
        self.setStyle()

    def lock_switch(self, isChecked):
        if isChecked:
            remap_keys()
        else:
            remove_remap_keys()

    def setStyle(self):
        self.setStyleSheet(
            '* { background: #FFF }')

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.hide()

    def closeEvent(self, QCloseEvent):
        QCloseEvent.ignore()
        self.hide()


class Tray(QSystemTrayIcon):
    def __init__(self, UI):
        super(Tray, self).__init__()
        self.ui = UI
        self.setIcon(QIcon('fnlock.ico'))
        self.setToolTip('FnLock')
        self.activated.connect(self.clickedIcon)
        self.menu()
        self.show()

    def clickedIcon(self, reason):
        if reason == 3:
            self.trayClickedEvent()
        elif reason == 1:
            self.contextMenu()

    def menu(self):
        menu = QMenu()
        action = QAction('退出', self, triggered=self.triggered)
        menu.addAction(action)
        self.setContextMenu(menu)

    def trayClickedEvent(self):
        if self.ui.isHidden():
            self.ui.setHidden(False)
            if self.ui.windowState() == Qt.WindowMinimized:
                self.ui.showNormal()
            self.ui.raise_()
            self.ui.activateWindow()
        else:
            self.ui.setHidden(True)

    def triggered(self):
        self.deleteLater()
        qApp.quit()


class HotKeyThread(QThread, SystemHotkey):
    trigger = pyqtSignal()

    def __init__(self, UI):
        self.ui = UI
        super(HotKeyThread, self).__init__()
        self.register(('control', 'l'), callback=lambda x: self.start())
        self.trigger.connect(self.hotKeyEvent)

    def run(self):
        self.trigger.emit()

    def hotKeyEvent(self):
        if self.ui.checkBox.checkState() != QtCore.Qt.CheckState.Checked:
            self.ui.checkBox.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.ui.checkBox.setCheckState(QtCore.Qt.CheckState.Unchecked)

        # if self.ui.isHidden():
        #     self.ui.setHidden(False)
        #     if self.ui.windowState() == QtCore.Qt.WindowMinimized:
        #         self.ui.showNormal()
        #     self.ui.raise_()
        #     self.ui.activateWindow()
        # else:
        #     self.ui.setHidden(True)

    def quitThread(self):
        if self.isRunning():
            self.quit()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    demo = Main()
    demo.show()
    sys.exit(app.exec_())
