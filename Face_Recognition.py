import cv2
import numpy as np 
import os
from os import listdir
import pandas as pd
from PIL import Image, ImageTk
import datetime
import time

face_classifier = cv2.CascadeClassifier('HaarCascade\haarcascade_frontalface_default.xml')

def image_and_lables_extractor(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faces,Ids = [],[]
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage,'uint8')
        Id = int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces,Ids


def TakeImage():
    Id = input('Enter your Id: ')
    name = input('Enter your name: ')
    if (Id != None and name!= None):
        cap = cv2.VideoCapture(0)
        count =0
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                count+=1
                file_name_path='TrainingImages/'+name+'.'+Id+'.'+str(count)+'.jpg'
                cv2.imwrite(file_name_path,gray[y:y+h,x:x+w])
                cv2.imshow('Capturing Your Image',frame)
                cv2.putText(frame,str(count),(x,y+h),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                if cv2.waitKey(1)==13 or count==100:
                    cap.release()
                    cv2.destroyAllWindows()
                    print('Collecting Samples Complete!')
                    break

def TrainImage():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    faces,Id=image_and_lables_extractor('TrainingImages')
    recognizer.train(faces,np.array(Id))
    recognizer.save('TrainingData.yml')
    print('Images Trained Sucessfully!')

def TrackImage():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingData.yml")
    df=pd.read_csv("StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=face_classifier.detectMultiScale(gray, 1.2,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==13):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance/Attendance"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()



TakeImage()
TrainImage()
TrackImage()
