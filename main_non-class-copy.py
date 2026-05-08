#=============================================================================================================
# Import Modules
#=============================================================================================================

import tkinter as tk
import datetime
from modules.project import Project
import json


#=============================================================================================================
# Define Functions
#=============================================================================================================

# this is a test function to test json and project classes
def test_json():
    p = Project("Project1")
    
    s = json.dumps(p.__dict__)
    print(s)
    q = Project("Project2")
    q.__dict__ = json.loads(s)
    print(q.title)
    print(f"{q.title} Created on: {q.creationDate}")
    print(type(q))


# Show Project Details on Select Event
def get_project_details(event, active_listbox, hold_listbox, bottom_text_var, active_projects, hold_projects, selected_active_idx, selected_hold_idx, move_mode, move_button):
    # Get idx of selected item from/in listbox
    selectionActive = active_listbox.curselection()
    selectionHold = hold_listbox.curselection()

    # If nothing selected
    if not selectionHold and not selectionActive:
        selected_active_idx["value"] = None
        selected_hold_idx["value"] = None
        move_mode["value"] = None
        move_button.config(state='disabled')
        return
    
    # if selection is from Active Projects
    elif selectionActive:
        idx = selectionActive[0]
        selected_active_idx["value"] = idx
        selected_hold_idx["value"] = None
        move_mode["value"] = "to_hold"

        project = active_projects[idx]
        move_button.config(state='normal', text='Move Project to Hold Window')

    # if selection is from Projects on Hold
    else:
        idx = selectionHold[0]
        selected_hold_idx["value"] = idx
        selected_active_idx["value"] = None
        move_mode["value"] = "to_active"

        project = hold_projects[idx]
        move_button.config(state="normal", text="Move Project to Active Window")

    # set info on bottomFrame
    bottom_text_var.set(
        f"Title: {project.title}\nCreated on: {project.creationDate}\nLast Opened: {project.lastOpened}")


# Move Project on Button Click
def move_selected(active_projects, hold_projects, selected_active_idx, selected_hold_idx, move_mode, active_listbox, hold_listbox, bottom_text_var, move_button):

    # If project is Active
    if move_mode["value"] == "to_hold":
        idx = selected_active_idx["value"]
        if idx is None:
            return

        # Move to Projects on Hold
        project = active_projects.pop(idx)
        project.active = False    # Update project active status
        hold_projects.append(project)
        bottom_text_var.set(f"Moved '{project.title}' to Projects on Hold")

    # elif project is on Hold
    elif move_mode["value"] == "to_active":
        idx = selected_hold_idx["value"]
        if idx is None:
            return

        # Move to Active Projects        
        project = hold_projects.pop(idx)
        project.active = True
        active_projects.append(project)
        bottom_text_var.set(f"Moved '{project.title}' to Active Projects")

    else:
        return

    # Refresh Listboxes
    refresh_listboxes(active_listbox, hold_listbox, active_projects, hold_projects)

    # Clear State Holders
    selected_active_idx["value"] = None
    selected_hold_idx["value"] = None
    move_mode["value"] = None
    move_button.config(state='disabled')


# Open Project Window on Double Click Event (this just prints something right now)
def open_project(event, listbox, active_projects, selected_active_idx):
    # Get idx of selected item from/in listbox
    idx = selected_active_idx["value"]

    # If nothing is selected, do nothing
    if idx is None:
        return
    
    project = active_projects[idx]

    # execute these statements:

    # Update lastOpened when "opened"
    project.lastOpened = datetime.date.today().strftime("%A, %B, %d, %Y")

    print(f"You double-clicked: {project.title}")


# Refresh Project ListBoxes
def refresh_listboxes(active_listbox, hold_listbox, active_projects, hold_projects):
    # Clear both listboxes
    active_listbox.delete(0, tk.END)
    hold_listbox.delete(0, tk.END)

    # Refill from the Project Objects
    for project in active_projects:
        active_listbox.insert(tk.END, project.title)

    for project in hold_projects:
        hold_listbox.insert(tk.END, project.title)


# Main Window
def main():
    # Initialize list of Active Projects (Class Objects)
    activeProjects = []

    # Initialize list of Projects on Hold (Class Objects)
    holdProjects = []

    # Initialize State Holders - Mutable Containers
    selected_active_idx = {"value": None}    # active project index
    selected_hold_idx = {"value": None}      # hold project index
    move_mode = {"value": None}              # project will be moved "to_hold" or "to_active"

    # Create root window
    root = tk.Tk()
    root.title("Studdy Buddy - Project Tracker")    # window title
    root.geometry("800x600")   # window size - can change later

    #==========================================
    # ---------- Create Header Frame ----------
    #==========================================
    headerFrame = tk.Frame(
        root,              # parent: the main window
        borderwidth=1,     # draw a 1-pixel-wide border
        relief="solid",    # style of the border (plain, solid edge)
        padx=8,            # padding inside the frame (left/right)
        pady=4             # padding inside the frame (top/bottom)
    )
    headerFrame.pack(side='top', fill='x')    # Place the Header Frame at the top, spanning full width - using the pack method

    today_str = datetime.date.today().strftime("%A, %B %d, %Y")    # Get today's date from System Clock using datetime module

    # Label inside the Header
    headerLabel = tk.Label(
        headerFrame,                                # parent: the header frame
        text=f"Today's Date:    {today_str}",       # Today's date
        font=('Arial', 10)                          # font and size
    )
    headerLabel.pack(anchor='e')    # Put label inside header frame; 'e' - (east)(right side)

    #=================================================================
    # ---------- Create Middle Frame: Left and Right Panels ----------
    #=================================================================
    middleFrame = tk.Frame(root)
    middleFrame.pack(side='top', fill='both', expand=True)    # Place frame below headerFrame, expand both ways, allow growth

    # Create Left Panel: Active Projects
    #-----------------------------------
    activeFrame = tk.Frame(
        middleFrame,       # parent: middleFrame
        borderwidth=1,
        relief='solid',    # border style
        padx=8,
        pady=4
    )
    activeFrame.pack(side='left', fill='both', expand=True)    # Pack the frame on the left side of the middleFrame

    activeLabel = tk.Label(
        activeFrame,
        text='Active Projects',
        font=('Arial', 10, 'bold')
    )
    activeLabel.pack(anchor='w')    # pack the label inside the active project frame, left side

    activeListBox = tk.Listbox(activeFrame)    # Create list box for activeFrame, call Listbox method, pass activeFrame as arg
    activeListBox.pack(fill='both', expand=True, pady=(4, 4))    # Place frame

    

    # Create Right Panel: Projects on hold
    #-------------------------------------
    holdFrame = tk.Frame(
        middleFrame,
        borderwidth=1,
        relief='solid',
        padx=8,
        pady=4
    )
    holdFrame.pack(side='right', fill='both', expand=True)    # pack the frame on the right side of middleFrame

    holdLabel = tk.Label(
        holdFrame,
        text='Projects on Hold',
        font=('Arial', 10, 'bold')
    )
    holdLabel.pack(anchor='w')    # pack label inside projects on hold frame, left side

    holdListBox = tk.Listbox(holdFrame)
    holdListBox.pack(fill='both', expand=True, pady=(4, 4))

    #=============================
    # Bind Events
    #=============================
    
    # Double-Click Event - open project if active
    activeListBox.bind(
        "<Double-Button-1>",
        lambda event: open_project(event, activeListBox, activeProjects, selected_active_idx)
    )

    # Single-Click Event - get info
    activeListBox.bind(
        "<<ListboxSelect>>",
        lambda event: get_project_details(event, activeListBox, holdListBox, bottomText, activeProjects, holdProjects, selected_active_idx, selected_hold_idx, move_mode, moveToHoldButton)
    )

    holdListBox.bind(
        "<<ListboxSelect>>",
        lambda event: get_project_details(event, activeListBox, holdListBox, bottomText, activeProjects, holdProjects, selected_active_idx, selected_hold_idx, move_mode, moveToHoldButton)
    )

    #=================================================
    # ---------- Refresh/Populate Listboxes ----------
    #=================================================
    refresh_listboxes(activeListBox, holdListBox, activeProjects, holdProjects)

    #==========================================
    # ---------- Create Bottom Frame ----------
    #==========================================
    bottomFrame = tk.Frame(
        root,
        borderwidth=1,
        relief='solid',
        padx=8,
        pady=4,
        height=80    # define height
    )    
    bottomFrame.pack(side='bottom', fill='x')
    bottomFrame.pack_propagate(False)    # keep defined height; don't shrink to contents

    # Create and set text in bottomFrame
    bottomText = tk.StringVar()
    bottomText.set("Select an Active Project to see details here.")

    bottomLabel = tk.Label(
        bottomFrame,
        textvariable=bottomText,    # always show value in bottomText
        font=('Arial', 9, 'italic')
    )
    bottomLabel.pack(anchor='w')

    # Create Move Button TODO: Clean up the name, this now moves between hold and active
    moveToHoldButton = tk.Button(
        bottomFrame,
        text='Put Project on Hold',
        state='disabled'    # disabled until an Active project is selected
    )
    moveToHoldButton.pack(anchor='e', pady=(6,0))

    # On Button Press
    moveToHoldButton.config(
        command=lambda: move_selected(activeProjects, holdProjects, selected_active_idx, selected_hold_idx, move_mode, activeListBox, holdListBox, bottomText, moveToHoldButton)
    )

    #===============================================
    # ---------- Start Tkinter event loop ----------
    #===============================================
    root.mainloop()


#test_json()



# Import check and open main window
if __name__ == "__main__":
    main()