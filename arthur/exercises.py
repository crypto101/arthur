"""
UI tools related to exercise search and selection.
"""
import urwid


class ExerciseSelectionTool(object):
    name = u"Missions"
    position = ("relative", 20), 30, "middle", 30

    def __init__(self):
        self.nextButton = urwid.Button(u"Next")

        search = urwid.Edit(u"Search: ", multiline=False)
        body = urwid.Filler(urwid.Text(u"Mission selection", align="center"))
        self.frame = urwid.Frame(body, header=search, footer=self.nextButton)

        self.widget = urwid.LineBox(self.frame)


    def next(self):
        pass



class ExerciseSelectionCommandLocator(object):
    def __init__(self):
        self.tool = ExerciseSelectionTool()
