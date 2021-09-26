from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QMessageBox
import sys
import psycopg2

from registration import RegistrationWindow
from users_app import UserWindow
from manager_app import ManagerWindow
from accountant_app import AccountantWindow


class AutorizationWindow(QWidget): 
    def __init__(self):
        super(AutorizationWindow, self).__init__()

        self.setWindowTitle("Autorization")
        
        self.login_label = QLabel('Login:', self)
        self.login_line = QLineEdit(self)     

        self.password_label = QLabel('Password:', self)
        self.password_line = QLineEdit(self)     

        self.login_button = QPushButton("LogIn", self)
        self.signup_button = QPushButton("SignUp", self)     
    
        self.vbox_labels = QVBoxLayout()               
        self.vbox_labels.addWidget(self.login_label) 
        self.vbox_labels.addWidget(self.password_label)  

        self.hbox_first = QHBoxLayout()
        self.hbox_first.addLayout(self.vbox_labels)     

        self.vbox_lines = QVBoxLayout()
        self.vbox_lines.addWidget(self.login_line) 
        self.vbox_lines.addWidget(self.password_line)
        
        self.hbox_first.addLayout(self.vbox_lines)
        
        self.hbox_second = QHBoxLayout()
        self.hbox_second.addWidget(self.login_button)
        self.hbox_second.addWidget(self.signup_button)
        
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addLayout(self.hbox_second)
 
        self.setLayout(self.vbox)

        self.signup_button.clicked.connect(self.registration)
        self.login_button.clicked.connect(self.login)

    def registration(self):
        self.sign_up = RegistrationWindow()
        self.sign_up.show()
    
    def login(self):
        if str(self.login_line.text()) != '' and str(self.password_line.text()) != '':
            conn = psycopg2.connect(database="postgres", 
                                    user="arshegor", 
                                    password="", 
                                    host="localhost", 
                                    port="5432")

            cursor = conn.cursor()
            cursor.execute('SELECT * FROM taxi.users')
            records = cursor.fetchall()

            for r in records:
                r = list(r)
                if self.login_line.text() == r[2] or self.login_line.text() == r[5]:
                    if self.password_line.text() == r[6] and r[7] == "user":
                        self.destroy()

                        self.userWindow = UserWindow(self.login_line.text())
                        self.userWindow.show()
            
            cursor.execute('SELECT * FROM taxi.workers')
            records = cursor.fetchall()

            for r in records:
                r = list(r)
                if self.login_line.text() == r[5]:
                    if self.password_line.text() == r[6] and r[3] == "manager":
                        self.destroy()

                        self.managerWindow = ManagerWindow(self.login_line.text())
                        self.managerWindow.show()
                    elif self.password_line.text() == r[6] and r[3] == "accountant":
                        self.destroy()

                        self.accountantWindow = AccountantWindow(self.login_line.text())
                        self.accountantWindow.show()




        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AutorizationWindow()
    win.show()
    sys.exit(app.exec_())
