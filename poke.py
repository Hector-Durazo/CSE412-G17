from cProfile import label
from logging import PlaceHolder
import os
import sys, psycopg2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5 import QtSql
from PyQt5.QtWidgets import QApplication,QSlider,QComboBox, QMainWindow, QHeaderView, QAbstractItemView, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtCore import Qt

class window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1280, 600)

        mainLayout = QHBoxLayout()
        
        # Make VBox for window layout
        labelLayout = QVBoxLayout()
        vwidget = QWidget()
        vwidget.setLayout(labelLayout)
        vwidget.setContentsMargins(50,0,50,0)
        vwidget.setFixedWidth(300)


        #add checkbox to vbox
        checkbox = QtWidgets.QCheckBox("Show Shiny")
        checkbox.setChecked(False)
        

        # Make new VBox
        labelLayout2 = QVBoxLayout()
        vwidget2 = QWidget()
        vwidget2.setLayout(labelLayout2)
        vwidget2.setContentsMargins(50,0,50,0)
        vwidget2.setFixedWidth(400)
        abilitiesLabel = QLabel()
        abilitiesLabel.setAlignment(Qt.AlignCenter)
        iconLabel = QLabel()
        iconLabel.setAlignment(Qt.AlignCenter)
        labelLayout2.addWidget(checkbox)
        labelLayout2.addWidget(iconLabel)
        labelLayout2.addWidget(abilitiesLabel)





        # Add Pokeball image to VBox
        imagelabel = QLabel()
        image = QPixmap('poke.png')
        image = image.scaled(200, 200, Qt.KeepAspectRatio)
        imagelabel.setPixmap(image)
        imagelabel.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(imagelabel)


        def search(self):
            sqlquery = "SELECT * FROM pokemon WHERE pokemon.identifier LIKE'" + text1.text() + "%'"
            cur.execute(sqlquery)
            tableUpdate(cur)

  
        text1 = QLineEdit()
        text1.setPlaceholderText('Search')
        labelLayout.addWidget(text1)
        text1.textChanged.connect(search)


        # Add Slider to VBox
        def slider1Changed(self):
            sqlquery = "SELECT * FROM pokemon WHERE pokemon.height < " + str(slider1.value())
            cur.execute(sqlquery)
            tableUpdate(cur)
        heightLabel = QLabel(self)
        heightLabel.setText('Max height (M)')
        heightLabel.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(heightLabel)
        slider1 = QSlider(Qt.Horizontal)
        slider1.setMinimum(0)
        slider1.setMaximum(30)
        slider1.setValue(0)
        labelLayout.addWidget(slider1,0, Qt.AlignBottom)
        label3 = QLabel(self)
        label3.setText('0')
        label3.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(label3, 0, Qt.AlignTop)
        slider1.valueChanged.connect(label3.setNum)
        slider1.valueChanged.connect(slider1Changed)
        

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

        
        # select row in table
        def tableClicked(self):
            row = table.currentRow()
            #get the data from the table
            data = table.item(row, 1).text()
            print(data)
            # select icon from icons folder

            # checks if shiny
            if checkbox.isChecked():
                icons = 'shiny'
            else:
                icons = 'icons'


            print('icons: '+ icons)
            for icon in os.listdir(icons):
                if icon == data + '.png':
                    icon = QPixmap( icons +'/' + data + '.png')
                    icon = icon.scaled(400, 400, Qt.KeepAspectRatio)
                    iconLabel.setPixmap(icon)
                    iconLabel.setAlignment(Qt.AlignCenter)
                #else:

            #show pokemon info from database
            data = table.item(row, 0).text()
            sqlquery ="""   SELECT identifier
                            FROM abilities, pokemon_abilities
                            WHERE abilities.ability_id = pokemon_abilities.ability_id
                            AND pokemon_abilities.pokemon_id = """ + str(data) + ";"
            cur.execute(sqlquery)
            abilities = cur.fetchall()
            abilities = [i[0] for i in abilities]
            abilities = ', '.join(abilities)
            abilitiesLabel.setText('Abilities: ' + abilities)

                    


        #create table
        table = QTableWidget()
        table.setFixedWidth(555)
        table.setRowCount(0)
        table.setColumnCount(4)
        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 150)
        table.setColumnWidth(2, 150)
        table.setColumnWidth(3, 100)
        table.setRowHeight(0, 30)
        table.setHorizontalHeaderLabels(['id','Name', 'Height', 'Weight'])
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.cellClicked.connect(tableClicked)

    
        def tableUpdate(cur):
            table.setRowCount(cur.rowcount)
            tablerow= 0
            for row in cur.fetchall():
                table.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                table.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                table.setItem(tablerow,2,QTableWidgetItem(str(row[3]/10)))
                table.setItem(tablerow,3,QTableWidgetItem(str(row[4]/10)))
                tablerow += 1
        connection = psycopg2.connect(user = "postgres", password = "Disney903", host = "127.0.0.1" ,port = "5432", database = "Pokemon")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM pokemon"
        cur.execute(sqlquery)
        tableUpdate(cur)




        # Add widgets to mainLayout
        mainLayout.addWidget(vwidget)
        mainLayout.addWidget(table)
        mainLayout.addWidget(vwidget2)
        self.setLayout(mainLayout)

app = QApplication(sys.argv)
win = window()
win.show()
sys.exit(app.exec_())
#window()