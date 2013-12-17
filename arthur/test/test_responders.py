"""Tests the protocols built by the default factory have the
appropriate responders.

"""

from arthur.protocol import Factory
from arthur.test.fakes import FakeWorkbench
from clarent.exercise import NotifySolved
from twisted.trial.unittest import SynchronousTestCase
from txampext.respondertests import ResponderTestMixin


workbench = FakeWorkbench()
factory = Factory(workbench)


class NotifySolvedResponderTests(SynchronousTestCase, ResponderTestMixin):
    """The protocol has a responder for NotifySolved.

    """
    command = NotifySolved
    locator = factory.buildProtocol(None)
