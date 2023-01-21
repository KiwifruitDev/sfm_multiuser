# SFM Multiuser
# =====================
# MIT License
# 
# Copyright (c) 2023 KiwifruitDev
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PySide import QtCore, QtGui, shiboken
from vs import g_pDataModel as dm
import vs, sfmApp, sfm, sfmUtils

class Multiuser_Window(QtGui.QWidget):

    def __init__(self):
        super(Multiuser_Window, self).__init__()
        self.session = ""
        # Session select button
        self.select_button = QtGui.QPushButton("Select Session")
        self.select_button.clicked.connect(self.selectSession)
        # Session reload button
        self.reload_button = QtGui.QPushButton("Reload Session (Ctrl+R)")
        self.reload_button.clicked.connect(self.reloadSession)
        self.reload_button.setEnabled(False)
        # Wait delay
        self.delay_spinbox = QtGui.QSpinBox()
        self.delay_spinbox.setRange(0, 10000)
        self.delay_spinbox.setValue(5000)
        self.delay_spinbox.setSuffix(" ms")
        self.delay_spinbox.setToolTip("Delay in milliseconds before reloading session.")
        # Add to layout
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.delay_spinbox)
        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.reload_button)
        self.setLayout(self.layout)
        # Add ctrl+r binding
        self.shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        self.shortcut.activated.connect(self.reloadSession)

    def reloadSession(self):
        # Reload session
        if self.session == "":
            QtGui.QMessageBox.warning(None, "Multiuser: Error", "Please select a session first.", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return
        sfmApp.SaveDocument()
        sfmApp.CloseDocument(forceSilent=False)
        # Wait 5 seconds for presumably Multiuser script
        QtCore.QTimer.singleShot(self.delay_spinbox.value(), self.openSession)

    def openSession(self):
        # Open session
        sfmApp.OpenDocument(self.session)

    def selectSession(self):
        # Select session
        session, type = QtGui.QFileDialog.getOpenFileName(self, "Select Session", "", "Session (*.dmx)")
        if session:
            self.reload_button.setEnabled(True)
            self.reload_button.setToolTip("Reload session: " + session)
            self.session = session.encode("ascii", "ignore").replace("/", "\\")
            print("Session: " + self.session)

try:
    # Create window if it doesn't exist
    globalMultiuser = globals().get("multiuser_window")
    if globalMultiuser is None:
        multiuser_window=Multiuser_Window()
        sfmApp.RegisterTabWindow("WindowMultiuser", "Multiuser", shiboken.getCppPointer( multiuser_window )[0])
        sfmApp.ShowTabWindow("WindowMultiuser")
    else:
        dialog = QtGui.QMessageBox.warning(None, "Multiuser: Error", "Multiuser is already open.\n\nIf you are a developer, click Yes to forcibly open a new instance.\n\nOtherwise, click No to close this message.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if dialog == QtGui.QMessageBox.Yes:
            multiuser_window=Multiuser_Window()
            sfmApp.RegisterTabWindow("WindowMultiuser", "Multiuser", shiboken.getCppPointer( multiuser_window )[0])
            sfmApp.ShowTabWindow("WindowMultiuser")
except Exception  as e:
    import traceback
    traceback.print_exc()        
    msgBox = QtGui.QMessageBox()
    msgBox.setText("Error: %s" % e)
    msgBox.exec_()