from task import Task
from task_DataBase import TaskDB
import tkinter as tk
from tkinter import ttk , font , messagebox , PhotoImage

window = tk.Tk()
window.title("To_Do_List")
window.configure(bg="#F0F0F0")
window.geometry("1200x800")


taskDB = TaskDB()

def save_task():

    task_title = task_entry.get().strip()
    if task_title and task_title != "Write your task here" :
         taskDB.add_task(task_title)
         task_entry.delete(0,tk.END)
         task_entry.configure(fg="black")
         load_tasks()
    else : 
         messagebox.showwarning("invalid title " , "please enter a good title !!")

def load_tasks() :
     for widget in canvas_inner.winfo_children() :
          widget.destroy()
    
     tasks_list = taskDB.get_all()
     display_tasks(tasks_list)

# here i get the image that i will use for the delete icone

delete_icon = PhotoImage(file = "delete_icon.png").subsample(24,24)
     
def display_tasks(list_tasks : list[Task]):
     
     for task in list_tasks :
          task_frame = tk.Frame(canvas_inner , bg= "#FAFAFA"  , bd=1, relief="solid" ) 

          task_lable = tk.Label(task_frame , text= task.title , font = ("Garamond" ,16 ) , bg = "#FAFAFA" , width = 25 , height=2 , anchor='w')
          task_lable.pack(side = tk.LEFT, pady = 8  )

          delete_button = tk.Button(task_frame , command= lambda tid=task.id :delete_task(tid) ,image= delete_icon , bg = "#F0F0F0"  )
          delete_button.pack( side=tk.RIGHT, fill= "x" , padx= 10)
        
          task.status_var = tk.BooleanVar(value=task.done) 
          checkbox = ttk.Checkbutton(task_frame , variable= task.status_var, command= lambda t = task : toggle_status(t))
          checkbox.pack( side=tk.RIGHT, padx= 5)

          task_frame.pack(fill=tk.X , padx= 5 , pady = 5)
          canvas_inner.update_idletasks()
          canvas.config(scrollregion=canvas.bbox("all"))   

def delete_task( task_id):
     print(task_id)
     taskDB.delete_by_id(task_id)
     load_tasks()

def toggle_status( task :Task):
     print(task.done)
     task.toggle_status()
     print(task.done)

     taskDB.update_status(task)
     load_tasks()


def on_entry_click(event):
     if task_entry.get() == "Write your task here" :
          task_entry.delete(0 , tk.END)
          task_entry.configure(fg= "black")

def on_focus_out(event):
     if not  task_entry.get().strip():
          task_entry.delete(0 , tk.END)
          task_entry.insert(0,"Write your task here")
          task_entry.configure(fg= "grey")




header_font = font.Font(family="Garamond" , size = 24 , weight="bold")
header_label = tk.Label(window, text= "To_Do_List App" , font=header_font , bg="#F0F0F0" , fg="#222" )
header_label.pack(pady= 20)

frame = tk.Frame(window , bg="#F0F0F0"  )
frame.pack(pady=15)

task_entry = tk.Entry(frame , font = ("Garamond" ,14 ) , bg = "white" , fg = "grey" ,  width=30)
task_entry.insert(0 , "Write your task here")
task_entry.bind("<FocusIn>" , on_entry_click)
task_entry.bind("<FocusOut>" , on_focus_out)
task_entry.pack(side=tk.LEFT, padx= 10)


add_button = tk.Button(frame , command= save_task , text="add task" , bg = "#28A745" , fg= "white" , height= 1 , width= 13  , font=("Ronoto" , 12) ,)
add_button.pack( side=tk.LEFT, pady= 10)

task_list_frame = tk.Frame(window , bg="#F0F0F0"  )
task_list_frame.pack(fill=tk.BOTH,expand= True  )

canvas = tk.Canvas(task_list_frame , bg= "#F0F0F0")
canvas.pack(side = tk.LEFT , fill= "both" , expand= True  ,  pady= 10 , padx= 10  )

scrollbar = ttk.Scrollbar( task_list_frame , command= canvas.yview) # this par defuat is vertical 
scrollbar.pack(side=tk.RIGHT , fill= tk.Y)

canvas.configure(yscrollcommand= scrollbar.set)
canvas_inner = tk.Frame(canvas , bg = "#EAEAEA" )
canvas.create_window((0,0 ) , window = canvas_inner , anchor= "nw")

canvas_inner.bind("<Configure>" , lambda e : canvas.configure(scrollregion= canvas.bbox("all")))

load_tasks()

window.mainloop()
