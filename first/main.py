from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtSql import *
from PyQt6.QtGui import QIntValidator, QDoubleValidator
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
        self.filterDate1_age.setValidator(QIntValidator())
        self.filterDate1_month.setValidator(QIntValidator())
        self.filterDate1_day.setValidator(QIntValidator())
        self.filterDate2_age.setValidator(QIntValidator())
        self.filterDate2_month.setValidator(QIntValidator())
        self.filterDate2_day.setValidator(QIntValidator())
        self.filterq1.setValidator(QDoubleValidator())
        self.filterq2.setValidator(QDoubleValidator())
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
        print('клик')
        if self.connectDB:
            self.OutButTable_2.setText('')
            self.filter=''
            filter_check = False
            Dateot=['1900','01','01']
            Datedo=['2022','12','31']
            if (self.filterDate2_age.text() != ''):
                if int(self.filterDate2_age.text())<1000 or len(self.filterDate2_age.text())<4:
                    self.filterDate2_age.setText('1000')
                Datedo[0]=self.filterDate2_age.text()

            if (self.filterDate2_month.text() != ''):
                if int(self.filterDate2_month.text()) < 1:
                    self.filterDate2_month.setText('01')
                if int(self.filterDate2_month.text()) > 12:
                    self.filterDate2_month.setText('12')
                if len(self.filterDate2_month.text()) < 2:
                    self.filterDate2_month.setText('0'+self.filterDate2_month.text())
                Datedo[1]=self.filterDate2_month.text()



            if (self.filterDate2_day.text() != ''):
                if int(self.filterDate2_day.text()) < 1:
                    self.filterDate2_day.setText('01')


                if int(Datedo[0])%4!=0:                                # високосный ли год
                    if int(self.filterDate2_day.text()) > 28 and self.filterDate2_month.text()=='02':
                        self.filterDate2_day.setText('28')
                else:
                    if int(self.filterDate2_day.text()) > 29 and self.filterDate2_month.text() == '02':
                        self.filterDate2_day.setText('29')


                if int(self.filterDate2_day.text()) > 30:
                    if self.filterDate2_month.text() == '04' or self.filterDate2_month.text() == '06' or self.filterDate2_month.text() == '09' or self.filterDate2_month.text() == '11':
                        self.filterDate2_day.setText('30')
                    else:
                        if int(self.filterDate2_day.text()) > 31 and self.filterDate2_month.text()!='02':
                            self.filterDate2_day.setText('31')
                if len(self.filterDate2_day.text()) < 2:
                    self.filterDate2_day.setText('0' + self.filterDate2_day.text())
                Datedo[2]=self.filterDate2_day.text()


            if (self.filterDate1_age.text() != ''):
                if int(self.filterDate1_age.text())<1000 or len(self.filterDate1_age.text())<4:
                    self.filterDate1_age.setText('1000')
                Dateot[0]=self.filterDate1_age.text()

            if (self.filterDate1_month.text() != ''):
                if int(self.filterDate1_month.text()) < 1:
                    self.filterDate1_month.setText('01')
                if int(self.filterDate1_month.text()) > 12:
                    self.filterDate1_month.setText('12')
                if len(self.filterDate1_month.text()) < 2:
                    self.filterDate1_month.setText('0'+self.filterDate1_month.text())
                Dateot[1]=self.filterDate1_month.text()

            if (self.filterDate1_day.text() != ''):
                if int(self.filterDate1_day.text()) < 1:
                    self.filterDate1_day.setText('01')

                if int(Dateot[0])% 4 != 0:  # високосный ли год
                    if int(self.filterDate1_day.text()) > 28 and self.filterDate1_month.text() == '02':
                        self.filterDate1_day.setText('28')
                else:
                    if int(self.filterDate1_day.text()) > 29 and self.filterDate1_month.text() == '02':
                        self.filterDate1_day.setText('29')

                if int(self.filterDate1_day.text()) > 30:
                    if self.filterDate1_month.text() == '04' or self.filterDate1_month.text() == '06' or self.filterDate1_month.text() == '09' or self.filterDate1_month.text() == '11':
                        self.filterDate1_day.setText('30')
                    else:
                        if int(self.filterDate1_day.text()) > 31 and self.filterDate1_month.text() != '02':
                            self.filterDate1_day.setText('31')
                if len(self.filterDate1_day.text()) < 2:
                    self.filterDate1_day.setText('0' + self.filterDate1_day.text())
                Dateot[2] = self.filterDate1_day.text()

            DateOT=Dateot[0]+'.'+Dateot[1]+'.'+Dateot[2]
            DateDO = Datedo[0] + '.' + Datedo[1] + '.' + Datedo[2]
            print(DateOT+'\t:\t'+DateDO)
            self.filter=self.filter+"torg_date_2>='"+DateOT+"' AND torg_date_2<='"+DateDO+"'"

            if (self.filterq1.text()!= ''):
                filt3='CAST(quotation as real)>='+self.filterq1.text()
                self.filter = self.filter + ' AND ' + filt3

            if (self.filterq2.text() != ''):
                filt4='CAST(quotation as real)<='+self.filterq2.text()
                self.filter = self.filter + ' AND ' + filt4

            if (self.KodBox.currentText() != ''):
                filt5="kod = '"+self.KodBox.currentText()+"'"
                self.filter = self.filter + ' AND ' + filt5

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