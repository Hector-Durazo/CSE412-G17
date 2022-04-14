from cProfile import label
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication,QSlider, QMainWindow, QHeaderView, QAbstractItemView, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtCore import Qt

class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__(1,4)
        self.setHorizontalHeaderLabels(list('ABC'))
        self.verticalHeader().setDefaultSectionSize(20)
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
        self.resize(1280, 600)
        
        mainLayout = QHBoxLayout()
        table = TableWidget()

        # Make VBox for window layout
        labelLayout = QVBoxLayout()
        vwidget = QWidget()
        vwidget.setLayout(labelLayout)
        vwidget.setContentsMargins(50,0,50,0)
        vwidget.setFixedWidth(400)


        # Add Pokeball image to VBox
        imagelabel = QLabel(self)
        image = QPixmap('poke.png')
        image = image.scaled(200, 200, Qt.KeepAspectRatio)
        imagelabel.setPixmap(image)
        imagelabel.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(imagelabel)


        # Add Searchbar to VBox
        text1 = QLineEdit()
        text1.setPlaceholderText('Search')
        labelLayout.addWidget(text1)


        # Add Slider to VBox
        slider1 = QSlider(Qt.Horizontal)
        slider1.setMinimum(0)
        slider1.setMaximum(4000)
        slider1.setValue(0)
        labelLayout.addWidget(slider1,0, Qt.AlignBottom)
        label3 = QLabel(self)
        label3.setText('0')
        label3.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(label3, 0, Qt.AlignTop)
        slider1.valueChanged.connect(label3.setNum)


        # Add Slider to VBox
        slider2 = QSlider(Qt.Horizontal)
        slider2.setMinimum(0)
        slider2.setMaximum(4000)
        slider2.setValue(0)
        labelLayout.addWidget(slider2, 0, Qt.AlignBottom)
        label4 = QLabel(self)
        label4.setText('0')
        label4.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(label4 , 0, Qt.AlignTop)
        slider2.valueChanged.connect(label4.setNum)


        # Add widgets to mainLayout
        mainLayout.addWidget(vwidget)
        mainLayout.addWidget(table)

        self.setLayout(mainLayout)


app = QApplication(sys.argv)
win = window()
win.show()
sys.exit(app.exec_())
#window()