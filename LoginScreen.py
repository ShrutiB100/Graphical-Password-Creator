import tkinter as tk
from Pages.config import LARGE_FONT
from PIL import ImageTk, Image
from tkinter import messagebox
import tkinter as tk
import mysql.connector as sql

# Connecting MYSQL with Python
con = sql.connect(host='localhost', user='root', password='simmba@2003')
cur = con.cursor()
cur.execute('create database if not exists graphical_password')
cur.execute('use graphical_password')


class LoginScreen(tk.Frame):
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

    # Creating the frame
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
        self.create_widgets(controller)
        self.coords_list = []

    def create_widgets(self, controller):
        instructions_label = tk.Label(self, text=self.label_text, justify=tk.LEFT, font=LARGE_FONT)
        instructions_label.grid(row=0, column=0, sticky='w')

        # Justifications of the frame
        name_label = tk.Label(self, text='Username', font=('calibre', 10, 'bold'))
        name_entry = tk.Entry(self, textvariable=self.name_var, font=('calibre', 10, 'normal'))
        name_label.grid(row=1, sticky='w')
        name_entry.grid(row=2, sticky='nsew')

        image_selector_frame = tk.LabelFrame(self, text='Image To Use')

        # Creates all the widgets
        for key, label in self.labels_map.items():
            y_index = label['index'] // 2;
            x_index = label['index'] % 2;
            radio = tk.Radiobutton(image_selector_frame, text=key, variable=self.image_selection, value=key,
                                   command=self.select_image)
            radio.grid(row=y_index, column=x_index, sticky='w', padx=10, pady=5)

        image_selector_frame.grid(row=3, sticky='nsew')

        self.canvas.grid(row=0, column=1, rowspan=6, columnspan=3, sticky='nsew')
        self.canvas.bind("<Button 1>", self.on_canvas_click)

        button_frame = tk.Frame(self)
        button_frame.grid(row=5, sticky='nsew')

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Tkinter button displayed on the frame
        reset_button = tk.Button(button_frame, text='reset', command=self.reset_button)
        reset_button.grid(row=0, column=0, sticky='nsew')

        # Tkinter button displayed on the frame
        submit_button = tk.Button(button_frame, text='Submit', command=self.submit)
        submit_button.grid(row=0, column=1, sticky='nsew')
        self.select_image()

    # Reset button - used to reset the data entered
    def reset_button(self):
        self.click_points = []
        self.select_image()
        self.coords_list = []

    # Function to check the user's username
    def submit(self):
        username = self.name_var.get()
        old_coord = []
        username_l1 = [username]
        name = tuple(username_l1)
        self.name_var.set("")
        new_coord = self.coords_list
        image_key = self.image_selection.get()

        # To get the corresponding values with the help of the username
        cur.execute('''select * from password where username= '%s' ''' % name)

        # To store the old & new image and coordinates
        self.old_coords = cur.fetchone()
        if self.old_coords is None:
            messagebox.showerror("Error", "Username does not match")
            self.click_points = []
            self.select_image()
            self.coords_list = []
        else:
            image = self.old_coords[1]
            username = self.old_coords[0]
            list = []
            new_list = []
            for i in range(2, 8):
                list += [self.old_coords[i]]
            for j in self.coords_list:
                for k in j:
                    new_list += [k]

        count = 0

        # Distance Check for the clicked coordinates
        for a in range(6):
            if list[a] < new_list[a]:
                # Acceptable range given is 40 units
                if new_list[a] - list[a] <= 40:
                    pass
                else:
                    count += 1

            elif new_list[a] < list[a]:
                # Acceptable range given is 40 units
                if list[a] - new_list[a] <= 40:
                    pass
                else:
                    count += 1
            else:
                pass

        # Checking if the Image selected is correct or not
        if image == image_key:
            pass
        else:
            # If the image is not matching
            messagebox.showerror("Error", "Wrong image selected.")

        self.click_points = []
        self.select_image()
        self.coords_list = []

        # Checking if the User has entered everything correct
        if count >= 1:
            # If the user has not entered correct values
            messagebox.askretrycancel("Failure", "You have entered the wrong coordinates")

        else:
            # The user has entered correct values
            # This results in the commencement of the Colour Game
            result = messagebox.askquestion("Success", "Congratulations!! Do you want to start playing the game?")

            # Checking if the user is interested to begin the game or not
            if result == "yes":
                from Pages import colorgame
            elif result == "no":
                exit()

    # Determine the origin by clicking
    def on_canvas_click(self, eventorigin):

        # Accepting the coordinates by click
        x0 = eventorigin.x
        y0 = eventorigin.y
        radius = 10

        # The coordinates
        points = (x0, y0)
        self.coords_list.append(points)

        print(self.coords_list)

        length = len(self.click_points)
        if length < 3:
            self.canvas.create_oval(x0 - radius, y0 - radius, x0 + radius, y0 + radius, fill='blue')
            self.canvas.create_text(x0, y0, text=str(length + 1), fill='white')
            self.click_points.append((x0, y0))

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
