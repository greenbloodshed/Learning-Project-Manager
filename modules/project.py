import datetime

class Project:
    def __init__(self, title):
        # set defaults // create instance vars
        self.title = title
        self.description = "Enter a Project description here..."
        self.creation_date = datetime.date.today().strftime("%A, %B %d, %Y")
        self.last_opened = datetime.date.today().strftime("%A, %B %d, %Y")
        self.goals = []
        #TODO: Refactor this to be the authoritative representation; eliminate 2 project lists, and filter them into each listbox ----> self.active = True
        #self.timeSpent = f"You've spent __ hrs, __ minutes, and __ seconds working on {self.title}"