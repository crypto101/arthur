from arthur.ui import alert, prompt, _Splash
from clarent.certificate import makeCertificate, generateKey
from platform import system
from OpenSSL import crypto
from os.path import expanduser
from twisted.internet import reactor, ssl
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.endpoints import SSL4ClientEndpoint
from twisted.internet.error import ConnectError
from twisted.internet.protocol import ClientFactory
from twisted.protocols.amp import AMP
from twisted.python.filepath import FilePath


def connect(workbench):
    """Connection inititalization routine.

    """
    d = _getContextFactory(_getDataPath(), workbench)
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


@inlineCallbacks
def _getContextFactory(path, workbench):
    """Get a context factory.

    If the client already has a credentials at path, use them.
    Otherwise, generate them at path. Notifications are reported to
    the given workbench.

    """
    if not path.isdir():
        path.makedirs()
    pemPath = path.child("client.pem")

    if not pemPath.isfile():
        email = yield prompt(workbench, u"E-mail entry", u"Enter e-mail:")
        _makeCredentials(workbench, path, email)

    with pemPath.open() as pemFile:
        cert = ssl.PrivateCertificate.loadPEM(pemFile.read())

    returnValue(cert.options()) # TODO: require server cert verification


def _makeCredentials(workbench, path, email):
    """Makes client certs and writes them to disk at path.

    """
    splash = _Splash(u"SSL credential generation",
                     u"Generating SSL credentials. (This can take a while.)")
    workbench.display(splash)

    key = generateKey()
    cert = makeCertificate(key, email)

    with path.child("client.pem").open("wb") as pemFile:
        pemFile.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
        pemFile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    workbench.undisplay()


thisSystem = system()


def _getDataPath(_system=thisSystem):
    """Gets an appropriate path for storing some local data, such as TLS
    credentials.

    """
    if _system == "Windows":
        path = "~/Crypto101/"
    else:
        path = "~/.crypto101/"

    return FilePath(expanduser(path))
