"""The arthur AMP protocol and factory.

"""
from arthur.exercises import Locator
from twisted.internet.protocol import ClientFactory
from twisted.protocols.amp import AMP


class AMP(AMP, Locator):
    """The arthur AMP protocol.

    """



factory = ClientFactory.forProtocol(AMP)
