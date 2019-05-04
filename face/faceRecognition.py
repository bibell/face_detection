import numpy as np
import os
import cv2
from PIL import Image
import pickle, sqlite3

face_cascade = cv2.CascadeClassifier('Classifiers/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('Classifiers/haarcascade_eye.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/training_data.yml")

#To train using images captured or saved online
#img = cv2.imread("him.jpg")

def getProfile(Id):
    conn=sqlite3.connect("MyData")
    query="SELECT * FROM HIT WHERE ID="+str(Id)
    cursor=conn.execute(query)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile



#def validation(test):
#    # connecting to the db
#    conn = sqlite3.connect("MyData")

    # check if id already exists
#    query = "SELECT * FROM HIT WHERE test="+str(test)
    # returning the data in rows
#    cursor = conn.execute(query)
#    isRecordExist = 0
#    for row in cursor:
#           test=isRecordExist  
#    if isRecordExist == 1:
        #query = "UPDATE HIT SET Name='"+str(name)+"' WHERE ID='"+str(id)+"' WHERE department='"+str(department)+"' WHERE year='"+str(year)+"'"
#        print "access denaied"
#    else:
#        query = "INSERT INTO HIT(test) VALUES(''"+str(1)+"')"
#    conn.execute(query)
#    conn.commit()
#    conn.close()


faces=face_cascade.load('haarcascade_frontalface_default.xml')

#to train using frames from video
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX
while True:
    #comment the next line and make sure the image being read is names img when using imread
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        # Hiding the eye detector for now
        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex, ey, ew, eh) in eyes:
        #     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
        nbr_predicted, conf = recognizer.predict(gray[y:y+h, x:x+w])
        if conf < 90:
            profile=getProfile(nbr_predicted)
            
            #for cafterial use add some function that connects to the data base 
            #if the person id exist than some kind of sound must be heard
 
            #validation(test)  
            if profile != None:
                cv2.putText(img, "Name: "+str(profile[0]), (x, y+h+30), font, 0.4, (0, 0, 255), 1);
                cv2.putText(img, "IDS: " + str(profile[1]), (x, y + h + 50), font, 0.4, (0, 0, 255), 1);
                cv2.putText(img, "department: " + str(profile[2]), (x, y + h + 70), font, 0.4, (0, 0, 255), 1);
                cv2.putText(img, "year: " + str(profile[3]), (x, y + h + 90), font, 0.4, (0, 0, 255), 1); 
                cv2.putText(img, "test: " + str(profile[4]), (x, y + h + 90), font, 0.4, (0, 0, 255), 1);

                #hear add some function that write the id of the person in the database in increamented way
                #to determain wither the person reapit or not
            #for n in range(nbr_predicted):
            #     print(n)     
            #     if n==10:
            #        print "access denaid"
        else:
            cv2.putText(img, "Name: Unknown", (x, y + h + 30), font, 0.4, (0, 0, 255), 1);
            cv2.putText(img, "id: Unknown", (x, y + h + 50), font, 0.4, (0, 0, 255), 1);
            cv2.putText(img, "department: Unknown", (x, y + h + 70), font, 0.4, (0, 0, 255), 1);
            cv2.putText(img, "year: Unknown", (x, y + h + 90), font, 0.4, (0, 0, 255), 1);
            cv2.putText(img, "test: Unknown", (x, y + h + 90), font, 0.4, (0, 0, 255), 1);

    cv2.imshow('img', img)
    if(cv2.waitKey(1) == ord('q')):
        #there must be some kind of funcition over hear that elimenate the increamented id when we enter q
        break

cap.release()
cv2.destroyAllWindows()

