from task import Task
from event import Event
from check_input import *
from math import ceil
import csv, random

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import messagebox

TASK_FILENAME = "tasks.csv"

class CustomCheckbox(tk.Frame):
    """ Custom-style checkbox to represent the task completion status
    Args:
        tk (Frame): the Frame instance to build on
    """
    def __init__(self, master, task, icon=None, *args, **kwargs):
        """ Initialize the checkbox widget
        Args:
            master (tk.Widget): parent widget
            task (Task): the Task instance to refer to
            icon (PIL.Image.Image, optional): the custom image for the checkbox. Defaults to None
        """
        super().__init__(master, bg="white", *args, **kwargs)
        
        self.task = task  # Store the task object
        self.var = tk.IntVar() # gets the state of the widget

        # Set icons; DEFAULT or PROVIDED
        if icon: # icon for task REMOVAL 
                self.img_unchecked= ImageTk.PhotoImage(Image.open("interfaces/neutral.png").resize((30, 30)))
                self.img_checked = ImageTk.PhotoImage(icon.resize((30, 30)))
        else: # icon for task COMPLETION status
            if task.status == 1: # current task is active (check=incomplete, uncheck=completed)
                self.img_checked = ImageTk.PhotoImage(Image.open("interfaces/incompleted.png").resize((30, 30)))                
                self.img_unchecked = ImageTk.PhotoImage(Image.open("interfaces/completed.png").resize((30, 30)))
            else:
                self.img_checked = ImageTk.PhotoImage(Image.open("interfaces/completed.png").resize((30, 30)))
                self.img_unchecked = ImageTk.PhotoImage(Image.open("interfaces/incompleted.png").resize((30, 30)))                

        self.checklist_picture_label = tk.Label(self, image=self.img_unchecked, bg="white")
        self.checklist_picture_label.pack(side="left", padx=5, pady=5)

        self.task_desc_label = tk.Label(self, text=task.desc, bg="white", font=("Courier", 12),
                                        fg="#72615A", width=22, anchor="w", justify="left", wraplength=220)
        self.task_desc_label.pack(side="left", pady=0)

        self.checklist_picture_label.bind("<Button-1>", self.toggle)
        self.task_desc_label.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        """ Toggle checkboxes between check/uncheck

        Args:
            event (tk.Event, optional): Event object to be accessed. Defaults to None
        """
        if self.var.get() == 0:
            self.var.set(1)
            self.checklist_picture_label.config(image=self.img_checked)
        else:
            self.var.set(0)
            self.checklist_picture_label.config(image=self.img_unchecked)

    def get_state(self):
        """ returns current checkbox state

        Returns:
            1 if checked; otherwise 0
        """
        return self.var.get()
       

class Pet:
    """ Represents a virtual pet with tasks associated
    Attributes:
        root (Tk): The root Tkinter window
        frame (Frame): The GUI frame where the pet is displayed
        acc (Account): The account associated with this pet
        _name (str): Name of the pet
        _pet_id (int): Unique 5-digit ID of the pet.
        _status (int): Current status of the pet (1-5).
        _species (int): Encoded species type of the pet
        _animal_id (int): Encoded specific animal chosen
        _event (int): Current status of event's completion for the day
        _tasks (list): A list of Task objects assigned to the pet.
        checkboxes (list): GUI checkbox widgets linked to each task.        
    """
    def __init__(self, root, frame, account, name, pet_id, status, species, animal_id, event):
        """ Initialize the Pet instance
        Args:
            root (Tk): The root Tkinter window
            frame (Frame): The GUI frame displayed on
            account (Account): The account associated with this pet
            name (str): The pet's name.
            pet_id (str): Unique 5-digit id 
            status (str): The current status of the pet (1-5).
            species (str): Encoded species code of the pet.
            animal_id (str): Enconded animal type code.
            event (str): Current status of event's completion for the day
        """
        self.root = root
        self.frame = frame
        self.acc = account
        
        self._name = name
        self._pet_id = pet_id
        self._status = int(status)
        self._species = int(species)
        self._animal_id = int(animal_id)
        self._event = int(event)
        self._tasks = []
        self.checkboxes = []                
    
    @property
    def species(self):
        return self._species
                
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def pet_id(self):
        return self._pet_id
    
    @property
    def animal_id(self):
        return self._animal_id
    
    @property
    def status(self):
        return self._status
    
    @property
    def species(self):
        return self._species
    
    @property
    def event(self):
        return self._event
    
    def open_pet_room(self):
        """ Opening screen for pet room with simple background animation """
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        bg_stored = {1: ("pets/dog1.png", "pets/dog2.png"),
                     2: ("pets/cat1.png", "pets/cat2.png"),
                     3: ("pets/ham1.png", "pets/ham2.png"),
                     4: ("pets/rex1.png", "pets/rex2.png"),
                     5: ("pets/bronto1.png", "pets/bronto2.png"),
                     6: ("pets/trice1.png", "pets/trice2.png")}
        species_bg = bg_stored[self._animal_id]
        self.load_csv()
        
        # Load both images
        self.bg_images = [ImageTk.PhotoImage(Image.open(img_path)) for img_path in species_bg]
        self.bg_index = 0  # Start with the first image

        # Set up background label
        self.bg_label = tk.Label(self.frame)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # STATUS INTERFACE
        completed_tasks = [1 if task.status == 1 else 0 for task in self._tasks]
        if len(self._tasks) != 0:
            calc_status = ceil(sum(completed_tasks)/len(self._tasks) * 5) # ceil(completed_perc_decimal * 5)
            self.final_status = max(1, min(calc_status,5)) # range 1-5
        else:
            self.final_status = 1
                        
        self._status = max(1, min(self.final_status + self.event,5))
        status_path = f"interfaces/status{self._status}.png"
        self.status_image = ImageTk.PhotoImage(Image.open(status_path))
        self.status_label = tk.Label(self.frame, image=self.status_image, bg="black")
        self.status_label.place(relx=0.1, rely=0.13)
        self.status_label.tkraise()

        # STATUS LABEL
        status_text = {1: "exhausted", 2:"tired", 3:"fine", 4:"happy", 5:"elated"}
        self.status_label = tk.Label(self.frame, font = ("Arial", 9, "bold"), text = f"~{status_text[self.final_status]}~",
                                     fg="white", bg="#0E1917")
        self.status_label.place(relx=0.27, rely=0.30, anchor="center")
        self.status_label.tkraise()


        # NAME LABEL
        self.name_label = tk.Label(self.frame, font=("Courier", 24,"bold"),
                                   text=f"{self._name}", fg="#72615A", bg="#EE8B5F")
        self.name_label.place(relx=0.5, rely=0.06, anchor="center")
        self.name_label.tkraise()

        # BACK BUTTON
        self.return_img = Image.open("interfaces/return_button.png").resize((33,33))
        self.return_button_image = ImageTk.PhotoImage(self.return_img)     
        self.return_button = tk.Button(self.frame, image=self.return_button_image, background="#EE8B5F",
                                       activebackground="#EE8B5F", highlightbackground="#EE8B5F",
                                       command=(self.acc).open_home_screen, borderwidth=0)
        self.return_button.place(relx=0.05, rely=0.03)

        # ACTIVITY BUTTON
        self.activity_img = Image.open("interfaces/activity_button.png")
        self.activity_button_img = ImageTk.PhotoImage(self.activity_img)             
        self.activity_button = tk.Button(self.frame, image=self.activity_button_img, background="#0E1917",
                                    command=self.open_activity_screen, borderwidth=0)
        self.activity_button.place(relx=0.14, rely=0.72)
        
        
        # EVENT BUTTON
        self.event_img = Image.open("interfaces/event_button.png")
        self.event_button_img = ImageTk.PhotoImage(self.event_img)
        self.event_button = tk.Button(self.frame, image=self.event_button_img, background="#0E1917",
                                    command=self.open_event_window, borderwidth=0)
        self.event_button.place(relx=0.57, rely=0.72)
        

        # Animation function
        def animate_bg():
            try:
                self.bg_label.configure(image=self.bg_images[self.bg_index])
                self.bg_index = (self.bg_index + 1) % len(self.bg_images)
                self.bg_animation_id = self.frame.after(500, animate_bg)  # Save ID to stop animation
            except tk.TclError:                
                return # Widget destroyed, stop animation

        animate_bg()
        
    def load_csv(self):
        """ Load task data from csv
        """
        self._tasks = []
        try:
            with open(TASK_FILENAME, mode="r") as file:
                reader = csv.reader(file)            
                for row in reader:
                    read_pet_id, task_id, description, status = row
                    if read_pet_id == self._pet_id: #checking for correct pet_id                        
                        self._tasks.append(Task(self.root, self.frame, self, self._pet_id, task_id, description, int(status)))
        except FileNotFoundError: # create new file if task.csv not found            
            open(TASK_FILENAME, mode="w").close()  
    
    def open_activity_screen(self):
        """ Display the screen for activities
        """
        if hasattr(self, 'bg_animation_id'):
            self.frame.after_cancel(self.bg_animation_id)        

        for widget in self.frame.winfo_children():
            widget.destroy()

        # Change bg
        self.new_bg_image = Image.open("interfaces/activity_room.png")  # New background image
        self.new_bg_photo = ImageTk.PhotoImage(self.new_bg_image)
        self.bg_label = tk.Label(self.frame, image=self.new_bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # ACTIVITES LABEL
        self.activities_label = tk.Label(self.frame, text="Activities", bg = "#EE8B5F",
                                         font=("Courier", 29, "bold"), fg="#72615A")
        self.activities_label.place(relx=.5, rely=.12, anchor="center")
        
        # REMOVE button
        self.remove_img = Image.open("interfaces/remove_button.png").resize((33, 33))
        self.remove_button_image = ImageTk.PhotoImage(self.remove_img)
        
        self.remove_button = tk.Button(self.frame, 
                                        image=self.remove_button_image, 
                                        command=self.handle_task_removal,
                                        background="#A9745C", 
                                        borderwidth=0, relief="flat",
                                        highlightthickness=0, 
                                        activebackground="#A9745C")
        self.remove_button.place(relx=0.27, rely=0.6, anchor="center")
        
        # ADD button
        self.add_img = Image.open("interfaces/add_button.png").resize((33, 33))
        self.add_button_image = ImageTk.PhotoImage(self.add_img)
        
        self.add_button = tk.Button(self.frame, image=self.add_button_image, 
                                        command=self.handle_new_task, 
                                        background="#A9745C", borderwidth=0, relief="flat", 
                                        highlightthickness=0, activebackground="#A9745C")
        self.add_button.place(relx=0.16, rely=0.6, anchor="center")
        
        # CONFIRM BUTTON
        self.confirm_button_image = Image.open("interfaces/confirm_button.png")
        self.confirm_button_image = self.confirm_button_image.resize((226, 85))
        self.confirm_button_photo = ImageTk.PhotoImage(self.confirm_button_image)
        
        self.confirm_button = tk.Button(self.frame, image=self.confirm_button_photo, 
                                        command=self.process_task_status, 
                                        bd=0, highlightthickness=0, activebackground="#EE8B5F")
        self.confirm_button.place(relx=0.5, rely=0.75, anchor="center")
        
        # RETURN BUTTON        
        self.return_img = Image.open("interfaces/return_button.png").resize((33,33))
        self.return_button_image = ImageTk.PhotoImage(self.return_img)     
        self.return_button = tk.Button(self.frame, image=self.return_button_image, background="#EE8B5F",
                                    activebackground="#EE8B5F", highlightbackground="#EE8B5F",
                                    command=self.open_pet_room, borderwidth=0)
        self.return_button.place(relx=0.05, rely=0.03)
        
        # CHECKLIST CANVAS (scrollable)
        self.checklist_canvas = tk.Canvas(self.frame, width=320, height=240, bd=0, background="white")
        self.checklist_canvas.place(relx=0.5, rely=0.38, anchor="center")
        # Create scrollbars (VERTICAL)
        self.v_scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.checklist_canvas.yview)
        self.v_scrollbar.place(relx=0.87, rely=0.38, anchor="center", height=244)

        self.checklist_canvas.configure(yscrollcommand=self.v_scrollbar.set)
        # frame for checkbox
        self.checklist_frame = tk.Frame(self.checklist_canvas, bg="white")
        self.checklist_canvas.create_window((0, 0), window=self.checklist_frame, anchor="nw")
        self.checklist_canvas.bind("<MouseWheel>", self.on_mouse_wheel) # Mousewheel bind
        
        # CHECKBOX PROCESS
        if hasattr(self, 'checkboxes'):
            for checkbox in self.checkboxes:
                checkbox.destroy()  # Destroy previous checkboxes
        
        self.checkboxes = []  # Store and clear checkbox widgets
        if not self._tasks:  # If there's no item
            no_tasks_label = tk.Label(self.checklist_frame, text="No existing activities", bg="white", font=("Courier", 12))
            no_tasks_label.pack(padx=50,pady=30)
        else:
            for task in self._tasks:
                checkbox = CustomCheckbox(self.checklist_frame, task=task)                
                checkbox.pack(padx=10, pady=15, anchor="w")
                self.checkboxes.append(checkbox)  # Add checkbox to the list

        # Update the canvas scroll region when items are added to the checklist
        self.checklist_frame.update_idletasks()        
        self.checklist_canvas.config(scrollregion=self.checklist_canvas.bbox("all"))

        # Ensure scrollregion updates after packing is done (delay update if necessary)
        self.checklist_frame.after(10, lambda: self.checklist_canvas.config(scrollregion=self.checklist_canvas.bbox("all")))

        # Add this line to bind mousewheel to the canvas itself for scrolling anywhere
        self.checklist_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)  # Enable scrolling anywhere
    
    def on_mouse_wheel(self, event):
        """ Function to handle mouse wheel scrolling on the canvas """
        if hasattr(self, 'checklist_canvas') and self.checklist_canvas.winfo_exists():  # Check if canvas exists
            if event.delta > 0:            
                self.checklist_canvas.yview_scroll(-1, "units")  # Scroll up
            else:            
                self.checklist_canvas.yview_scroll(1, "units")  # Scroll down

    def process_task_status(self):
        """ Process the marking of task status
        """
        for checkbox in self.checkboxes:
            task = checkbox.task  # Each checkbox holds its task
            if checkbox.get_state() == 1: # if box is selected, invert
                if task.status == 0:
                    task.status = 1
                else:
                    task.status = 0
        
        self.save_tasks()
        self.open_pet_room()
        
    def handle_task_removal(self):
        """ Handle task removal internally
        """
        # Display screen to remove tasks
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Change bg
        self.new_bg_image = Image.open("interfaces/task_remove_bg.png")
        self.new_bg_photo = ImageTk.PhotoImage(self.new_bg_image)
        self.bg_label = tk.Label(self.frame, image=self.new_bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # REMOVAL LABEL
        self.activities_label = tk.Label(self.frame, text="REMOVAL", bg = "#BC0E00",
                                         font=("Courier", 29, "bold"), fg="white")
        self.activities_label.place(relx=.5, rely=.12, anchor="center")
        
        # Confirm BUTTON
        self.confirm_button_image = Image.open("interfaces/confirm_button.png")
        self.confirm_button_image = self.confirm_button_image.resize((226, 85))
        self.confirm_button_photo = ImageTk.PhotoImage(self.confirm_button_image)
        
        self.confirm_button = tk.Button(self.frame, image=self.confirm_button_photo, 
                                        command=self.process_task_removal, 
                                        bd=0, highlightthickness=0, activebackground="#EE8B5F")
        self.confirm_button.place(relx=0.5, rely=0.67, anchor="center")
                
        # RETURN BUTTON        
        self.return_img = Image.open("interfaces/return_button.png").resize((33,33))
        self.return_button_image = ImageTk.PhotoImage(self.return_img)     
        self.return_button = tk.Button(self.frame, image=self.return_button_image, background="#EE8B5F",
                                    activebackground="#EE8B5F", highlightbackground="#EE8B5F",
                                    command=self.open_activity_screen, borderwidth=0)
        self.return_button.place(relx=0.05, rely=0.03)
        
        # CHECKLIST CANVAS (scrollable)
        self.checklist_canvas = tk.Canvas(self.frame, width=320, height=240, bd=0, background="white")
        self.checklist_canvas.place(relx=0.5, rely=0.38, anchor="center")
        # Create scrollbars (VERTICAL)
        self.v_scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.checklist_canvas.yview)
        self.v_scrollbar.place(relx=0.87, rely=0.38, anchor="center", height=244)

        # Configure canvas to use scrollbars
        self.checklist_canvas.configure(yscrollcommand=self.v_scrollbar.set)

        # Frame to hold checkbox
        self.checklist_frame = tk.Frame(self.checklist_canvas, bg="white")
        self.checklist_canvas.create_window((0, 0), window=self.checklist_frame, anchor="nw")

        # Mousewheel bind
        self.checklist_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)        
        
        # Clear previous checkboxes before adding new ones        
        if hasattr(self, 'checkboxes'):
            for checkbox in self.checkboxes:
                checkbox.destroy()  # Destroy previous checkboxes
        
        self.checkboxes = []  # Store and clear checkbox widgets
        if not self._tasks:  # If there's no item
            no_tasks_label = tk.Label(self.checklist_frame, text="No existing activities", bg="white", font=("Courier", 12))
            no_tasks_label.pack(padx=50,pady=30)
        else:
            task_icon = Image.open("interfaces/exile.png")
            for task in self._tasks:
                checkbox = CustomCheckbox(self.checklist_frame, task=task, icon=task_icon)
                checkbox.pack(padx=10, pady=15, anchor="w")
                checkbox.task_ref = task  # Attach the whole Task object
                self.checkboxes.append(checkbox)  # Add checkbox to the list

        # Update the canvas scroll region when items are added to the checklist
        self.checklist_frame.update_idletasks()        
        self.checklist_canvas.config(scrollregion=self.checklist_canvas.bbox("all"))
    
    def process_task_removal(self):
        """ handles task removal and stays at the same screen
        """
        selected_tasks = [checkbox.task_ref for checkbox in self.checkboxes if checkbox.get_state() == 1]
        
        if len(selected_tasks) > 0:
            confirm_text = "Are you sure you want to delete the following activity?\n\n"
            confirm_text += "\n".join(f"- {task.desc}" for task in selected_tasks)
            
            confirmed = messagebox.askyesno("Confirm Deletion", confirm_text)
            if confirmed:            
                self._tasks = [task for task in self._tasks if task not in selected_tasks]                
                
                # Refresh the task removal screen                
                self.handle_task_removal()                
                self.save_tasks()    

    def handle_new_task(self):
        """ Display screen to add new_task
        """
        # Clear screen
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Change bg
        self.new_bg_image = Image.open("interfaces/new_task_bg.png")
        self.new_bg_photo = ImageTk.PhotoImage(self.new_bg_image)
        self.bg_label = tk.Label(self.frame, image=self.new_bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # RETURN button
        self.return_img = Image.open("interfaces/return_button.png").resize((33,33))
        self.return_button_image = ImageTk.PhotoImage(self.return_img)     
        self.return_button = tk.Button(self.frame, image=self.return_button_image, background="#EE8B5F",
                                       activebackground="#EE8B5F", highlightbackground="#EE8B5F",
                                       command=self.open_activity_screen, borderwidth=0)
        self.return_button.place(relx=0.05, rely=0.03)
        
        # DESCRIPTION LABEL
        self.label = tk.Label(self.frame, text="Enter new activity:", font=("Courier", 19, "bold"), fg="#72615A", bg= "#C77E5D")
        self.label.place(relx=0.5, rely=0.35, anchor="center")

        # Add a text input (Entry widget)
        self.username_entry = tk.Entry(self.frame, font=("Courier", 14), width = 20)
        self.username_entry.place(relx=0.5, rely=0.40, anchor="center")

        # CONFIRM BUTTON
        self.confirm_button_image = Image.open("interfaces/confirm_button.png")
        self.confirm_button_image = self.confirm_button_image.resize((285, 100))
        self.confirm_button_photo = ImageTk.PhotoImage(self.confirm_button_image)
        
        self.confirm_button = tk.Button(self.frame, image=self.confirm_button_photo, 
                                        command = self.process_new_task, 
                                        bd=0, highlightthickness=0, activebackground="#EE8B5F")
        self.confirm_button.place(relx=0.5, rely=0.58, anchor="center")
        
    def process_new_task(self):
        """ Handles the creation of a new task and go back to activity room
        """
        # choose and validate username
        new_desc = self.username_entry.get().strip()        
        
        # Check if the username is empty
        if not new_desc:
            #removes previous error labels
            if hasattr(self, 'error_label'): 
                self.error_label.destroy()
            
            # Show an error message if the username is empty
            self.error_label = tk.Label(self.frame, text="Please write a description", 
                                        font=("Courier", 13, "bold"), fg="white", bg="#BC0E00")
            self.error_label.place(relx=0.5, rely=0.31, anchor="center")
            return  # Stop further processing
        
        # Remove the error label if it exists
        if hasattr(self, 'error_label'):
                self.error_label.destroy()                

        # Generate a random 5-digit ID
        curr_ids = [task.task_id for task in self._tasks]
        while True:
            new_id = str(random.randint(10000, 99999))
            if new_id not in curr_ids:
                break
        new_task = Task(self.root, self.frame,self, self._pet_id, new_id, new_desc, 0)
        self._tasks.append(new_task)
        self._selected_task = new_task
        
        # saving new account to csv
        with open(TASK_FILENAME, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self._pet_id, new_id, new_desc, 0])
        
        self.open_activity_screen()

    def wipe_tasks(self):        
        new_rows = []
        with open(TASK_FILENAME, mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] != self.pet_id:
                    new_rows.append(row)

        # Rewrite CSV without the deleted 
        with open(TASK_FILENAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(new_rows)
  
    def save_tasks(self):
        """ Save the current internal data to csv file
        """
        with open(TASK_FILENAME, mode = "r") as file:
            reader = csv.reader(file)
                                        
            new_rows = []
            for row in reader:
                read_pet_id, read_task_id, description, status = row  
                if read_pet_id == self.pet_id:
                    for task in self._tasks:  
                        if read_task_id == task.task_id:
                            new_rows.append([self.pet_id, task.task_id, description, task.status])
                else: # keep original row if belong to other users
                    new_rows.append(row)
        
        with open(TASK_FILENAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(new_rows)

    def open_event_window(self):
        """ Display output for random event
        """
        def close_event_window():
            """ Function to close the event label ("Window")
            """
            if hasattr(self, 'event_frame'):
                self.event_frame.destroy()
                self.event_frame = None
                (self.acc).save_pets()
                self.update_status_interface()
            else:
                self.update_status_interface()
                
                
        if hasattr(self, 'event_frame') and self.event_frame is not None:
            return  # prevent multiple event frames at once

        if self._event == 0:  # Unoccured event
            event_random = random.randint(1, 3)
            self.called_event = Event()
            available = {1: self.called_event.park, 2: self.called_event.swim, 3: self.called_event.bake}
            result, prompt = available[event_random]()            
            
            # Process result
            if (result > 0):
                final = 1
            else:
                final = -1
            
            self._status += final
            self._status = max(1, min(5, self._status))  # Ensure range 1-5            
            self._event = 1
            
            (self.acc).save_pets()
            
            # Create the event window frame; above parent frame
            self.event_frame = tk.Frame(self.frame, bg="#87CEEB", bd=5,
                                        highlightthickness=5, highlightbackground="white")
            self.event_frame.place(relx=0.5, rely=0.45, anchor="center", width=320, height=140)

            # PROMPT LABEL
            label = tk.Label(self.event_frame, text=prompt, font=("Courier", 10, "bold"),
                            fg="white", bg="#87CEEB", wraplength=300, justify="center", pady=4)
            label.place(relx=0.5, rely=0.4, anchor="center")
                
            if result != 0:                
                status_prompt = "(mood increased)" if result > 0 else "(mood decreased)"
                label = tk.Label(self.event_frame, text=status_prompt, font=("Courier", 10, "bold"),
                            bg="white", fg="#87CEEB", wraplength=300, justify="center", pady=1)
                label.place(relx=0.5, rely=0.01, anchor="center")

            # CONTINUE BUTTON
            continue_button = tk.Button(self.event_frame, text="Continue", font=("Courier", 12),
                                        command=close_event_window, fg="white", bg="#5E9D3E", width=8,
                                        activebackground="#5E9D3E", activeforeground="white")
            continue_button.place(relx=0.5, rely=0.83, anchor="center")

            # Update the frame layout
            self.frame.update_idletasks()
            self.status_label.update_idletasks() 
        else:
            # EVENT FRAME
            self.event_frame = tk.Frame(self.frame, bg="#87CEEB", bd=5, highlightthickness=5, highlightbackground="white")
            self.event_frame.place(relx=0.5, rely=0.45, anchor="center", width=320, height=140)            
            # EVENT LABEL
            event_occured_label = tk.Label(self.event_frame, text=f"{self._name} attended an event today already.", 
                                           font=("Courier", 15, "bold"),
                            fg="white", bg="#87CEEB", wraplength=240, justify="center", pady=4)
            event_occured_label.place(relx=0.5, rely=0.4, anchor="center")
            #CONTINUE BUTTON
            continue_button = tk.Button(self.event_frame, text="Continue", font=("Courier", 12),
                                        command=close_event_window, fg="white", bg="#5E9D3E", width=8,
                                        activebackground="#5E9D3E", activeforeground="white")
            continue_button.place(relx=0.5, rely=0.82, anchor="center")

    def update_status_interface(self):
        """ Update the pet image based on the current status. """        
        status_path = f"interfaces/status{self._status}.png"

        self.pet_image = Image.open(status_path)  # Update the image based on the status
        self.pet_photo = ImageTk.PhotoImage(self.pet_image)

        # Assuming self.status_label is the label where the pet image is displayed
        self.status_label.config(image=self.pet_photo)
        self.status_label.image = self.pet_photo  # Keep a reference to the image        
        self.status_label.place(relx=0.265, rely=0.202)        
        self.acc.save_pets()        
        
    