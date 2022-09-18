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
        self.loadButDB.clicked.connect(self.browsefiles)
        self.OutButTable.clicked.connect(self.ShowDB)
        self.tableDB.setSortingEnabled(True)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:\Project1\PrSUBD\DataBase', '(*.db)')
        self.loadButDB_1.setText(fname[0])
        self.db.setDatabaseName(fname[0])
        if not self.db.open() or fname[0]=='':
            self.connectDB = False
        else:
            self.connectDB = True

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