"""
UI tools related to exercise search and selection.
"""
import urwid

from arthur.ui import DIVIDER


class SearchTool(object):
    name = u"Mission search"
    position = ("relative", 20), 30, "middle", 10

    def __init__(self):
        title = urwid.Text(u"Mission search")
        search = urwid.Edit(u"Search terms: ", multiline=False)
        self.pile = urwid.Pile([title, DIVIDER, search])
        self.widget = urwid.LineBox(urwid.Filler(self.pile))
