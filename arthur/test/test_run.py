from arthur import run, exercises, ui
from twisted.trial import unittest


class RunLogicTests(unittest.SynchronousTestCase):
    def test_buildWorkbench(self):
        """The workbench has a launcher with all the default tools. The
        launcher is displayed.

        """
        workbench, _launcher = run.buildWorkbenchWithLauncher()
        self.assertEqual(workbench.header.title.text, u"Launcher")

        attrMap, _opts = workbench.widget.contents["body"]
        launcherWidget, _opts = attrMap.original_widget.contents[1]
        listWalker = launcherWidget.original_widget.body

        toolButtons = listWalker[2:]

        searchToolButton = toolButtons[0].original_widget
        self.assertEqual(searchToolButton.label, exercises.SearchTool.name)


    def test_buildMainLoop(self):
        """A mainloop uses the given workbench's widget and the default
        palette. It also uses the default unhandled input handler,
        partially applied with the workbench.

        """
        workbench, launcher = run.buildWorkbenchWithLauncher()
        screen = FakeScreen()
        mainLoop = run.buildMainLoop(workbench, launcher, screen=screen)
        self.assertIdentical(mainLoop.widget, workbench.widget)
        self.assertIdentical(screen.palette, ui.DEFAULT_PALETTE)

        unhandledInput = mainLoop._unhandled_input
        self.assertIdentical(unhandledInput.func, ui._unhandledInput)
        self.assertEqual(unhandledInput.keywords,
                         {"workbench": workbench, "launcher": launcher})



class FakeScreen(object):
    """
    A fake urwid screen.
    """
    def __init__(self):
        self.palette = None


    def register_palette(self, palette):
        self.palette = palette


    def get_input_descriptors(self, *a, **kw):
        """Needed to fake event loop support.

        """
        return [] # pragma: no cover
