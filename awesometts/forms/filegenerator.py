# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/filegenerator.ui'
#
# Created: Sat May 19 22:29:22 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        Dialog.setWindowTitle(_("AwesomeTTS :: MP3 File Generator"))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.texttoTTS = QtGui.QPlainTextEdit(Dialog)
        self.texttoTTS.setObjectName(_fromUtf8("texttoTTS"))
        self.gridLayout.addWidget(self.texttoTTS, 6, 2, 1, 2)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setText(_("TextLabel"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 3, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 2, 1, 2)
        self.label = QtGui.QLabel(Dialog)
        self.label.setText(_("Text:"))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 2, 1, 1)
        self.previewbutton = QtGui.QPushButton(Dialog)
        self.previewbutton.setText(_("Preview"))
        self.previewbutton.setObjectName(_fromUtf8("previewbutton"))
        self.gridLayout.addWidget(self.previewbutton, 7, 2, 1, 2)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setText(_("Service:"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.comboBoxService = QtGui.QComboBox(Dialog)
        self.comboBoxService.setObjectName(_fromUtf8("comboBoxService"))
        self.verticalLayout_2.addWidget(self.comboBoxService)
        self.stackedWidget = QtGui.QStackedWidget(Dialog)
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.verticalLayout_2.addWidget(self.stackedWidget)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout_2, 4, 0, 5, 1)

        self.retranslateUi(Dialog)
        self.stackedWidget.setCurrentIndex(-1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass

