# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EventDetailsWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QPushButton,
    QSizePolicy, QTableView, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1080, 570)
        Form.setMinimumSize(QSize(1080, 570))
        Form.setMaximumSize(QSize(1080, 570))
        Form.setStyleSheet(u"* {\n"
"	background-color: #383838;\n"
"	color: #fff;\n"
"	outline: none;\n"
"}\n"
"\n"
"*:focus {\n"
"	outline: none;\n"
"}")
        self.pbtnGetH2hData = QPushButton(Form)
        self.pbtnGetH2hData.setObjectName(u"pbtnGetH2hData")
        self.pbtnGetH2hData.setGeometry(QRect(260, 500, 221, 51))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.pbtnGetH2hData.setFont(font)
        self.pbtnGetH2hData.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pbtnGetOddsData = QPushButton(Form)
        self.pbtnGetOddsData.setObjectName(u"pbtnGetOddsData")
        self.pbtnGetOddsData.setGeometry(QRect(20, 500, 221, 51))
        self.pbtnGetOddsData.setFont(font)
        self.pbtnGetOddsData.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tblvwEventDetails = QTableView(Form)
        self.tblvwEventDetails.setObjectName(u"tblvwEventDetails")
        self.tblvwEventDetails.setGeometry(QRect(20, 20, 1041, 461))
        self.tblvwEventDetails.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tblvwEventDetails.setStyleSheet(u"QTableView {\n"
"	background-color: #383838;\n"
"	color: #fff;\n"
"	border: 1px solid #282828;\n"
"	padding: 4px;\n"
"}\n"
"\n"
"QTableView::item::selected {\n"
"	background-color: #484848;\n"
"}\n"
"\n"
"QHeaderView {\n"
"	border: none;\n"
"	background-color: #383838;\n"
"	color: #000;\n"
"	font: 700 12pt \"Arial\";\n"
"}\n"
"\n"
"QHeaderView:section {\n"
"	background-color: #383838;\n"
"	color: #fff;\n"
"	font: 700 12pt \"Arial\";\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"	background-color: #383838;\n"
"}")
        self.tblvwEventDetails.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tblvwEventDetails.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tblvwEventDetails.horizontalHeader().setStretchLastSection(True)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pbtnGetH2hData.setText(QCoreApplication.translate("Form", u"H2H Verilerini G\u00f6ster", None))
        self.pbtnGetOddsData.setText(QCoreApplication.translate("Form", u"ODDS Verilerini G\u00f6ster", None))
    # retranslateUi

