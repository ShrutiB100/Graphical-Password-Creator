import tkinter as tk

from Pages.config import LARGE_FONT
from PIL import ImageTk, Image
from tkinter import messagebox

# Connecting MYSQL with Python
import mysql.connector as sql
con = sql.connect(host='localhost', user='root', password='simmba@2003')
cur = con.cursor()
cur.execute('create database if not exists graphical_password')
cur.execute('use graphical_password')


class RegisterScreen(tk.Frame):

    # The images being used
    labels_map = {
        "Taj mahal": {"image_path": "./images/Taj mahal.jpg", "index": 0},
        "Burj khalifa": {"image_path": "./images/burj-khalifa.jpg", "index": 1},
        "Buckingham palace": {"image_path": "./images/Buckingham palace.jpg", "index": 2},
        "Eiffel tower": {"image_path": "./images/Eiffel tower.jpg", "index": 3},
        "Hogwarts": {"image_path": "./images/Hogwarts.jpg", "index": 4},
        "Lemonade": {"image_path": "./images/lemonade.jpg", "index": 5},
        "Lighthouse": {"image_path": "./images/lighthouse.jpg", "index": 6},
        "black forest": {"image_path": "./images/black forest.jpg", "index": 7},
        "new york skyline": {"image_path": "./images/new york city skyline.jpg", "index": 8},
        "Venice": {"image_path": "./images/venice.jpg", "index": 9},
    }

    # Instructions to be printed on the tkinter frame
    label_text = "\n".join(["Enter Username",
                            "1.Create a username of at least 8 characters.",
                            "2.Include both uppercase and lowercase letters.",
                            "3.Include numbers and special characters[ @ , ? , ! , _ ]",
                            "4.Only input 3 points."
                            "NOTE: Do not use blankspace in the username."])

    # Initializing the variables used in the latter program
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_configure(sticky='nsew')
        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.click_points = []
        self.name_var = tk.StringVar()

        self.image_selection = tk.StringVar()
        self.image_selection.set("Taj mahal")

        # Adjustment of the background(Canvas)
        self.canvas = tk.Canvas(self, bg='grey', width=711, height=400)
        self.coords_list = []
        self.create_widgets()

    # Creating the widgets
    def create_widgets(self):
        instructions_label = tk.Label(self, text=self.label_text, justify=tk.LEFT, font=LARGE_FONT)
        instructions_label.grid(row=0, column=0, sticky='w')

        # Justifications of the label
        name_label = tk.Label(self, text='Username', font=('calibre', 10, 'bold'))
        name_label.grid(row=1, sticky='w')
        name_entry = tk.Entry(self, textvariable=self.name_var, font=('calibre', 10, 'normal'))
        name_entry.grid(row=2, sticky='nsew')

        # Creating a label
        image_selector_frame = tk.LabelFrame(self, text='Image To Use')
        image_selector_frame.grid(row=3, sticky='nsew')

        # Specifications related to the Radiobutton
        for key, label in self.labels_map.items():
            y_index = label['index'] // 2;
            x_index = label['index'] % 2;
            radio = tk.Radiobutton(image_selector_frame, text=key, variable=self.image_selection, value=key,
                                   command=self.select_image)
            radio.grid(row=y_index, column=x_index, sticky='w', padx=10, pady=5)


        # Canvas
        self.canvas.grid(row=0, column=1, rowspan=6, columnspan=3, sticky='nsew')
        self.canvas.bind("<Button 1>", self.on_canvas_click)

        # Frame
        button_frame = tk.Frame(self)
        button_frame.grid(row=5, sticky='nsew')
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Tkinter buttons displayed on the frame
        reset_button = tk.Button(button_frame, text='reset', command=self.reset_button)
        reset_button.grid(row=0, column=0, sticky='nsew')

        # Tkinter buttons displayed on the frame
        submit_button = tk.Button(button_frame, text='Submit', command=self.submit)
        submit_button.grid(row=0, column=1, sticky='nsew')
        self.select_image()

    # Reset button - used to reset the data entered
    def reset_button(self):
        self.click_points = []
        self.select_image()

    # Function to accept the user's username
    def submit(self):
        username = self.name_var.get()
        self.name_var.set("")

        # Creating a sql table to store the user's data
        cur.execute('''create table if not exists password
                               (username char(20) primary key,
                                image char(40) ,
                                x1 decimal(28,20),
                                y1 decimal(28,20),
                                x2 decimal(28,20), 
                                y2 decimal(28,20),
                                x3 decimal(28,20),
                                y3 decimal(28,20))''')
        print(username)

        # To check if the Username is of the correct strength
        image_key = self.image_selection.get()
        g = [username, image_key]
        ifcasesleft = True
        no_digits = 0
        no_specialchar = 0
        no_alpha = 0
        length = len(username)
        for char in username:

            if char.isdigit():
                no_digits += 1

            elif char in "$@%":
                no_specialchar += 1

            elif char.isalpha():
                no_alpha += 1

        # To raise errors on the Username entered
        else:
            if length == 0:
                messagebox.showerror("Error", "you have not entered a username")
            elif length < 8:
                messagebox.showerror("Error", "Username must be greater then 8 char")
            elif no_digits == 0:
                messagebox.showerror("Error", "The password must have a number")
            elif no_specialchar == 0:
                messagebox.showerror("Error", "The password must have a special character")
            elif no_alpha == 0:
                messagebox.showerror("Error", "The password must have an alphabet")
            elif not char.isalnum() and char not in "@$%!_":
                messagebox.showerror("Error", "password must have only @ $ or %")

        # Appending the coordinates
        for coords in self.click_points:
            for coord in coords:
                g.append(coord)

        specialchar = 0
        digits = 0
        alphabet = 0
        len_username = 0
        if no_digits >= 1:
            digits += 1
        if no_alpha>=1:
              alphabet+=1
        if no_specialchar >= 1:
            specialchar += 1
        if len(username) >= 8:
            len_username += 1
        count = digits + specialchar + len_username + alphabet
        record = tuple(g)

        # To accept username only if it is in the given standards
        if count == 4:
            try:
                # To insert the suitable Username into MYSQL
                cur.execute('''insert into password values
                   ('%s','%s','%s','%s','%s','%s','%s','%s')''' % record)
                con.commit()
                result = messagebox.showinfo("Success", "You have successfully registered with Graphical Password "
                                                        "Creator!!")
                exit()

            # Checking for unique Username
            except sql.IntegrityError as err:
                print("Error- duplicate value for username")

    # Determine the coordinates by clicking
    def on_canvas_click(self, eventorigin):

        # Accepting the coordinates by click
        self.x0 = eventorigin.x
        self.y0 = eventorigin.y
        radius = 10


        length = len(self.click_points)

        if length < 3:
            self.canvas.create_oval(self.x0 - radius, self.y0 - radius, self.x0 + radius, self.y0 + radius, fill='blue')
            self.canvas.create_text(self.x0, self.y0, text=str(length + 1), fill='white')
            self.click_points.append((self.x0, self.y0))

        # Only three coordinates are acceptable
        else:
            messagebox.showerror("Error", "Only 3 points can be recorded.")

    # Function to select the  user's desired image
    def select_image(self):
        image_key = self.image_selection.get()
        image_path = self.labels_map[image_key]["image_path"]

        if image_path != '':
            self.click_points = []
            img = Image.open(image_path)

            # Resizing the image
            img = img.resize((711, 400))

            # Placing the image on the Canvas
            self.img = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
