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
        self.options = tuple()
        #Widgets
        self.widgets()
        #Dropdown options
        self.options = ("Q1.", "Q2.", "Q3.", "Q4.")
        self.n_question.set(self.options[0])


    #Login Function
    def login(self):
        #Build Connection to DB
        with sql.connect('faculty.db') as db:
            c= db.cursor()

        #Find user in the database and take proper action
        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user,[(self.username.get()), (self.password.get())])
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

        #Create new account
        insert = 'INSERT INTO user(username, password, question, answer) values(?, ?, ?, ?)'
        c.execute(insert,[(self.n_username.get()),(self.n_password.get()),(self.n_question.get()),(self.n_answer.get())])
        db.commit()

    #Frame Packing
    def log(self):
        self.username.set('')
        self.password.set('')
        self.regf.pack_forget()
        self.head['text'] = 'Login'
        self.logf.pack()

    def reg(self):
        self.n_username.set('')
        self.n_password.set('')
        self.n_question.set('')
        self.n_answer.set('')
        self.head['text'] = 'Register'
        self.regf.pack()

    #Draw widgets
    def widgets(self):
        self.head = Label(self.master, text = 'Login', font = ('', 35), pady = 10)
        self.head.pack()
        self.logf = Frame(self.master, padx = 10, pady = 10)
        Label(self.logf, text = 'Username: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.logf, textvariable = self.username, bd = 5, font = ('', 15)).grid(row = 0, column = 1)
        Label(self.logf, text = 'Password: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.logf, textvariable = self.password, bd = 5, font = ('', 15), show = '*').grid(row = 1, column = 1)
        Button(self.logf, text = ' Login ', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.login).grid()
        Button(self.logf, text = ' Register ', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.reg).grid(row = 2, column = 1)
        self.logf.pack()

        self.regf = Frame(self.master, padx = 10, pady = 10)
        Label(self.regf, text = 'Username: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.regf, textvariable = self.n_username, bd = 5, font = ('', 15)).grid(row = 0, column = 1)
        Label(self.regf, text = 'Password: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.regf, textvariable = self.n_password, bd = 5, font = ('', 15), show = '*').grid(row = 1, column = 1)
        Label(self.regf, text = 'Security Question: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        OptionMenu(self.regf, textvariable = self.n_question, value = *(self.options) ,  bd = 5, font = ('', 15)).grid(row = 2, column = 1)
        Label(self.regf, text = 'Answer: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.regf, textvariable = self.n_answer, bd = 5, font = ('', 15)).grid(row = 3, column = 1)
        Button(self.regf, text = 'Register', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.new_user).grid(row = 4, column = 1)
        Button(self.regf, text = 'Go to Login', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.log).grid(row = 4, column = 2)

#Create Window and Application Object
root = Tk()
main(root)
root.mainloop()
