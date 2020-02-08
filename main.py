#Modules
from tkinter import *
from tkinter import messagebox as ms
from tkinter import ttk
from tkinter import font
import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import datetime
import sqlite3 as sql

#Make database and users table(if doesn't already exist)
with sql.connect('faculty.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (name TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, question TEXT NOT NULL, answer TEXT NOT NULL);')
db.commit()
db.close()

#main class
class main:
    def __init__(self, master):
        #Window
        self.master = master
        #Variables
        self.name = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.question = StringVar()
        self.answer = StringVar()
        self.course = StringVar()
        self.n_name = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.n_question = StringVar()
        self.n_answer = StringVar()
        self.n_course = StringVar()
        self.studID = StringVar()
        self.studName = StringVar()
        self.options = list()
        #Widgets
        self.widgets()

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
            ms.showinfo(self.username.get() + 'succesfully logged in!')
            self.dashB()
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
        insert = 'INSERT INTO user(name, username, password, question, answer) values(?, ?, ?, ?, ?)'
        c.execute(insert,[(self.n_name.get()),(self.n_username.get()),(self.n_password.get()),(self.n_question.get()),(self.n_answer.get())])
        db.commit()

    #Attendance
    def attendance(self):
        self.course.set('')
        self.dashBf.pack_forget()
        self.head['text'] = 'Attendance'
        self.attendancef.pack()

    #Report
    def report(self):
        return None

    #Student Registration
    def studReg(self):
        self.studID.set('')
        self.studName.set('')
        self.dashBf.pack_forget()
        self.head['text'] = 'Student Registration'
        self.studRegf.pack()

    def take_images(self):
        cam = cv2.VideoCapture(0)
        #harcascadePath = "data/haarcascade/haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier('F:\GitHub\Attendance-System\data\haarcascade\haarcascade_frontalface_default.xml')
        sampleNum = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                #incrementing sample number
                sampleNum += 1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+ self.studName +"_"+ self.studID +'_'+ str(sampleNum) + ".jpg", gray[y : y + h, x : x + w])
                #display the frame
                cv2.imshow('frame', img)
            #wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 60:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + self.studID +" Name : "+ studName
        row = [Id , name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text = res)

    def track(self):
        return None

    #Logout
    def logout(self):
        self.log()
        self.dashBf.pack_forget()

    #Frame Packing
    def log(self):
        self.username.set('')
        self.password.set('')
        self.regf.pack_forget()
        self.head['text'] = 'Login'
        self.logf.pack()

    def reg(self):
        self.n_name.set('')
        self.n_username.set('')
        self.n_password.set('')
        self.n_question.set('')
        self.n_answer.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Register'
        self.regf.pack()

    def dashB(self):
        self.attendancef.pack_forget()
        self.studRegf.pack_forget()
        self.logf.pack_forget()
        with sql.connect('faculty.db') as db:
            c = db.cursor()
        find_name = ('SELECT name FROM user WHERE username = ?')
        c.execute(find_name,[(self.username.get())])
        name = c.fetchone()
        self.head['text'] = 'Welcome ' + name[0]
        self.dashBf.pack()

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
        Label(self.regf, text = 'Name: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.regf, textvariable = self.n_name, bd = 5, font = ('', 15)).grid(row = 0, column = 1)
        Label(self.regf, text = 'Username: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.regf, textvariable = self.n_username, bd = 5, font = ('', 15)).grid(row = 1, column = 1)
        Label(self.regf, text = 'Password: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.regf, textvariable = self.n_password, bd = 5, font = ('', 15), show = '*').grid(row = 2, column = 1)
        Label(self.regf, text = 'Security Question: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        ttk.Combobox(self.regf, textvariable = self.n_question, values = ["1","2","3","4"], font = ('', 15)).grid(row = 3, column = 1)
        Label(self.regf, text = 'Answer: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.regf, textvariable = self.n_answer, bd = 5, font = ('', 15)).grid(row = 4, column = 1)
        Button(self.regf, text = 'Register', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.new_user).grid(row = 5, column = 1)
        Button(self.regf, text = 'Go to Login', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.log).grid(row = 5, column = 2)

        self.dashBf = Frame(self.master, padx = 10, pady = 10)
        Button(self.dashBf, text = 'Attendance', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.attendance).grid(row = 0, column = 1)
        Button(self.dashBf, text = 'Report', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.report).grid(row = 1, column = 1)
        Button(self.dashBf, text = 'Student Registration', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.studReg).grid(row = 2, column = 1)
        Button(self.dashBf, text = 'Logout', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.logout).grid(row = 3, column = 1)

        self.attendancef = Frame(self.master, padx = 10, pady = 10)
        Label(self.attendancef, text = 'Select Course: ', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        ttk.Combobox(self.attendancef, textvariable = self.n_course, values = ["a","b","c","d"], font = ('', 15)).grid(row = 0, column = 1)
        Button(self.attendancef, text = 'Take Attendance', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.track).grid(row = 1, column = 1)
        Button(self.attendancef, text = 'Back', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.dashB).grid(row = 1, column = 2)

        self.studRegf = Frame(self.master, padx = 10, pady = 10)
        Label(self.studRegf, text = 'ID', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.studRegf, textvariable = self.studID, bd = 5, font = ('', 15)).grid(row = 0, column = 1)
        Label(self.studRegf, text = 'Name', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.studRegf, textvariable = self.studName, bd = 5, font = ('', 15)).grid(row = 1, column = 1)
        Button(self.studRegf, text = 'Take Image', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.take_images).grid(row = 2, column = 1)
        Button(self.studRegf, text = 'Back', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.dashB).grid(row = 2, column = 2)

#Create Window and Application Object
root = Tk()
main(root)
root.mainloop()
