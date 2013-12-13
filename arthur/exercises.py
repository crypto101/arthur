"""
UI tools related to exercise search and selection.
"""
from arthur.ui import _Prompt, notify
from clarent.exercise import NotifySolved
from twisted.protocols import amp


class SearchTool(_Prompt):
    name = u"Mission search"
    position = ("relative", 20), 30, "middle", 10

    def __init__(self):
        _Prompt.__init__(self, self.name, u"Search terms: ")



class ExercisesLocator(amp.CommandLocator):
    def __init__(self, workbench):
        self.workbench = workbench


    @NotifySolved.responder
    def notifySolved(self, _identifier, title):
        """Notifies the user that a particular exercise has been solved.

        """
        notify(self.workbench, u"Congratulations", u"Congratulations! You "
               "have completed the '{title}' exercise.".format(title=title))
        return {}
