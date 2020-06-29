import unittest

from carreralib import ControlUnit
from skyhopper import Skyhopper
from skyhopper import Driver
from skyhopper import Status

class SkyhopperTest(unittest.TestCase):
    
    def test_status_conversion(self):
        status = ControlUnit.Status(fuel=(15, 15, 15, 15, 15, 15, 0, 0), start=7, mode=6, pit=(False, False, False, False, False, False, False, False), display=8)
        drivers=[]
        for i in range(len(status.fuel)):
            drivers.append(Driver(fuel=status.fuel[i], pit=status.pit[i], id=i+1))
        expected_value = Status(timestamp=0, start_light=7, mode=6, display=8, drivers=drivers)

        skyh = Skyhopper(None, None)
        s = skyh.construct_status(status)

        self.assertTrue(expected_value.start_light == s.start_light)
        self.assertTrue(expected_value.mode == s.mode)
        self.assertTrue(expected_value.display == s.display)
        self.assertTrue(expected_value.drivers == s.drivers)
        
