# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QTableView,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1080, 570)
        MainWindow.setMinimumSize(QSize(1080, 570))
        MainWindow.setMaximumSize(QSize(1080, 570))
        MainWindow.setStyleSheet(u"* {\n"
"	background-color: #383838;\n"
"	color: #fff;\n"
"	outline: none;\n"
"}\n"
"\n"
"*:focus {\n"
"	outline: none;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pbtnGetLiveMatches = QPushButton(self.centralwidget)
        self.pbtnGetLiveMatches.setObjectName(u"pbtnGetLiveMatches")
        self.pbtnGetLiveMatches.setGeometry(QRect(860, 500, 201, 51))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.pbtnGetLiveMatches.setFont(font)
        self.pbtnGetLiveMatches.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tblvwLiveMatches = QTableView(self.centralwidget)
        self.tblvwLiveMatches.setObjectName(u"tblvwLiveMatches")
        self.tblvwLiveMatches.setGeometry(QRect(20, 20, 1041, 461))
        self.tblvwLiveMatches.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tblvwLiveMatches.setStyleSheet(u"QTableView {\n"
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
        self.tblvwLiveMatches.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tblvwLiveMatches.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tblvwLiveMatches.horizontalHeader().setStretchLastSection(True)
        self.lblMessage = QLabel(self.centralwidget)
        self.lblMessage.setObjectName(u"lblMessage")
        self.lblMessage.setGeometry(QRect(20, 500, 831, 51))
        self.lblMessage.setFont(font)
        self.lblMessage.setStyleSheet(u"background: none; color: #f9f1a5;")
        self.lblMessage.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pbtnGetLiveMatches.setText(QCoreApplication.translate("MainWindow", u"Canl\u0131 Ma\u00e7 Verilerini Al", None))
        self.lblMessage.setText("")
    # retranslateUi

