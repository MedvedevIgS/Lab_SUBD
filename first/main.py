from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtSql import *

import sys

class MainWindow(QMainWindow):
    db = QSqlDatabase.addDatabase('QSQLITE')
    connectDB=False
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("FormApp.ui",self)
        self.loadButDB.clicked.connect(self.LoadDB)
        self.BrowBut.clicked.connect(self.browsefiles)
        self.OutButTable.clicked.connect(self.ShowDB)
        self.tableDB.setSortingEnabled(True)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '..\DataBase\ ', '(*.db)')
        self.BrowLine.setText(fname[0])

    def LoadDB(self):
        if self.BrowLine.text() != '':
            self.loadButDB_1.setText('')
            self.db.setDatabaseName(self.BrowLine.text())
            if not self.db.open():
                self.connectDB = False
            else:
                self.connectDB = True
        else:
            self.loadButDB_1.setText('Укажите путь')
            self.connectDB = False

    def ShowDB(self):
        self.OutButTable_1.setText('Работает')
        if self.connectDB:
            self.OutButTable_2.setText('')
            F_USD = QSqlTableModel()
            F_USD.setTable('F_usd')
            F_USD.select()
            self.tableDB.setModel(F_USD)
        else:
            self.OutButTable_2.setText('Загрузите БД')
            EmptyTab=QSqlTableModel()
            self.tableDB.setModel(EmptyTab)


def application():
    app=QApplication(sys.argv)
    window=MainWindow()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(window)
    widget.setMinimumWidth(840)
    widget.setMinimumHeight(660)
    widget.show()
    app.exec()

if __name__ == "__main__":
    application()