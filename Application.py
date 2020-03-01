from PIL import ImageTk, Image
import tkinter as tk
import Face_Recognition as fr

window = tk.Tk()
window.iconbitmap('GuiFiles/icon.ico')
#window.attributes('-fullscreen',True) # This line takes up the entire screen 
window.state('zoomed') # This line lets the application have a title bar
window.title('FaceRec Attandance System')
tk.Label(window,text='FACE RECOGNITION BASED ATTENDANCE SYSTEM',font=('Arial Bold',35)).place(x=60,y=0)

#Creating 
first_frame = tk.LabelFrame(window,text=' Add a new record: ',font=('Arial Bold',20),padx=10,pady=10)
first_frame.place(x=80,y=150)

second_frame = tk.LabelFrame(window,text='Notification',font=('Arial Bold',20),padx=160,pady=10)
second_frame.place(x=80,y=500)

# defining the controls of the record
tk.Label(first_frame,text='Enter Roll no:',font=('Lucia',19)).grid(row=0,column=0,padx=10,pady=10)
roll=tk.Entry(first_frame,width=60)
roll.grid(row=0,column=1)
tk.Label(first_frame,text='Enter Name: ',font=('Lucia',19)).grid(row=1,column=0)
name=tk.Entry(first_frame,width=60)
name.grid(row=1,column=1)
notification=tk.Label(second_frame,text='',font=('Lucia',16),bg='white')
notification.grid(row=0,column=1)


#defining the functions for all buttons
def clear():
    roll.delete(0,'end')
    name.delete(0,'end')
    notification.configure(text='')


def Quit():
    window.destroy()

def addRecord():
    ID=roll.get()
    NAME=name.get()
    message=fr.TakeImage(ID,NAME)
    notification.configure(text=message)

def trainRecord():
    fr.TrainImage()
    notification.configure(text='Images Trained Sucessfully')

def takeAttendance():
    message = fr.TrackImage()
    notification.configure(text=message)


#defining a second frame for buttons
third_frame = tk.LabelFrame(window)
third_frame.place(x=80,y=400)


#making the button to call the functions
tk.Button(first_frame,text='Clear',fg='white',bg='orange',font=('Lucida Fax',16),command=clear).grid(row=6,column=0,padx=10,pady=20)
tk.Button(first_frame,text='Add Record',fg='white',bg='blue',font=('Lucida Fax',16),command=addRecord).grid(row=6,column=1,padx=10,pady=20)
tk.Button(third_frame,text='Train Records',font=('Lucida Fax',16),fg='white',bg='green',command=trainRecord).grid(row=6,column=3,padx=20,pady=10)
tk.Button(third_frame,text='Take Attandance',font=('Lucida fax',16),fg='black',bg='Gray',command=takeAttendance).grid(row=6,column=4,padx=20,pady=10)
tk.Button(third_frame,text='Close',font=('Lucida fax',16),fg='white',bg='red',command=Quit).grid(row=6,column=7,padx=20,pady=10)



#creating a third frame for notification bar where user can get notified about the operations


#creating a fourth frame to add image
fourth_frame=tk.LabelFrame(window,width=100,height=100)
fourth_frame.place(x=670,y=170)
img=ImageTk.PhotoImage(Image.open('GuiFiles/Face-ID.jpg'))
tk.Label(fourth_frame,image=img,width=400,height=400).grid(column=0,row=0)

# creating a fifth frame 
fifth_frame = tk.LabelFrame(window,text='View Reports',font=('Arial Bold',20),width=100,height=100,padx=10,pady=10)
fifth_frame.place(x=1100,y=150)

# making report buttons
tk.Button(fifth_frame,text='Late Report',fg='white',bg='orange',font=('Lucida Fax',16)).pack(padx=10,pady=20,fill='x')
tk.Button(fifth_frame,text='Weekly Report',fg='white',bg='purple',font=('Lucida Fax',16)).pack(padx=10,pady=20,fill='x')
tk.Button(fifth_frame,text='Monthly Report',fg='white',bg='black',font=('Lucida Fax',16)).pack(padx=10,pady=20,fill='x')
tk.Button(fifth_frame,text='Annual Report',fg='white',bg='brown',font=('Lucida Fax',16)).pack(padx=10,pady=20,fill='x')

window.mainloop()
