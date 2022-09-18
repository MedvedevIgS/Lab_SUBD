from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtSql import *

import sys

class MainWindow(QMainWindow):
    db = QSqlDatabase.addDatabase('QSQLITE')
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
        F_USD = QSqlTableModel()
        F_USD.setTable('F_usd')
        F_USD.select()
        self.tableDB.setModel(F_USD)


    """      
            fname=QFileDialog.getOpenFileName(self, 'Open file', 'C:\Project1\PrSUBD\DataBase', '(*.db)')
            db=QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(fname)
            F_USD = QSqlTableModel()
            F_USD.setTable('F_usd')
            F_USD.select()
    """
    def ShowDB(self):
        self.OutButTable_1.setText('Работает')

        """
        F_USD=QSqlTableModel()
        F_USD.setTable('F_usd')
        F_USD.select()
        self.tableDB.setModel(F_USD)
        """

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