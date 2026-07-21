class Goal:
    ''' Accepts a string for a Goal name'''
    def __init__(self, name):
        # set defaults // create instance vars
        self.name = name
        self.steps = []
        self.description = ""