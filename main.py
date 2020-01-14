#Modules
from tkinter import *
import sqlite3 as sql

#Make database and users table(if doesn't already exist)
with sql.connect('faculty.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL, password TEXT NOT NULL, question TEXT NOT NULL, answer TEXT NOT NULL);')
db.commit()
db.close()

#main class
class main:
    def __init__(self, master):
        #Window
        self.master = master
        #Variables
        self.username = StringVar()
        self.password = StringVar()
        self.question = StringVar()
        self.answer = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.n_question = StringVar()
        self.n_answer = StringVar()
        #Widgets
        self.widgets()


    #Login Function
    def login(self):
        #Build Connection to DB
        with sql.connect('faculty.db') as db:
            c= db.cursor()

        #Find user in the database and take proper action
        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user,[(self.username.get()), self.password.get())])
        result = c.fetchall()
        if result:
            self.logf.pack_forget()
            self.head['text'] = self.username.get() + '\n Logged In'
            self.head['pady'] = 150
        else:
            ms.showerror('Username or Password incorrect!')

    #New User
    def new_user(self):
        #Build Connectio to DB
        with sql.connect('faculty.db') as db:
            c = db.cursor()

        #Find existing username (if any), take proper action
        find_user = ('SELECT * FROM user WHERE username = ?')
        c.execute(find_user,[(self.username.get())])
        if c.fetchall():
            ms.showerror('Error!\nUsername already taken!')
        else:
            ms.showinfo('Faculty Registration Completed!')
            self.log()
