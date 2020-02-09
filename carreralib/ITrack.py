from interfaces import Interface

class ITrack(Interface):

    class Request:
        RESET = b'=10'

        WORD_WRITE = b'J'

        VERSION = b'J'

        STATUS = b'?'


    def close(self):
        """Close any connections this thing might have"""
        pass

    def reset(self):
        """Reset the CU timer."""
        pass
    
    def clearpostower(self):
        """Clear everything from the Position Tower"""
        pass

    def send(self, buf, maxlength=None):
        """Send a message to the track"""
        pass

    def setlap(self, value):
        """Set the lap on the position tower"""
        pass

    def setbrake(self, address, value):
        """For a given car (0 indexed) set the brake value.
           Address:     The address of the car, 
                            0-5 (car)
                            6 (autonomous car)
                            7 pace car
           Value:       The value to set the brake to; [0-15]
        """
        pass
    
    def setfuel(self, address, value):
        """For a given car (0 indexed) set the fuel tank value.
           Address:     The address of the car, 
                            0-5 (car)
                            6 (autonomous car)
                            7 pace car
           Value:       The value to set the fuel tank to; [0-15]
        """
        pass
    
    def setSpeed(self, address, value):
        """For a given car (0 indexed) set the speed value.
           Address:     The address of the car, 
                            0-5 (car)
                            6 (autonomous car)
                            7 pace car
           Value:       The value to set the speed to; [0-15]
        """
        pass
    
    def setPos(self, address, value):
        pass

    def version(self):
        """Return the version of the software on the track"""
        pass
