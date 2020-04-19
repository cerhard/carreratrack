import logging

from . import connection
from . import ControlUnit
from . import protocol
from .ITrack import ITrack

logger = logging.getLogger(__name__)

class Track(ITrack):

    class Word():
        """Various constants defining location of words to write when setting values"""

        SPEED = 0
        """Word to write if setting a car's speed value."""

        BRAKE = 1
        """Word to write if setting a car's brake value."""

        FUEL = 2
        """Word to write if setting a car's fuel value."""

        POSITION_TOWER = 6
        """Word to write if setting the position tower."""

        HIGH_NIBBLE_POSITION_TOWER = 17
        """Word to write when changing high nibble on the position tower."""

        LOW_NIBBLE_POSITION_TOWER = 18
        """Word to write when changing low nibble on the position tower."""

    def __init__(self, device, **kwargs):
        if isinstance(device, connection.Connection):
            self.__connection = device
        else:
            logger.debug('Connecting to %s', device)
            self.__connection = connection.open(device, **kwargs)
            logger.debug('Connection established')

    def close(self):
        self.__connection.close()

    def reset(self):
        """Reset the CU timer."""
        return self.send(ITrack.Request.RESET)
    
    def clearpostower(self):
        self.setword(Track.Word.POSITION_TOWER, 0, 9)

    def send(self, buf, maxlength=None):
        self.__connection.send(buf)
        return self.__nextMessage(buf, maxlength)

    def __nextMessage(self, buf, maxlength):
        while True:
            res = self.__connection.recv(maxlength)
            if res.startswith(buf[0:1]):
                break
            else:
                logger.warn('Received unexpected message %r', res)

        if res.startswith(b'?:'):
            # recent CU versions report two extra unknown bytes with '?:'
            try:
                parts = protocol.unpack('2x8YYYBYC', res)
            except protocol.ChecksumError:
                parts = protocol.unpack('2x8YYYBYxxC', res)
            fuel, (start, mode, pitmask, display) = parts[:8], parts[8:]
            pit = tuple(pitmask & (1 << n) != 0 for n in range(8))
            status = ControlUnit.Status(fuel, start, mode, pit, display)
            logger.debug("Status from track: {}".format(status))
            return status
        elif res.startswith(b'?'):
            address, timestamp, sector = protocol.unpack('xYIYC', res)
            timer = ControlUnit.Timer(address - 1, timestamp, sector)
            logger.debug("Timer from track: {}".format(timer))
            return timer

        logger.debug("Unknown from track: {}".format(res))
        return res

    def setlap(self, value):
        high_nibble_value = value >> 4
        low_nibble_value  = value & 0xf
        self.setword(Track.Word.HIGH_NIBBLE_POSITION_TOWER, 7, high_nibble_value)
        self.setword(Track.Word.LOW_NIBBLE_POSITION_TOWER, 7, low_nibble_value)

    def setbrake(self, address, value):
        self.setword(Track.Word.BRAKE, address, value, repeat=2)
    
    def setfuel(self, address, value):
        self.setword(Track.Word.FUEL, address, value, repeat=2)
    
    def setSpeed(self, address, value):
        self.setword(Track.Word.SPEED, address, value, repeat=2)
    
    def setPos(self, address, value):
        self.setword(Track.Word.POSITION_TOWER, address, value)

    def setword(self, word, address, value, repeat=1):
        if word < 0 or word > 31:
            raise ValueError('Command word out of range')
        if repeat < 1 or repeat > 15:
            raise ValueError('Repeat count out of range')
        
        buf = protocol.pack('cBYYC', ITrack.Request.WORD_WRITE, word | address << 5, value, repeat)
        return self.send(buf)

    def version(self):
        return protocol.unpack('x4sC', self.send(ITrack.Request.VERSION))[0]



