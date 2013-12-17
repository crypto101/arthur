"""Tests for exercises-related code. """
from arthur import exercises
from arthur.test.fakes import FakeWorkbench
from clarent.exercise import NotifySolved
from twisted.trial.unittest import SynchronousTestCase
from txampext.respondertests import ResponderTestMixin


class NotifySolvedResponderTests(SynchronousTestCase, ResponderTestMixin):
    """The exercise responder locator has a responder for NotifySolved.

    """
    command = NotifySolved
    locator = exercises.ExercisesLocator(None)



class NotifySolvedTests(SynchronousTestCase):
    """Tests for exercise solution notifications.

    """
    def setUp(self):
        self.workbench = FakeWorkbench()
        factory = Factory(self.workbench)
        proto = factory.buildProtocol(None)
        self.locator = proto.locator


    def test_notifySolved(self):
        """The user receives a notification when an exercise is completed. The
        notification can be clicked away.

        """
        self.assertEqual(self.workbench.tools, [])

        result = self.responder.notifySolved(b"identifier", u"The Exercise")
        self.assertEqual(result, {})

        notification = self.workbench.tools[-1]
        self.assertIn(u"Congratulations", notification.text)
        self.assertIn(u"The Exercise", notification.text)

        notification.button.keypress((1,), " ")
        self.assertEqual(self.workbench.tools, [])
