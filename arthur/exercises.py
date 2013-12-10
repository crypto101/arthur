"""
UI tools related to exercise search and selection.
"""
from arthur.ui import Prompt


class SearchTool(Prompt):
    position = ("relative", 20), 30, "middle", 10

    def __init__(self):
        Prompt.__init__(self, u"Mission search", u"Search terms: ")
