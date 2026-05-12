#=============================================================================================================
# Import Modules
#=============================================================================================================
import tkinter as tk
import datetime
import webbrowser
from modules.project import Project
from modules.basewindow import BaseWindow

#=============================================================================================================
# Main Function // Start Program
#=============================================================================================================
def main():
    root = tk.Tk()
    app = StuddyBuddyApp(root)
    root.mainloop()

#=============================================================================================================
# Studdy Buddy - Long Term Productivity/Learning Tool
#=============================================================================================================
class StuddyBuddyApp:
    def __init__(self, root):

        #=============================================================================================================
        # Declare Attributes, Variable, and Build GUI
        #=============================================================================================================
        self.root = root
        self.root.title("Studdy Buddy - Long Term Learning Tool")
        self.root.geometry("800x600")

        # Initialize Project Lists for Project Class Instances
        # Listbox(created below) indices are mapped to these list indices
        # e.g. a Project instance at idx [0] in one of these lists, will have its title at idx [0] in the corresponding(Active/Hold) Listbox
        self.active_projects = []
        self.hold_projects = []

        #====================================
        # Application State Trackers
        #====================================
        # If a Project is selected in the GUI(Listbox), 
        # then these values will be the idx of the Project in both the corresponding Listbox, and the Project Class Instance List
        # See lines 37 and 38
        self.selected_active_idx = {"value": None}
        self.selected_hold_idx = {"value": None}

        # If Project is Active, the move_mode value will be 'to_hold', else 'to_active'
        self.move_mode = {"value": None}

        # Initialize Bottom Label Details
        self.bottom_label_text = tk.StringVar()
        self.bottom_label_text.set("Select a Project to see details here.")

        #====================================
        # Menu Bar
        #====================================
        # Create the menu bar
        menu_bar = tk.Menu(self.root)

        # Create the File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Project", command=self.open_new_project_dialog)
        file_menu.add_command(label="Preferences", state="disabled")
        file_menu.add_command(label="Settings", state="disabled")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Create the Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Report a Bug", command=self.open_github_repo_issues)
        help_menu.add_command(label="View GitHub Repo", command=self.open_github_repo)
        help_menu.add_command(label="About", state="disabled")
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # Display menu bar
        self.root.config(menu=menu_bar)

        #====================================
        # Frames and Listboxes
        #====================================
        # --- Header Frame ---
        self.header_frame = tk.Frame(
            self.root,
            borderwidth=1,
            relief="solid",
            padx=8,
            pady=4
        )
        self.header_frame.pack(side='top', fill='x')

        # Header Frame - Date/Time label
        today_str = datetime.date.today().strftime("%A, %B %d, %Y")
        self.header_label = tk.Label(
            self.header_frame,
            text=f"Today's Date:    {today_str}",
            font=("Arial", 10)
        )
        self.header_label.pack(anchor="e")
        
        # --- Middle Frame ---
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(side="top", fill="both", expand=True)

        # Middle Frame -> Left Panel: Active Projects
        self.active_frame = tk.Frame(
            self.middle_frame,
            borderwidth=1,
            relief="solid",
            padx=8,
            pady=4
        )
        self.active_frame.pack(side="left", fill="both", expand=True)

        self.active_label = tk.Label(
            self.active_frame,
            text="Active Projects",
            font=("Arial", 10, "bold")
        )
        self.active_label.pack(anchor='w')

        # Create Active Listbox
        self.active_list_box = tk.Listbox(self.active_frame, exportselection=False)
        self.active_list_box.pack(fill="both", expand=True, pady=(4, 4))

        # Middle Frame -> Right Panel: Projects on Hold
        self.hold_frame = tk.Frame(
            self.middle_frame,
            borderwidth=1,
            relief="solid",
            padx=8,
            pady=4
        )
        self.hold_frame.pack(side="right", fill="both", expand=True)

        self.hold_label = tk.Label(
            self.hold_frame,
            text="Projects on Hold",
            font=("Arial", 10, "bold")
        )
        self.hold_label.pack(anchor="w")

        # Create Hold Listbox
        self.hold_list_box = tk.Listbox(self.hold_frame, exportselection=False)
        self.hold_list_box.pack(fill="both", expand=True, pady=(4, 4))

        # --- Bottom Frames ---
        self.bottom_frame = tk.Frame(
            self.root,
            borderwidth=1,
            relief="solid",
            padx=8,
            pady=4,
            height=80
        )
        self.bottom_frame.pack(side="bottom", fill="x")
        self.bottom_frame.pack_propagate(False)

        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

        self.bottom_left_frame = tk.Frame(self.bottom_frame)
        self.bottom_left_frame.grid(row=0, column=0, sticky="news")

        self.bottom_right_frame = tk.Frame(self.bottom_frame)
        self.bottom_right_frame.grid(row=0, column=1, sticky="swe")

        # Set Bottom Label Details in Bottom Left Frame
        self.bottom_info_label = tk.Label(
            self.bottom_left_frame,
            textvariable=self.bottom_label_text,
            font=("Arial", 9, "italic", "bold"),
            justify=tk.LEFT
        )
        self.bottom_info_label.pack(anchor="nw", expand=True)

        #====================================
        # Bindings
        #====================================
        self.active_list_box.bind("<<ListboxSelect>>", self.on_select_event)
        self.hold_list_box.bind("<<ListboxSelect>>", self.on_select_event)
        
        # Testing
        self.active_list_box.bind("<Double-Button-1>", self.open_project)

        #====================================
        # Buttons
        #====================================
        # New Project Button
        self.new_project_button = tk.Button(
            self.bottom_right_frame,
            text="New Project",
            command=self.open_new_project_dialog
        )
        self.new_project_button.pack(anchor="e")

        # Delete Project Button
        self.delete_project_button = tk.Button(
            self.bottom_right_frame,
            text="Delete Project",
            fg="red",
            state="disabled",
            command=self.open_delete_project_dialog
        )
        self.delete_project_button.pack(anchor="e")

        # Move Project Button
        self.move_button = tk.Button(
            self.bottom_right_frame,
            text="Move to Projects on Hold",
            state="disabled",
            command=self.move_selected
        )
        self.move_button.pack(anchor="e")

        #====================================
        # Refresh UI
        #====================================
        self.refresh_listboxes()

    #=============================================================================================================
    # Methods
    #=============================================================================================================

    def get_active_project(self):
        ''' Returns a tuple containing [0]The currently selected project(instance), and [1]the idx of the project in the project instance list and the listbox.
            If you only want the project, and not the idx, or vice versa, call using '_'. 
            e.g.: project, _ = self.get_active_project().
            Otherwise, the entire tuple will be retuned. In other words, you must unpack the tuple if you want the values inside assigned to seperate variables.'''
        # Get index for currently selected element(project title) in the active listbox which is mapped to the index of the Project Class Instance
        idx = self.selected_active_idx["value"]

        # Get selected Project's Class Instance
        project_class_instance = self.active_projects[idx]

        # If nothing selected
        if idx is None:
            return
        # Return Project Class Instance and its idx
        else:
            return project_class_instance, idx
        

    def open_project(self, event):
        # Get Active Project
        project, _ = self.get_active_project()

        # Creare new window for the Project
        project_window = tk.Toplevel(self.root)
        project_window.title(project.title)
        project_window.geometry("800x600")

        # TODO: Instantiate 'Base Window'
        project_window = BaseWindow(project_window, self).pack()


    def open_new_project_dialog(self):
        # Create modal window
        dialog = tk.Toplevel(self.root)
        dialog.title("New Project")
        dialog.resizable(False, False)
        dialog.transient(self.root)    # keep above main window
        dialog.grab_set()              # make it modal (force user to interact w/ the dialog before anything else)

        # Layout
        container = tk.Frame(dialog, padx=10, pady=10)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Project title:").pack(anchor="w")

        title_var = tk.StringVar()
        title_entry = tk.Entry(container, textvariable=title_var, width=60)
        title_entry.pack(fill="x", pady=(4, 10))
        title_entry.focus_set()

        # Status label for validation errors
        status_var = tk.StringVar()
        status_label = tk.Label(container, textvariable=status_var, font=("Arial", 9, "italic"))
        status_label.pack(anchor="w", pady=(0, 8))

        def close():
            dialog.grab_release()
            dialog.destroy()
        

        def create_project():
            # Get title from user in title input box
            title = title_var.get().strip()

            # Validate Input
            if not title:
                status_var.set("Title cannot be blank.")
                return
            
            # Prevent Duplicate Titles
            all_titles = [p.title for p in self.active_projects] + [p.title for p in self.hold_projects]
            if title in all_titles:
                status_var.set("A project with that title already exists.")
                return
            
            # Create new Project Class Instance & add to Active Projects
            self.active_projects.append(Project(title))

            # Refresh UI
            self.refresh_listboxes()

            # Auto-select the new project
            new_idx = len(self.active_projects) - 1
            self.hold_list_box.selection_clear(0, tk.END)
            self.active_list_box.selection_clear(0, tk.END)
            self.active_list_box.selection_set(new_idx)
            self.active_list_box.activate(new_idx)
            self.active_list_box.see(new_idx)

            # Trigger normal selection logic and update bottom panel w/ proj info
            self.on_select_event(None)

            close()


        # Close window button handling
        dialog.protocol("WM_DELETE_WINDOW", close)

        # Buttons row
        btn_row = tk.Frame(container)
        btn_row.pack(fill="x")

        tk.Button(btn_row, text="Cancel", command=close).pack(side="right")
        tk.Button(btn_row, text="Create", command=create_project).pack(side="right", padx=(0, 6))

        # Keyboard shortcuts
        dialog.bind("<Return>", lambda event: create_project())
        dialog.bind("<Escape>", lambda event: close())


    def open_delete_project_dialog(self):
        """ This method opens a confirmation dialog for project deletion. """

        # Get project and its index
        project, idx = self.get_active_project()

        # Create modal window
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Project")
        dialog.resizable(False, False)
        dialog.transient(self.root)    # keep above main window
        dialog.grab_set()              # make it modal (force user to interact w/ the dialog before anything else)

        # Layout
        container = tk.Frame(dialog, padx=10, pady=10)
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text=(
                f"Are you sure you want to delete Project: '{project.title}' ?\n\n"
                "WARNING: This action cannot be undone!!!"
            )
        ).pack(anchor="w")

        def close():
            dialog.grab_release()
            dialog.destroy()

        
        def delete_project():
            deleted_project = self.active_projects.pop(idx)
            
            # Refresh UI
            self.refresh_listboxes()

            # Trigger normal selection logic and update bottom panel w/ relevant info
            self.selected_active_idx["value"] = None
            self.selected_hold_idx["value"] = None
            self.move_mode["value"] = None

            self.move_button.config(state="disabled")
            self.delete_project_button.config(state="disabled", text="Delete Project")

            self.bottom_label_text.set(f"Deleted Project: {deleted_project.title}")

            close()


        # Close window button handling
        dialog.protocol("WM_DELETE_WINDOW", close)

        # Buttons
        btn_row = tk.Frame(container)
        btn_row.pack(fill="x", pady=(10, 0))

        tk.Button(btn_row, text="No: Cancel", command=close).pack(side="right")
        tk.Button(btn_row, text="Yes: Delete Forever", command=delete_project).pack(side="right", padx=(0, 6))

        # Keyboard shortcuts
        dialog.bind("<Escape>", lambda event: close())


    def refresh_listboxes(self):
        """ This method Clears both Listboxes and refills them from the lists of Project Class Instances"""

        # Clear Listboxes
        self.active_list_box.delete(0, tk.END)
        self.hold_list_box.delete(0, tk.END)

        # Rebuild the listboxes from the Project lists
        for p in self.active_projects:
            self.active_list_box.insert(tk.END, p.title)
        
        for p in self.hold_projects:
            self.hold_list_box.insert(tk.END, p.title)


    def on_select_event(self, event):
        """
        This method gets details about a specific Project when selected, sets those details in bottom_label_text,
        and activates button the Move and Delete buttons.
        """
        # Clear the opposite listbox selection
        if event is not None:
            if event.widget == self.active_list_box:
                self.hold_list_box.selection_clear(0, tk.END)
            elif event.widget == self.hold_list_box:
                self.active_list_box.selection_clear(0, tk.END)
        
        # Get the Listbox idx for the currently selected item (Returns a Tuple w/ idx)
        selection_active = self.active_list_box.curselection()
        selection_hold = self.hold_list_box.curselection()

        # If nothing selected
        if not selection_active and not selection_hold:
            self.selected_active_idx["value"] = None
            self.selected_hold_idx["value"] = None
            self.move_mode["value"] = None
            self.move_button.config(state="disabled")
            self.delete_project_button.config(state="disabled", text="Delete Project")
            self.bottom_label_text.set("Select a Project to see details here.")
            return
        
        # If the currently selected item is an Active Project
        if selection_active:
            # Update Application State
            idx = selection_active[0]
            self.selected_active_idx["value"] = idx    # Update the selected active idx
            self.selected_hold_idx["value"] = None
            self.move_mode["value"] = "to_hold"        # Active projects can only be moved to Projects on hold

            project = self.active_projects[idx]        # Get project class instance
            self.move_button.config(state="normal", text="Move to Projects on Hold")    # Activate move button
            self.delete_project_button.config(state="normal", text="Delete Project")

        else:
            idx = selection_hold[0]
            self.selected_hold_idx["value"] = idx
            self.selected_active_idx["value"] = None
            self.move_mode["value"] = "to_active"    # Projects on hold can only be moved to Active Projects

            project = self.hold_projects[idx]        # Get project class instance
            self.move_button.config(state="normal", text="Move to Active Projects")    # Activate move button
            self.delete_project_button.config(state="disabled", text="Project must be Active to Delete")

        # Show project details in bottom label
        self.bottom_label_text.set(
            f"Project Selected: {project.title}\nCreated on: {project.creation_date}\nLast opened: {project.last_opened}"
        )


    def move_selected(self):
        """ This method moves the selected Project between Active and Hold Panels """
        if self.move_mode["value"] == "to_hold":
            idx = self.selected_active_idx["value"]
            project = self.active_projects.pop(idx)    # Remove Project Class Instance from active_projects list and store in var
            self.hold_projects.append(project)         # Put Project Class Instance into hold_projects list
            project.active = False
            self.bottom_label_text.set(f"Moved to Projects on Hold: {project.title}")

        elif self.move_mode["value"] == "to_active":
            idx = self.selected_hold_idx["value"]
            project = self.hold_projects.pop(idx)      # Remove Project Class Instance from hold_projects list and store in var
            self.active_projects.append(project)       # Put Project Class Instance into active_projects list
            project.active = True
            self.bottom_label_text.set(f"Moved to Active Projects: {project.title}")

        else:
            return
        
        # Refresh Listboxes
        self.refresh_listboxes()
        self.move_button.config(state="disabled")              # Disable move button
        self.delete_project_button.config(state="disabled", text="Delete Project")    # Disable Delete button

        # Reset State Holders
        self.selected_active_idx["value"] = None
        self.selected_hold_idx["value"] = None
        self.move_mode["value"] = None


    def open_github_repo(self):
        '''opens system default browser to the github repo for this app'''

        github_repo_url = "https://github.com/greenbloodshed/Learning-Project-Manager"

        webbrowser.open(github_repo_url, new=0, autoraise=True)


    def open_github_repo_issues(self):
        ''' opens issues page of the github repo '''

        github_repo_issues_url = "https://github.com/greenbloodshed/Learning-Project-Manager/issues"

        webbrowser.open(github_repo_issues_url, new=0, autoraise=True)

# Import check and open main window
if __name__ == "__main__":
    main()