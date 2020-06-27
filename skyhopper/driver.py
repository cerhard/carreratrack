from collections import namedtuple

class Driver(namedtuple('Driver', 'fuel pit')):
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
        """
