from __future__ import absolute_import, division, unicode_literals

import logging
from collections import namedtuple

from . import connection
from . import protocol
from . import ITrack

logger = logging.getLogger(__name__)


class ControlUnit(object):
    """Interface to a Carrera Digital 124/132 Control Unit."""

    class Status(namedtuple('Status', 'fuel start mode pit display')):
        """Response type returned if no timer events are pending.

        This is a :class:`collections.namedtuple` subclass with the
        following read-only attributes:

        +-----------------+-------+-------------------------------------------+
        | Attribute       | Index | Value                                     |
        +=================+=======+===========================================+
        | :attr:`fuel`    | 0     | Eight-item list of fuel levels (0..15)    |
        +-----------------+-------+-------------------------------------------+
        | :attr:`start`   | 1     | Start light indicator (0..9)              |
        +-----------------+-------+-------------------------------------------+
        | :attr:`mode`    | 2     | 4-bit mode bit mask                       |
        +-----------------+-------+-------------------------------------------+
        | :attr:`pit`     | 3     | 8-bit pit lane bit mask                   |
        +-----------------+-------+-------------------------------------------+
        | :attr:`display` | 4     | Number of drivers to display (6 or 8)     |
        +-----------------+-------+-------------------------------------------+

        """

        __slots__ = ()

        FUEL_MODE = 0x1
        """Mode bit mask indicating fuel mode is enabled."""

        REAL_MODE = 0x2
        """Mode bit mask indicating real fuel mode is enabled."""

        PIT_LANE_MODE = 0x4
        """Mode bit mask indicating a pit lane adapter is connected."""

        LAP_COUNTER_MODE = 0x8
        """Mode bit mask indicating a lap counter is connected."""

    class Timer(namedtuple('Timer', 'address timestamp sector')):
        """Response type for timer events.

        This is a :class:`collections.namedtuple` subclass with the
        following read-only attributes:

        +-------------------+-------+-----------------------------------------+
        | Attribute         | Index | Value                                   |
        +===================+=======+=========================================+
        | :attr:`address`   | 0     | Controller address (0..7)               |
        +-------------------+-------+-----------------------------------------+
        | :attr:`timestamp` | 1     | 32-bit time stamp in milleseconds       |
        +-------------------+-------+-----------------------------------------+
        | :attr:`sector`    | 2     | Sector (1 for start/finish, 2 or 3 for  |
        |                   |       | times reported by Check Lanes)          |
        +-------------------+-------+-----------------------------------------+

        """
        pass

    class Button(object):
        PACE_CAR = b'T1'
        """Request for emulating the Control Unit's PACE CAR/ESC key."""

        START = b'T2'
        """Request for emulating the Control Unit's START/ENTER key."""

        SPEED = b'T5'
        """Request for emulating the Control Unit's SPEED key."""

        BRAKE = b'T6'
        """Request for emulating the Control Unit's BRAKE key."""

        FUEL = b'T7'
        """Request for emulating the Control Unit's FUEL key."""

        CODE = b'T8'
        """Request for emulating the Control Unit's CODE key."""

    def __init__(self, track):
        self.__track = track
    
    def close(self):
        """Close the connection to the CU."""
        self.__track.close()

    def clrpos(self):
        """Clear/reset the Position Tower display."""
        self.__track.clearpostower()

    def ignore(self, mask):
        """Ignore the controllers represented by bitmask `mask`."""
        self.request(protocol.pack('cBC', b':', mask))

    def request(self, buf=ITrack.ITrack.Request.STATUS, maxlength=None):
        """Send a message to the CU and wait for a response.

        The returned value will be an instance of either
        :class:`ControlUnit.Timer` or :class:`ControlUnit.Status`,
        depending on whether any timer events are pending.
        """
        logger.debug('Sending message %r', buf)
        message = self.__track.send(buf, maxlength)
        logger.debug('Received response ' + message)        

    def reset(self):
        """Reset the CU timer."""
        self.__track.reset()

    def setbrake(self, address, value):
        """Set the brake value for controller `address`."""
        self.__validateAddress(address)
        self.__validateStandardValue(value)
        logger.debug("Setting brake on car {}(0 addressed) to {}".format(address, value))
        self.__track.setbrake(address, value)

    def setfuel(self, address, value):
        """Set the fuel value for controller `address`."""
        self.__validateAddress(address)
        self.__validateStandardValue(value)
        logger.debug("Setting fuel on car {}(0 addressed) to {}".format(address, value))
        self.__track.setfuel(address, value)

    def setlap(self, value):
        """Set the current lap displayed by the Position Tower."""
        if value < 0 or value > 255:
            raise ValueError('Lap value out of range')
        logger.debug("Setting lap to {}".format(value))
        self.__track.setlap(value)

    def setpos(self, address, position):
        """Set the controller's position displayed by the Position Tower."""
        self.__validateAddress(address)
        if position < 1 or position > 8:
            raise ValueError('Position out of range')
        logger.debug("Setting position of car {}(0 addressed) to {}".format(address, position))
        self.__track.setPos(address, position)

    def setspeed(self, address, value):
        """Set the speed value for controller address."""
        self.__validateAddress(address)
        self.__validateStandardValue(value)
        logger.debug("Setting speed of car {}(0 addressed) to {}".format(address, value))
        self.__track.setSpeed(address, value)

    def start(self):
        """Initiate the CU start sequence."""
        self.request(ControlUnit.Button.START)

    def version(self):
        """Retrieve the CU version."""
        return self.__track.version()

    def __validateAddress(self, address):
        if address < 0 or address > 7:
            raise ValueError('Address out of range')
    
    def __validateStandardValue(self, value):
        if value < 0 or value > 15:
            raise ValueError('Value out of range')
