from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtSql import *
from PyQt6.QtGui import QIntValidator, QDoubleValidator
import sqlite3
import os

import sys

class addWindow(QMainWindow):
    Name_table = ''
    browDB = ''
    table=QSqlTableModel()
    sqlloadtable=''
    def __init__(self, tablesql: QSqlTableModel, nameT, BROWDB, sqltabload):
        super(addWindow, self).__init__()
        self.table = tablesql
        self.Name_table=nameT
        self.browDB=BROWDB
        self.sqlloadtable=sqltabload
        uic.loadUi("AddForm.ui", self)
        self.Error.setVisible(False)
        self.quo.setValidator(QDoubleValidator())
        self.num_c.setValidator(QIntValidator())
        self.addBut.clicked.connect(self.click_add)

    def click_add(self):
        if self.quo.text()=='' or self.kod.text()=='' or self.torgd.text()=='' or self.num_c.text()=='':
            self.Error.setVisible(True)
            self.Error.setText('Заполните все поля')
        else:
            provDat=self.torgd.text().split('.')

            provKod=self.kod.text().split('_')

            if len(provDat)!=3 or len(provDat[0])!=2 or len(provDat[1])!=2 or len(provDat[2])!=4 or provDat[0].isdigit()!=True or provDat[1].isdigit()!=True or provDat[2].isdigit()!=True:
                self.Error.setVisible(True)
                self.Error.setText('Некорекктная запись даты')
            elif len(provKod)!=3 or provKod[0]!='FUSD' or len(provKod[1])!=2 or len(provKod[2])!=2 or provKod[1].isdigit()!=True or provKod[2].isdigit()!=True:
                self.Error.setVisible(True)
                self.Error.setText('Некорекктная запись кода')
            else:
                torgdatRevers = provDat[2] + '.' + provDat[1] + '.' + provDat[0]
                self.Error.setVisible(False)
                self.Error.setText('')
                sql = "INSERT INTO F_usd VALUES ('" + self.torgd.text() + "', '" + self.kod.text() + "', '" + self.quo.text() + "', " + self.num_c.text() + ", '" + torgdatRevers + "')"
                qry=QSqlQuery()
                qry.prepare(sql)
                qry.exec()
                sql = QSqlQuery(self.sqlloadtable)
                self.table.setQuery(sql)
                self.table.select()
                self.Error.setVisible(True)
                self.Error.setText('Запись добавлена')
                self.quo.setText('')
                self.kod.setText('')
                self.torgd.setText('')
                self.num_c.setText('')






class MainWindow(QMainWindow):
    db=QSqlDatabase.addDatabase('QSQLITE')
    connectDB=False
    filter = ''
    Name_table=''
    browDB=''
    model = QSqlTableModel()
    sqltabload=''
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("FormApp.ui",self)
        self.setWindowTitle("LR_SUBD")
        self.loadButDB.clicked.connect(self.LoadDB)
        self.BrowBut.clicked.connect(self.browsefiles)
        self.filterBut.clicked.connect(self.filter_use)
        self.tableDB.setSortingEnabled(True)
        self.Error.setVisible(False)
        self.ErrorBUT.setVisible(False)
        self.AddBut.clicked.connect(self.addinBD)
        self.DelBut.clicked.connect(self.delinBD)


        self.filterDate1_age.setValidator(QIntValidator())
        self.filterDate1_month.setValidator(QIntValidator())
        self.filterDate1_day.setValidator(QIntValidator())
        self.filterDate2_age.setValidator(QIntValidator())
        self.filterDate2_month.setValidator(QIntValidator())
        self.filterDate2_day.setValidator(QIntValidator())
        self.filterq1.setValidator(QDoubleValidator())
        self.filterq2.setValidator(QDoubleValidator())
        self.filterDate1_month.setEnabled(False)
        self.filterDate1_day.setEnabled(False)
        self.filterDate2_month.setEnabled(False)
        self.filterDate2_day.setEnabled(False)
        self.filterDate1_age.textChanged.connect(self.Enable_line)
        self.filterDate2_age.textChanged.connect(self.Enable_line)
        self.filterDate1_month.textChanged.connect(self.Enable_line)
        self.filterDate2_month.textChanged.connect(self.Enable_line)


        RBmass=(self.RB1, self.RB2, self.RB3, self.RB4, self.RB5, self.RB6, self.RB7, self.RB8)
        for RB in RBmass:
            RB.setVisible(False)

    def prints(self):
        print(1)
    def delinBD(self):
        #print('++++++++++++++++++++++++++++')
        select1 = self.tableDB.selectedIndexes()
        #print(select1)
        #print(len(select1))
        if len(select1)>=2:
            self.ErrorBUT.setText('')
            self.ErrorBUT.setVisible(False)
            #print('-----------------')
            for i in range(len(select1)):
                if i%4==0:
                    ind0 = self.tableDB.model().index(select1[i].row(), 0, select1[i].parent())
                    ind1 = self.tableDB.model().index(select1[i+1].row(), 1, select1[i+1].parent())
                    #print(ind0.data())
                    #print(ind1.data())
                    #print('-----------------')
                    sql = "DELETE FROM F_usd WHERE torg_date = '" + ind0.data() + "' AND kod = '" + ind1.data()+"'"
                    #print(sql)
                    qry = QSqlQuery()
                    qry.prepare(sql)
                    qry.exec()
            self.loadtable()
        else:
            self.ErrorBUT.setText('Выделите всю строку')
            self.ErrorBUT.setVisible(True)

    def addinBD(self):
        if self.connectDB:
            self.Error.setVisible(False)
            self.Error.setText('')
            global widget2
            addWind = addWindow(self.model, self.Name_table, self.browDB, self.sqltabload)
            widget2 = QtWidgets.QStackedWidget()
            widget2.addWidget(addWind)
            widget2.setMinimumWidth(565)
            widget2.setMinimumHeight(299)
            widget2.show()
        else:
            self.Error.setVisible(True)
            self.Error.setText('Для добавления записи нужно подключить БД')


    def Enable_line(self):
        if self.filterDate1_age.text()!='':
            self.filterDate1_month.setEnabled(True)
        else:
            self.filterDate1_month.setEnabled(False)
            self.filterDate1_month.setText('')

        if self.filterDate2_age.text()!='':
            self.filterDate2_month.setEnabled(True)
        else:
            self.filterDate2_month.setEnabled(False)
            self.filterDate2_month.setText('')

        if self.filterDate1_month.text()!='':
            self.filterDate1_day.setEnabled(True)
        else:
            self.filterDate1_day.setEnabled(False)
            self.filterDate1_day.setText('')

        if self.filterDate2_month.text()!='':
            self.filterDate2_day.setEnabled(True)
        else:
            self.filterDate2_day.setEnabled(False)
            self.filterDate2_day.setText('')

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '..\DataBase\ ', '(*.db)')
        self.BrowLine.setText(fname[0])

    def LoadDB(self):
        if self.BrowLine.text() != '':
            if os.path.isfile(self.BrowLine.text()):
                self.browDB=self.BrowLine.text()
                self.loadButDB_1.setText('')
                self.db.setDatabaseName(self.browDB)


                con = sqlite3.connect(self.browDB)
                cur = con.cursor()
                sql = "SELECT name FROM sqlite_master WHERE TYPE = 'table'"
                Ntabl = cur.execute(sql).fetchall()
                cur.close()
                con.close()


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
            self.filter=''
            self.Name_table = rb.text()


            con = sqlite3.connect(self.BrowLine.text())
            cur = con.cursor()
            sql = "SELECT DISTINCT kod FROM F_USD"
            kod = cur.execute(sql).fetchall()
            cur.close()
            con.close()



            self.KodBox.clear()
            self.KodBox.addItem('')
            for i in range(len(kod)):
                self.KodBox.addItem(kod[i][0])
            self.loadtable()

    def loadtable(self):
        self.db.open()
        self.sqltabload = "SELECT * FROM "+self.Name_table
        if self.Name_table == "F_usd":
            self.sqltabload="SELECT torg_date, kod, quotation, num_contr FROM F_usd"
        if self.Name_table == "dataisp":
            self.sqltabload="SELECT kod, exec_date FROM dataisp"
        if self.filter!='':
            self.sqltabload = self.sqltabload+" WHERE "+self.filter
        sql=QSqlQuery(self.sqltabload)
        self.model.setQuery(sql)
        self.tableDB.setModel(self.model)
        self.connectDB = True


    def filter_use(self):
        if self.connectDB:
            self.OutButTable_2.setText('')
            self.filter=''
            if self.Name_table=='F_usd':
                Dateot = ['1900', '01', '01']
                Datedo = ['2022', '12', '31']
                if (self.filterDate2_age.text() != ''):
                    if int(self.filterDate2_age.text()) < 1000 or len(self.filterDate2_age.text()) < 4:
                        self.filterDate2_age.setText('1000')
                    Datedo[0] = self.filterDate2_age.text()

                if (self.filterDate2_month.text() != ''):
                    if int(self.filterDate2_month.text()) < 1:
                        self.filterDate2_month.setText('01')
                    if int(self.filterDate2_month.text()) > 12:
                        self.filterDate2_month.setText('12')
                    if len(self.filterDate2_month.text()) < 2:
                        self.filterDate2_month.setText('0' + self.filterDate2_month.text())
                    Datedo[1] = self.filterDate2_month.text()

                if (self.filterDate2_day.text() != ''):
                    if int(self.filterDate2_day.text()) < 1:
                        self.filterDate2_day.setText('01')

                    if int(Datedo[0]) % 4 != 0:  # високосный ли год
                        if int(self.filterDate2_day.text()) > 28 and self.filterDate2_month.text() == '02':
                            self.filterDate2_day.setText('28')
                    else:
                        if int(self.filterDate2_day.text()) > 29 and self.filterDate2_month.text() == '02':
                            self.filterDate2_day.setText('29')

                    if int(self.filterDate2_day.text()) > 30:
                        if self.filterDate2_month.text() == '04' or self.filterDate2_month.text() == '06' or self.filterDate2_month.text() == '09' or self.filterDate2_month.text() == '11':
                            self.filterDate2_day.setText('30')
                        else:
                            if int(self.filterDate2_day.text()) > 31 and self.filterDate2_month.text() != '02':
                                self.filterDate2_day.setText('31')
                    if len(self.filterDate2_day.text()) < 2:
                        self.filterDate2_day.setText('0' + self.filterDate2_day.text())
                    Datedo[2] = self.filterDate2_day.text()

                if (self.filterDate1_age.text() != ''):
                    if int(self.filterDate1_age.text()) < 1000 or len(self.filterDate1_age.text()) < 4:
                        self.filterDate1_age.setText('1000')
                    Dateot[0] = self.filterDate1_age.text()

                if (self.filterDate1_month.text() != ''):
                    if int(self.filterDate1_month.text()) < 1:
                        self.filterDate1_month.setText('01')
                    if int(self.filterDate1_month.text()) > 12:
                        self.filterDate1_month.setText('12')
                    if len(self.filterDate1_month.text()) < 2:
                        self.filterDate1_month.setText('0' + self.filterDate1_month.text())
                    Dateot[1] = self.filterDate1_month.text()

                if (self.filterDate1_day.text() != ''):
                    if int(self.filterDate1_day.text()) < 1:
                        self.filterDate1_day.setText('01')

                    if int(Dateot[0]) % 4 != 0:  # високосный ли год
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
                flag_coret = True
                if int(Dateot[0]) > int(Datedo[0]):
                    flag_coret = False
                elif int(Dateot[0]) == int(Datedo[0]):
                    if int(Dateot[1]) > int(Datedo[1]):
                        flag_coret = False
                    elif int(Dateot[1]) == int(Datedo[1]):
                        if int(Dateot[2]) > int(Datedo[2]):
                            flag_coret = False

                if flag_coret:
                    self.Error.setVisible(False)
                    self.Error.setText('')
                    DateOT = Dateot[0] + '.' + Dateot[1] + '.' + Dateot[2]
                    DateDO = Datedo[0] + '.' + Datedo[1] + '.' + Datedo[2]
                    self.filter = self.filter + "torg_date_2>='" + DateOT + "' AND torg_date_2<='" + DateDO + "'"

                    if (self.filterq1.text() != ''):
                        filt3 = 'CAST(quotation as real)>=' + self.filterq1.text()
                        self.filter = self.filter + ' AND ' + filt3

                    if (self.filterq2.text() != ''):
                        filt4 = 'CAST(quotation as real)<=' + self.filterq2.text()
                        self.filter = self.filter + ' AND ' + filt4

                    if (self.KodBox.currentText() != ''):
                        filt5 = "kod = '" + self.KodBox.currentText() + "'"
                        self.filter = self.filter + ' AND ' + filt5

                    self.loadtable()
                else:
                    self.Error.setVisible(True)
                    self.Error.setText('Некоректно выбран диапазон дат')

        else:
            self.OutButTable_2.setText('Загрузите БД')
            EmptyTab=QSqlTableModel()
            self.tableDB.setModel(EmptyTab)

def application():
    app=QApplication(sys.argv)
    window = MainWindow()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(window)
    widget.setMinimumWidth(1050)
    widget.setMinimumHeight(630)
    widget.show()
    app.exec()

if __name__ == "__main__":
    application()