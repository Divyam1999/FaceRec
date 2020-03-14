import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image,ImageTk
import Face_Recognition as fr

window = tk.Tk()
gender=tk.StringVar()
department=tk.StringVar()
hh=tk.StringVar()
mm=tk.StringVar()
ss=tk.StringVar()
window.state('zoomed')
window.iconbitmap('GuiFiles/icon.ico')
window.title('FaceRec Attendance System')

#creating three frames for heading, body and buttons
top_frame  = tk.Frame(window,height=150,width=1400,bg='#ffffb3')
top_frame.place(x=0,y=0)
bottom_frame = tk.Frame(window,height=450,width=1400,bg='#b3ccff')
bottom_frame.place(x=0,y=150)
last_frame=tk.Frame(window,height=200,width=1400,bg='#d9ffb3')
last_frame.place(x=0,y=600)

image_frame = tk.LabelFrame(bottom_frame,width=100,height=100)
image_frame.place(x=1000,y=70)
search_frame = tk.LabelFrame(bottom_frame,text='Search',font=('Arial Bold',16),width=700,height=100,bg='#b3ccff',padx=10,pady=10)
search_frame.place(x=60,y=40)
add_frame = tk.LabelFrame(bottom_frame,text='Add a new record',font=('Arial Bold',16),width=700,height=500,bg='#b3ccff',padx=20,pady=10)
add_frame.place(x=60,y=150)

button_frame = tk.LabelFrame(last_frame,padx=10,pady=10,bg='#d9ffb3')
button_frame.place(x=60,y=10)

info_frame = tk.LabelFrame(last_frame,padx=10,pady=10,bg='#d9ffb3')
info_frame.place(x=1100,y=40)

logo=ImageTk.PhotoImage(Image.open('GuiFiles/icon.ico'))
tk.Label(top_frame,image=logo,bg='#ffffb3').place(x=30,y=10)
tk.Label(top_frame,text='FACE RECOGNITION  BASED ATTENDANCE SYSTEM',font=('Arial Bold',30),bg='#ffffb3').place(x=210,y=60)
#Defining all the functions
def clear():
    Id.delete(0,'end')
    name.delete(0,'end')
    email.delete(0,'end')
    hh.delete(0,'end')
    mm.delete(0,'end')
    ss.delete(0,'end')
    department.set('')

def search():
    uid = userid.get()
    name = nm.get()
    if name == '' and uid=='':
        messagebox.showerror('Error','Please enter Id or name to search')
    else:
        sw = tk.Toplevel()
        sw.title('Search Result')
        sw.geometry('800x500')
        sw.resizable(0,0)
        sw.iconbitmap('GuiFiles/icon.ico')
        sw.configure(background='#d9ffb3')
        hf = tk.Frame(sw,height=100,width=800,bg='#b3ccff')
        hf.place(x=0,y=0)
        logo=ImageTk.PhotoImage(Image.open('GuiFiles/search.png'))
        tk.Label(hf,image=logo,bg='#b3ccff',height=60,width=60).place(x=30,y=10)
        tk.Label(hf,text='SEARCH RECORDS',font=('Arial Bold',18),bg='#b3ccff').place(x=100,y=10)
        sf = tk.LabelFrame(sw,height=200,width=800,bg='#ffffb3')
        sf.place(x=20,y=140)
        cols = ['userid','name','department','stoa','gender','email']
        for item in cols:
            tk.Label(sf,text=item.capitalize(),font=('Arial Bold',16),bg='#ffffb3').grid(row=0,column=cols.index(item),padx=10,pady=10)
        if name == '' or name == None:
            result = fr.getName(uid,'all')
            if result.empty:
                tk.Label(sf,text='No Record Exists',font=('Lucia',12),bg='#ffffb3').grid(row=2,column=1,columnspan=2)
            else:
                for i in cols:
                    for j in range(len(result)):
                        tk.Label(sf,text=result[i][j],font=('Lucia',12),bg='#ffffb3').grid(row=j+1,column=cols.index(i))
        else:
            result = fr.getFromName(name)
            if result.empty:
                tk.Label(sf,text='No Record Exists',font=('Lucia',12),bg='#ffffb3').grid(row=2,column=1,columnspan=2)
            else:
                for i in cols:
                    for j in range(len(result)):
                        tk.Label(sf,text=result[i][j],font=('Lucia',12),bg='#ffffb3').grid(row=j+1,column=cols.index(i))
        tk.Button(sw,text='Close',command=lambda:sw.destroy(),fg='white',bg='red',font=('Lucia',16)).place(x=700,y=400)
        sw.mainloop()

def train():
    msg = fr.TrainImage()
    messagebox.showinfo('Notification',msg)

def TakeAttendance():
    msg = fr.TrackImage()
    messagebox.showinfo('Notification',msg)

def addrecord():
    ID=Id.get()
    NAME=name.get()
    EMAIL = email.get()
    HH = hh.get()
    MM = mm.get()
    SS = ss.get()
    GENDER = gender.get()
    ARRIVAL = ''+str(HH)+':'+str(MM)+':'+str(SS)
    DEPARTMENT = department.get()
    if ID =='' or NAME=='' or EMAIL=='' or ARRIVAL=='::' or GENDER=='':
        messagebox.showerror('Error','Please fill in all the details')
    else:
        msg = fr.TakeImage(int(ID),NAME,DEPARTMENT,GENDER,ARRIVAL,EMAIL)
        messagebox.showinfo('Notification',msg)

def about():
    myfile = open('README.md','r')
    aboutText = myfile.read()
    myfile.close()
    about_window = tk.Toplevel()
    about_window.title('About FaceRec')
    about_window.configure(background='#b3ccff')
    about_window.geometry("500x400")
    about_window.iconbitmap('GuiFiles/icon.ico')
    about_window.resizable(0,0)
    hf=tk.Frame(about_window,height=80,width=500,bg='#d9ffb3')
    hf.place(x=0,y=0)
    logo=ImageTk.PhotoImage(Image.open('GuiFiles/search.png'))
    tk.Label(hf,image=logo,bg='#d9ffb3',height=60,width=60).place(x=30,y=10)
    tk.Label(hf,text='About FaceRec Attendance System',font=('Arial Bold',16),bg='#d9ffb3').place(x=90,y=40)
    tk.Message(about_window,text=aboutText,font=('Lucia',9),bg='#b3ccff').place(x=10,y=80)
    tk.Button(about_window,text='Close',command=lambda:about_window.destroy(),bg='red',fg='white',font=('Lucia',14)).place(x=400,y=330)
    about_window.mainloop()

def dailyReport():
    messagebox.showinfo('Notification',"Please wait while report gets generated")
    rw = tk.Toplevel()
    rw.geometry('900x500')
    rw.resizable(0,0)
    rw.title('Daily Report')
    rw.iconbitmap('GuiFiles/icon.ico')
    hf = tk.Frame(rw,height=100,width=900,bg='#b3ccff')
    hf.place(x=0,y=0)
    logo=ImageTk.PhotoImage(Image.open('GuiFiles/search.png'))
    tk.Label(hf,image=logo,bg='#b3ccff',height=60,width=60).place(x=30,y=10)
    tk.Label(hf,text='DAILY REPORT',font=('Arial Bold',20),bg='#b3ccff').place(x=100,y=10)
    rw.configure(background='#d9ffb3')
    pf = tk.LabelFrame(rw,text='Present Today',font=('Arial Bold',18),bg='#ffffb3')
    pf.grid(row=0,column=0,padx=40,pady=120,columnspan=3)
    af = tk.LabelFrame(rw,text='Absent Today',font=('Arial Bold',18),bg='#ffffb3')
    af.grid(row=0,column=4,padx=40,pady=120,columnspan=3)
    lf = tk.LabelFrame(rw,text='Late Today',font=('Arial Bold',18),bg='#ffffb3')
    lf.grid(row=0,column=8,padx=40,pady=120,columnspan=3)
    p,a,l=fr.DailyReport()
    col = ['userid','name']
    col_l= ['userid','name','delay']
    for i in col:
        tk.Label(pf,text=i.capitalize(),font=('Arial',12),bg='#ffffb3').grid(row=0,column=col.index(i))
        tk.Label(af,text=i.capitalize(),font=('Arial',12),bg='#ffffb3').grid(row=0,column=col.index(i))
        for j in p.index:
            tk.Label(pf,text=p[i][j],font=('Lucia',14),bg='#ffffb3').grid(row=j+1,column=col.index(i))
        for j in a.index:
            tk.Label(af,text=a[i][j],font=('Lucia',14),bg='#ffffb3').grid(row=j+1,column=col.index(i))
    for i in col_l:
        tk.Label(lf,text=i.capitalize(),font=('Arial',12),bg='#ffffb3').grid(row=0,column=col_l.index(i))
        for j in l.index:
            tk.Label(lf,text=l[i][j],font=('Lucia',14),bg='#ffffb3').grid(row=j+1,column=col_l.index(i))
    tk.Button(rw,text='Import Excel',command=lambda:fr.ImportExcel(p,a,l),font=('Lucia',16),bg='green',fg='white').grid(row=200,column=2)
    tk.Button(rw,text='Close',command=lambda:rw.destroy(),font=('Lucia',16),bg='red',fg='white').grid(row=200,column=8)
    rw.mainloop()

#Search_Frame
tk.Label(search_frame,text='ID: ',font=('Lucia',16),bg='#b3ccff').grid(row=0,column=0)
userid=tk.Entry(search_frame,width=10)
userid.grid(row=0,column=1)
tk.Label(search_frame,text=' OR Name: ',font=('Lucia',16),bg='#b3ccff').grid(row=0,column=2)
nm=tk.Entry(search_frame,width=40)
nm.grid(row=0,column=3)
tk.Button(search_frame,text='Search',bg='#008080',fg='#ffffff',font=('Sans serif',15),command=search).grid(row=0,column=4,padx=10)

#defining the lists for add_frame
hours=['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
minutes=hours
for i in range(24,61):
    minutes.append(str(i))
seconds=minutes
#Add_frame
tk.Label(add_frame,text='ID:',font=('Lucia',16),bg='#b3ccff').grid(row=0,column=0)
Id=tk.Entry(add_frame,width=10)
Id.grid(row=0,column=1)
tk.Label(add_frame,text='Department:',font=('Lucia',16),bg='#b3ccff').grid(row=0,column=2,pady=10)
designation = ttk.Combobox(add_frame,textvariable=department,values=['Design','Development','Finance','Marketing','Sales','Security','Testing'])
designation.grid(row=0,column=3,pady=10)
tk.Label(add_frame,text='Name:',font=('Lucia',16),bg='#b3ccff').grid(row=1,column=0)
name=tk.Entry(add_frame,width=50)
name.grid(row=1,column=1,columnspan=2,padx=10,pady=10)
tk.Label(add_frame,text='Gender: ',font=('Lucia',16),bg='#b3ccff').grid(row=2,column=0)
tk.Radiobutton(add_frame,text='Male',value='M',variable=gender,bg='#b3ccff',font=('Lucia',16)).grid(row=2,column=1)
tk.Radiobutton(add_frame,text='Female',value='F',variable=gender,bg='#b3ccff',font=('Lucia',16)).grid(row=2,column=1,columnspan=2)
gender.set('M')
tk.Label(add_frame,text='Email: ',font=('Lucia',16),bg='#b3ccff').grid(row=3,column=0)
email=tk.Entry(add_frame,width=60)
email.grid(row=3,column=1,columnspan=2,padx=10,pady=10)
tk.Label(add_frame,text='Arrival Time(HH:MM:SS)',font=('Lucia',16),bg='#b3ccff').grid(row=2,column=3)
hh=ttk.Combobox(add_frame,textvariable=hh,values=hours,width=3)
hh.grid(row=2,column=4,padx=3,pady=20)
mm=ttk.Combobox(add_frame,textvariable=mm,values=minutes,width=3)
mm.grid(row=2,column=5,padx=3)
ss=ttk.Combobox(add_frame,textvariable=ss,values=seconds,width=3)
ss.grid(row=2,column=6,padx=3)

tk.Button(add_frame,text='Clear',bg='#008080',fg='#ffffff',font=('Sans serif',15),command=clear).grid(row=4,column=1)
tk.Button(add_frame,text='Add Face',bg='#008080',fg='#ffffff',font=('Sans serif',15),command=addrecord).grid(row=4,column=4,columnspan=3)

#button_frame
tk.Button(button_frame,text='Train Records',bg='#008080',fg='#ffffff',font=('Sans serif',15),command=train).grid(row=0,column=0,padx=25,pady=10)
tk.Button(button_frame,text='Take Attendance',bg='#008080',fg='#ffffff',font=('Sans serif',15),command=TakeAttendance).grid(row=0,column=1,padx=25,pady=10)
tk.Button(button_frame,text='Get Daily Report',bg='#008080',fg='#ffffff',font=('Sans serif',15),command=dailyReport).grid(row=0,column=2,padx=26,pady=10)
tk.Button(button_frame,text='About',bg='#008080',fg='#ffffff',font=('Sans serif',15),command=about).grid(row=0,column=3,padx=26,pady=10)
tk.Button(button_frame,text='Close',bg='#008080',fg='#ffffff',font=('Sans serif',15),command=lambda:window.destroy()).grid(row=0,column=4,padx=26,pady=10)

#info_frame
tk.Label(info_frame,text='A Project by: Kumar Divyam',font=('Sans serif',10),bg='#d9ffb3').pack()

img=ImageTk.PhotoImage(Image.open('GuiFiles/Face-ID.jpg'))
tk.Label(image_frame,image=img).pack(padx=20,pady=20)
window.mainloop()