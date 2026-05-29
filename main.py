import tkinter as tk
from Pages.MainScreen import MainScreen
from Pages.RegisterScreen import RegisterScreen
from Pages.LoginScreen import LoginScreen


class MainApplication(tk.Frame):

    # Creating the frame
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.container = tk.Frame(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.container.grid(sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Importing other frames
        self.frames = {
            'RegisterScreen': RegisterScreen,
            'MainScreen': MainScreen,
            'LoginScreen': LoginScreen
        }

        self.current_frame = None
        self.show_frame('MainScreen')

    def show_frame(self, cont):
        print('open ' + cont)
        if self.current_frame:
            frame_combine = self.container.grid_slaves()
            for slave in frame_combine:
                slave.destroy()

        self.current_frame = self.frames[cont](self.container, self)

        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.current_frame.tkraise()


if __name__ == "__main__":
    root = tk.Tk()
    main_app = MainApplication(root)
    main_app.grid(row=0, column=0, sticky='nsew')

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()
