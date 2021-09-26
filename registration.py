from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QMessageBox, QErrorMessage
import sys
import psycopg2


class RegistrationWindow(QWidget): 
    def __init__(self):
        super(RegistrationWindow, self).__init__()

        self.setWindowTitle("Registration")

        self.full_name_label = QLabel('Full Name:', self)
        self.full_name_line = QLineEdit(self) 

        self.email_label = QLabel('Email:', self)
        self.email_line = QLineEdit(self)

        self.phone_label = QLabel('Phone:', self)
        self.phone_line = QLineEdit(self)

        self.adress_label = QLabel('Adress:', self)
        self.adress_line = QLineEdit(self)
        
        self.login_label = QLabel('Login:', self)
        self.login_line = QLineEdit(self)     

        self.password_label = QLabel('Password:', self)
        self.password_line = QLineEdit(self)

        self.signup_button = QPushButton("SignUp", self)

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
        self.vbox.addWidget(self.signup_button)

        self.setLayout(self.vbox)

        self.signup_button.clicked.connect(self.registration)

    def registration(self):
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

            is_correct = True
            for r in records:
                r = list(r)
                if self.email_line.text() == r[2]:
                    QMessageBox.about(self, "Error", "Email is already used.")
                    is_correct = False
                    break
                elif self.phone_line.text() == r[3]:
                    QMessageBox.about(self, "Error", "Phone number is already used.")
                    is_correct = False
                    break
                elif self.login_line.text() == r[5]:
                    QMessageBox.about(self, "Error", "Login is already used.")
                    is_correct = False
                    break
                
            if is_correct:
                try:
                    cursor.execute("INSERT INTO taxi.users (full_name, email, phone, adress, login, password, role) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (user_fields["full_name"], 
                    user_fields["email"],
                    user_fields["phone"],
                    user_fields["adress"],
                    user_fields["login"],
                    user_fields["password"],
                    user_fields["role"]))

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

        

    