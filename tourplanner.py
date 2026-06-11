import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
import cv2  
import threading
def register():
    username = register_username_entry.get()
    password = register_password_entry.get()
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lahari@12i7",
        database="tour_planner"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone() is not None:
        messagebox.showerror("Registration Failed", "Username already exists. Please choose a different username.")
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        messagebox.showinfo("Registration Successful", "You have successfully registered.")
        switch_to_tour_planner()

def login():
    username = login_username_entry.get()
    password = login_password_entry.get()
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lahari@12i7",
        database="tour_planner"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    if cursor.fetchone() is not None:
        switch_to_tour_planner()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
def switch_to_login_page():
    notebook.select(login_frame)
def switch_to_tour_planner():           
    notebook.select(page2)
def get_places():
    state = state_var.get()
    season = season_var.get()
    if state and season:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lahari@12i7",
            database="states_places"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT place FROM places WHERE state_id = (SELECT id FROM states WHERE name = %s) AND season_id = (SELECT id FROM seasons WHERE name = %s)", (state, season))
        places = [row[0] for row in cursor.fetchall()]
        
        if places:
            places_label.config(text="\n".join(places))
        else:
            places_label.config(text=f"No specific recommendations for {state} during {season}.")
    else:
        places_label.config(text="Please select a state and a season.")
def create_window():
    global notebook, page2, register_username_entry, register_password_entry,login_username_entry,login_password_entry,state_var,season_var,result_label,places_label,video_player
    global login_frame

    root = tk.Tk()
    root.title("Tour Planner - India")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    register_frame = ttk.Frame(notebook)
    notebook.add(register_frame, text='Register')
    register_username_label = ttk.Label(register_frame, text="Username:")
    register_username_label.grid(row=0, column=0, padx=10, pady=5)
    register_username_entry = ttk.Entry(register_frame)
    register_username_entry.grid(row=0, column=1, padx=10, pady=5)
    register_password_label = ttk.Label(register_frame, text="Password:")
    register_password_label.grid(row=1, column=0, padx=10, pady=5)
    register_password_entry = ttk.Entry(register_frame, show="*")
    register_password_entry.grid(row=1, column=1, padx=10, pady=5)
    register_image = Image.open("registerimg.jpg")  
    register_image = register_image.resize((400, 400))
    register_photo = ImageTk.PhotoImage(register_image)
    register_image_label = ttk.Label(register_frame, image=register_photo)
    register_image_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    register_button = ttk.Button(register_frame, text="Register", command=register)
    register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    login_frame = ttk.Frame(notebook)
    notebook.add(login_frame, text='Login')
    login_username_label = ttk.Label(login_frame, text="Username:")
    login_username_label.grid(row=0, column=0, padx=10, pady=5)
    login_username_entry = ttk.Entry(login_frame)
    login_username_entry.grid(row=0, column=1, padx=10, pady=5)
    login_password_label = ttk.Label(login_frame, text="Password:")
    login_password_label.grid(row=1, column=0, padx=10, pady=5)
    login_password_entry = ttk.Entry(login_frame, show="*")
    login_password_entry.grid(row=1, column=1, padx=10, pady=5)
    login_image = Image.open("registerimage.jpg") 
    login_image = login_image.resize((200, 200))
    login_photo = ImageTk.PhotoImage(login_image)
    login_image_label = ttk.Label(login_frame, image=login_photo)
    login_image_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    login_button = ttk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    page2 = ttk.Frame(notebook)
    notebook.add(page2, text='Tour Planner')
    tour_planner_image = Image.open("tourplan.jpg")  
    tour_planner_image = tour_planner_image.resize((200, 200))
    tour_planner_photo = ImageTk.PhotoImage(tour_planner_image)
    tour_planner_image_label = ttk.Label(page2, image=tour_planner_photo)
    tour_planner_image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    state_label = ttk.Label(page2, text="Select a state in India:")
    state_label.grid(row=1, column=0, padx=10, pady=5)
    state_var = tk.StringVar()
    state_dropdown = ttk.Combobox(page2, textvariable=state_var, values=["Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chattishgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharastra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttarakhand","Uttar Pradesh","west Bengal"])  # Update with more states if needed
    state_dropdown.grid(row=1, column=1, padx=10, pady=5)
    state_dropdown.state(["readonly"])
    season_label = ttk.Label(page2, text="Select a season:")
    season_label.grid(row=2, column=0, padx=10, pady=5)
    season_var = tk.StringVar()
    season_dropdown = ttk.Combobox(page2, textvariable=season_var, values=["Summer", "Monsoon", "Winter"])
    season_dropdown.grid(row=2, column=1, padx=10, pady=5)
    season_dropdown.state(["readonly"])
    get_places_button = ttk.Button(page2, text="Get Places", command=lambda: (get_places(), notebook.select(page3)))
    get_places_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    result_label = ttk.Label(page2, text="")
    result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
    page3 = ttk.Frame(notebook)
    notebook.add(page3, text='Places & Video')
    places_label = ttk.Label(page3, text="Places Information")
    places_label.pack(padx=10, pady=10)
    class VideoPlayer:
        def _init_(self, parent, video_source):
            self.parent = parent
            self.video_source = video_source
            self.vid = cv2.VideoCapture(self.video_source)
            self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.canvas = tk.Canvas(parent, width=self.width, height=self.height)
            self.canvas.pack()
            self.update()
        def update(self):
            ret, frame = self.vid.read()
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.parent.after(50, self.update)
        def stop(self):
            if self.vid.isOpened():
                self.vid.release()
                self.canvas.destroy()

    video_player = VideoPlayer(page3,"placesss.mp4")  
    root.mainloop()
if _name_ == "_main_":
    mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lahari@12i7",
        database="tour_planner"
    )
    create_window()