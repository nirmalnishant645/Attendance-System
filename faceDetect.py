import numpy as np
import cv2
import csv

cam = cv2.VideoCapture(0)

detector = cv2.CascadeClassifier('data\haarcascade\haarcascade_frontalface_default.xml')

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #incrementing sample number
        sampleNum += 1
        #saving the captured face in the dataset folder TrainingImage
        cv2.imwrite("TrainingImage1\ "+ 'Nishant' +"_"+ '11008' +'_'+ str(sampleNum) + ".jpg", gray[y : y + h, x : x + w])
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
res = "Images Saved for ID : " + '11008' +" Name : "+ 'Nishant'
row = ['11008' , 'Nishant']
with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
csvFile.close()
message.configure(text = res)
