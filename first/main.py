from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.uic import loadUi
from PyQt6.QtSql import *

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("FormApp.ui",self)
        self.loadButDB.clicked.connect(self.browsefiles)
        self.OutButTable.clicked.connect(self.ShowDB)

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', 'C:\Project1\PrSUBD\DataBase', '(*.db)')
        db=QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(fname)
        if not db.open():
            print('Не удалось подключится к базе')
            re
        else:
            print('Connection OK')
        return db

    def ShowDB(self):
        F_USD=QSqlTableModel()
        F_USD.setTable('F_usd')
        F_USD.select()
        self.tableDB.setModel(F_USD)


def application():
    app=QApplication(sys.argv)
    window=MainWindow()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(window)
    widget.setFixedWidth(900)
    widget.setFixedHeight(900)
    widget.show()
    app.exec()

if __name__ == "__main__":
    application()