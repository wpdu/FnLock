# FnLock
HP keyboard fn lock

support f1-f6 & f9-f12

# ui to py
pyuic5 -o FnLock_ui.py FnLock.ui

# build
pyinstaller -F -w -i .\fnlock.ico .\FnLockMain.py

# use
fn lock switch short cut: ctrl + l + f