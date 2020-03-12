import cv2
import numpy as np 
import os
from os import listdir
from pandas.io import sql
import pandas as pd
from PIL import Image, ImageTk
import datetime
import time
import sqlalchemy

connection = sqlalchemy.create_engine('mysql+pymysql://root:open5920@localhost/facerecdb')
face_classifier = cv2.CascadeClassifier('HaarCascade/haarcascade_frontalface_default.xml')

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


def TakeImage(ID,NAME,DEPARTMENT,GENDER,ARRIVAL,EMAIL):
    if (ID != None and NAME!= None) or (ID!='' and NAME != ''):
        count =0
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                count+=1
                cv2.putText(frame,str(count),(x,y+h),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                file_name_path='TrainingImages/'+NAME+'.'+ID+'.'+str(count)+'.jpg'
                cv2.imwrite(file_name_path,gray[y:y+h,x:x+w])
                cv2.imshow('Capturing Your Image',frame)
                if cv2.waitKey(1)==13 or count==100:
                    cap.release()
                    cv2.destroyAllWindows()
                    cols = ['userid','name','department','gender','stoa','email']
                    df = pd.DataFrame(columns=cols)
                    df.loc[len(df)]=[int(ID),NAME,DEPARTMENT,GENDER,ARRIVAL,EMAIL]
                    df.to_sql(con=connection,name='details',if_exists='append',index=False)
                    return 'Image samples collected and record added!' 
    else:
        return 'Please enter your credentials'


def TrainImage():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    faces,Id=image_and_lables_extractor('TrainingImages')
    recognizer.train(faces,np.array(Id))
    recognizer.save('TrainingData.yml')
    return 'Images Trained Sucessfully!'
    
def TrackImage():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingData.yml")
    df = pd.read_sql('SELECT userid,name FROM details',con=connection)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names =  ['userid','name','date','time']
    attendance = pd.DataFrame(columns = col_names)
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=face_classifier.detectMultiScale(gray, 1.2,5)
        for x,y,w,h in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['userid'] == Id]['name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa[0],date,timeStamp]
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)      
        attendance=attendance.drop_duplicates(subset=['userid'],keep='first')    
        cv2.imshow('Taking Your Attendance',im) 
        if (cv2.waitKey(1)==13):
            break
    cam.release()
    cv2.destroyAllWindows()
    attendance.to_sql(con=connection,name='attendance',if_exists='append',index=False)
    if attendance.empty:
        return 'No Known record found!'
    else:
        return 'Attendance Taken!'

def getFromName(name):
    query="SELECT * FROM details WHERE name='"+name+"';"
    result = pd.read_sql(query,con=connection)
    return result

def getName(ID,text=None):
    query = "SELECT * from details WHERE userid="+str(ID)+";"
    result = pd.read_sql(query,con=connection)
    if text == None:
        return result['name'][0]
    else:
        return result

def searchUser(name):
    query = "SELECT * from details WHERE name='"+name+"';"
    result = pd.read_sql(query,con=connection)

def InsertShifts():
    df = pd.read_sql("SELECT * FROM fake_attendance;",con=connection) # reading the attendance
    IDs= df['userid'].tolist() 
    IDs=set(IDs)
    Dates= df['date'].tolist()
    Dates=set(Dates)
    cols=['userid','arrival','departure','workedhour','date']
    shifts = pd.DataFrame(columns=cols)
    for d in Dates:
        for i in IDs:
            df = pd.read_sql("SELECT time from fake_attendance WHERE date='"+str(d)+"' and userid="+str(i)+";",con=connection)
            checkin,checkout = df['time'][0],df['time'][1]
            HoursWorked = checkout-checkin
            shifts.loc[len(shifts)]=[i,str(checkin),str(checkout),str(HoursWorked),str(d)]
            shifts.to_sql(name='shifts',con=connection,if_exists='replace',index=False)
    return IDs,Dates

def lateReport():
    late = []
    Ids,Dates=InsertShifts()
    for d in Dates:
        for i in Ids:
            arrivalFrame = pd.read_sql("SELECT arrival FROM shifts WHERE userid="+str(i)+" and date='"+str(d)+"';",con=connection)
            scheduledFrame = pd.read_sql("SELECT stoa FROM details WHERE userid="+str(i)+";",con=connection)
            actualArrival,scheduledArrival = arrivalFrame['arrival'][0],scheduledFrame['stoa'][0]
            scheduledArrival=pd.to_timedelta(scheduledArrival)
            actualArrival=pd.to_timedelta(actualArrival)
            if actualArrival>scheduledArrival:
                name = getName(i)
                delay = actualArrival-scheduledArrival
                row = [d,i,name,delay]
                late.append(row)
    return late,Ids

def absentReport():
    absent = []
    allIds = pd.read_sql("SELECT userid FROM details;",con=connection)
    allIds=allIds['userid'].tolist()
    Ids,Dates = InsertShifts()
    for d in Dates:
        for i in allIds:
            if i not in Ids:
                name = getName(i)
                row = [d,i,name]
                absent.append(row)
    return absent 

def DailyReport():
    present=[]
    absent = absentReport()
    late,Ids = lateReport()
    myDate='2020-02-07'
    myDate=pd.to_datetime(myDate)
    cols=['date','userid','name']
    AbsentFrame = pd.DataFrame(absent,columns=cols)
    AbsentFrame.drop(AbsentFrame[AbsentFrame['date']!=myDate].index,inplace=True)
    del AbsentFrame['date']
    cols=['date','userid','name','delay']
    LateFrame =pd.DataFrame(late,columns=cols)
    LateFrame.drop(LateFrame[LateFrame['date']!=myDate].index,inplace=True)
    del LateFrame['date']
    for i in Ids:
        name = getName(i)
        row = [i,name]
        present.append(row)
    cols=['userid','name']
    presentFrame=pd.DataFrame(present,columns=cols)
    LateFrame = LateFrame.astype({'userid':int,'name':str,'delay':str})
    for i in LateFrame.index:
        string = LateFrame['delay'][i]
        LateFrame['delay'][i] = string[7:15]
    return presentFrame,AbsentFrame,LateFrame

def ImportExcel(presentFrame,AbsentFrame,LateFrame):
    filename = "Reports/Daily_Report.xlsx"
    writer=pd.ExcelWriter(filename,engine='xlsxwriter')
    presentFrame.to_excel(writer,sheet_name='present',index=False)
    AbsentFrame.to_excel(writer,sheet_name='absent',index=False)
    LateFrame.to_excel(writer,sheet_name='Late',index=False)
    writer.save()