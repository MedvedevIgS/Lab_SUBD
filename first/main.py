from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtSql import *
from PyQt6.QtGui import QIntValidator, QDoubleValidator
import sqlite3
import os

import sys

class addWindow(QMainWindow):
    def __init__(self, mainWin):
        super(addWindow, self).__init__()
        self.MainWin=mainWin
        self.table = self.MainWin.model
        uic.loadUi("AddForm.ui", self)
        self.Error.setVisible(False)
        self.quo.setValidator(QDoubleValidator())
        self.num_c.setValidator(QIntValidator())
        self.torgd_day.setValidator(QIntValidator())
        self.torgd_mount.setValidator(QIntValidator())
        self.torgd_age.setValidator(QIntValidator())
        self.addBut.clicked.connect(self.click_add)
        self.kod1.setValidator(QIntValidator())
        self.kod2.setValidator(QIntValidator())
        self.kod=''



    def click_add(self):
        flagDateChang = False
        if self.quo.text() == '' or self.kod1.text() == '' or self.num_c.text() == '' or self.kod2.text() == '':
            self.Error.setVisible(True)
            self.Error.setText('Заполните все поля')
        else:
            if self.torgd_day.text() == '' or self.torgd_mount.text() == '' or self.torgd_age.text() == '':
                self.Error.setVisible(True)
                self.Error.setText('Введите дату полностью')
            elif len(self.kod1.text())<2 or len(self.kod2.text())<2 or int(self.kod1.text())>12:
                    self.Error.setVisible(True)
                    self.Error.setText('Некорекктная запись кода')
            else:
                flagkod = False
                self.kod="FUSD_"+self.kod1.text()+"_"+self.kod2.text()
                for i in self.MainWin.kod:
                    if self.kod in i:
                        flagkod = True
                if flagkod:
                    if int(self.torgd_age.text()) < 1000 or len(self.torgd_age.text()) < 4:
                        self.self.torgd_age.setText('1000')
                        flagDateChang = True
                    if int(self.torgd_mount.text()) < 1:
                        self.torgd_mount.setText('01')
                        flagDateChang = True
                    if int(self.torgd_mount.text()) > 12:
                        self.torgd_mount.setText('12')
                        flagDateChang = True
                    if len(self.torgd_mount.text()) < 2:
                        self.torgd_mount.setText('0' + self.torgd_mount.text())
                        flagDateChang = True
                    print('4')

                    if int(self.torgd_day.text()) < 1:
                        self.torgd_day.setText('01')
                        flagDateChang = True

                    if int(self.torgd_age.text()) % 4 != 0:  # високосный ли год
                        if int(self.torgd_day.text()) > 28 and self.torgd_day.text() == '02':
                            self.torgd_day.setText('28')
                            flagDateChang = True
                    else:
                        if int(self.torgd_day.text()) > 29 and self.torgd_day.text() == '02':
                            self.torgd_day.setText('29')
                            flagDateChang = True
                    if int(self.torgd_day.text()) > 30:
                        if self.torgd_mount.text() == '04' or self.torgd_mount.text() == '06' or self.torgd_mount.text() == '09' or self.torgd_mount.text() == '11':
                            self.torgd_day.setText('30')
                            flagDateChang = True
                        else:
                            if int(self.torgd_day.text()) > 31 and self.torgd_mount.text() != '02':
                                self.torgd_day.setText('31')
                                flagDateChang = True
                    if len(self.torgd_day.text()) < 2:
                        self.torgd_day.setText('0' + self.torgd_day.text())
                        flagDateChang = True
                    if flagDateChang:
                        self.Error.setVisible(True)
                        self.Error.setText('Дата была изменена на более корректную')
                    else:
                        torgdate = self.torgd_day.text() + '.' + self.torgd_mount.text() + '.' + self.torgd_age.text()
                        torgdatRevers = self.torgd_age.text() + '.' + self.torgd_mount.text() + '.' + self.torgd_day.text()
                        self.Error.setVisible(False)
                        self.Error.setText('')
                        sql = "INSERT INTO F_usd VALUES ('" + torgdate + "', '" + self.kod + "', '" + self.quo.text() + "', " + self.num_c.text() + ", '" + torgdatRevers + "')"
                        print(sql)
                        qry = QSqlQuery()
                        qry.prepare(sql)
                        qry.exec()
                        self.MainWin.loadtable()
                        self.Error.setVisible(True)
                        self.Error.setText('Запись добавлена')
                        self.quo.setText('')
                        self.kod1.setText('')
                        self.kod2.setText('')
                        self.torgd_day.setText('')
                        self.torgd_mount.setText('')
                        self.torgd_age.setText('')
                        self.num_c.setText('')

                else:
                    error_kod=QMessageBox(parent=self, text="Hello World")
                    error_kod.setInformativeText("Добавить код?")
                    error_kod.setWindowTitle("Код не найден")
                    error_kod.setStandardButtons(QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)
                    error_kod.buttonClicked.connect(self.but_action)
                    ret=error_kod.exec()


    def but_action(self, btn):
        if btn.text()=="OK":
            buf=self.kod.split('_')
            print(buf)
            date = '15.' + buf[1] + '.19' + buf[2]
            reverdate = '19' + buf[2] + '.' + buf[1] + '.15'
            sql = "INSERT INTO dataisp VALUES ('" + self.kod + "', '" + date + "', '" + reverdate + "')"
            print(sql)
            qry = QSqlQuery()
            qry.prepare(sql)
            qry.exec()
            self.MainWin.loadtable()
            self.MainWin.appdate_KodBox()





class changWindow(QMainWindow):
    def __init__(self, ind, mainWin):
        super(changWindow, self).__init__()
        self.MainWin=mainWin
        self.table = self.MainWin.model
        self.inputDat = ind
        uic.loadUi("ChangForm.ui", self)
        self.Error.setVisible(False)
        self.quo.setValidator(QDoubleValidator())
        self.num_c.setValidator(QIntValidator())
        self.torgd.setText(self.inputDat[0])
        self.kod.setText(self.inputDat[1])
        self.quo.setText(self.inputDat[2])
        self.num_c.setText(self.inputDat[3])
        self.changBut.clicked.connect(self.click_chang)

    def click_chang(self):
        if self.quo.text() == '' or self.kod.text() == '' or self.torgd.text() == '' or self.num_c.text() == '':
            self.Error.setVisible(True)
            self.Error.setText('Заполните все поля')
        else:
            provDat = self.torgd.text().split('.')
            provKod = self.kod.text().split('_')
            if len(provDat) != 3 or len(provDat[0]) != 2 or len(provDat[1]) != 2 or len(provDat[2]) != 4 or provDat[0].isdigit() != True or provDat[1].isdigit() != True or provDat[2].isdigit() != True:
                self.Error.setVisible(True)
                self.Error.setText('Некорекктная запись даты')
            elif len(provKod) != 3 or provKod[0] != 'FUSD' or len(provKod[1]) != 2 or len(provKod[2]) != 2 or provKod[1].isdigit() != True or provKod[2].isdigit() != True:
                self.Error.setVisible(True)
                self.Error.setText('Некорекктная запись кода')
            else:
                torgdatRevers = provDat[2] + '.' + provDat[1] + '.' + provDat[0]
                self.Error.setVisible(False)
                self.Error.setText('')
                sql = "UPDATE F_usd SET torg_date = '" + self.torgd.text() + "', kod = '" + self.kod.text() + "', quotation = '" + self.quo.text() + "', num_contr = " + self.num_c.text() + ", torg_date_2 = '" + torgdatRevers + "' WHERE torg_date = '" + self.inputDat[0] + "' AND kod = '" + self.inputDat[1] + "' AND quotation = '" + self.inputDat[2] + "' AND num_contr = " + self.inputDat[3]
                qry = QSqlQuery()
                qry.prepare(sql)
                qry.exec()
                self.MainWin.loadtable()
                self.inputDat = [self.torgd.text(), self.kod.text(), self.quo.text(), self.num_c.text()]
                self.Error.setVisible(True)
                self.Error.setText('Изменения добавлены')



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.connectDB = False
        self.browDB=''
        self.kod=[]
        self.EmptyTab = QSqlTableModel()
        self.filter = ''
        self.Name_table = ''
        self.model = QSqlTableModel()
        self.sort_F_usd='torg_date_2'
        self.sort_dataisp = 'exec_date_2'
        self.db=QSqlDatabase.addDatabase('QSQLITE')
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
        self.ChangBut.clicked.connect(self.chaninBD)


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
        self.RB1.setVisible(False)
        self.RB2.setVisible(False)
        self.RB1.toggled.connect(self.RB_z)
        self.RB2.toggled.connect(self.RB_z)

    def addinBD(self):
        if self.connectDB:
            self.Error.setVisible(False)
            self.Error.setText('')
            global widget2
            addWind = addWindow(self)
            widget2 = QtWidgets.QStackedWidget()
            widget2.addWidget(addWind)
            widget2.setMinimumWidth(565)
            widget2.setMinimumHeight(299)
            widget2.show()
        else:
            self.ErrorBUT.setVisible(True)
            self.ErrorBUT.setText('Для добавления записи нужно подключить БД')

    def delinBD(self):
        select1 = self.tableDB.selectedIndexes()
        row=[]
        col=[]
        for i in select1:
            row.append(i.row())
            col.append(i.column())
        if self.Name_table=="F_usd":
            colF_usd=[]
            rowF_usd=[]
            j=-1
            for i in range(len(col)):
                if i%5==0:
                    rowF_usd.append(row[i])
                    colF_usd.append([])
                    j+=1
                colF_usd[j].append(col[i])
            flagcol=True
            for i in colF_usd:
                if i!=[0, 1, 2, 3, 4]:
                    flagcol = False
            print(rowF_usd)


            if flagcol:
                self.ErrorBUT.setText('')
                self.ErrorBUT.setVisible(False)
                for i in range(len(rowF_usd)):
                    ind0 = self.tableDB.model().index(rowF_usd[i], 0, select1[i].parent())
                    ind1 = self.tableDB.model().index(rowF_usd[i], 1, select1[i + 1].parent())
                    sql = "DELETE FROM F_usd WHERE torg_date = '" + ind0.data() + "' AND kod = '" + ind1.data() + "'"
                    print(sql)
                    qry = QSqlQuery()
                    qry.prepare(sql)
                    qry.exec()
                    self.loadtable()
            else:
                self.ErrorBUT.setText('Выделите строки полностью')
                self.ErrorBUT.setVisible(True)
        if self.Name_table=="dataisp":
            col_daisp = []
            row_daisp= []
            j = -1
            for i in range(len(col)):
                if i % 2 == 0:
                    row_daisp.append(row[i])
                    col_daisp.append([])
                    j += 1
                col_daisp[j].append(col[i])
            flagcol = True
            for i in col_daisp:
                if i != [0, 1]:
                    flagcol = False
            print(row_daisp)
            if flagcol:
                self.ErrorBUT.setText('')
                self.ErrorBUT.setVisible(False)
                for i in range(len(row_daisp)):
                    ind0 = self.tableDB.model().index(row_daisp[i], 0, select1[i].parent())
                    sql = "DELETE FROM dataisp WHERE kod = '" + ind0.data() + "'"
                    print(sql)
                    qry = QSqlQuery()
                    qry.prepare(sql)
                    qry.exec()
                    self.loadtable()
                    self.appdate_KodBox()
            else:
                self.ErrorBUT.setText('Выделите строки полностью')
                self.ErrorBUT.setVisible(True)



    def chaninBD(self):
        if self.Name_table=="F_usd":
            select1 = self.tableDB.selectedIndexes()
            col = []
            for i in select1:
                col.append(i.column())
            if col == [0, 1, 2, 3, 4]:
                self.ErrorBUT.setText('')
                self.ErrorBUT.setVisible(False)
                self.ErrorBUT.setText('')
                self.ErrorBUT.setVisible(False)
                ind0 = self.tableDB.model().index(select1[0].row(), 0, select1[0].parent()).data()
                ind1 = self.tableDB.model().index(select1[1].row(), 1, select1[1].parent()).data()
                ind2 = self.tableDB.model().index(select1[2].row(), 2, select1[2].parent()).data()
                ind3 = self.tableDB.model().index(select1[3].row(), 3, select1[3].parent()).data()
                ind = [str(ind0), str(ind1), str(ind2), str(ind3)]
                global widget3
                changWind = changWindow(ind, self)
                widget3 = QtWidgets.QStackedWidget()
                widget3.addWidget(changWind)
                widget3.setMinimumWidth(565)
                widget3.setMinimumHeight(299)
                widget3.show()
            else:
                self.ErrorBUT.setText('Выделите 1 строку (полностью)')
                self.ErrorBUT.setVisible(True)
        else:
            self.ErrorBUT.setText('Записи можно изменять только в F_usd')
            self.ErrorBUT.setVisible(True)

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
        self.LoadDB()

    def LoadDB(self):
        if self.BrowLine.text() != '':
            if os.path.isfile(self.BrowLine.text()):
                self.browDB=self.BrowLine.text()
                con = sqlite3.connect(self.browDB)
                cur = con.cursor()
                sql = "SELECT name FROM sqlite_master WHERE TYPE = 'table'"
                Ntabl = cur.execute(sql).fetchall()
                cur.close()
                con.close()
                print(Ntabl)
                if Ntabl[1][0]=='F_usd' and Ntabl[0][0]=='dataisp' and len(Ntabl)==2:
                    self.loadButDB_1.setText('')
                    self.db.setDatabaseName(self.browDB)
                    self.RB1.setVisible(True)
                    self.RB2.setVisible(True)
                    self.connectDB = True
                    self.RB1.setChecked(True)
                else:
                    self.loadButDB_1.setText('Некорректная БД')
                    self.connectDB = False
                    self.RB1.setVisible(False)
                    self.RB2.setVisible(False)
                    rb = self.sender()
                    rb.setChecked(False)
            else:
                self.loadButDB_1.setText('Указан неверный путь')
                self.connectDB = False
                self.RB1.setVisible(False)
                self.RB2.setVisible(False)
                rb = self.sender()
                rb.setChecked(False)
        else:
            self.loadButDB_1.setText('Укажите Путь')
            self.connectDB = False
            self.RB1.setVisible(False)
            self.RB2.setVisible(False)
            rb = self.sender()
            rb.setChecked(False)

    def RB_z(self):
        rb = self.sender()
        if rb.isChecked():
            self.filter=''
            self.Name_table = rb.text()
            self.appdate_KodBox()
            self.loadtable()

    def appdate_KodBox(self):
        self.KodBox.clear()
        self.KodBox.addItem('')
        self.kod = self.getmasskod()
        for i in range(len(self.kod)):
            self.KodBox.addItem(self.kod[i][0])


    def getmasskod(self):
        con = sqlite3.connect(self.BrowLine.text())
        cur = con.cursor()
        sql = "SELECT DISTINCT kod FROM dataisp"
        kod = cur.execute(sql).fetchall()
        return kod

    def loadtable(self):
        self.db.open()
        if self.Name_table == "F_usd":
            self.sqltabload = """SELECT torg_date, kod, quotation, num_contr, round (CAST(quotation as REAL)/CAST(quo2 as REAL),4) xk
               FROM 
               (SELECT torg_date, kod, quotation, num_contr, torg_date_2, COALESCE(quo2, quotation) quo2, COALESCE(kod2, kod) kod2, COALESCE(num2, num1) num2
                 FROM
                 (SELECT *, row_number() over(PARTITION BY kod) num1 FROM F_usd) as T1
                 LEFT JOIN 
                 (SELECT quotation quo2, kod kod2, row_number() over(PARTITION BY kod) num2 FROM F_usd) as T2
               ON T1.num1-2=T2.num2 AND  T1.kod=T2.kod2
            """
            #self.sqltabload = "SELECT torg_date, kod, quotation, num_contr FROM F_usd"
            if self.filter!='':
                self.sqltabload+=" WHERE "+self.filter+")"
            else:
                self.sqltabload +=")"
            self.sqltabload+=" ORDER BY "+self.sort_F_usd
        if self.Name_table == "dataisp":
            self.sqltabload = "SELECT kod, exec_date FROM dataisp"
            self.sqltabload += " ORDER BY " + self.sort_dataisp
        print(self.sqltabload)
        sql = QSqlQuery(self.sqltabload)
        self.model.setQuery(sql)
        self.tableDB.setModel(self.model)

    def filter_use(self):
        if self.connectDB:
            self.OutButTable_2.setText('')
            self.filter = ''
            self.setFilter()
            self.loadtable()
        else:
            self.OutButTable_2.setText('Загрузите БД')
            self.tableDB.setModel(self.EmptyTab)

    def setFilter(self):
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
            print(self.filter)



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