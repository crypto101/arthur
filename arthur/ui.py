"""
Game user interface.
"""
import urwid

from arthur.util import MultiDeferred
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
class _PopUp(object):
    """
    A generic pop-up.
    """
    position = ("relative", 20), 30, "middle", 10

    def __init__(self, name):
        self.name = name

        headerWidgets = [urwid.Text(name), DIVIDER]
        self.pile = urwid.Pile(headerWidgets + self._makeExtraWidgets())
        self.widget = urwid.LineBox(urwid.Filler(self.pile))


    def _makeExtraWidgets(self):
        return []



class _ButtonPopUp(_PopUp):
    """A pop up with one or more buttons, and support for notification
    when they've been clicked.

    """
    def __init__(self, name):
        _PopUp.__init__(self, name)
        self._result = MultiDeferred()


    def _makeExtraWidgets(self):
        """Makes the extra widgets.

        This defers to the ``make(TextWidgets|Buttons)`` methods; so
        they can be overridden separately.

        """
        return self._makeTextWidgets() + self._makeButtons()


    def _makeTextWidgets(self):
        """Makes (optional) text widgets.

        Override this in a subclass.
        """
        return []


    def _makeButtons(self):
        """Makes buttons and wires them up.

        """
        self.button = button = urwid.Button(u"OK")
        urwid.connect_signal(button, "click", self._completed)
        return [self.button]


    def notifyCompleted(self):
        """Request to be notified when this prompt is completed.

        """
        return self._result.tee()


    def _completed(self, result=None):
        """Call the completion deferreds that have been handed out.

        """
        self._result.callback(result)



class _Notification(_ButtonPopUp):
    """A generic notification, which can be clicked away.

    """
    def __init__(self, name, notificationText):
        self.notificationText = notificationText
        _ButtonPopUp.__init__(self, name)


    def _makeTextWidgets(self):
        """Makes a text widget.

        """
        self.textWidget = urwid.Text(self.notificationText)
        return [self.textWidget]



def notify(workbench, name, text):
    """Runs a notification.

    """
    return _runPopUp(workbench, _Notification(name, text))



class _Prompt(_ButtonPopUp):
    """
    A generic prompt for a single string value.
    """
    def __init__(self, name, promptText):
        self.promptText = promptText
        _ButtonPopUp.__init__(self, name)


    def _makeTextWidgets(self):
        """Makes an editable prompt widget.

        """
        self.prompt = urwid.Edit(self.promptText, multiline=False)
        return [self.prompt]


    def _completed(self):
        """The prompt was completed. Fire all waiting deferreds with the
        prompt's edit text.

        """
        self._result.callback(self.prompt.edit_text)



def prompt(workbench, name, promptText):
    """Runs a prompt.

    """
    return _runPopUp(workbench, _Prompt(name, promptText))


def _runPopUp(workbench, popUp):
    """Displays the pop-up on the workbench and gets a completion
    notification deferred. When that fires, undisplay the pop-up and
    return the result of the notification deferred verbatim.

    """
    workbench.display(popUp)

    d = popUp.notifyCompleted()
    d.addCallback(_popUpCompleted, workbench)
    return d


def _popUpCompleted(result, workbench):
    """The popUp was completed; undisplay it and return the result.

    """
    workbench.undisplay()
    return result
