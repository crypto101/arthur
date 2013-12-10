from twisted.internet.defer import Deferred, succeed, fail
from twisted.internet.defer import AlreadyCalledError, _NO_RESULT


class MultiDeferred(object):
    """An object that produces other deferreds. When this object is
    callbacked or errbacked, those deferreds are callbacked or
    errbacked with the same result or failure.

    This class has been submitted to Twisted, see tm.tl/6365.

    """
    def __init__(self):
        self._deferreds = []
        self._result = _NO_RESULT
        self._isFailure = None


    def tee(self):
        """
        Produces a new deferred and returns it. If this C{MultiDeferred}
        has not been fired (callbacked or errbacked) yet, the deferred
        will not have been fired yet either, but will be fired when
        and if this C{MultiDeferred} gets fired in the future. If this
        C{MultiDeferred} has been fired, returns a deferred
        synchronously fired with the same result.

        @return: A deferred that will fire with whatever this object
        is fired with.
        @rtype: L{Deferred}
        """
        if self._result is not _NO_RESULT:
            if not self._isFailure:
                return succeed(self._result)
            else:
                return fail(self._result)

        d = Deferred()
        self._deferreds.append(d)
        return d


    def callback(self, result):
        """
        Callbacks the deferreds previously produced by this object.

        @param result: The object which will be passed to the
        C{callback} method of all C{Deferred}s previously produced by
        this object's C{tee} method.
        @raise AlreadyCalledError: If L{callback} or L{errback} has
        already been called on this object.
        """
        self._setResult(result)
        self._isFailure = False

        for d in self._deferreds:
            d.callback(result)


    def errback(self, failure):
        """
        Errbacks the deferreds previously produced by this object.

        @param failure: The object which will be passed to the
        C{errback} method of all C{Deferred}s previously produced by
        this object's C{tee} method.
        @raise AlreadyCalledError: If L{callback} or L{errback} has
        already been called on this object.
        """
        self._setResult(failure)
        self._isFailure = True

        for d in self._deferreds:
            d.errback(failure)


    def _setResult(self, result):
        """
        Sets the result. If the result is already set, raises
        C{AlreadyCalledError}.

        @raise AlreadyCalledError: The result was already set.
        @return: C{None}, if the result was successfully set.
        """
        if self._result is not _NO_RESULT:
            raise AlreadyCalledError()

        self._result = result
