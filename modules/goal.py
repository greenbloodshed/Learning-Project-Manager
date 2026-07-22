import datetime

class Goal:
    ''' Accepts a string for a Goal name'''
    def __init__(self, name, description):
        # set defaults // create instance vars
        self.name = name
        self.steps = []
        self.description = description
        self.creation_date = datetime.date.today().strftime("%A, %B %d, %Y")