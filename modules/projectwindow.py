import tkinter as tk
import datetime


class ProjectWindow(tk.Toplevel):
    """A seperate window for viewing and editing a single Project."""

    def __init__(self, parent, main_app, project):
        super().__init__(parent)

        self.parent = parent
        self.main_app = main_app
        self.project = project

        self.title(project.title)
        self.geometry("800x600")

        self.build_menu()
        self.build_header()
        self.build_body()
        self.build_bottom()


    def build_menu(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Close", command=self.destroy)

        menu_bar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu_bar)


    def build_header(self):
        header_frame = tk.Frame(
            self,
            borderwidth=1,
            relief="solid",
            padx=8,
            pady=4
        )
        header_frame.pack(side="top", fill="x")

        today_str = datetime.date.today().strftime("%A, %B, %D, %Y")

        self.title_label = tk.Label(
            header_frame,
            text=f"Project: {self.project.title}",
            font=("Arial", 12, "bold")
        )
        self.title_label.pack(side="left")

        date_label = tk.Label(
            header_frame,
            text=f"Today's Date: {today_str}",
            font=("Arial", 10)
        )
        date_label.pack(side="right")


    def build_body(self):
        body_frame = tk.Frame(self)
        body_frame.pack(side="top", fill="both", expand=True)

        # Description box
        description_box = tk.Text(
            body_frame,
            height=2,
            font=("Arial", 10),
            padx=8,
            pady=4
        )
        # Initial description
        description_box.insert(tk.END, "Enter a Project description here...")

        description_box.pack(side="top", fill="x")

        # Middle Frame -> Left Panel: Goals
        self.goals_frame = tk.Frame(
            body_frame,
            borderwidth=1,
            relief="solid",
            padx=8,
            pady=4
        )
        self.goals_frame.pack(side="left", fill="both", expand=True)

        goals_label = tk.Label(
            self.goals_frame,
            text="Project Goals",
            font=("Arial", 10, "bold")
        )
        goals_label.pack(anchor='w')

        # Middle Frame -> Right Panel: Step Tracker
        self.step_tracker_frame = tk.Frame(
            body_frame,
            borderwidth=1,
            relief="solid",
            padx=8,
            pady=4
        )
        self.step_tracker_frame.pack(side="right", fill="both", expand=True)

        step_tracker_label = tk.Label(
            self.step_tracker_frame,
            text="Step Tracker",
            font=("Arial", 10, "bold")
        )
        step_tracker_label.pack(anchor='w')


    def build_bottom(self):
        # --- Bottom Frames ---
        bottom_frame = tk.Frame(
            self,
            borderwidth=1,
            relief="solid",
            padx=8,
            pady=4,
            height=80
        )
        bottom_frame.pack(side="bottom", fill="x")
        bottom_frame.pack_propagate(False)

        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.rowconfigure(0, weight=1)

        bottom_left_frame = tk.Frame(bottom_frame)
        bottom_left_frame.grid(row=0, column=0, sticky="news")

        bottom_right_frame = tk.Frame(bottom_frame)
        bottom_right_frame.grid(row=0, column=1, sticky="swe")

        # Add Goal Button
        add_goal_button = tk.Button(
            bottom_right_frame,
            text="Add Goal",
            command=self.add_goal
        )
        add_goal_button.pack(anchor="e")

        # Project Log Button
        project_log_button = tk.Button(
            bottom_right_frame,
            text="Project Log",
            command=self.open_project_logs
        )
        project_log_button.pack(anchor="e")


    def open_project_logs(self):
        print("Project logs feature to be implemented...")


    def add_goal(self):
        print("Adding goals to be implemented...")