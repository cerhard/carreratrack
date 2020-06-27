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
            drivers.append(Driver(fuel=status.fuel[i], pit=status.pit[i]))
        expected_value = Status(start_light=7, mode=6, display=8, drivers=drivers)

        s = Skyhopper.construct_status(status)
        self.assertTrue(expected_value == s)
        self.assertTrue(False)
        
