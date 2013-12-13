"""Resuable testing fakes.

"""
class FakeWorkbench(object):
    """A fake workbench.

    """
    def __init__(self):
        self.tools = []


    def undisplay(self):
        self.tools.pop()


    def display(self, tool):
        self.tools.append(tool)


    def clear(self):
        del self.tools[:]
