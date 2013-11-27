"""
The journal tool, which tells the story line progression.
"""
import urwid


class Journal(object):
    name = u"Journal"

    def __init__(self):
        self.nextButton = urwid.Button(u"Next")

        self.frame = urwid.Frame()
        self.widget = urwid.LineBox(self.frame)


    def next(self):
        pass



class JournalCommandLocator(object):
    def __init__(self):
        self.tool = Journal()
