# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pluginWidget.ui'
#
# Created: Wed Feb 29 18:43:26 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(416, 70)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(200, 70))
        Form.setMaximumSize(QtCore.QSize(416, 16777215))
        Form.setBaseSize(QtCore.QSize(200, 70))
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.txtName = QtGui.QLabel(Form)
        self.txtName.setText(QtGui.QApplication.translate("Form", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.txtName.setObjectName(_fromUtf8("txtName"))
        self.horizontalLayout.addWidget(self.txtName)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout.addWidget(self.line)
        self.txtDesc = QtGui.QLabel(Form)
        self.txtDesc.setToolTip(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Desc:</span> this is the description</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.txtDesc.setStatusTip(QtGui.QApplication.translate("Form", "tesssst statustipp", None, QtGui.QApplication.UnicodeUTF8))
        self.txtDesc.setText(QtGui.QApplication.translate("Form", "Desc", None, QtGui.QApplication.UnicodeUTF8))
        self.txtDesc.setObjectName(_fromUtf8("txtDesc"))
        self.horizontalLayout.addWidget(self.txtDesc)
        self.line_2 = QtGui.QFrame(Form)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout.addWidget(self.line_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.btnEdit = QtGui.QPushButton(Form)
        self.btnEdit.setText(QtGui.QApplication.translate("Form", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.verticalLayout.addWidget(self.btnEdit)
        self.btnRemove = QtGui.QPushButton(Form)
        self.btnRemove.setText(QtGui.QApplication.translate("Form", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))
        self.verticalLayout.addWidget(self.btnRemove)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

