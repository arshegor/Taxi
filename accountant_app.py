from PyQt5.QtWidgets import QComboBox, QTabWidget, QAction, QLineEdit, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QMessageBox, QMenuBar, QMenu
import sys
import psycopg2

class AccountantWindow(QWidget):
    def __init__(self, login):
        super(AccountantWindow, self).__init__()

        self.login = login

        self.vbox = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.drivers_salaries_tab = QWidget()
        self.workers_salaries_tab = QWidget()
        self.workers_tab = QTabWidget()
        self.logout_tab = QWidget()

        self._create_drivers_salaries_tab()
        self._create_workers_salaries_tab()
        self._create_workers_tab()
        self._createLogoutTab()

        self.vbox.addWidget(self.tabs)

        self.setLayout(self.vbox)

    def _create_workers_tab(self):
        self.tabs.addTab(self.workers_tab, "Workers")

        self.vboxWorkers = QVBoxLayout()

        self.updateWorkersButton = QPushButton("Update")

        self.workersTable = QTableWidget()
        self.workersTable.setColumnCount(8)
        

        self.workersTable.setHorizontalHeaderLabels(["id", "Full name","BirthDate", "Post", "Phone", "Status", "", ""])
        
        self.vboxWorkers.addWidget(self.workersTable)
        self.vboxWorkers.addWidget(self.updateWorkersButton)

        self._update_workers_table()

        self.workers_tab.setLayout(self.vboxWorkers)

        self.updateWorkersButton.clicked.connect(self._update_workers_table)

    def _update_workers_table(self):
        self.workersTable.setRowCount(0)
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
                    
        cursor.execute('SELECT * FROM taxi.workers')
        records = list(cursor.fetchall())

        self.workersTable.setRowCount(len(records) + 1)

        i = 0
        
        for r in records:
            r = list(r)
            print(r)
            self.workersTable.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.workersTable.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.workersTable.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.workersTable.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.workersTable.setItem(i, 4, QTableWidgetItem(str(r[7])))
            self.workersTable.setCellWidget(i, 5, self._get_workers_status_cmb(str(r[4])))
            
            
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.workersTable.setCellWidget(i, 6, joinButton)
            self.workersTable.setCellWidget(i, 7, deleteButton)

            joinButton.clicked.connect(lambda ch, rowNum = i: (self._change_workers_from_table(rowNum)))
            deleteButton.clicked.connect(lambda ch, rowNum = i: (self._delete_workers_from_table(rowNum)))
            

            i+=1

        self.createWorkerButton = QPushButton("Create")
        self.workersTable.setCellWidget(len(records), 7, self.createWorkerButton)
        self.createWorkerButton.clicked.connect(self._create_worker)

    def _create_worker(self):
        self.createworkerwin = CreateWorkerWindow()
        self.createworkerwin.show()

    def _get_workers_status_cmb(self, status):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT name FROM taxi.workers_status') 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        
        r = list(records)
        print(r)
        

        cmb.addItem(status)

        

        
        for i in r:
            i = list(i)
            if str(i[0]) != str(status):
                cmb.addItem(str(i[0]))
        
        return cmb

    def _delete_workers_from_table(self, rowNum):
        id = self.workersTable.item(rowNum, 0).text()
        
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM taxi.workers WHERE id=%s", 
                (
                str(id),
                ))
            conn.commit()
        except:
            QMessageBox.about(self, "Error", "Error")

    def _change_workers_from_table(self, rowNum):
        row = list()
        print(rowNum)
        for i in range(self.workersTable.columnCount() - 1):
            if i == 5:
                cmbDriver = self.workersTable.cellWidget(rowNum, i)
                row.append(cmbDriver.currentText())
            else:
                try:
                    row.append(self.workersTable.item(rowNum, i).text())
                except:
                    row.append(None)
            
                    
        print(row)

        conn = psycopg2.connect(database="postgres", 
                                        user="arshegor", 
                                        password="", 
                                        host="localhost", 
                                        port="5432")

        cursor = conn.cursor()

        # try:
        cursor.execute("UPDATE taxi.workers SET full_name=%s, birth_date=%s, post=%s, phone=%s ,status=%s WHERE id = %s", 
                    (
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[0],
                    ))
        conn.commit()
        
        # except:
        #     QMessageBox.about(self, "Error", "Enter all fields")

    def _createLogoutTab(self):
        self.tabs.addTab(self.logout_tab,"Log Out")

        self.vbox_logout = QVBoxLayout()

        self.logoutButton = QPushButton("Log Out")
        
        self.vbox_logout.addWidget(self.logoutButton)
        self.logout_tab.setLayout(self.vbox_logout)
        self.logoutButton.clicked.connect(self._logout)

    def _logout(self):
        self.destroy()

    def _create_workers_salaries_tab(self):
        self.tabs.addTab(self.workers_salaries_tab, "Workers salaries")

        self.vboxWorkersS = QVBoxLayout()

        self.updateWorkersSalariesButton = QPushButton("Update")

        self.workersSalariesTable = QTableWidget()
        self.workersSalariesTable.setColumnCount(5)
        

        self.workersSalariesTable.setHorizontalHeaderLabels(["id", "Worker id","Salary", "", ""])
        
        self.vboxWorkersS.addWidget(self.workersSalariesTable)
        self.vboxWorkersS.addWidget(self.updateWorkersSalariesButton)

        self._update_workers_salaries_table()

        self.workers_salaries_tab.setLayout(self.vboxWorkersS)

        self.updateWorkersSalariesButton.clicked.connect(self._update_workers_salaries_table)

    def _update_workers_salaries_table(self):
        self.workersSalariesTable.setRowCount(0)
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
                    
        cursor.execute('SELECT * FROM taxi.workers_salaries')
        records = list(cursor.fetchall())

        self.workersSalariesTable.setRowCount(len(records) + 1)

        i = 0
        
        for r in records:
            r = list(r)
            self.workersSalariesTable.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.workersSalariesTable.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.workersSalariesTable.setItem(i, 2, QTableWidgetItem(str(r[2])))
            
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            self.workersSalariesTable.setCellWidget(i, 3, joinButton)
            self.workersSalariesTable.setCellWidget(i, 4, deleteButton)

            joinButton.clicked.connect(lambda ch, rowNum = i: (self._change_workers_salary_from_table(rowNum)))
            deleteButton.clicked.connect(lambda ch, rowNum = i: (self._delete_workers_salary_from_table(rowNum)))
            

            i+=1

        self.createSalaryButton = QPushButton("Create")
        self.workersSalariesTable.setCellWidget(len(records), 4, self.createSalaryButton)
        self.createSalaryButton.clicked.connect(self._create_salary)

    def _delete_workers_salary_from_table(self, rowNum):
        id = self.workersSalariesTable.item(rowNum, 0).text()
        
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM taxi.workers_salaries WHERE id=%s", 
                (
                str(id),
                ))
            conn.commit()
        except:
            QMessageBox.about(self, "Error", "Error")

    def _change_workers_salary_from_table(self, rowNum):
        row = list()
        print(rowNum)
        for i in range(self.workersSalariesTable.columnCount() - 1):
            try:
                row.append(self.workersSalariesTable.item(rowNum, i).text())
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
            cursor.execute("UPDATE taxi.workers_salaries SET salary=%s WHERE worker = %s", 
                        (
                        row[2],
                        row[1]
                        ))
            conn.commit()
        
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _create_salary(self):
        self.createsalarywin = CreateSalaryWindow()
        self.createsalarywin.show()
    
    def _create_drivers_salaries_tab(self):
        self.tabs.addTab(self.drivers_salaries_tab, "Drivers salaries")

        self.vboxDriversS = QVBoxLayout()

        self.updateDriversSalariesButton = QPushButton("Update")

        self.driversSalariesTable = QTableWidget()
        self.driversSalariesTable.setColumnCount(6)
        

        self.driversSalariesTable.setHorizontalHeaderLabels(["id", "Driver id", "Order id","Salary", "Status", ""])
        
        self.vboxDriversS.addWidget(self.driversSalariesTable)
        self.vboxDriversS.addWidget(self.updateDriversSalariesButton)

        self._update_drivers_salaries_table()

        self.drivers_salaries_tab.setLayout(self.vboxDriversS)

        self.updateDriversSalariesButton.clicked.connect(self._update_drivers_salaries_table)

    def _update_drivers_salaries_table(self):
        self.driversSalariesTable.setRowCount(0)
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
                    
        cursor.execute('SELECT * FROM taxi.drivers_salaries')
        records = list(cursor.fetchall())

        self.driversSalariesTable.setRowCount(len(records))

        i = 0
        
        for r in records:
            r = list(r)
            self.driversSalariesTable.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.driversSalariesTable.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.driversSalariesTable.setItem(i, 2, QTableWidgetItem(str(r[4])))
            self.driversSalariesTable.setItem(i, 3, QTableWidgetItem(str(r[2])))
            self.driversSalariesTable.setItem(i, 4, QTableWidgetItem(str(r[3])))
            
            if str(r[3]) != "paid":
                joinButton = QPushButton("Pay out")
                self.driversSalariesTable.setCellWidget(i, 5, joinButton)

                joinButton.clicked.connect(lambda ch, rowNum = i: (self._change_driver_salary_from_table(rowNum)))
            
            i+=1


    def _change_driver_salary_from_table(self, rowNum):
        row = list()
        print(rowNum)
        for i in range(self.driversSalariesTable.columnCount()):
            try:
                row.append(self.driversSalariesTable.item(rowNum, i).text())
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
            cursor.execute("UPDATE taxi.drivers_salaries SET status=%s WHERE id = %s", 
                        (
                        "paid",
                        row[0]
                        ))
            conn.commit()
            self.driversSalariesTable.cellWidget(rowNum, 5).setParent(None)
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_workers_salary_from_table(self, rowNum):
        row = list()
        print(rowNum)
        for i in range(self.workersSalariesTable.columnCount() - 1):
            try:
                row.append(self.workersSalariesTable.item(rowNum, i).text())
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
            cursor.execute("UPDATE taxi.workers_salaries SET salary=%s WHERE worker = %s", 
                        (
                        row[2],
                        row[1]
                        ))
            conn.commit()
        
        except:
            QMessageBox.about(self, "Error", "Enter all fields")



class CreateSalaryWindow(QWidget): 
    def __init__(self):
        super(CreateSalaryWindow, self).__init__()

        self.setWindowTitle("Create salary")

        self.worker_label = QLabel('Worker id:', self)
        self.worker_line = self._get_worker_cmb()

        self.salary_label = QLabel('Salary:', self)
        self.salary_line = QLineEdit()

        
        

        self.createButton = QPushButton("Create", self)

        self.vbox_labels = QVBoxLayout()   
        self.vbox_labels.addWidget(self.worker_label)
        self.vbox_labels.addWidget(self.salary_label) 
    
        

        self.hbox_first = QHBoxLayout()
        self.hbox_first.addLayout(self.vbox_labels)

        self.vbox_lines = QVBoxLayout()
        self.vbox_lines.addWidget(self.worker_line)
        self.vbox_lines.addWidget(self.salary_line)

        
        self.hbox_first.addLayout(self.vbox_lines)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addWidget(self.createButton)

        self.setLayout(self.vbox)

        self.createButton.clicked.connect(self.registration)

    
    def _get_worker_cmb(self):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT id FROM taxi.workers') 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        

       

 
        r = list(records)

        
        for i in r:
            i = list(i)
            
            cmb.addItem(str(i[0]))
        
        return cmb
    

    def registration(self):
        if (str(self.worker_line.currentText()) != '' and
            str(self.salary_line.text()) != '' 
            ):

            fields = {"worker" : self.worker_line.currentText(),
                            "salary" : self.salary_line.text(),
                            }
            

            conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

            cursor = conn.cursor()

           

            
            
                
            
            # try:
            cursor.execute("INSERT INTO taxi.workers_salaries (worker, salary) VALUES (%s, %s)",
            (
                fields["worker"], 
            fields["salary"],
            ))

            QMessageBox.about(self, "Info", "Sucsessful.")

            self.destroy()

            conn.commit()
            cursor.close()
            conn.close()
            # except:
            #     QMessageBox.about(self, "Error", "Something wrong. Try again")
            #     cursor.close()
            #     conn.close()

            
        else:
            QMessageBox.about(self, "Error", "Enter all fields")

class CreateWorkerWindow(QWidget): 
    def __init__(self):
        super(CreateWorkerWindow, self).__init__()

        self.setWindowTitle("Create salary")

        self.name_label = QLabel('Full name:', self)
        self.name_line = QLineEdit()

        self.birth_label = QLabel('Birth:', self)
        self.birth_line = QLineEdit()

        self.post_label = QLabel('Post:', self)
        self.post_line = QLineEdit()

        self.phone_label = QLabel('Phone:', self)
        self.phone_line = QLineEdit()

        self.status_label = QLabel('Status:', self)
        self.status_line = self._get_workers_status_cmb("")
        
        self.login_label = QLabel('Login:', self)
        self.login_line = QLineEdit()
        
        self.password_label = QLabel('Password:', self)
        self.password_line = QLineEdit()

        self.createButton = QPushButton("Create", self)

        self.vbox_labels = QVBoxLayout()   
        self.vbox_labels.addWidget(self.name_label)
        self.vbox_labels.addWidget(self.birth_label) 
        self.vbox_labels.addWidget(self.post_label)
        self.vbox_labels.addWidget(self.phone_label)
        self.vbox_labels.addWidget(self.status_label)
        self.vbox_labels.addWidget(self.login_label)
        self.vbox_labels.addWidget(self.password_label)
    
        

        self.hbox_first = QHBoxLayout()
        self.hbox_first.addLayout(self.vbox_labels)

        self.vbox_lines = QVBoxLayout()
        self.vbox_lines.addWidget(self.name_line)
        self.vbox_lines.addWidget(self.birth_line) 
        self.vbox_lines.addWidget(self.post_line)
        self.vbox_lines.addWidget(self.phone_line)
        self.vbox_lines.addWidget(self.status_line)
        self.vbox_lines.addWidget(self.login_line)
        self.vbox_lines.addWidget(self.password_line)

        
        self.hbox_first.addLayout(self.vbox_lines)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addWidget(self.createButton)

        self.setLayout(self.vbox)

        self.createButton.clicked.connect(self.registration)

    
    def _get_workers_status_cmb(self, status):
        conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

        cursor = conn.cursor()
        cursor.execute('SELECT name FROM taxi.workers_status') 
        records = cursor.fetchall()
        

        cmb = QComboBox()
        
        r = list(records)
        

        cmb.addItem(status)

        cursor.execute('SELECT name FROM taxi.workers_status WHERE name != %s', (str(r[0][0]),)) 
        records = cursor.fetchall()
        
        r = list(records)

        
        for i in r:
            i = list(i)
            cmb.addItem(str(i[0]))
        
        return cmb
    

    def registration(self):
        if (str(self.name_line.text()) != '' and
            str(self.birth_line.text()) != '' and
            str(self.post_line.text()) != '' and
            str(self.status_line.currentText()) != ''
            ):

            fields = {"name" : self.name_line.text(),
                            "birth" : self.birth_line.text(),
                            "post" : self.post_line.text(),
                            "phone" : self.phone_line.text(),
                            "status" : self.status_line.currentText(),
                            "login" : self.login_line.text(),
                            "password" : self.password_line.text(),
                            }
            

            conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

            cursor = conn.cursor()

           

            
            
                
            
            try:
                cursor.execute("INSERT INTO taxi.workers (full_name, birth_date, post, phone, status, login, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    fields["name"], 
                    fields["birth"],
                    fields["post"], 
                    fields["phone"],
                    fields["status"],
                    fields["login"], 
                    fields["password"],
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