from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtSql import *
import sqlite3
import os

import sys

class MainWindow(QMainWindow):
    db=QSqlDatabase.addDatabase('QSQLITE')
    connectDB=False
    filter = ''
    Name_table=''
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("FormApp.ui",self)
        self.setWindowTitle("LR_SUBD")
        self.loadButDB.clicked.connect(self.LoadDB)
        self.BrowBut.clicked.connect(self.browsefiles)
        self.filterBut.clicked.connect(self.filter_use)
        self.tableDB.setSortingEnabled(True)
        RB0=QtWidgets.QRadioButton()
        RBmass=(self.RB1, self.RB2, self.RB3, self.RB4, self.RB5, self.RB6, self.RB7, self.RB8)
        for RB in RBmass:
            RB.setVisible(False)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '..\DataBase\ ', '(*.db)')
        self.BrowLine.setText(fname[0])

    def LoadDB(self):
        if self.BrowLine.text() != '':
            if os.path.isfile(self.BrowLine.text()):
                self.loadButDB_1.setText('')
                self.db.setDatabaseName(self.BrowLine.text())
                con = sqlite3.connect(self.BrowLine.text())
                cur = con.cursor()
                sql = "SELECT name FROM sqlite_master WHERE TYPE = 'table'"
                Ntabl = cur.execute(sql).fetchall()
                print(len(Ntabl))
                print(Ntabl[1][0])
                RBmass=(self.RB1, self.RB2, self.RB3, self.RB4, self.RB5, self.RB6, self.RB7, self.RB8)
                for i in range(len(Ntabl)):
                    RBmass[i].setVisible(True)
                    RBmass[i].setText(Ntabl[i][0])
                    RBmass[i].toggled.connect(self.RB_z)
            else:
                self.loadButDB_1.setText('Указан неверный путь')
                self.connectDB = False
        else:
            self.loadButDB_1.setText('Укажите Путь')
            self.connectDB = False

    def RB_z(self):
        rb = self.sender()
        if rb.isChecked():
            self.Name_table = rb.text()
            con = sqlite3.connect(self.BrowLine.text())
            cur = con.cursor()
            sql = "SELECT DISTINCT kod FROM F_USD"
            kod = cur.execute(sql).fetchall()
            print(len(kod))
            self.KodBox.addItem('')
            for i in range(len(kod)):
                print(kod[i][0])
                self.KodBox.addItem(kod[i][0])
            self.loadtable()
            cur.close()
            con.close()

    def loadtable(self):
        table = QSqlTableModel()
        table.setTable(self.Name_table)
        table.setFilter(self.filter)
        print('Filter: ' + table.filter())
        table.select()
        print('table - ' + table.tableName())
        self.tableDB.setModel(table)
        self.connectDB = True


    def filter_use(self):
        if self.connectDB:
            self.OutButTable_2.setText('')
            self.filter=''
            filter_check = False
            if (self.filterDate1.text() != ''):
                filt1='torg_date >= '+self.filterDate1.text()
                self.filter=self.filter+filt1
                filter_check=True
            if (self.filterDate2.text() != ''):
                filt2='torg_date <= '+self.filterDate2.text()
                if filter_check:
                    self.filter = self.filter + ' AND ' + filt2
                else:
                    self.filter = self.filter + filt2
                filter_check = True

            if (self.filterq1.text()!= ''):
                filt3='quotation>='+self.filterq1.text()
                if filter_check:
                    self.filter = self.filter + ' AND ' + filt3
                else:
                    self.filter = self.filter + filt3
                filter_check = True
            if (self.filterq2.text() != ''):
                filt4='quotation<='+self.filterq2.text()
                if filter_check:
                    self.filter = self.filter + ' AND ' + filt4
                else:
                    self.filter = self.filter + filt4
                filter_check = True
            if (self.KodBox.currentText() != ''):
                filt5="kod = '"+self.KodBox.currentText()+"'"
                if filter_check:
                    self.filter = self.filter + ' AND ' + filt5
                else:
                    self.filter = self.filter + filt5
            print(self.filter)
            self.loadtable()
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