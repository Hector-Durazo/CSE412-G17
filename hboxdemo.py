import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QAbstractItemView, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtCore import Qt

class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__(1,5)
        self.setHorizontalHeaderLabels(list('ABCDE'))
        self.verticalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(250)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
    def _addRow(self):
        rowCount = self.rowCount()
        self.insertRow(rowCount)
    
    def _removeRow(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)
    
    def _copyRow(self):
        self.insertRow(self.rowCount())
        rowCount = self.rowCount()
        columnCount = self.columnCount()
        
        for j in range(columnCount):
            if not self.item(rowCount-2, j) is None:
                self.setItem(rowCount-1, j, QTableWidgetItem(self.item(rowCount-2, j).text()))

class window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1600, 600)
        
        mainLayout = QHBoxLayout()
        table = TableWidget()
        
        labelLayout = QVBoxLayout()
        #label1 = QLabel("Pokemon Search")
        #labelLayout.addWidget(label1)
        text1 = QLineEdit()
        labelLayout.addWidget(text1)
        #label1.move(50,50)
        mainLayout.addLayout(labelLayout)
        mainLayout.addWidget(table)
        
        self.setLayout(mainLayout)

#win.setGeometry(200, 200, 300, 300)
#win.setWindowTitle("App pls")
app = QApplication(sys.argv)
win = window()
win.show()
sys.exit(app.exec_())
#window()