import urwid

from arthur import exercises, ui
from functools import partial


def buildWorkbenchWithLauncher():
    """Builds a workbench.

    The workbench has a launcher with all of the default tools. The
    launcher will be displayed on the workbench.

    """
    workbench = ui.Workbench()

    tools = [exercises.SearchTool()]
    launcher = ui.Launcher(workbench, tools)
    workbench.display(launcher)

    return workbench, launcher


def buildMainLoop(workbench, launcher, **kwargs):
    """Builds a main loop from the given workbench and launcher.

    The main loop will have the default pallette, as well as the
    default unused key handler. The key handler will have a reference
    to the workbench and launcher so that it can clear the screen.

    The extra keyword arguments are passed to the main loop.
    """
    unhandledInput = partial(ui._unhandledInput,
                             workbench=workbench,
                             launcher=launcher)
    mainLoop = urwid.MainLoop(widget=workbench.widget,
                              palette=ui.DEFAULT_PALETTE,
                              unhandled_input=unhandledInput,
                              **kwargs)
    return mainLoop
