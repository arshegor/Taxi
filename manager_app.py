from PyQt5.QtWidgets import QComboBox, QTabWidget, QAction, QLineEdit, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QMessageBox, QMenuBar, QMenu
import sys
import psycopg2

class ManagerWindow(QWidget):
    def __init__(self, login):
        super(ManagerWindow, self).__init__()

        self.login = login

        self.vbox = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.driver_tab = QWidget()
        self.order_tab = QWidget()
        self.cars_tab = QWidget()
        self.users_tab = QWidget()
        self.logout_tab = QWidget()
        self.carsdrivers_tab = QWidget()

        self._create_books_tab()
        self._create_driver_tab()
        self._create_cars_tab()
        self._create_carsdrivers_tab()
        self._create_users_tab()
        self._createLogoutTab()

        self.vbox.addWidget(self.tabs)

        self.setLayout(self.vbox)


    def _create_carsdrivers_tab(self):
        self.tabs.addTab(self.carsdrivers_tab, "Cars/Drivers")

        self.vboxCarsDrivers = QVBoxLayout()

        self.updateCarsDriversButton = QPushButton("Update")

        self.carsdriversTable = QTableWidget()
        self.carsdriversTable.setColumnCount(4)
        

        self.carsdriversTable.setHorizontalHeaderLabels(["Driver", "Car", "", ""])
        
        self.vboxCarsDrivers.addWidget(self.carsdriversTable)
        self.vboxCarsDrivers.addWidget(self.updateCarsDriversButton)

        self._update_carsdrivers_table()

        self.carsdrivers_tab.setLayout(self.vboxCarsDrivers)

        self.updateCarsDriversButton.clicked.connect(self._update_carsdrivers_table)

    def _update_carsdrivers_table(self):
        self.carsdriversTable.setRowCount(0)
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
                    
        cursor.execute('SELECT * FROM taxi.carsdrivers')
        records = list(cursor.fetchall())

        self.carsdriversTable.setRowCount(len(records) + 1)

        i = 0
        
        for r in records:
            r = list(r)
            self.carsdriversTable.setCellWidget(i, 1, self._get_cdcar_cmb(r[1]))
            self.carsdriversTable.setCellWidget(i, 0, self._get_cddriver_cmb(r[0]))
           
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.carsdriversTable.setCellWidget(i, 2, joinButton)
            self.carsdriversTable.setCellWidget(i, 3, deleteButton)

            joinButton.clicked.connect(lambda ch, rowNum = i: (self._change_carsdrivers_from_table(rowNum)))
            deleteButton.clicked.connect(lambda ch, rowNum = i: (self._delete_carsdrivers_from_table(rowNum)))
            
            i+=1

        self.createCarsDriversButton = QPushButton("Create")
        self.carsdriversTable.setCellWidget(len(records), 3, self.createCarsDriversButton)
        self.createCarsDriversButton.clicked.connect(self._create_carsdrivers)

    def _create_carsdrivers(self):
        self.carsdriverswin = RegistrationCarsDriversWindow()
        self.carsdriverswin.show()
        

    def _delete_carsdrivers_from_table(self, rowNum):
        id = self.carsdriversTable.cellWidget(rowNum, 0).currentText()
        
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM taxi.carsdrivers WHERE driver=%s", 
                (
                str(id),
                ))
            conn.commit()
        except:
            QMessageBox.about(self, "Error", "Error")

        

    def _change_carsdrivers_from_table(self, rowNum):
        row = list()
        print(rowNum)
        for i in range(self.driversTable.columnCount()):
            if i == 0:
                cmbDriver = self.carsdriversTable.cellWidget(rowNum, i)
                row.append(cmbDriver.currentText())
            elif i == 1:
                cmbDriver = self.carsdriversTable.cellWidget(rowNum, i)
                row.append(cmbDriver.currentText())
                
        print(row)

        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE taxi.carsdrivers SET car=%s WHERE driver=%s", 
                (
                row[1],
                row[0]
                ))
            conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _get_cdcar_cmb(self, car):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT id FROM taxi.cars') 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        

        cmb.addItem(str(car))

 
        r = list(records)

        
        for i in r:
            i = list(i)
            if str(i[0]) != str(car):
                cmb.addItem(str(i[0]))
        
        return cmb

    def _get_cddriver_cmb(self, driver):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT id FROM taxi.drivers') 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        

        cmb.addItem(str(driver))

 
        r = list(records)

        
        for i in r:
            i = list(i)
            if str(i[0]) != str(driver):
                cmb.addItem(str(i[0]))
        
        return cmb



    def _createLogoutTab(self):
        self.tabs.addTab(self.logout_tab,"Log Out")

        self.vbox_logout = QVBoxLayout()

        self.logoutButton = QPushButton("Log Out")
        
        self.vbox_logout.addWidget(self.logoutButton)
        self.logout_tab.setLayout(self.vbox_logout)
        self.logoutButton.clicked.connect(self._logout)

    def _logout(self):
        self.destroy()

    def _create_books_tab(self):
        self.tabs.addTab(self.order_tab, "Orders")

        self.vboxOrders = QVBoxLayout()

        self.updateButton = QPushButton("Update")

        self.ordersTable = QTableWidget()
        self.ordersTable.setColumnCount(13)
        

        self.ordersTable.setHorizontalHeaderLabels(["id", "Start adress", "Finish adress", "Price", "Passenger id", "Driver", "Car", "Comment", "Status", "Class", "Time", "", ""])
        
        self.vboxOrders.addWidget(self.ordersTable)
        self.vboxOrders.addWidget(self.updateButton)

        self._update_table()

        self.order_tab.setLayout(self.vboxOrders)

        self.updateButton.clicked.connect(self._update_table)

    def _create_driver_tab(self):
        self.tabs.addTab(self.driver_tab, "Drivers")

        self.vboxDrivers = QVBoxLayout()

        self.updateDriversButton = QPushButton("Update")

        self.driversTable = QTableWidget()
        self.driversTable.setColumnCount(7)
        

        self.driversTable.setHorizontalHeaderLabels(["id", "Full name", "Birth date", "Status", "Class", "", ""])
        
        self.vboxDrivers.addWidget(self.driversTable)
        self.vboxDrivers.addWidget(self.updateDriversButton)

        self._update_driver_table()

        self.driver_tab.setLayout(self.vboxDrivers)

        self.updateDriversButton.clicked.connect(self._update_driver_table)

    def _create_cars_tab(self):
        self.tabs.addTab(self.cars_tab, "Cars")

        self.vboxCars = QVBoxLayout()

        self.updateCarsButton = QPushButton("Update")

        self.carsTable = QTableWidget()
        self.carsTable.setColumnCount(8)
        

        self.carsTable.setHorizontalHeaderLabels(["id", "Number plate", "Status", "Model", "Class",  "Odometr", "", ""])
        
        self.vboxCars.addWidget(self.carsTable)
        self.vboxCars.addWidget(self.updateCarsButton)

        self._update_cars_table()

        self.cars_tab.setLayout(self.vboxCars)

        self.updateCarsButton.clicked.connect(self._update_cars_table)

    def _create_users_tab(self):
        self.tabs.addTab(self.users_tab, "Users")

        self.vboxUsers = QVBoxLayout()

        self.updateUsersButton = QPushButton("Update")

        self.usersTable = QTableWidget()
        self.usersTable.setColumnCount(5)
        

        self.usersTable.setHorizontalHeaderLabels(["id", "Full name", "Email", "Phone", "Adress"])
        
        self.vboxUsers.addWidget(self.usersTable)
        self.vboxUsers.addWidget(self.updateUsersButton)

        self._update_users_table()

        self.users_tab.setLayout(self.vboxUsers)

        self.updateUsersButton.clicked.connect(self._update_users_table)

    def _update_users_table(self):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
                    
        cursor.execute('SELECT * FROM taxi.users')
        records = list(cursor.fetchall())

        self.usersTable.setRowCount(len(records))

        i = 0
        
        for r in records:
            r = list(r)
            self.usersTable.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.usersTable.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.usersTable.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.usersTable.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.usersTable.setItem(i, 4, QTableWidgetItem(str(r[4])))
            i+=1

    def _update_cars_table(self):
        self.carsTable.setRowCount(0)
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
                    
        cursor.execute('SELECT * FROM taxi.cars')
        records = list(cursor.fetchall())

        self.carsTable.setRowCount(len(records) + 1)

        i = 0
        
        for r in records:
            r = list(r)
            self.carsTable.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.carsTable.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.carsTable.setCellWidget(i, 2, self._get_car_status_cmb(r[0]))
            self.carsTable.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.carsTable.setCellWidget(i, 4, self._get_classes(str(r[4])))
            self.carsTable.setItem(i, 5, QTableWidgetItem(str(r[5])))
            
            
            
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.carsTable.setCellWidget(i, 6, joinButton)
            self.carsTable.setCellWidget(i, 7, deleteButton)

            joinButton.clicked.connect(lambda ch, rowNum = i: (self._change_car_from_table(rowNum)))
            deleteButton.clicked.connect(lambda ch, rowNum = i: (self._delete_car_from_table(rowNum)))
            
            i+=1

        self.createCarButton = QPushButton("Create car")
        self.carsTable.setCellWidget(len(records), 7, self.createCarButton)
        self.createCarButton.clicked.connect(self._create_car)

    def _create_car(self):
        self.carwin = RegistrationCarWindow()
        self.carwin.show()

    def _get_classes(self, trip_class):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT name FROM taxi.trip_classes') 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        

        cmb.addItem(str(trip_class))

 
        r = list(records)

        
        for i in r:
            i = list(i)
            if str(i[0]) != str(trip_class):
                cmb.addItem(str(i[0]))
        
        return cmb


    def _update_driver_table(self):
        self.driversTable.setRowCount(0)
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
                    
        cursor.execute('SELECT * FROM taxi.drivers')
        records = list(cursor.fetchall())

        self.driversTable.setRowCount(len(records) + 1)

        i = 0
        
        for r in records:
            r = list(r)
            self.driversTable.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.driversTable.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.driversTable.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.driversTable.setCellWidget(i, 3, self._get_workers_status_cmb(r[0]))
            self.driversTable.setCellWidget(i, 4, self._get_classes(r[4]))
            
            
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")

            self.driversTable.setCellWidget(i, 5, joinButton)
            self.driversTable.setCellWidget(i, 6, deleteButton)

            joinButton.clicked.connect(lambda ch, rowNum = i: (self._change_driver_from_table(rowNum)))
            deleteButton.clicked.connect(lambda ch, rowNum = i: (self._delete_driver_from_table(rowNum)))
            
            i+=1
        
        self.createDriverButton = QPushButton("Create driver")

        self.driversTable.setCellWidget(len(records), 6, self.createDriverButton)
        self.createDriverButton.clicked.connect(self._createDriver)

    def _createDriver(self):
        self.win = RegistrationDriverWindow()
        self.win.show()

    def _update_table(self):
        self.ordersTable.setRowCount(0)
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
                    
        cursor.execute('SELECT * FROM taxi.orders')
        records = list(cursor.fetchall())

        self.ordersTable.setRowCount(len(records))

        i = 0
        
        for r in records:
            r = list(r)
            self.ordersTable.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.ordersTable.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.ordersTable.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.ordersTable.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.ordersTable.setItem(i, 4, QTableWidgetItem(str(r[4])))
            if r[5] == None:
                self.ordersTable.setCellWidget(i, 5, self._get_free_drivers_cmb())
            else:
                self.ordersTable.setCellWidget(i, 5, self._get_driver_cmb(str(r[0])))
            self.ordersTable.setItem(i, 6, QTableWidgetItem(str(r[10])))
            self.ordersTable.setItem(i, 7, QTableWidgetItem(str(r[6])))
            self.ordersTable.setCellWidget(i, 8, self._get_trip_statuses_cmb(str(r[0])))
            self.ordersTable.setItem(i, 9, QTableWidgetItem(str(r[8])))
            self.ordersTable.setItem(i, 10, QTableWidgetItem(str(r[9])))
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.ordersTable.setCellWidget(i, 11, joinButton)
            self.ordersTable.setCellWidget(i, 12, deleteButton)

            joinButton.clicked.connect(lambda ch, rowNum = i: (self._change_order_from_table(rowNum)))
            deleteButton.clicked.connect(lambda ch, rowNum = i: (self._delete_order_from_table(rowNum)))
            
            i+=1

        # self.createOrderButton.clicked.connect(self.createOrder)
        

        # for i in range(len(self.buttons)):
        #     self.buttons[i].clicked.connect(lambda i: self._change_order_from_table())
    
    def _get_trip_statuses_cmb(self, id):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT status FROM taxi.orders WHERE id = %s', (str(id),)) 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        
        r = list(records)
        

        cmb.addItem(str(r[0][0]))

        cursor.execute('SELECT status FROM taxi.trip_status WHERE status != %s', (str(r[0][0]),)) 
        records = cursor.fetchall()
        
        r = list(records)

        
        for i in r:
            i = list(i)
            cmb.addItem(str(i[0]))
        
        return cmb

    def _get_car_status_cmb(self, id):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT status FROM taxi.cars WHERE id = %s', (str(id),)) 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        
        r = list(records)
        

        cmb.addItem(str(r[0][0]))

        cursor.execute('SELECT name FROM taxi.cars_status WHERE name != %s', (str(r[0][0]),)) 
        records = cursor.fetchall()
        
        r = list(records)

        
        for i in r:
            i = list(i)
            cmb.addItem(str(i[0]))
        
        return cmb

    def _get_workers_status_cmb(self, id):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT status FROM taxi.drivers WHERE id = %s', (str(id),)) 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        
        r = list(records)
        

        cmb.addItem(str(r[0][0]))

        cursor.execute('SELECT name FROM taxi.workers_status WHERE name != %s', (str(r[0][0]),)) 
        records = cursor.fetchall()
        
        r = list(records)

        
        for i in r:
            i = list(i)
            cmb.addItem(str(i[0]))
        
        return cmb


    def _get_driver_cmb(self, id):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT driver_id FROM taxi.orders WHERE id = %s', (str(id),))
        records = cursor.fetchall()

        cmb = QComboBox()
        
        r = list(records)
        cmb.addItem(str(r[0][0]))
        
        
        return cmb
            
            
    def _get_free_drivers_cmb(self):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute("SELECT id FROM taxi.drivers WHERE status = 'ready'")
        records = cursor.fetchall()

        cmb = QComboBox()
        cmb.addItem("")
        r = list(records)

        for i in r:
            i = list(i)
            cmb.addItem(str(i[0]))
        
        return cmb

    def _delete_car_from_table(self, rowNum):
        id = self.carsTable.item(rowNum, 0).text()
        
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM taxi.cars WHERE id=%s", 
                (
                str(id),
                ))
            conn.commit()
        except:
            QMessageBox.about(self, "Error", "Error")


    def _change_car_from_table(self, rowNum):
        row = list()
        print(rowNum)
        for i in range(self.carsTable.columnCount()):
            if i == 2:
                cmbCar = self.carsTable.cellWidget(rowNum, i)
                row.append(cmbCar.currentText())
            elif i == 4:
                cmbCar = self.carsTable.cellWidget(rowNum, i)
                row.append(cmbCar.currentText())
            else:
                try:
                    row.append(self.carsTable.item(rowNum, i).text())
                except:
                    row.append(None)
                
        print(row)

        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE taxi.cars SET number_plate=%s, status=%s, model=%s, class=%s, odometr=%s  WHERE id=%s", 
                    (
                    row[1],
                    row[2], 
                    row[3],
                    row[4],
                    row[5],
                    row[0]
                    ))
            conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_order_from_table(self, rowNum):
        id = self.ordersTable.item(rowNum, 0).text()
        
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM taxi.orders WHERE id=%s", 
                (
                str(id),
                ))
            conn.commit()
        except:
            QMessageBox.about(self, "Error", "Error")
        
    def _change_order_from_table(self, rowNum):
        row = list()
        print(rowNum)
        for i in range(self.ordersTable.columnCount()):
            if i == 5:
                cmbDriver = self.ordersTable.cellWidget(rowNum, i)
                row.append(cmbDriver.currentText())
            elif i == 8:
                cmbStatus = self.ordersTable.cellWidget(rowNum, i)
                row.append(cmbStatus.currentText())
            else:
                try:
                    row.append(self.ordersTable.item(rowNum, i).text())
                except:
                    row.append(None)
                
        print(row)

        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE taxi.orders SET start_adress=%s, finish_adress=%s, price=%s, passenger_id=%s, driver_id=%s, comment=%s, status=%s, class=%s WHERE id=%s", 
                        (
                        row[1],
                        row[2], 
                        row[3],
                        row[4],
                        row[5],
                        row[7],
                        row[8],
                        row[9],
                        row[0]
                        ))
            conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_driver_from_table(self, rowNum):
        id = self.driversTable.item(rowNum, 0).text()
        
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM taxi.drivers WHERE id=%s", 
                (
                str(id),
                ))
            conn.commit()
        except:
            QMessageBox.about(self, "Error", "Error")


    def _change_driver_from_table(self, rowNum):
        row = list()
        print(rowNum)
        for i in range(self.driversTable.columnCount()):
            if i == 3:
                cmbDriver = self.driversTable.cellWidget(rowNum, i)
                row.append(cmbDriver.currentText())
            elif i == 4:
                cmbDriver = self.driversTable.cellWidget(rowNum, i)
                row.append(cmbDriver.currentText())
            else:
                try:
                    row.append(self.driversTable.item(rowNum, i).text())
                except:
                    row.append(None)
                
        print(row)

        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE taxi.drivers SET full_name=%s, birth_date=%s, status=%s, class=%s WHERE id=%s", 
                (
                row[1],
                row[2], 
                row[3],
                row[4],
                row[0]
                ))
            conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")


class RegistrationDriverWindow(QWidget): 
    def __init__(self):
        super(RegistrationDriverWindow, self).__init__()

        self.setWindowTitle("Create driver")

        self.full_name_label = QLabel('Full Name:', self)
        self.full_name_line = QLineEdit(self) 

        self.birth_label = QLabel('Birthdate:', self)
        self.birth_line = QLineEdit(self)

        self.phone_label = QLabel('Phone:', self)
        self.phone_line = QLineEdit(self)

        self.class_label = QLabel('Class:', self)
        self.class_line = self._get_classes()
        
        

        self.createButton = QPushButton("Create", self)

        self.vbox_labels = QVBoxLayout()   
        self.vbox_labels.addWidget(self.full_name_label)
        self.vbox_labels.addWidget(self.birth_label) 
        self.vbox_labels.addWidget(self.phone_label)
        self.vbox_labels.addWidget(self.class_label)
        

        self.hbox_first = QHBoxLayout()
        self.hbox_first.addLayout(self.vbox_labels)

        self.vbox_lines = QVBoxLayout()
        self.vbox_lines.addWidget(self.full_name_line)
        self.vbox_lines.addWidget(self.birth_line)
        self.vbox_lines.addWidget(self.phone_line)
        self.vbox_lines.addWidget(self.class_line)

        
        self.hbox_first.addLayout(self.vbox_lines)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addWidget(self.createButton)

        self.setLayout(self.vbox)

        self.createButton.clicked.connect(self.registration)

    def _get_classes(self):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT name FROM taxi.trip_classes') 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        
        r = list(records)

        
        for i in r:
            i = list(i)
            cmb.addItem(str(i[0]))
        
        return cmb

    def registration(self):
        if (str(self.full_name_line.text()) != '' and
            str(self.birth_line.text()) != '' and
            str(self.phone_line.text()) != '' and
            str(self.class_line.currentText()) != ''
            ):

            driver_fields = {"full_name" : self.full_name_line.text(),
                            "birthdate" : self.birth_line.text(),
                            "phone" : self.phone_line.text(),
                            "class" : self.class_line.currentText(),
                            }
            

            conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

            cursor = conn.cursor()

           

            
            
                
            
            try:
                cursor.execute("INSERT INTO taxi.drivers (full_name, birth_date, class, phone) VALUES (%s, %s, %s, %s)",
                (driver_fields["full_name"], 
                driver_fields["birthdate"],
                driver_fields["class"],
                driver_fields["phone"]
                ))

                QMessageBox.about(self, "Info", "Sucsessful.")

                self.destroy()

                conn.commit()
                cursor.close()
                conn.close()
            except:
                QMessageBox.about(self, "Error", "Something wrong. Try again")
                cursor.close()
                conn.close()

            
        else:
            QMessageBox.about(self, "Error", "Enter all fields")
        

class RegistrationCarWindow(QWidget): 
    def __init__(self):
        super(RegistrationCarWindow, self).__init__()

        self.setWindowTitle("Create car")

        self.number_label = QLabel('Number_plate:', self)
        self.number_line = QLineEdit(self) 

        self.model_label = QLabel('Model:', self)
        self.model_line = QLineEdit(self)

        self.odometr_label = QLabel('Odometr:', self)
        self.odometr_line = QLineEdit(self)

        self.class_label = QLabel('Class:', self)
        self.class_line = self._get_classes()
        
        

        self.createButton = QPushButton("Create", self)

        self.vbox_labels = QVBoxLayout()   
        self.vbox_labels.addWidget(self.number_label)
        self.vbox_labels.addWidget(self.model_label) 
        self.vbox_labels.addWidget(self.odometr_label)
        self.vbox_labels.addWidget(self.class_label)
        

        self.hbox_first = QHBoxLayout()
        self.hbox_first.addLayout(self.vbox_labels)

        self.vbox_lines = QVBoxLayout()
        self.vbox_lines.addWidget(self.number_line)
        self.vbox_lines.addWidget(self.model_line)
        self.vbox_lines.addWidget(self.odometr_line)
        self.vbox_lines.addWidget(self.class_line)

        
        self.hbox_first.addLayout(self.vbox_lines)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addWidget(self.createButton)

        self.setLayout(self.vbox)

        self.createButton.clicked.connect(self.registration)

    def _get_classes(self):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT name FROM taxi.trip_classes') 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        
        r = list(records)

        
        for i in r:
            i = list(i)
            cmb.addItem(str(i[0]))
        
        return cmb

    

    def registration(self):
        if (str(self.number_line.text()) != '' and
            str(self.model_line.text()) != '' and
            str(self.odometr_line.text()) != '' and
            str(self.class_line.currentText()) != ''
            ):

            car_fields = {"number" : self.number_line.text(),
                            "model" : self.model_line.text(),
                            "odometr" : self.odometr_line.text(),
                            "class" : self.class_line.currentText(),
                            }
            

            conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

            cursor = conn.cursor()

           

            
            
                
            
            try:
                cursor.execute("INSERT INTO taxi.cars (number_plate, model, class, odometr) VALUES (%s, %s, %s, %s)",
                (car_fields["number"], 
                car_fields["model"],
                car_fields["class"],
                car_fields["odometr"]
                ))

                QMessageBox.about(self, "Info", "Sucsessful.")

                self.destroy()

                conn.commit()
                cursor.close()
                conn.close()
            except:
                QMessageBox.about(self, "Error", "Something wrong. Try again")
                cursor.close()
                conn.close()

            
        else:
            QMessageBox.about(self, "Error", "Enter all fields")


class RegistrationCarsDriversWindow(QWidget): 
    def __init__(self):
        super(RegistrationCarsDriversWindow, self).__init__()

        self.setWindowTitle("Create Cars/Drivers")

        self.driver_label = QLabel('Driver:', self)
        self.driver_line = self._get_cddriver_cmb("")

        self.car_label = QLabel('Car:', self)
        self.car_line = self._get_cdcar_cmb("")

        
        

        self.createButton = QPushButton("Create", self)

        self.vbox_labels = QVBoxLayout()   
        self.vbox_labels.addWidget(self.driver_label)
        self.vbox_labels.addWidget(self.car_label) 
    
        

        self.hbox_first = QHBoxLayout()
        self.hbox_first.addLayout(self.vbox_labels)

        self.vbox_lines = QVBoxLayout()
        self.vbox_lines.addWidget(self.driver_line)
        self.vbox_lines.addWidget(self.car_line)

        
        self.hbox_first.addLayout(self.vbox_lines)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addWidget(self.createButton)

        self.setLayout(self.vbox)

        self.createButton.clicked.connect(self.registration)

    def _get_cdcar_cmb(self, car):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT id FROM taxi.cars') 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        

        cmb.addItem(str(car))

 
        r = list(records)

        
        for i in r:
            i = list(i)
            if str(i[0]) != str(car):
                cmb.addItem(str(i[0]))
        
        return cmb

    def _get_cddriver_cmb(self, driver):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT id FROM taxi.drivers') 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        

        cmb.addItem(str(driver))

 
        r = list(records)

        
        for i in r:
            i = list(i)
            if str(i[0]) != str(driver):
                cmb.addItem(str(i[0]))
        
        return cmb
    

    def registration(self):
        if (str(self.driver_line.currentText()) != '' and
            str(self.car_line.currentText()) != '' 
            ):

            car_fields = {"driver" : self.driver_line.currentText(),
                            "car" : self.car_line.currentText(),
                            }
            

            conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

            cursor = conn.cursor()

           

            
            
                
            
            try:
                cursor.execute("INSERT INTO taxi.carsdrivers (driver, car) VALUES (%s, %s)",
                (car_fields["driver"], 
                car_fields["car"],
                ))

                QMessageBox.about(self, "Info", "Sucsessful.")

                self.destroy()

                conn.commit()
                cursor.close()
                conn.close()
            except:
                QMessageBox.about(self, "Error", "Something wrong. Try again")
                cursor.close()
                conn.close()

            
        else:
            QMessageBox.about(self, "Error", "Enter all fields")