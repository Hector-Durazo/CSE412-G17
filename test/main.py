import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
import psycopg2


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("tabletutorial.ui",self)
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 350)
        self.tableWidget.setHorizontalHeaderLabels(["City","Country","Subcountry"])
        self.loaddata()

    def loaddata(self):
        connection = psycopg2.connect(user = "postgres", password = "251557251557hd", host = "127.0.0.1"
                                        , port = "5432", database = "postgres")
        cur = connection.cursor()
        sqlstr = 'SELECT * FROM pokemon'

        tablerow=0
        results = cur.execute(sqlstr)
        self.tableWidget.setRowCount(40)
        for row in results:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            tablerow+=1
# main
app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(850)
widget.setFixedWidth(1120)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")