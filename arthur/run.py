import urwid
from arthur import exercises, ui


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


def buildMainLoop(workbench):
    """Builds a main loop from the given workbench.

    The main loop will have the default pallette, as well as the
    default unused key handler.

    """
    urwid.MainLoop(workbench.widget, ui.DEFAULT_PALETTE)


def run():
    """
    Builds a workbench and a main loop for it, and runs the main loop.
    """
    buildMainLoop(buildWorkbench()).run()
