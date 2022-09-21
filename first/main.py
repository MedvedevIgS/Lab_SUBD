from PyQt6 import uic, QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtSql import *
import sqlite3
import os

import sys

class MainWindow(QMainWindow):
    db=QSqlDatabase.addDatabase('QSQLITE')
    connectDB=False
    filter = ''
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("FormApp.ui",self)
        self.setWindowTitle("LR_SUBD")
        self.loadButDB.clicked.connect(self.LoadDB)
        self.BrowBut.clicked.connect(self.browsefiles)
        self.filterBut.clicked.connect(self.filter_use)
        self.tableDB.setSortingEnabled(True)
        self.RB1.setVisible(False)
        self.RB2.setVisible(False)
        self.RB3.setVisible(False)
        self.RB4.setVisible(False)
        self.RB5.setVisible(False)
        self.RB6.setVisible(False)
        self.RB7.setVisible(False)
        self.RB8.setVisible(False)
        radBut = QtWidgets.QRadioButton('radBut')
        radBut.move(310, 100)


    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '..\DataBase\ ', '(*.db)')
        self.BrowLine.setText(fname[0])

    def LoadDB(self):
        if self.BrowLine.text() != '':
            if os.path.isfile(self.BrowLine.text()):
                self.loadButDB_1.setText('')
                self.db.setDatabaseName(self.BrowLine.text())
                table = QSqlTableModel()
                table.setTable('F_USD')
                table.setFilter(self.filter)
                print(table.filter())
                table.select()
                print('table - '+table.tableName())

                sqlqery = QSqlQuery()
                # sqlqery.exec("SELECT * FROM F_USD")
                self.tableDB.setModel(table)
                connectDB = True
            else:
                self.loadButDB_1.setText('Указан неверный путь')
                connectDB = False
        else:
            self.loadButDB_1.setText('Укажите Путь')
            connectDB = False


    def filter_use(self):
        if self.connectDB:
            self.OutButTable_2.setText('')
            filter_count = 0
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