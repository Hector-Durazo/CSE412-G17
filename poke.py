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
        self.resize(1200, 600)
        self.setWindowTitle("Pokemon Database")
        mainLayout = QHBoxLayout()
        # change window title icon to pokemon logo
        self.setWindowIcon(QtGui.QIcon("poke.png"))
        # change window background to dark grey


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
        vwidget2.setFixedWidth(400)
       

        abilitiesLabel = QLabel()
        iconLabel = QLabel()
        regionLabel = QLabel()
        typeLabel = QLabel()
        weightHightLabel = QLabel()

        abilitiesLabel.setAlignment(Qt.AlignLeft)
        iconLabel.setAlignment(Qt.AlignCenter)
        regionLabel.setAlignment(Qt.AlignLeft)
        typeLabel.setAlignment(Qt.AlignLeft)
        weightHightLabel.setAlignment(Qt.AlignLeft)

        # increase font size
        abilitiesLabel.setFont(QtGui.QFont("Arial", 12))
        iconLabel.setFont(QtGui.QFont("Arial", 12))
        regionLabel.setFont(QtGui.QFont("Arial", 12))
        typeLabel.setFont(QtGui.QFont("Arial", 12))
        weightHightLabel.setFont(QtGui.QFont("Arial", 12))


        
        labelLayout2.addWidget(checkbox)
        labelLayout2.addWidget(iconLabel)
        labelLayout2.addWidget(typeLabel)
        labelLayout2.addWidget(regionLabel)
        labelLayout2.addWidget(abilitiesLabel)
        labelLayout2.addWidget(weightHightLabel)



        # Add Pokeball image to VBox
        imagelabel = QLabel()
        image = QPixmap('poke.png')
        image = image.scaled(200, 200, Qt.KeepAspectRatio)
        imagelabel.setPixmap(image)
        imagelabel.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(imagelabel)

        # Add search bar to VBox
        text1 = QLineEdit()
        text1.setPlaceholderText('Search')
        labelLayout.addWidget(text1)
        #text1.textChanged.connect(valueChanged)


        heightLabel = QLabel(self)
        heightLabel.setText('Max height (M)')
        heightLabel.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(heightLabel)
        slider1 = QSlider(Qt.Horizontal)
        slider1.setMinimum(0)
        slider1.setMaximum(30)
        slider1.setValue(30)
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
        slider2.setValue(1000)
        labelLayout.addWidget(slider2, 0, Qt.AlignBottom)
        label4 = QLabel(self)
        label4.setText('0')
        label4.setAlignment(Qt.AlignCenter)
        labelLayout.addWidget(label4 , 0, Qt.AlignTop)
        slider2.valueChanged.connect(label4.setNum)


        # Add type combobox to VBox
        combobox = QComboBox()
        combobox.addItems([ 'All', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 
                            'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'])
        labelLayout.addWidget(combobox)


        # Add Region combobox to VBox
        combobox1 = QComboBox()
        combobox1.addItems([ 'All', 'Kanto', 'Johto', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos'])
        combobox1.setCurrentIndex = 'All'
        labelLayout.addWidget(combobox1)

        def valueChanged(self):
            heighttemp = slider1.value()
            heightVar = str(heighttemp)
            weightTemp= slider2.value()
            weightVar = str(weightTemp)
            fromVar = "pokemon"
            nameVar = text1.text()
            typeVar = combobox.currentText().lower()
            regionVar = combobox1.currentText().lower()
            if typeVar != 'all':
                 fromVar = fromVar+", pokemon_types, types"
            if regionVar != 'all':
                fromVar = fromVar+", encounters, locations, location_areas, regions"
            sqlquery= sqlquery = "SELECT DISTINCT(pokemon.pokemon_id), pokemon.identifier, pokemon.species_id, pokemon.height, pokemon.weight, pokemon.base_experience FROM "+ fromVar+" WHERE pokemon.height < "+heightVar+" AND pokemon.weight < "+weightVar
            if typeVar != 'all':
                sqlquery = sqlquery + """   AND pokemon.pokemon_id = pokemon_types.pokemon_id 
                                            AND pokemon_types.type_id = types.type_id 
                                            AND types.identifier LIKE '"""+typeVar+"'"
            if regionVar != 'all':
               sqlquery= sqlquery + """ AND pokemon.pokemon_id = encounters.pokemon_id 
                                        AND location_areas.location_area_id = encounters.location_area_id 
                                        AND location_areas.location_id = locations.location_id 
                                        AND locations.region_id = regions.region_id 
                                        AND regions.identifier 
                                        LIKE '"""+ regionVar +"'"
            if nameVar != "":
               sqlquery = sqlquery + " AND pokemon.identifier LIKE '"+nameVar+"%'"
            sqlquery = sqlquery + " ORDER BY pokemon.identifier"
            
            cur.execute(sqlquery)
            tableUpdate(cur)

        slider2.valueChanged.connect(valueChanged)
        slider1.valueChanged.connect(valueChanged)
        combobox.currentIndexChanged.connect(valueChanged)
        combobox1.currentIndexChanged.connect(valueChanged)
        text1.textChanged.connect(valueChanged)


        # select row in table
        def tableClicked(self):
            row = table.currentRow()
            #get the data from the table
            data = table.item(row, 1).text()

            # checks if shiny
            if checkbox.isChecked():
                icons = 'shiny'
            else:
                icons = 'icons'


            #print('icons: '+ icons)
            for icon in os.listdir(icons):
                if icon == data + '.png':
                    icon = QPixmap( icons +'/' + data + '.png')
                    icon = icon.scaled(400, 400, Qt.KeepAspectRatio)
                    iconLabel.setPixmap(icon)
                    iconLabel.setAlignment(Qt.AlignCenter)
                    break
                else:
                    icon = QPixmap( 'unknown-item.png')
                    icon = icon.scaled(300, 300, Qt.KeepAspectRatio)
                    iconLabel.setPixmap(icon)
                    #iconLabel.setText('No Icon')
                    iconLabel.setAlignment(Qt.AlignCenter)
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

            #show pokemon region
            sqlquery ="""   SELECT DISTINCT regions.identifier FROM pokemon, encounters, locations, location_areas, regions 
                            WHERE pokemon.pokemon_id = encounters.pokemon_id 
                            AND location_areas.location_area_id = encounters.location_area_id 
                            AND location_areas.location_id = locations.location_id 
                            AND locations.region_id = regions.region_id 
                            AND pokemon.pokemon_id = '""" + str(data) + """';"""
            cur.execute(sqlquery)
            region = cur.fetchall()
            #print(region)
            if region.__len__() == 0:
                region = 'No region'
            else:
                region = [i[0] for i in region]
                region = ', '.join(region)
            regionLabel.setText('Region: ' + region)

            #show pokemon type
            sqlquery ="""   SELECT DISTINCT types.identifier FROM pokemon, pokemon_types, types
                            WHERE pokemon.pokemon_id = pokemon_types.pokemon_id
                            AND pokemon_types.type_id = types.type_id
                            AND pokemon.pokemon_id = '""" + str(data) + """';"""
            cur.execute(sqlquery)
            types = cur.fetchall()
            if types.__len__() == 0:
                types = 'No types'
            else:
                types = [i[0] for i in types]
                types = ', '.join(types)
            typeLabel.setText('Types: ' + types)

            #show pokemon weight and hight
            weight = table.item(row, 3).text()
            height = table.item(row, 2).text()
            weightHightLabel.setText('Weight: ' + weight + ' Kg' + '\n\n' + 'Height: ' + height + ' M')


                    

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
        connection = psycopg2.connect(user = "postgres", password = "251557251557hd", host = "127.0.0.1"
                                        , port = "5432", database = "postgres")
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