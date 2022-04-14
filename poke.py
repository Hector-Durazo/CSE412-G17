from cProfile import label
import sys, psycopg2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication,QSlider,QComboBox, QMainWindow, QHeaderView, QAbstractItemView, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtCore import Qt
def loaddata():
    try:
        connection = psycopg2.connect(user = "postgres", password = "251557251557hd", host = "127.0.0.1"
                                        , port = "5432", database = "postgres")
        cursor = connection.cursor()
        print("Opened database successfully")
        cursor.execute("SELECT pokemon.identifier FROM pokemon WHERE pokemon.identifier LIKE 's%'")
        records = cursor.fetchall()
        print(records)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

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
        heightLabel = QLabel(self)
        heightLabel.setText('Max height (M)')
        heightLabel.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(heightLabel)

        slider1 = QSlider(Qt.Horizontal)
        slider1.setMinimum(0)
        slider1.setMaximum(20)
        slider1.setValue(0)
        labelLayout.addWidget(slider1,0, Qt.AlignBottom)
        label3 = QLabel(self)
        label3.setText('0')
        label3.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(label3, 0, Qt.AlignTop)
        slider1.valueChanged.connect(label3.setNum)


        # Add Slider to VBox
        weightLabel = QLabel(self)
        weightLabel.setText('Max Weight (Kg)')
        weightLabel.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(weightLabel)

        slider2 = QSlider(Qt.Horizontal)
        slider2.setMinimum(0)
        slider2.setMaximum(1000)
        slider2.setValue(0)
        labelLayout.addWidget(slider2, 0, Qt.AlignBottom)
        label4 = QLabel(self)
        label4.setText('0')
        label4.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(label4 , 0, Qt.AlignTop)
        slider2.valueChanged.connect(label4.setNum)


        # Add type combobox to VBox
        combobox = QComboBox()
        combobox.addItems(['All', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'])
        labelLayout.addWidget(combobox)


        # Add Region combobox to VBox
        combobox = QComboBox()
        combobox.addItems([ 'All', 'Kanto', 'Johto', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos'])
        labelLayout.addWidget(combobox)


        # Add Button to VBox
        button1 = QPushButton('Search')
        button1.clicked.connect(table._addRow)
        labelLayout.addWidget(button1)


        # Add widgets to mainLayout
        mainLayout.addWidget(vwidget)
        mainLayout.addWidget(table)

        self.setLayout(mainLayout)

loaddata()
app = QApplication(sys.argv)
win = window()
win.show()
sys.exit(app.exec_())
#window()