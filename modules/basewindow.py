import tkinter as tk
import datetime

# TODO: Create a Class for the 'Base' window of all windows in the app so that it can be instantiated everytime a new window is created.
class BaseWindow(tk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)

        self.window = parent
        self.main_app = main_app

        #====================================
        # Menu Bar
        #====================================
        self.menu_bar = tk.Menu(self.window)

        # Create the File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New Project", command=self.main_app.open_new_project_dialog)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Display Menu Bar
        self.window.config(menu=self.menu_bar)

        self.header_frame = tk.Frame(
            self.window,
            borderwidth=1,
            relief="solid",
            padx=8,
            pady=4,
            bg="black"
        )
        self.header_frame.pack(side="top", fill="x")

        today_str = datetime.date.today().strftime("%A, %B %d, %Y")
        self.header_label = tk.Label(
            self.window,
            text=f"Today's Date:    {today_str}",
            font=("Arial", 10)
        )
        self.header_label.pack(anchor="e")


