from collections import namedtuple

import calendar
import contextlib
import json
import pika
import time

from carreralib import ControlUnit

EXCHANGE_NAME = 'skyhopper'

class Status(namedtuple("Status", "timestamp start_light mode display drivers")):
        """Response type returned if no timer events are pending.

        This is a :class:`collections.namedtuple` subclass with the
        following read-only attributes:

        +-----------------+-------+-------------------------------------------+
        | Attribute       | Index | Value                                     |
        +=================+=======+===========================================+
        | :attr:`timestamp`   | 0     | Start light indicator (0..9)              |
        +---------------------+-------+-------------------------------------------+
        | :attr:`start`       | 1     | Start light indicator (0..9)              |
        +---------------------+-------+-------------------------------------------+
        | :attr:`mode`        | 2     | 4-bit mode bit mask                       |
        +---------------------+-------+-------------------------------------------+
        | :attr:`display`     | 3     | Number of drivers to display (6 or 8)     |
        +---------------------+-------+-------------------------------------------+
        | :attr:`drivers`     | 4     | Array of all :class:`skyhopper.driver`    |
        +---------------------+-------+-------------------------------------------+
        """

class Driver(namedtuple('Driver', 'fuel pit id')):
        """
        This is a :class:`collections.namedtuple` subclass with the
        following read-only attributes:

        +-----------------+-------+-------------------------------------------+
        | Attribute       | Index | Value                                     |
        +=================+=======+===========================================+
        | :attr:`fuel`    | 0     | Fuel level (0..15)                        |
        +-----------------+-------+-------------------------------------------+
        | :attr:`pit`     | 1     | Pit lane bit mask (Boolean)               |
        +-----------------+-------+-------------------------------------------+
        | :attr:`id`      | 2     | Pit lane bit mask (Boolean)               |
        +-----------------+-------+-------------------------------------------+
        """

class Timer(namedtuple('Timer', 'timestamp_epoch timer_value driver sector')):
        """
        This is a :class:`collections.namedtuple` subclass with the
        following read-only attributes:

        +-----------------+-------+-----------------------------------------------------------+
        | Attribute       | Index | Value                                                     |
        +=================+=======+===========================================================+
        | :attr:`timestamp_epoch`    | 0     | The time in which the message was constructed  |
        +-----------------+----------+--------------------------------------------------------+
        | :attr:`timer_value`        | 1     | Timer this event represents (lap time)         |
        +-----------------+----------+--------------------------------------------------------+
        | :attr:`driver`             | 2     | Driver number (1-indexed)                      |
        +-----------------+----------+--------------------------------------------------------+
        | :attr:`sector`             | 2     | Sector                                         |
        +-----------------+----------+--------------------------------------------------------+
        """

class Skyhopper(object):
    def __init__(self, cu, rmq_channel):
        self.cu = cu
        self.channel = rmq_channel

    def run(self):
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
            except Exception as e:
                continue

    # TODO - Status only!
    def status_to_json(self, data):
        d = dict()
        # timestamp start_light mode display drivers
        d['timestamp'] = data.timestamp
        d['start_light'] = data.start_light
        d['mode'] = data.mode
        d['display'] = data.display
        d['drivers'] = []
        for driver in data.drivers:
            d['drivers'].append(driver._asdict())
        return json.dumps(d)

    def construct_status(self, data):
        # Status(fuel=(15, 15, 15, 15, 15, 15, 0, 0), start=7, mode=6, pit=(False, False, False, False, False, False, False, False), display=8)
        mode = data.mode
        start_light = data.start
        display = data.display
        drivers = []
        for fuel, pit, id in zip(data.fuel, data.pit, range(0,len(data.fuel))):
            drivers.append(Driver(fuel=fuel, pit=pit, id=id+1))
        timestamp = calendar.timegm(time.gmtime())
        return Status(timestamp=timestamp, start_light=start_light,display = display,mode = mode,drivers = drivers)

    def handle_status(self, data):
        status = self.construct_status(data)
        routing_key = 'track.event.status'
        self.channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=routing_key, body=self.status_to_json(status))

    def construct_timer(self, data):
        # Timer(address=0, timestamp=59493, sector=1)
        driver = data.address + 1  # 0 indexed
        timestamp_ms = data.timestamp
        sector = data.sector
        timestamp_epoch = calendar.timegm(time.gmtime())
        return Timer(timestamp_epoch = timestamp_epoch, driver=driver, timer_value = timestamp_ms, sector = sector)

    def timer_to_json(self, data):
        return json.dumps(data.__asdict())

    def handle_timer(self, data):
        timer = self.construct_timer(data)
        routing_key = 'track.event.timer'
        self.channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=routing_key, body=self.timer_to_json(timer))
        pass

if __name__ == "__main__":

    with pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq')) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')

        # TODO - debugging
        channel.queue_declare('foobar')
        channel.queue_bind(exchange=EXCHANGE_NAME, queue='foobar', routing_key='track.event.status')

        with contextlib.closing(ControlUnit('/dev/ttyUSB0', timeout=1.0)) as cu:
            while True:
                try:
                    print('CU version %s' % cu.version())
                    s = Skyhopper(cu, channel)
                    s.run()
                except Exception as e:
                    continue




