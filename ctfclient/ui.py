"""
Game user interface.
"""
import urwid

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


    def display(self, tool):
        """
        Displays the given tool and sets the title to its name.
        """
        self.header.title.set_text(tool.name)

        body, _options = self.widget.contents["body"]
        overlay = urwid.Overlay(tool.widget, body, *tool.position)
        self._surface = urwid.AttrMap(overlay, "foreground")
        self.widget.contents["body"] = self._surface, None


    def clear(self):
        """
        Clears the workbench.
        """
        self.header.title.set_text(u"")
        self.widget.contents["body"] = BACKGROUND, None



class Header(object):
    """
    The header. Contains a title and an aside.
    """
    def __init__(self):
        self.title = urwid.Text(u"", align="left")
        self.aside = urwid.Text(u"", align="right")

        columns = urwid.Columns([self.title, self.aside])

        self.widget = urwid.AttrMap(columns, "header")



class Launcher(object):
    """The launcher.

    The launcher is a tool that launches other tools. Since it has to
    display other tools, it has a reference to the workbench.

    """
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