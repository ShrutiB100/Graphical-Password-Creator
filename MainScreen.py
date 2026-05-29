import tkinter as tk

from Pages.config import LARGE_FONT


class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Specifications of the Frame
        self.grid_configure(sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Creating a Tkinter Frame of the specifications mentioned above
        holder = tk.Frame(self)
        holder.grid()

        # Adding text onto the Tkinter Frame
        self.label = tk.Label(holder, text='WELCOME TO GRAPHICAL PASSWORD CREATOR.', font=LARGE_FONT)
        self.label.grid(row=0, sticky='n')

        # Adding a button on the Frame for Login
        self.login_button = tk.Button(holder, text='''Login''',
                                      command=lambda: controller.show_frame('LoginScreen'))
        self.login_button.grid(row=1, padx=30, pady=30)

        # Adding a button on the Frame for Register
        self.register_button = tk.Button(holder, text="Register",
                                         command=lambda: controller.show_frame('RegisterScreen'))
        self.register_button.grid(row=2)
