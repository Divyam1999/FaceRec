from PIL import ImageTk, Image
import tkinter as tk


window = tk.Tk()
window.iconbitmap('GuiFiles/icon.ico')
#window.attributes('-fullscreen',True) # This line takes up the entire screen 
window.state('zoomed') # This line lets the application have a title bar
window.title('FaceRec Attandance System')
tk.Label(window,text='FACE RECOGNITION BASED ATTENDANCE SYSTEM',font=('Arial Bold',35)).place(x=60,y=0)

#Creating a frame that holds the controls to add a new record
first_frame = tk.LabelFrame(window,text=' Add a new record: ',font=('Lucida',20),padx=10,pady=10)
first_frame.place(x=40,y=150)

# defining the controls of the record
tk.Label(first_frame,text='Enter Name:',font=('Lucia',19)).grid(row=0,column=0,padx=10,pady=10)
tk.Entry(first_frame,width=60).grid(row=0,column=1)
tk.Label(first_frame,text='Enter ID: ',font=('Lucia',19)).grid(row=1,column=0)
tk.Entry(first_frame,width=60).grid(row=1,column=1)
tk.Button(first_frame,text='Clear',fg='white',bg='orange',font=('Lucida Fax',20)).grid(row=6,column=1,padx=10,pady=20)
tk.Button(first_frame,text='Add Record',fg='white',bg='blue',font=('Lucida Fax',20)).grid(row=6,column=4,padx=10,pady=20)

#creating a second frame for other features (like training and trackig students)
second_frame=tk.LabelFrame(window)
second_frame.place(x=40,y=480)
tk.Button(second_frame,text='Train Records',font=('Lucida Fax',20,),fg='white',bg='green').grid(row=10,column=1,padx=33,pady=10)
tk.Button(second_frame,text='Take Attandance',font=('Lucida fax',20),fg='white',bg='black').grid(row=10,column=4,padx=33,pady=10)
tk.Button(second_frame,text='Quit',font=('Lucida fax',20),fg='white',bg='red').grid(row=10,column=7,padx=33,pady=10)

#creating a third frame for notification bar where user can get notified about the operations
third_frame=tk.LabelFrame(window)
third_frame.place(x=40,y=600)
tk.Label(third_frame,text='Notification',font=('Lucia',20)).grid(row=0,column=0,padx=10,pady=10)
tk.Label(third_frame,text='',font=('Lucia',16)).grid(row=0,column=3,padx=10,pady=10)

#creating a fourth frame to add image
fourth_frame=tk.LabelFrame(window,width=100,height=100)
fourth_frame.place(x=850,y=160)
img=ImageTk.PhotoImage(Image.open('GuiFiles/Face-ID.jpg'))
tk.Label(fourth_frame,image=img,width=400,height=400).grid(column=0,row=0)

window.mainloop()
