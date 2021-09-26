from PyQt5.QtWidgets import QComboBox, QTabWidget, QAction, QLineEdit, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QMessageBox, QMenuBar, QMenu
import sys
import psycopg2
import os





class UserWindow(QWidget): 
    def __init__(self, login):
        super(UserWindow, self).__init__()

        self.login = login

        self.vbox = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.account_tab = QWidget()
        self.order_tab = QWidget()
        self.logout_tab = QWidget() 

        self._createBookTab()
        self._createAccountTab()
        self._createLogoutTab()

        self.vbox.addWidget(self.tabs)
    
    def _createLogoutTab(self):
        self.tabs.addTab(self.logout_tab,"Log Out")

        self.vbox_logout = QVBoxLayout()

        self.logoutButton = QPushButton("Log Out")
        
        self.vbox_logout.addWidget(self.logoutButton)
        self.logout_tab.setLayout(self.vbox_logout)
        self.logoutButton.clicked.connect(self._logout)

    def _logout(self):
        self.destroy()
        
        
        

    def _createBookTab(self):
        self.tabs.addTab(self.order_tab,"Book a trip")
        self.accountInfo = self._getAccountInfo()
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM taxi.orders where passenger_id = %s AND status != 'done'", (str(self.accountInfo[0])))
        records = list(cursor.fetchall())

        self.vbox_bookTab = QVBoxLayout()
        self.hbox_bookTab_start = QHBoxLayout()
        self.hbox_bookTab_finish = QHBoxLayout()
        self.hbox_bookTab_comment = QHBoxLayout()
        self.hbox_bookTab_tripclass = QHBoxLayout()
        self.hbox_bookTab_driver = QHBoxLayout()
        self.hbox_bookTab_car = QHBoxLayout()
        self.hbox_bookTab_status = QHBoxLayout()
        self.hbox_bookTab_price = QHBoxLayout()

        self.updateOrderButton = QPushButton("Update")
        self.updateOrderButton.clicked.connect(self._update_order)

        self.start_adress_label_text = QLabel()
        self.finish_adress_label_text = QLabel()
        self.comment_label_text = QLabel()
        self.tripclass_label_text = QLabel()

        self.start_adress_label = QLabel('Start adress: ', self)
        self.finish_adress_label = QLabel('Finish adress:  ', self)
        self.comment_label = QLabel("Comment:     ", self)
        self.tripclass_label = QLabel("Class of trip:", self)
        self.driver_label = QLabel("Driver        ", self)
        self.driver_label.setParent(None)
        self.car_label = QLabel("Car           ", self)
        self.car_label.setParent(None)
        self.status_label = QLabel("Status        ", self)
        self.status_label.setParent(None)
        self.price_label = QLabel("Price         ", self)
        self.price_label.setParent(None)

        self.driver_label_text = QLabel(self)
        self.car_label_text = QLabel(self)
        self.status_label_text = QLabel(self)
        self.price_label_text = QLabel(self)

        self.hbox_bookTab_start.addWidget(self.start_adress_label)
        self.hbox_bookTab_finish.addWidget(self.finish_adress_label)
        self.hbox_bookTab_comment.addWidget(self.comment_label)
        self.hbox_bookTab_tripclass.addWidget(self.tripclass_label)

        self.hbox_bookTab = QVBoxLayout()

        if len(records) > 0:
            self._update_order()
        else:
            self._bookATrip()

    def _createAccountTab(self):
        # Add tabs
        self.tabs.addTab(self.account_tab,"Account")
        

        self.accountInfo = self._getAccountInfo()
        print(self.accountInfo)
        
        # Create first tab
        self.full_name_label = QLabel('Full Name:', self)
        self.full_name_info = QLabel(self.accountInfo[1], self) 

        self.email_label = QLabel('Email:', self)
        self.email_info = QLabel(self.accountInfo[2], self)

        self.phone_label = QLabel('Phone:', self)
        self.phone_info = QLabel(self.accountInfo[3], self)

        self.adress_label = QLabel('Adress:', self)
        self.adress_info = QLabel(self.accountInfo[4], self)
        
        self.login_label = QLabel('Login:', self)
        self.login_info = QLabel(self.accountInfo[5], self)     

        self.password_label = QLabel('Password:', self)
        self.password_info = QLabel(self.accountInfo[6], self)

        self.editButton = QPushButton("Edit account \n information")

        self.account_tab.vbox_labels = QVBoxLayout()   
        self.account_tab.vbox_labels.addWidget(self.full_name_label)
        self.account_tab.vbox_labels.addWidget(self.email_label) 
        self.account_tab.vbox_labels.addWidget(self.phone_label)
        self.account_tab.vbox_labels.addWidget(self.adress_label)
        self.account_tab.vbox_labels.addWidget(self.login_label) 
        self.account_tab.vbox_labels.addWidget(self.password_label)

        self.account_tab.vbox_info = QVBoxLayout()   
        self.account_tab.vbox_info.addWidget(self.full_name_info)
        self.account_tab.vbox_info.addWidget(self.email_info) 
        self.account_tab.vbox_info.addWidget(self.phone_info)
        self.account_tab.vbox_info.addWidget(self.adress_info)
        self.account_tab.vbox_info.addWidget(self.login_info) 
        self.account_tab.vbox_info.addWidget(self.password_info)

        self.account_tab.hbox_first = QHBoxLayout()
        self.account_tab.hbox_first.addLayout(self.account_tab.vbox_labels)
        self.account_tab.hbox_first.addLayout(self.account_tab.vbox_info)

        self.account_tab.vbox = QVBoxLayout(self)

        self.account_tab.vbox.addLayout(self.account_tab.hbox_first)
        self.account_tab.vbox.addWidget(self.editButton)
        self.account_tab.setLayout(self.account_tab.vbox)
        
        # Add tabs to widget
        
        self.setLayout(self.vbox)

        self.editButton.clicked.connect(self._editInfo)

    def _changeAccountTab(self):
        self.accountInfo = self._getAccountInfo()
        self.full_name_info.setText(self.accountInfo[1])
        self.email_info.setText(self.accountInfo[2])
        self.phone_info.setText(self.accountInfo[3])
        self.adress_info.setText(self.accountInfo[4])
        self.login_info.setText(self.accountInfo[5])
        self.password_info.setText(self.accountInfo[6])
        
    def _getAccountInfo(self):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
                
        cursor.execute('SELECT * FROM taxi.users WHERE login = %s', (self.login,))
        records = cursor.fetchall()

        if len(records) == 0:
            cursor.execute('SELECT * FROM taxi.users WHERE email = %s', (self.login,))
            records = cursor.fetchall()

        return list(records[0])
    
    def _get_trip_classes(self):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM taxi.trip_classes')
        records = cursor.fetchall()
        return records
        
    
    def _editInfo(self):
        self.accountInfo = self._getAccountInfo()
        self.editWindow = EditWindow(self)
        self.editWindow.show()
        self._changeAccountTab()
        self.show()

    def _bookATrip(self):
        self.start_adress_line = QLineEdit(self)
        self.finish_adress_line = QLineEdit(self)
        self.comment_textbox = QTextEdit()
        self.tripclass_combobox = QComboBox()

        self.finishOrderButton = QPushButton("Book a trip")

        self.classes = list()
        self.classes_records = self._get_trip_classes()
        for r in self.classes_records:
            self.classes.append(list(r))
        
        for c in self.classes:
            self.tripclass_combobox.addItem(c[1])
  
        self.hbox_bookTab_start.addWidget(self.start_adress_line)
        self.hbox_bookTab_finish.addWidget(self.finish_adress_line)
        self.hbox_bookTab_comment.addWidget(self.comment_textbox)
        self.hbox_bookTab_tripclass.addWidget(self.tripclass_combobox)

        self.hbox_bookTab.addLayout(self.hbox_bookTab_start)
        self.hbox_bookTab.addLayout(self.hbox_bookTab_finish)
        self.hbox_bookTab.addLayout(self.hbox_bookTab_comment)
        self.hbox_bookTab.addLayout(self.hbox_bookTab_tripclass)

        self.vbox_bookTab.addLayout(self.hbox_bookTab)
        self.vbox_bookTab.addWidget(self.finishOrderButton)

        self.order_tab.setLayout(self.vbox_bookTab)

        self.finishOrderButton.clicked.connect(self._progress_booking)


    def _progress_booking(self):
        if str(self.start_adress_line.text()) != '' and str(self.finish_adress_line.text()) != '':
            self.start_adress_line.setParent(None)
            self.finish_adress_line.setParent(None)
            self.comment_textbox.setParent(None)
            self.tripclass_combobox.setParent(None)
            self.finishOrderButton.setParent(None)
            
            
            conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

            cursor = conn.cursor()

            cursor.execute('INSERT INTO taxi.orders (start_adress, finish_adress, passenger_id, comment, status, class) VALUES (%s, %s, %s, %s, %s, %s)', 
            (str(self.start_adress_line.text()), 
            str(self.finish_adress_line.text()),
            self.accountInfo[0],
            str(self.comment_textbox.toPlainText()), 
            "waiting for driver",
            str(self.tripclass_combobox.currentText())
            ))

            conn.commit()

            self._update_order()

    def _update_order(self):
        self.hbox_bookTab.addLayout(self.hbox_bookTab_start)
        self.hbox_bookTab.addLayout(self.hbox_bookTab_finish)
        self.hbox_bookTab.addLayout(self.hbox_bookTab_comment)
        self.hbox_bookTab.addLayout(self.hbox_bookTab_tripclass)
        self.hbox_bookTab.addLayout(self.hbox_bookTab_driver)
        self.hbox_bookTab.addLayout(self.hbox_bookTab_car)
        self.hbox_bookTab.addLayout(self.hbox_bookTab_status)
        self.hbox_bookTab.addLayout(self.hbox_bookTab_price)


        self.vbox_bookTab.addLayout(self.hbox_bookTab)
        self.vbox_bookTab.addWidget(self.updateOrderButton)
            

        self.order_tab.setLayout(self.vbox_bookTab)


        self.hbox_bookTab_start.addWidget(self.start_adress_label_text)
        self.hbox_bookTab_finish.addWidget(self.finish_adress_label_text)
        self.hbox_bookTab_comment.addWidget(self.comment_label_text)
        self.hbox_bookTab_tripclass.addWidget(self.tripclass_label_text)
        self.hbox_bookTab_driver.addWidget(self.driver_label)
        self.hbox_bookTab_car.addWidget(self.car_label)
        self.hbox_bookTab_status.addWidget(self.status_label)
        self.hbox_bookTab_price.addWidget(self.price_label)

        self.hbox_bookTab_driver.addWidget(self.driver_label_text)
        self.hbox_bookTab_car.addWidget(self.car_label_text)
        self.hbox_bookTab_status.addWidget(self.status_label_text)
        self.hbox_bookTab_price.addWidget(self.price_label_text)

        conn = psycopg2.connect(database="postgres", 
                                        user="arshegor", 
                                        password="", 
                                        host="localhost", 
                                        port="5432")

        cursor = conn.cursor()
        

        self.accountInfo = self._getAccountInfo()

        
        cursor.execute("SELECT * FROM taxi.orders where passenger_id = %s AND status != 'done'", (str(self.accountInfo[0])))
        records = list(cursor.fetchall())

        records = records[0]

        self.start_adress_label_text.setText(str(records[1]))
        self.finish_adress_label_text.setText(str(records[2]))
        self.comment_label_text.setText(str(records[6]))
        self.tripclass_label_text.setText(str(records[8]))
        self.price_label_text.setText(str(records[3]))
        self.status_label_text.setText(str(records[7]))

        try:
            cursor.execute("SELECT full_name FROM taxi.drivers where id = %s", (str(records[5]),))
            recordsDriver = list(cursor.fetchall())

            recordsDriver = recordsDriver[0]
            self.driver_label_text.setText(str(recordsDriver[0]))
        except:
             self.driver_label_text.setText(str(''))

        try:
            cursor.execute("SELECT number_plate, model FROM taxi.cars where id = %s", (str(records[10]),))
            recordsCar = list(cursor.fetchall())

            recordsCar = recordsCar[0]
            
            self.car_label_text.setText(str(recordsCar[0]) + " " + str(recordsCar[1]))
            
        except:
            self.car_label_text.setText('')












class EditWindow(QWidget): 
    def __init__(self, account):
        super(EditWindow, self).__init__()

        self.account = account

        self.accountInfo = account.accountInfo
        self.setWindowTitle("Edit informations")

        self.full_name_label = QLabel('Full Name:', self)
        self.full_name_line = QLineEdit(self) 
        self.full_name_line.setText(self.accountInfo[1])

        self.email_label = QLabel('Email:', self)
        self.email_line = QLineEdit(self)
        self.email_line.setText(self.accountInfo[2])

        self.phone_label = QLabel('Phone:', self)
        self.phone_line = QLineEdit(self)
        self.phone_line.setText(self.accountInfo[3])

        self.adress_label = QLabel('Adress:', self)
        self.adress_line = QLineEdit(self)
        self.adress_line.setText(self.accountInfo[4])
            
        self.login_label = QLabel('Login:', self)
        self.login_line = QLineEdit(self)   
        self.login_line.setText(self.accountInfo[5])  

        self.password_label = QLabel('Password:', self)
        self.password_line = QLineEdit(self)
        self.password_line.setText(self.accountInfo[6])

        self.edit_button = QPushButton("Edit", self)

        self.vbox_labels = QVBoxLayout()   
        self.vbox_labels.addWidget(self.full_name_label)
        self.vbox_labels.addWidget(self.email_label) 
        self.vbox_labels.addWidget(self.phone_label)
        self.vbox_labels.addWidget(self.adress_label)
        self.vbox_labels.addWidget(self.login_label) 
        self.vbox_labels.addWidget(self.password_label)

        self.hbox_first = QHBoxLayout()
        self.hbox_first.addLayout(self.vbox_labels)

        self.vbox_lines = QVBoxLayout()
        self.vbox_lines.addWidget(self.full_name_line)
        self.vbox_lines.addWidget(self.email_line)
        self.vbox_lines.addWidget(self.phone_line)
        self.vbox_lines.addWidget(self.adress_line)
        self.vbox_lines.addWidget(self.login_line) 
        self.vbox_lines.addWidget(self.password_line)

        
        self.hbox_first.addLayout(self.vbox_lines)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addWidget(self.edit_button)

        self.setLayout(self.vbox)

        self.edit_button.clicked.connect(self._edit)


    def _edit(self):
        if (str(self.full_name_line.text()) != '' and
            str(self.email_line.text()) != '' and
            str(self.phone_line.text()) != '' and
            str(self.adress_line.text()) != '' and
            str(self.login_line.text()) != '' and
            str(self.password_line.text()) != ''):

            user_fields = {"full_name" : self.full_name_line.text(),
                            "email" : self.email_line.text(),
                            "phone" : self.phone_line.text(),
                            "adress" : self.adress_line.text(),
                            "login" : self.login_line.text(),
                            "password" : self.password_line.text(), "role" : "user"}
            

            conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

            cursor = conn.cursor()

            cursor.execute('SELECT * FROM taxi.users')
            records = cursor.fetchall()

            self.is_correct = True
            for r in records:
                r = list(r)
                if self.email_line.text() == r[2] and self.accountInfo[0] != r[0]:
                    QMessageBox.about(self, "Error", "Email is already used.")
                    self.is_correct = False
                    break
                elif self.phone_line.text() == r[3] and self.accountInfo[0] != r[0]:
                    QMessageBox.about(self, "Error", "Phone number is already used.")
                    self.is_correct = False
                    break
                elif self.login_line.text() == r[5] and self.accountInfo[0] != r[0]:
                    QMessageBox.about(self, "Error", "Login is already used.")
                    self.is_correct = False
                    break
                
            if self.is_correct:
                try:
                    cursor.execute("UPDATE taxi.users SET full_name=%s, email=%s, phone=%s, adress=%s, login=%s, password=%s, role=%s WHERE id=%s", (user_fields["full_name"], 
                    user_fields["email"],
                    user_fields["phone"],
                    user_fields["adress"],
                    user_fields["login"],
                    user_fields["password"],
                    user_fields["role"],
                    self.accountInfo[0]))

                    QMessageBox.about(self, "Info", "Sucsessful.")

                    self.destroy()
                    self.account.login = user_fields["login"]
                
                    conn.commit()
                    cursor.close()
                    conn.close()

                    self.account._changeAccountTab()

                except:
                    QMessageBox.about(self, "Error", "Something wrong. Try again")
                    cursor.close()
                    conn.close()

            
        else:
            QMessageBox.about(self, "Error", "Enter all fields")

        

    