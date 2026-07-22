import tkinter as tk
import datetime
from modules.goal import Goal
from modules.step import Step


#=============================================================================================================
# Project Window
#=============================================================================================================
class ProjectWindow(tk.Toplevel):
    """A seperate window for viewing and editing a single Project."""
    #=============================================================================================================
    # Initializer
    #=============================================================================================================
    def __init__(self, parent, project):
        super().__init__(parent)

        self.parent = parent
        self.project = project

        self.title(project.title)
        self.geometry("800x600")

        # Build GUI
        self.build_menu()
        self.build_header()
        self.build_body()
        self.build_bottom()

        # Load Project Data
        self.refresh_listboxes()

        self.protocol("WM_DELETE_WINDOW", self.close_window)

        # Bindings
        self.goals_list_box.bind("<<ListboxSelect>>", self.on_select_event)

        # Application State Trackers
        #----------------------------
        # If a Goal is selected in the GUI(Listbox), 
        # then these values will be the idx of the Goal in the Listbox, and the Goal Instance List(Project Attribute)
        self.selected_goal_idx = {"value": None}
        # TODO: add step idx = {"value": None}

        # get goal
        self.current_goal = self.selected_goal_idx["value"]


    def build_menu(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(
            label="Close",
            command=self.close_window
        )

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

        today_str = datetime.date.today().strftime("%A, %B, %d, %Y")

        self.title_label = tk.Label(
            header_frame,
            text=f"Project: {self.project.title}",
            font=("Arial", 10, "bold")
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
        self.description_box = tk.Text(
            body_frame,
            height=2,
            font=("Arial", 10),
            padx=8,
            pady=4
        )
        # Initial description
        self.description_box.insert(tk.END, self.project.description)

        self.description_box.pack(side="top", fill="x")

        # --- Middle Frame ---
        self.middle_frame = tk.Frame(body_frame)
        self.middle_frame.pack(side="top", fill="both", expand=True)

        # Middle Frame -> Left Panel: Goals
        self.goals_frame = tk.Frame(
            self.middle_frame,
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

        # Create Goal Listbox
        self.goals_list_box = tk.Listbox(self.goals_frame, exportselection=False)
        self.goals_list_box.pack(fill="both", expand=True, pady=(4, 4))

        # Middle Frame -> Right Panel: Step Tracker
        self.step_tracker_frame = tk.Frame(
            self.middle_frame,
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

        # Create Step Tracker Listbox
        self.step_tracker_list_box = tk.Listbox(self.step_tracker_frame, exportselection=False)
        self.step_tracker_list_box.pack(fill="both", expand=True, pady=(4, 4))


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

        # Initialize Bottom Label Details
        self.bottom_label_text = tk.StringVar()
        self.bottom_label_text.set("Select a Goal to see details here.")

        # Set Bottom Label in Bottom Left Frame
        self.bottom_info_label = tk.Label(
            bottom_left_frame,
            textvariable=self.bottom_label_text,
            font=("Arial", 9, "italic", "bold"),
            justify=tk.LEFT
        )
        self.bottom_info_label.pack(anchor="nw", expand=True)

        # Add Goal Button
        self.add_goal_button = tk.Button(
            bottom_right_frame,
            text="Add Goal",
            command=self.add_goal_dialog
        )
        self.add_goal_button.pack(anchor="e")

        # Add Step Button
        self.add_step_button = tk.Button(
            bottom_right_frame,
            text="Add Step",
            state="disabled",
            command=self.add_step_dialog
        )
        self.add_step_button.pack(anchor="e")

        # Project Log Button
        self.project_log_button = tk.Button(
            bottom_right_frame,
            text="Project Log",
            command=self.open_project_logs
        )
        self.project_log_button.pack(anchor="e")


    def open_project_logs(self):
        print("Project logs feature to be implemented...")


    def refresh_listboxes(self):
        """ This method refreshes both listboxes"""

        # Clear Listboxes
        self.goals_list_box.delete(0, tk.END)
        self.step_tracker_list_box.delete(0, tk.END)

        # Rebuild the listboxes from the Project lists
        for g in self.project.goals:
            self.goals_list_box.insert(tk.END, g.name)
        
        # TODO: build step tracker listbox


    def refresh_step_tracker_listbox(self):
        """ This method refreshed the step tracker listbox """

        self.step_tracker_list_box.delete(0, tk.END)

        for step in self.project.goals[self.current_goal].steps:
            self.step_tracker_list_box.insert(tk.END, step.name)


    def add_step_dialog(self):
        # Create modal window
        dialog = tk.Toplevel(self)
        dialog.title("Add a Step to this Goal")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Layout
        container = tk.Frame(dialog, padx=10, pady=10)
        container.pack(fill="both", expand=True)

        # Set Step Name and info
        tk.Label(container, text="Set Step Name:").pack(anchor="w")
        step_var = tk.StringVar()
        step_entry = tk.Entry(container, textvariable=step_var, width=60)
        step_entry.pack(fill="x", pady=(4, 10))
        step_entry.focus_set()

        # Set Step Description box
        tk.Label(container, text="Description:").pack(anchor="w")
        description_var = tk.StringVar()
        description_entry = tk.Entry(container, textvariable=description_var, width=60)
        description_entry.pack(fill="x",pady=(4, 10))

        # Status label for validation errors
        status_var = tk.StringVar()
        status_label = tk.Label(container, textvariable=status_var, font=("Arial", 9, "italic"))
        status_label.pack(anchor="w", pady=(0, 8))

        def close():
            dialog.grab_release()
            dialog.destroy()


        def add_step():
            # Get step name from user
            step_name = step_var.get().strip()
            step_description = description_var.get().strip()

            # Validate Input
            if not step_name:
                status_var.set("Step name cannot be blank.")
                return
            
            if not step_description:
                status_var.set("Description cannot be blank.")
                return

            # Check for duplicate titled steps
            if any(
                step.name.casefold() == step_name.casefold()
                for step in self.project.goals[self.current_goal].steps
            ):
                status_var.set("A Step with that name already exists for this Goal.")
                return
            
            # Instantiate new Step for the Goal
            self.project.goals[self.current_goal].steps.append(Step(step_name, step_description))

            self.refresh_step_tracker_listbox()

            close()


        # Close window button handling
        dialog.protocol("WM_DELETE_WINDOW", close)

        # Buttons row
        btn_row = tk.Frame(container)
        btn_row.pack(fill="x")

        tk.Button(btn_row, text="Cancel", command=close).pack(side="right")
        tk.Button(btn_row, text="Add Step", command=add_step).pack(side="right", padx=(0, 6))

        # Keyboard shortcuts
        dialog.bind("<Return>", lambda event: add_step())
        dialog.bind("<Escape>", lambda event: close())
            

    def add_goal_dialog(self):
        # Create modal window
        dialog = tk.Toplevel(self)
        dialog.title("Add a Goal")
        dialog.resizable(False, False)
        dialog.transient(self)         # keep above main window
        dialog.grab_set()              # make it modal (force user to interact w/ the dialog before anything else)

        # Layout
        container = tk.Frame(dialog, padx=10, pady=10)
        container.pack(fill="both", expand=True)

        # Set Goal Name text box
        tk.Label(container, text="Set Goal Name:").pack(anchor="w")
        goal_var = tk.StringVar()
        goal_entry = tk.Entry(container, textvariable=goal_var, width=60)
        goal_entry.pack(fill="x", pady=(4, 10))
        goal_entry.focus_set()

        # Set Goal Description text box
        tk.Label(container, text="Description:").pack(anchor="w")
        description_var = tk.StringVar()
        description_entry = tk.Entry(container, textvariable=description_var, width=60)
        description_entry.pack(fill="x",pady=(4, 10))

        # Status label for validation errors
        status_var = tk.StringVar()
        status_label = tk.Label(container, textvariable=status_var, font=("Arial", 9, "italic"))
        status_label.pack(anchor="w", pady=(0, 8))

        def close():
            dialog.grab_release()
            dialog.destroy()


        def add_goal():
            # Get goal name from user in 'Set Goal Name' input box
            goal_name = goal_var.get().strip()
            goal_description = description_var.get().strip()

            # Validate Input
            if not goal_name:
                status_var.set("Goal name cannot be blank.")
                return
            
            if not goal_description:
                status_var.set("Description cannot be blank.")
                return
            
            # Check for and Prevent Duplicate Titles
            if any(
                goal.name.casefold() == goal_name.casefold()
                for goal in self.project.goals
            ):
                status_var.set("A Goal with that name already exists for this Project.")
                return
            
            # Instantiate new Goal Class Instance for the Project
            self.project.goals.append(Goal(goal_name, goal_description))

            # Refresh listboxes
            self.refresh_listboxes()

            # Auto-select the new goal
            new_idx = len(self.project.goals) - 1
            #self.step_tracker_list_box.selection_clear(0, tk.END)
            self.goals_list_box.selection_clear(0, tk.END)
            self.goals_list_box.selection_set(new_idx)
            self.goals_list_box.activate(new_idx)
            self.goals_list_box.see(new_idx)

            # Trigger normal selection logic and update bottom panel w/ proj info
            self.on_select_event(None)

            close()


        # Close window button handling
        dialog.protocol("WM_DELETE_WINDOW", close)

        # Buttons row
        btn_row = tk.Frame(container)
        btn_row.pack(fill="x")

        tk.Button(btn_row, text="Cancel", command=close).pack(side="right")
        tk.Button(btn_row, text="Add Goal", command=add_goal).pack(side="right", padx=(0, 6))

        # Keyboard shortcuts
        dialog.bind("<Return>", lambda event: add_goal())
        dialog.bind("<Escape>", lambda event: close())


    def on_select_event(self, event):
        """
        Gets details about the selected Project, updates bottom_label_text,
        and activates the Move and Delete buttons as appropriate.
        """
        # TODO: Clear the opposite listbox selection
        #if event is not None:
            #if event.widget == self.goals_list_box:
            #    self.hold_list_box.selection_clear(0, tk.END)
            #elif event.widget == self.hold_list_box:
            #    self.active_list_box.selection_clear(0, tk.END)
        
        # Get the Listbox idx for the currently selected item (Returns a Tuple w/ idx)
        selection_goal = self.goals_list_box.curselection()
        #TODO: add step listbox: selection_hold = self.hold_list_box.curselection()
        

        if not selection_goal:
            self.selected_goal_idx["Value"] = None
            self.add_step_button.config(state="disabled")
            self.bottom_label_text.set("Select a Goal to see details here.")

        else:
            idx = selection_goal[0]
            self.selected_goal_idx["value"] = idx
            self.current_goal = self.selected_goal_idx["value"]
            goal = self.project.goals[idx]    # Get Goal Instance
            self.add_step_button.config(state="normal", text="Add Step")

        # Show goal details in bottom label
        self.bottom_label_text.set(
            f"Goal Selected: {goal.name}\nCreated on: {goal.creation_date}\nDescription: {goal.description}"
        )

        self.refresh_step_tracker_listbox()


    def close_window(self):
        """Save editable project data and close the Project Window"""

        self.project.description = self.description_box.get(
            "1.0",    # line 1 char 0
            "end-1c"    # the end, minues one char (exclude newline char)
        )

        self.destroy()