from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from system_hotkey import SystemHotkey
from FnLock_ui import Ui_FnLock
from key_remap_util import remap_keys, remove_remap_keys


class Main(QWidget, Ui_FnLock):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('fnlock.ico'))
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


class HotKeyThread(QThread, SystemHotkey):
    trigger = pyqtSignal()

    def __init__(self, UI):
        self.ui = UI
        super(HotKeyThread, self).__init__()
        self.register(('control', 'l', 'f'), callback=lambda x: self.start())
        self.trigger.connect(self.hotKeyEvent)

    def run(self):
        self.trigger.emit()

    def hotKeyEvent(self):
        if self.ui.checkBox.checkState() != QtCore.Qt.CheckState.Checked:
            self.ui.checkBox.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.ui.checkBox.setCheckState(QtCore.Qt.CheckState.Unchecked)

    def quitThread(self):
        if self.isRunning():
            self.quit()

