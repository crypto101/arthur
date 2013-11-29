from arthur import run, exercises, ui
from twisted.trial import unittest


class RunLogicTests(unittest.SynchronousTestCase):
    def test_buildWorkbench(self):
        """The workbench has a launcher with all the default tools. The
        launcher is displayed.

        """
        workbench = run.buildWorkbench()
        self.assertEqual(workbench.header.title.text, u"Launcher")

        attrMap, _opts = workbench.widget.contents["body"]
        launcherWidget, _opts = attrMap.original_widget.contents[1]
        listWalker = launcherWidget.original_widget.body

        toolButtons = listWalker[2:]

        searchToolButton = toolButtons[0].original_widget
        self.assertEqual(searchToolButton.label, exercises.SearchTool.name)


    def test_buildMainLoop(self):
        """A mainloop uses the given workbench's widget and the default
        palette.

        """
        workbench = run.buildWorkbench()
        screen = FakeScreen()
        mainLoop = run.buildMainLoop(workbench, screen=screen)
        self.assertIdentical(mainLoop.widget, workbench.widget)
        self.assertIdentical(screen.palette, ui.DEFAULT_PALETTE)
        self.assertIdentical(mainLoop._unhandled_input, ui._unhandledInput)



class FakeScreen(object):
    """
    A fake urwid screen.
    """
    def __init__(self):
        self.palette = None


    def register_palette(self, palette):
        self.palette = palette
