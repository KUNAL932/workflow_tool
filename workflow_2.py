from datetime import datetime
from tkinter import *
import tkinter as tk
import json

class Task:
    def __init__(self, task_id, name, date, action=None, is_start=False, is_end=False, next_node=None, previous_node=None):
        self.task_id = task_id
        self.name = name
        self.date = date
        self.jobs = {
            "trigger": action,
            # "action": restapi
        }
        self.is_start = is_start
        self.is_end = is_end
        self.next_node = next_node
        self.previous_node = previous_node

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "name": self.name,
            "date": self.date.isoformat(),
            "jobs": self.jobs,
            "is_start": self.is_start,
            "is_end": self.is_end,
            "next_node": self.next_node.task_id if self.next_node else None,
            "previous_node": self.previous_node.task_id if self.previous_node else None,
        }

tasks = []

def create_schedule():
    time = str(time_entry.get())
    schedule_name = str(schedule_entry.get())
    schedule = {
        "name": schedule_name,
        "time": time,  # Every day at 5 AM
        "day": "Monday",
        "interval": {
            "day": "",
            "hours": "",
            "minutes": ""
        },
    }
    tasks.append(schedule)

def create_task(name, date, count, action, is_start=False, is_end=False):
    task_ids = "task_000{}".format(count)
    task1 = Task(task_ids, name, date, action, is_start, is_end)
    return task1

def add_rest_api(rest_url,get_or_post,params_entry):
    root2.destroy()
    rest_url_val = rest_url.get()
    params_val = params_entry.get()
    restapi = {
        "restapi_id": "restapi_0001",
        "url": str(rest_url_val),
        "method": get_or_post,
        "params": params_val,
        "headers": {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'},
    }
    tasks.append(restapi)

def delete_task():
    if tasks:
        tasks.pop()
        print("deleted ..", tasks)
        return
    print("Nothing to remove in the list")

# Create the main window
root = tk.Tk()
root.title("Workflow HomePage")
root.geometry("400x400")

# Create a button and attach the action_window function to it
def action_window():

    global rest_url_val, root2
    root2 = tk.Tk()
    rest_url = tk.Entry(root2, width="15")
    rest_url.pack(pady=20)
   
    def show(): 
        label.config( text = clicked.get() ) 
    
    # Dropdown menu options 
    options = [ 
       "GET",
       "POST",
       "PUT",
       "DELETE"
    ] 
    
    # datatype of menu text 
    clicked = StringVar() 
    
    # initial menu text 
    clicked.set( "GET" ) 
    
    # Create Dropdown menu 
    drop = OptionMenu( root2 , clicked , *options ) 
    drop.pack() 
    
    # Create button, it will change label text 
    button = Button( root2 , text = "click Me" , command = show ).pack() 
    
    # Create Label 
    label = Label( root2 , text = " " ) 
    label.pack() 
    get_or_post = str(clicked.get())
    params_entry = tk.Entry(root2, width="17")
    params_entry.insert(0, 'Enter Params')
    params_entry.pack(pady=20)
    rest_button = tk.Button(root2, text="Get Rest API", command=lambda: add_rest_api(rest_url,get_or_post,params_entry))
    rest_button.pack(pady=20)
    root2.mainloop()
def submit_task():
    root.destroy()

time_entry = tk.Entry(root, width="17")
time_entry.insert(0, '0 5 * * *')
time_entry.pack(pady=20)
schedule_entry = tk.Entry(root, width="17")
schedule_entry.insert(0, 'Enter Name')
schedule_entry.pack(pady=20)
schedule_button = tk.Button(root, text="Schedule a Task", command=create_schedule, width="15")
schedule_button.pack(pady=20)
action_button = tk.Button(root, text="Action", command=action_window, width="15")
action_button.pack(pady=20)
delete_button = tk.Button(root, text="Delete the task", command=delete_task, width="15")
delete_button.pack(pady=20)

submit_button = tk.Button(root, text="Submit", command=submit_task, width="15")
submit_button.pack(pady=20)
# Start the Tkinter event loop
root.mainloop()

count = 0
head = None
task_linked_list = None
for i in tasks:
    if count == 0:
        task_linked_list = create_task(is_start=True, name="Scheduler",date=datetime.now(), count=count, is_end=False, action=i)
        head = task_linked_list
    elif count == len(tasks) - 1:
        if task_linked_list:
            task_linked_list.next_node = create_task(is_start=False, name="action", date=datetime.now(), count=count, is_end=True, action=i)
        else:
            task_linked_list = create_task(is_start=False, name="action", date=datetime.now(), count=count, is_end=True, action=i)
        task_linked_list = task_linked_list.next_node
    else:
        if task_linked_list:
            task_linked_list.next_node = create_task(is_start=False, name="Scheduler", date=datetime.now(), count=count, is_end=False, action=i)
        else:
            task_linked_list =  create_task(is_start=False, name="Scheduler", date=datetime.now(), count=count, is_end=False, action=i)
        task_linked_list = task_linked_list.next_node

    count += 1
    # task_linked_list = task_linked_list.next_node

nodes = []
current = head
while current:
    nodes.append(current.to_dict())
    current = current.next_node
print("abc", json.dumps(nodes, indent=4))