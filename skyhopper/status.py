from collections import namedtuple

class Status(namedtuple("Status", "start_light mode display drivers")):
        """Response type returned if no timer events are pending.

        This is a :class:`collections.namedtuple` subclass with the
        following read-only attributes:

        +-----------------+-------+-------------------------------------------+
        | Attribute       | Index | Value                                     |
        +=================+=======+===========================================+
        | :attr:`start`   | 0     | Start light indicator (0..9)              |
        +-----------------+-------+-------------------------------------------+
        | :attr:`mode`    | 1     | 4-bit mode bit mask                       |
        +-----------------+-------+-------------------------------------------+
        | :attr:`display` | 2     | Number of drivers to display (6 or 8)     |
        +-----------------+-------+-------------------------------------------+
        | :attr:`drivers` | 3     | Array of all :class:`skyhopper.driver`    |
        +-----------------+-------+-------------------------------------------+
        """
