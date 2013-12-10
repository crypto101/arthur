"""
Game user interface.
"""
import urwid

from zope import interface

DEFAULT_PALETTE = (
    ('header', 'black', 'dark green'),
    ('foreground', 'dark green', 'black'),
    ('background', 'dark gray', 'black')
)
BACKGROUND = urwid.AttrMap(urwid.SolidFill(u"\N{LIGHT SHADE}"), "background")
DIVIDER = urwid.Divider(u'\N{UPPER ONE EIGHTH BLOCK}')



class Workbench(object):
    """
    A workbench, consisting of a top status bar and a background.
    """
    def __init__(self):
        self.header = Header()
        self.widget = urwid.Frame(header=self.header.widget, body=BACKGROUND)
        self._tools = []


    def display(self, tool):
        """Displays the given tool above the current layer, and sets the
        title to its name.

        """
        self._tools.append(tool)
        self._justDisplay(tool)


    def _justDisplay(self, tool):
        """
        Displays the given tool. Does not register it in the tools list.
        """
        self.header.title.set_text(tool.name)

        body, _options = self.widget.contents["body"]
        overlay = urwid.Overlay(tool.widget, body, *tool.position)
        self._surface = urwid.AttrMap(overlay, "foreground")
        self.widget.contents["body"] = self._surface, None


    def undisplay(self):
        """Undisplays the top tool.

        This actually forces a complete re-render.
        """
        self._tools.pop()
        self.clear()
        for tool in self._tools:
            self._justDisplay(tool)


    def clear(self):
        """
        Clears the workbench.
        """
        self._tools = []
        self.header.title.set_text(u"")
        self.widget.contents["body"] = BACKGROUND, None



class Header(object):
    """
    A header. Contains a title and an aside.
    """
    def __init__(self):
        self.title = urwid.Text(u"", align="left")
        self.aside = urwid.Text(u"Press C-w to quit", align="right")

        columns = urwid.Columns([self.title, self.aside])

        self.widget = urwid.AttrMap(columns, "header")



def _unhandledInput(event, workbench, launcher):
    """Handles input events that weren't handled anywhere else.

    """
    if event == "ctrl w":
        raise urwid.ExitMainLoop()
    elif event == "esc":
        workbench.clear()
        workbench.display(launcher)
        return True



class ITool(interface.Interface):
    """
    A tool, displayable by a workbench.
    """
    name = interface.Attribute(
        """
        The name of the tool, which will be used in the title.
        """)


    widget = interface.Attribute(
        """
        The widget that will be displayed on the workbench.
        """)


    position = interface.Attribute(
        """
        The position of the tool's widget on the workbench.
        """)



@interface.implementer(ITool)
class Launcher(object):
    """The launcher.

    The launcher is a tool that launches other tools. Since it has to
    display other tools, it has a reference to the workbench.

    """
    name = u"Launcher"
    position = "center", 30, "middle", 10

    def __init__(self, workbench, tools):
        self.workbench = workbench

        body = [urwid.Text(u"Select a tool to launch"), DIVIDER]

        for tool in tools:
            button = urwid.Button(tool.name)
            urwid.connect_signal(button, 'click', self._launch, tool)
            body.append(urwid.AttrMap(button, "foreground", focus_map="header"))

        self.menu = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.widget = urwid.LineBox(self.menu)


    def _launch(self, _button, tool):
        """Button callback to launch a tool.

        Tells the workbench to display the given tool.
        """
        self.workbench.display(tool)



@interface.implementer(ITool)
class Prompt(object):
    """
    A generic prompt.
    """
    position = ("relative", 20), 30, "middle", 10

    def __init__(self, name, promptText):
        self.name = name
        title = urwid.Text(name)
        prompt = urwid.Edit(promptText, multiline=False)
        self.pile = urwid.Pile([title, DIVIDER, prompt])
        self.widget = urwid.LineBox(urwid.Filler(self.pile))
