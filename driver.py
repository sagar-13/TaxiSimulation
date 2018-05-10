from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type speed: int
        The speed of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, identifier, location, speed):
        """Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None

        >>> new_driver = Driver('Bobby Schmurda', Location(1,2), 10)
        >>> print(new_driver.id)
        Bobby Schmurda
        >>> print(new_driver.location)
        Location Row: 1, Column: 2
        >>> print(new_driver.speed)
        10
        """

        self.id = identifier
        self.location = location
        self.speed = int(speed)
        self.destination = None
        self.is_idle = True

    def __str__(self):
        """Return a string representation.

        @type self: Driver
        @rtype: str

        >>> new_driver = Driver('Steve Jobs', Location(1,2), 10)
        >>> print(new_driver)
        Driver: Steve Jobs
        """

        return "Driver: {0}".format(self.id)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool

        >>> new_driver1 = Driver('Bobby Schmurda', Location(1,2), 10)
        >>> new_driver2 = Driver('Bobby Schmurda', Location(1,2), 10)
        >>> new_driver3 = Driver('Barack Obama', Location(3,4), 10)
        >>> new_driver1 == new_driver2
        True
        >>> new_driver1 == new_driver3
        False
        """

        return self.id == other.id and self.location == other.location and self.speed == other.speed\
               and self.destination == other.destination and self.is_idle == other.is_idle

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int

        >>> new_driver = Driver('Donald Trump', Location(1,2), 2)
        >>> new_driver.get_travel_time(Location(3,4))
        2
        """

        return (manhattan_distance(self.location, destination) / self.speed).__round__()

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int

        >>> new_driver = Driver('Hilary Clinton', Location(1,2), 2)
        >>> print(new_driver.destination)
        None
        >>> new_driver.start_drive(Location(3,4))
        2
        >>> print(new_driver.destination)
        Location Row: 3, Column: 4
        """

        self.destination = location
        self.is_idle = False
        return self.get_travel_time(self.destination)

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None

        >>> new_driver = Driver('Stephen Harper', Location(1,2), 2)
        >>> new_driver.destination = Location(3,4)
        >>> new_driver.end_drive()
        >>> print(new_driver.location)
        Location Row: 3, Column: 4
        """

        self.location = self.destination

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int

        >>> new_driver = Driver('Norm Kelly', Location(1,2), 2)
        >>> new_rider = Rider('Drake', Location(3,4), Location(5,6), 2)
        >>> new_driver.location == new_rider.origin
        False
        >>> new_driver.start_ride(new_rider)
        2
        >>> new_driver.location == new_rider.origin
        True
        >>> new_driver.destination == new_rider.destination
        True
        """

        self.is_idle = False
        self.location = rider.origin
        self.destination = rider.destination
        return self.get_travel_time(self.destination)

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None

        >>> new_driver = Driver('Bill Gates', Location(1,2), 2)
        >>> new_driver.start_drive(Location(3,4))
        2
        >>> print(new_driver.destination)
        Location Row: 3, Column: 4
        >>> new_driver.is_idle
        False
        >>> new_driver.end_ride()
        >>> new_driver.location == new_driver.destination
        True
        >>> new_driver.is_idle
        True
        """

        self.location = self.destination
        self.is_idle = True
