#Modules
from tkinter import *
from tkinter import messagebox as ms
from tkinter import ttk
from tkinter import font
from tkinter import Message, Text
import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import sqlite3 as sql
import shutil
from openpyxl import Workbook

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
        self.n_name = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.n_question = StringVar()
        self.n_answer = StringVar()
        self.n_level = StringVar()
        self.subject = StringVar()
        self.studID = StringVar()
        self.studName = StringVar()
        self.n_subject = StringVar()
        self.options = ["What primary school did you attend?",
                        "What is the middle name of your father?",
                        "What time of the day were you born?",
                        "What was the last four digits of your first telephone number?"]
        self.level = open("Course\Level.txt").read().splitlines()
        self.arts = open("Course\Arts.txt").read().splitlines()
        self.science = open("Course\Science.txt").read().splitlines()
        self.courses = {"BA": self.arts, "BSc": self.science, "MA":self.arts, "MSc": self.science}

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
        self.n_level.set('')
        self.n_subject.set('')
        self.dashBf.pack_forget()
        self.head['text'] = 'Attendance'
        self.subCombo = ttk.Combobox(self.attendancef, textvariable = self.n_subject, font = ('', 15))
        self.subCombo.grid(row = 0, column = 2)
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
        id = self.studID.get()
        name = self.studName.get()
        #harcascadePath = "data/haarcascade/haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier('data\haarcascade\haarcascade_frontalface_default.xml')
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
                cv2.imwrite("TrainingImage\ "+ name +"."+ id +'.'+ str(sampleNum) + ".jpg", gray[y : y + h, x : x + w])
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
        res = "Images Saved for ID : " + id +" Name : "+ name
        row = [id , name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        ms.showinfo(res)

    def train(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier('data\haarcascade\haarcascade_frontalface_default.xml')

        imagePaths = [os.path.join('TrainingImage', f) for f in os.listdir('TrainingImage')]
        faces = []
        ids = []

        for imagePath in imagePaths:
            pilImage = Image.open(imagePath).convert('L')
            imageNP = np.array(pilImage, 'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNP)
            ids.append(id)

        recognizer.train(faces, np.array(ids))
        recognizer.save("TrainingImageLabel\Trainer.yml")
        ms.showinfo("Images Saved Succesfully!")

    def track(self):
        book = Workbook()
        sheet = book.active
        now = datetime.datetime.now()
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("TrainingImageLabel\Trainer.yml")
        faceCascade = cv2.CascadeClassifier('data\haarcascade\haarcascade_frontalface_default.xml')
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['ID', 'NAME', 'DATE', 'TIME']
        attendance = pd.DataFrame(columns = col_names)
        for i in range(1, 32):
            sheet.cell(row = 1, column = i+1).value = str(i) + '-' + str(now.month)
        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for(x, y, w, h) in faces:
                cv2.rectangle(im, (x,y), (x+w, y+h), (255, 0, 0), 2)
                id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                if conf < 50:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['ID'] == id]['Name'].values
                    tt = str(id) + "-" + aa
                    attendance.loc[len(attendance)] = [id, aa, date, timeStamp]
                    sheet.cell(row = int(id) + 1, column = 1).value = str(tt)
                    sheet.cell(row = int(id) + 1, column = int(now.day) + 1).value = "Present"

                else:
                    id = 'Unknown'
                    tt = str(id)
                if conf > 75:
                    noOfFile = len(os.listdir("ImagesUnknown")) + 1
                    cv2.imwrite("ImagesUnknown\Image" + str(noOfFile) + ".jpg", im[y:y+h, x:x+w])
                cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
            attendance = attendance.drop_duplicates(subset = ['ID'], keep = 'first')
            cv2.imshow('im', im)
            if (cv2.waitKey(1) == ord('q')):
                break
        course = self.n_level.get() + self.n_subject.get()
        book.save('Attendance\_' + course + '-' + str(now.month)+ '.xlsx')
        cam.release()
        cv2.destroyAllWindows()
        ms.showinfo("Done!")



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

    def changeSubject(self, event):
        self.subCombo['values'] = self.courses[self.levelCombo.get()]

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
        ttk.Combobox(self.regf, textvariable = self.n_question, values = self.options, font = ('', 15)).grid(row = 3, column = 1)
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
        self.levelCombo = ttk.Combobox(self.attendancef, textvariable = self.n_level, values = self.level, font = ('', 15))
        self.levelCombo.bind('<<ComboboxSelected>>', self.changeSubject)
        self.levelCombo.grid(row = 0, column = 1)
        Button(self.attendancef, text = 'Take Attendance', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.track).grid(row = 1, column = 1)
        Button(self.attendancef, text = 'Back', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.dashB).grid(row = 1, column = 2)

        self.studRegf = Frame(self.master, padx = 10, pady = 10)
        Label(self.studRegf, text = 'ID', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.studRegf, textvariable = self.studID, bd = 5, font = ('', 15)).grid(row = 0, column = 1)
        Label(self.studRegf, text = 'Name', font = ('', 20), pady = 5, padx = 5).grid(sticky = W)
        Entry(self.studRegf, textvariable = self.studName, bd = 5, font = ('', 15)).grid(row = 1, column = 1)
        Button(self.studRegf, text = 'Take Image', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.take_images).grid(row = 2, column = 1)
        Button(self.studRegf, text = 'Back', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.dashB).grid(row = 2, column = 2)
        Button(self.studRegf, text = 'Save', bd = 3, font = ('', 15), padx = 5, pady = 5, command = self.train).grid(row = 3, column = 1)

#Create Window and Application Object
root = Tk()
main(root)
root.mainloop()
