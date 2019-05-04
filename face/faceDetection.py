import cv2
import time
import os
import sqlite3

def haramayaDataBase(name, id, department,year):
    # connecting to the db
    conn = sqlite3.connect("MyData")

    # check if id already exists
    query = "SELECT * FROM HDBASE WHERE ID="+str(id)
    # returning the data in rows
    cursor = conn.execute(query)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 1:
        query = "UPDATE HDBASE SET Name='"+str(name)+"' WHERE ID='"+str(id)+"' WHERE department='"+str(department)+"' WHERE year='"+str(year)+"'"
    else:
        query = "INSERT INTO HDBASE(Name,ID,department,year) VALUES('"+str(name)+"','"+str(id)+"','"+str(department)+"' ,'"+str(year)+"')"
    conn.execute(query)
    conn.commit()
    conn.close()


def nothing(x):
    pass

cv2.namedWindow("user interface")
cv2.createTrackbar("enter your name","user interface",0,170,nothing)

face_cas=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)


name = raw_input('Enter your name: ')
id = raw_input('Enter user id: ')
department = raw_input('Enter department: ')
year=raw_input('Enter year of study: ')
haramayaDataBase(name, id, department, year)


sample_number=0

while True:
   #a=a+1
     
   chake,frame=cam.read()
   gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
   
   faces=face_cas.detectMultiScale(frame,
                                   scaleFactor=1.2,
                                   minNeighbors=5,
                                   minSize=(20,20))  

   for (x,y,w,h) in faces:
       sample_number+=1

       if not os.path.exists('haramaya_students_dataSets'):
            os.makedirs('haramaya_students_dataSets')

       cv2.imwrite('haramaya_students_dataSets/User.'+str(id)+"."+str(sample_number)+".jpg",  gray[y:y+h,x:x+w])
       cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
       
   cv2.imshow('face detection system',frame)
   cv2.waitKey(1)
   if (sample_number>20):
             cam.release()
             cv2.destroyAllWindows() 
             break;
time.sleep(2)
#cam.release()
#cv2.distroyAllwindows()
