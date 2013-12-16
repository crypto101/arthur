from arthur.ui import alert, prompt, _Splash
from clarent.certificate import makeCredentials, getContextFactory
from clarent.path import getDataPath
from twisted.internet import reactor
from twisted.internet.defer import succeed
from twisted.internet.endpoints import SSL4ClientEndpoint
from twisted.internet.error import ConnectError
from twisted.internet.protocol import ClientFactory
from twisted.protocols.amp import AMP


def connect(workbench):
    """Connection inititalization routine.

    """
    d = _getContextFactory(getDataPath(), workbench)
    d.addCallback(_connectWithContextFactory, workbench)
    return d


def _connectWithContextFactory(ctxFactory, workbench):
    """Connect using the given context factory. Notifications go to the
    given workbench.

    """
    endpoint = SSL4ClientEndpoint(reactor, "localhost", 4430, ctxFactory)

    splash = _Splash(u"Connecting", u"Connecting...")
    workbench.display(splash)

    factory = ClientFactory.forProtocol(AMP)
    d = endpoint.connect(factory)

    @d.addBoth
    def closeSplash(returnValue):
        workbench.undisplay()
        return returnValue

    @d.addErrback
    def notifyFailure(f):
        f.trap(ConnectError)
        d = alert(workbench, u"Couldn't connect", u"Connection failed! "
                  "Check internet connection, or try again later.\n"
                  "Error: {!r}".format(f.value))
        return d

    return d


def _getContextFactory(path, workbench):
    """Get a context factory.

    If the client already has a credentials at path, use them.
    Otherwise, generate them at path. Notifications are reported to
    the given workbench.

    """
    try:
        return succeed(getContextFactory(path))
    except IOError:
        d = prompt(workbench, u"E-mail entry", u"Enter e-mail:")
        d.addCallback(_makeCredentials, path, workbench)
        d.addCallback(lambda _result: getContextFactory(path))
        return d


def _makeCredentials(email, path, workbench):
    """Makes client certs and writes them to disk at path.

    This essentially defers to clarent's ``makeCredentials`` function,
    except it also shows a nice splash screen.

    """
    splash = _Splash(u"SSL credential generation",
                     u"Generating SSL credentials. (This can take a while.)")
    workbench.display(splash)

    makeCredentials(path, email)

    workbench.undisplay()
