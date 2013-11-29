import urwid

from arthur import exercises, ui
from functools import partial


def buildWorkbench():
    """Builds a workbench.

    The workbench has a launcher with all of the default tools. The
    launcher will be displayed on the workbench.

    """
    workbench = ui.Workbench()

    tools = [exercises.SearchTool()]
    launcher = ui.Launcher(workbench, tools)
    workbench.display(launcher)

    return workbench


def buildMainLoop(workbench, **kwargs):
    """Builds a main loop from the given workbench.

    The main loop will have the default pallette, as well as the
    default unused key handler.

    The extra keyword arguments are passed to the main loop.
    """
    unhandledInput = partial(ui._unhandledInput, workbench=workbench)
    mainLoop = urwid.MainLoop(widget=workbench.widget,
                              palette=ui.DEFAULT_PALETTE,
                              unhandled_input=unhandledInput,
                              **kwargs)
    return mainLoop
