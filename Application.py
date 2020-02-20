from PIL import ImageTk, Image
import tkinter as tk
import Face_Recognition as fr

window = tk.Tk()
window.iconbitmap('GuiFiles/icon.ico')
#window.attributes('-fullscreen',True) # This line takes up the entire screen 
window.state('zoomed') # This line lets the application have a title bar
window.title('FaceRec Attandance System')
tk.Label(window,text='FACE RECOGNITION BASED ATTENDANCE SYSTEM',font=('Arial Bold',35)).place(x=60,y=0)

#Creating a frame that would take input and give notification
first_frame = tk.LabelFrame(window,text=' Add a new record: ',font=('Lucida',20),padx=10,pady=10)
first_frame.place(x=40,y=150)

# defining the controls of the record
tk.Label(first_frame,text='Enter Name:',font=('Lucia',19)).grid(row=0,column=0,padx=10,pady=10)
roll=tk.Entry(first_frame,width=60)
roll.grid(row=0,column=1)
tk.Label(first_frame,text='Enter ID: ',font=('Lucia',19)).grid(row=1,column=0)
name=tk.Entry(first_frame,width=60)
name.grid(row=1,column=1)
tk.Label(first_frame,text='Notification',font=('Lucia',20)).grid(row=2,column=0,padx=10,pady=10)
notification=tk.Label(first_frame,text='',font=('Lucia',16))
notification.grid(row=2,column=1,padx=5,pady=10)


#defining the functions for all buttons
def clear():
    roll.delete(0,'end')
    name.delete(0,'end')
    notification.configure(text='')

def addRecord():
    ID=roll.get()
    NAME=name.get()
    message=fr.TakeImage(ID,NAME)
    notification.configure(text=message)
    return

def trainRecord():
    fr.TrainImage()
    notification.configure(text='Images Trained Sucessfully')

def takeAttendance():
    fr.TrackImage()
    notification.configure(text='')


#defining a second frame for buttons
second_frame = tk.LabelFrame(window)
second_frame.place(x=40,y=400)


#making the button to call the functions
tk.Button(second_frame,text='Clear',fg='white',bg='orange',font=('Lucida Fax',16),command=clear).grid(row=6,column=1,padx=10,pady=20)
tk.Button(second_frame,text='Add Record',fg='white',bg='blue',font=('Lucida Fax',16),command=addRecord).grid(row=6,column=2,padx=10,pady=20)
tk.Button(second_frame,text='Train Records',font=('Lucida Fax',16),fg='white',bg='green',command=trainRecord).grid(row=6,column=3,padx=10,pady=10)
tk.Button(second_frame,text='Take Attandance',font=('Lucida fax',16),fg='white',bg='black',command=takeAttendance).grid(row=6,column=4,padx=10,pady=10)
tk.Button(second_frame,text='Quit',font=('Lucida fax',16),fg='white',bg='red').grid(row=10,column=7,padx=10,pady=10)



#creating a third frame for notification bar where user can get notified about the operations


#creating a fourth frame to add image
fourth_frame=tk.LabelFrame(window,width=100,height=100)
fourth_frame.place(x=850,y=160)
img=ImageTk.PhotoImage(Image.open('GuiFiles/Face-ID.jpg'))
tk.Label(fourth_frame,image=img,width=400,height=400).grid(column=0,row=0)

window.mainloop()
