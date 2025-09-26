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
    task_priority = priority_combobox.get()

    if (not task_title) or (task_title == "Write your task here") :
        messagebox.showwarning("invalid title " , "please enter a good title !!")
    elif not task_priority : 
          messagebox.showwarning("invalid priority " , "please choose the priority !!")
    else :
        taskDB.add_task(task_title , task_priority)
        task_entry.delete(0,tk.END)
        task_entry.configure(fg="black")
        load_tasks()


def load_tasks() :     
    for frame in [pending_inner , encours_inner , done_inner] :
        for widget in frame.winfo_children() :
            widget.destroy()
        
    tasks_list = taskDB.get_all()
    display_tasks(tasks_list)


delete_icon = PhotoImage(file = "delete_icon.png").subsample(24,24)
     
def display_tasks(list_tasks : list[Task]):
     
     for task in list_tasks :
              
          if task.status == "Pending":
              parent = pending_inner
          elif task.status == "EnCours":
              parent = encours_inner
          else:
                  parent = done_inner
      
          task_frame = tk.Frame(parent, bg="#FAFAFA", bd=1, relief="solid")  # FIX: add parent
          task_frame.pack(fill=tk.X, padx=5, pady=5)
      
          task_lable = tk.Label(task_frame , text= task.title , font = ("Garamond" ,16 ) , bg = "#FAFAFA"  , height=2 , anchor='w')
          task_lable.pack(side = tk.LEFT, pady = 8 )

          delete_button = tk.Button(task_frame , command= lambda tid=task.id :delete_task(tid) ,image= delete_icon , bg = "#F0F0F0"  )
          delete_button.pack( side=tk.RIGHT, fill= "x" , padx= 10)
      
          n_status = tk.StringVar(value=task.status)
          statuschoosen = ttk.Combobox(task_frame, textvariable = n_status , values=["Pending","EnCours","Done"] , width= 8 , state= 'readonly')
          statuschoosen.pack(side= tk.RIGHT , padx= 5)
          statuschoosen.bind("<<ComboboxSelected>>" , lambda e, t= task , v_status = n_status :update_status(t , v_status.get()))
          
          n_priority = tk.StringVar(value=task.priority)
          prioritychoosen = ttk.Combobox(task_frame, textvariable = n_priority , values=["P0","P1","P2" , "P3"] , width= 8 , state= 'readonly')
          prioritychoosen.pack(side= tk.RIGHT , padx= 5)
          prioritychoosen.bind("<<ComboboxSelected>>" , lambda e, t= task , v_priority = n_priority :update_priority(t , v_priority.get()))



def delete_task( task_id):
     print(task_id)
     taskDB.delete_by_id(task_id)
     load_tasks()

def update_status( task :Task , new_status):
     task.status = new_status
     taskDB.update(task)
     load_tasks()

def update_priority( task :Task , new_priority):
     task.priority = new_priority
     taskDB.update(task)
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

priority_combobox = ttk.Combobox(frame, values=["P0", "P1", "P2", "P3"], width=3, state="readonly")
priority_combobox.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(frame , command= save_task , text="add task" , bg = "#28A745" , fg= "white" , height= 1 , width= 13  , font=("Ronoto" , 12) ,)
add_button.pack( side=tk.LEFT, pady= 10)

task_list_frame = tk.Frame(window , bg="#F0F0F0"  )
task_list_frame.pack(fill=tk.BOTH,expand= True  )

pending_frame = tk.Frame(task_list_frame, bg="#EAEAEA", bd=1, relief="solid")
pending_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
tk.Label(pending_frame, text="Pending", font=("Garamond", 16, "bold"), bg="#EAEAEA").pack(pady=5)

pending_canvas = tk.Canvas(pending_frame, bg="#FAFAFA")
pending_scrollbar = ttk.Scrollbar(pending_frame, orient="vertical", command=pending_canvas.yview)
pending_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
pending_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
pending_canvas.configure(yscrollcommand=pending_scrollbar.set)
pending_inner = tk.Frame(pending_canvas, bg="#FAFAFA")
pending_canvas.create_window((0, 0), window=pending_inner, anchor="nw")
pending_inner.bind("<Configure>", lambda e: pending_canvas.configure(scrollregion=pending_canvas.bbox("all")))



encours_frame = tk.Frame(task_list_frame, bg="#EAEAEA", bd=1, relief="solid")
encours_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
tk.Label(encours_frame, text="EnCours", font=("Garamond", 16, "bold"), bg="#EAEAEA").pack(pady=5)
encours_canvas = tk.Canvas(encours_frame, bg="#FAFAFA")
encours_scrollbar = ttk.Scrollbar(encours_frame , orient='vertical' ,command= encours_canvas.yview)
encours_scrollbar.pack(side=tk.RIGHT , fill=tk.Y)
encours_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
encours_canvas.configure(yscrollcommand = encours_scrollbar.set)
encours_inner = tk.Frame(encours_canvas, bg="#FAFAFA")
encours_canvas.create_window((0,0), window=encours_inner, anchor="nw")
encours_inner.bind("<Configure>", lambda e: encours_canvas.configure(scrollregion=encours_canvas.bbox("all")))

done_frame = tk.Frame(task_list_frame, bg="#EAEAEA", bd=1, relief="solid")
done_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
tk.Label(done_frame, text="Done", font=("Garamond", 16, "bold"), bg="#EAEAEA").pack(pady=5)
done_canvas = tk.Canvas(done_frame, bg="#FAFAFA")
done_scrollbar = tk.Scrollbar(done_frame , orient= 'vertical' , command=done_canvas.yview)
done_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
done_canvas.configure(yscrollcommand= done_scrollbar.set)
done_inner = tk.Frame(done_canvas, bg="#FAFAFA")
done_canvas.create_window((0,0), window=done_inner, anchor="nw")
done_inner.bind("<Configure>", lambda e: done_canvas.configure(scrollregion=done_canvas.bbox("all")))

load_tasks()

window.mainloop()
