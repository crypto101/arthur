from arthur import run, exercises
from twisted.trial import unittest


class BuildWorkbenchTests(unittest.SynchronousTestCase):
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
