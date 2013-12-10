"""
UI tools related to exercise search and selection.
"""
from arthur.ui import Prompt


class SearchTool(Prompt):
    name = u"Mission search"
    position = ("relative", 20), 30, "middle", 10

    def __init__(self):
        Prompt.__init__(self, self.name, u"Search terms: ")
