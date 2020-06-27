import json

from carreralib import ControlUnit
from .driver import Driver
from .status import Status

class Skyhopper(object):
    def run():
        last = None
        while True:
            try:
                data = self.cu.request()
                # prevent counting duplicate laps
                if data == last:
                    continue
                elif isinstance(data, ControlUnit.Status):
                    self.handle_status(data)
                elif isinstance(data, ControlUnit.Timer):
                    self.handle_timer(data)
                else:
                    logging.warn('Unknown data from CU: ' + data)
                last = data
            except select.error as e:
                pass
            except IOError as e:
                if e.errno != errno.EINTR:
                    raise

    def named_tuple_to_json(data):
        return json.dumps(data._asdict())

    def construct_status(data):
        # Status(fuel=(15, 15, 15, 15, 15, 15, 0, 0), start=7, mode=6, pit=(False, False, False, False, False, False, False, False), display=8)
        mode = data.mode
        start_light = data.start
        display = data.display
        drivers = []
        for fuel, pit in zip(data.fuel, data.pit):
            drivers.append(Driver(fuel=fuel, pit=pit))
        return Status(start_light=start_light,display = display,mode = mode,drivers = drivers)

    def handle_status(data):
        status = construct_status(data)
        send_to_rmq(status)

    def handle_timer(data):
        pass

