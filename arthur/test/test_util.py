from arthur.util import MultiDeferred
from twisted.internet import defer
from twisted.trial import unittest


class MultiDeferredTests(unittest.SynchronousTestCase):
    """
    Tests for L{defer.MultiDeferred}, except now in Arthur.

    See tm.tl/6365.
    """
    def setUp(self):
        self.multiDeferred = MultiDeferred()


    def test_callback(self):
        """
        Any produced L{defer.Deferred}s have their callbacks called when the
        L{defer.MultiDeferred} does.
        """
        a, b, c = [self.multiDeferred.tee() for _ in xrange(3)]

        self.assertNoResult(a)
        self.assertNoResult(b)
        self.assertNoResult(c)

        result = object()
        self.multiDeferred.callback(result)

        self.assertIdentical(self.successResultOf(a), result)
        self.assertIdentical(self.successResultOf(b), result)
        self.assertIdentical(self.successResultOf(c), result)


    def test_errback(self):
        """
        Any produced L{defer.Deferred}s have their errbacks called when the
        L{defer.MultiDeferred} does.
        """
        a, b, c = [self.multiDeferred.tee() for _ in xrange(3)]

        self.assertNoResult(a)
        self.assertNoResult(b)
        self.assertNoResult(c)

        error = RuntimeError()
        self.multiDeferred.errback(error)

        self.assertIdentical(self.failureResultOf(a, RuntimeError).value, error)
        self.assertIdentical(self.failureResultOf(b, RuntimeError).value, error)
        self.assertIdentical(self.failureResultOf(c, RuntimeError).value, error)


    def test_callbackAfterCallback(self):
        """
        Calling C{callback} twice raises L{defer.AlreadyCalledError}.
        """
        self.multiDeferred.callback(None)
        self.assertRaises(defer.AlreadyCalledError,
                          self.multiDeferred.callback, None)


    def test_callbackAfterErrback(self):
        """
        Calling C{callback} after C{errback} raises L{defer.AlreadyCalledError}.
        """
        self.multiDeferred.errback(RuntimeError())
        self.assertRaises(defer.AlreadyCalledError,
                          self.multiDeferred.callback, None)


    def test_errbackAfterCallback(self):
        """
        Calling C{errback} after C{callback} raises L{defer.AlreadyCalledError}.
        """
        self.multiDeferred.callback(None)
        self.assertRaises(defer.AlreadyCalledError,
                          self.multiDeferred.errback, RuntimeError())


    def test_errbackAfterErrback(self):
        """
        Calling C{errback} after C{errback} raises L{defer.AlreadyCalledError}.
        """
        self.multiDeferred.errback(RuntimeError())
        self.assertRaises(defer.AlreadyCalledError,
                          self.multiDeferred.errback, RuntimeError())


    def test_synchronousCallbacks(self):
        """
        All callbacks are called sequentially, synchronously, and in the order
        they were produced. If one or more of the L{defer.Deferred}s produced
        by L{defer.MultiDeferred.tee} is waiting on a deferred that will never
        fire, all the other deferreds produced by that method are still fired.
        """
        called = []
        result = object()

        def callback(r, i):
            """
            Checks this is the correct result, adds this deferreds index to the list
            of called deferreds, and then returns a deferred that will never
            fire.
            """
            self.assertIdentical(r, result)
            called.append(i)
            return defer.Deferred()

        for i in range(10):
            self.multiDeferred.tee().addCallback(callback, i=i)

        self.assertEqual(called, [])
        self.multiDeferred.callback(result)
        self.assertEqual(called, range(10))


    def test_alreadyFiredWithResult(self):
        """
        If the C{MultiDeferred} already fired, C{tee} produces a
        C{Deferred} that has already been fired.
        """
        result = object()
        self.multiDeferred.callback(result)
        d = self.multiDeferred.tee()
        self.assertIdentical(self.successResultOf(d), result)


    def test_alreadyFiredWithError(self):
        """
        If the C{MultiDeferred} already fired with a failure, C{tee}
        produces a C{Deferred} that has already been fired with the
        failure.
        """
        error = RuntimeError()
        self.multiDeferred.errback(error)
        d = self.multiDeferred.tee()
        failure = self.failureResultOf(d, RuntimeError)
        self.assertIdentical(failure.value, error)
