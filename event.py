"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""

from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.
    This class is abstract; subclassesimplement do().


    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """

        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """

        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """

        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """

        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """

        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """

        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """

        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """

        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """

        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """

        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """

        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time, self.rider, driver))
        events.append(Cancellation(self.timestamp + self.rider.patience, self.rider))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str
        """

        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """

        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        # Notify the monitor about the request.

        # Request a rider from the dispatcher.
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.

        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.id, self.driver.location)

        events = []
        rider = dispatcher.request_rider(self.driver)

        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)
            events.append(Pickup(self.timestamp + travel_time, rider, self.driver))

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str
        """

        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):
    """A rider cancels a ride.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a Cancellation event.

        @type self: Cancellation
        @type rider: Rider
        @rtype: None
        """

        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Cancel the rider's ride.
        Notify the monitor of the cancellation
        If rider has not been picked up:
        Change rider's status from WAITING to CANCELLED. Remove the rider from the waiting riders.

        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: None
        """

        if self.rider.status != SATISFIED:
            self.rider.status = CANCELLED
            dispatcher.cancel_ride(self.rider)
            monitor.notify(self.timestamp, RIDER, CANCEL, self.rider.id, self.rider.origin)

    def __str__(self):
        """Return a string representation of this event.

        @type self: Cancellation
        @rtype: str
        """

        return "{0} -- {1}: Cancel request".format(self.timestamp, self.rider)

class Pickup(Event):
    """Rider is picked up by driver

    === Attributes ===
    @type rider: Rider
        The rider.
    @type: driver: Driver
        The driver.
    """

    def __init__(self, timestamp, rider, driver):
        """Initialize a Pickup event.

        @type self: Pickup
        @type rider: Rider
        @type: driver: Driver
        @rtype: None
        """

        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Pickup a rider
        If the rider is still waiting, this function sets the driver's location to the rider's location.
        The driver begins giving them a ride and the driver's destination becomes the rider's destination.
        At the same time, a dropoff event is scheduled for the time they will arrive at the rider's destination,
        and the rider becomes satisfied.

        If the rider has cancelled, a new event for the driver requesting a rider is scheduled to take place
        immediately, and the driver has no destination for the moment.
        It also notifies the monitor.

        @type self: Pickup
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: lst
        """

        events = []

        if self.rider.status == WAITING:
            self.rider.status = SATISFIED
            monitor.notify(self.timestamp, DRIVER, PICKUP, self.driver.id, self.rider.origin)
            monitor.notify(self.timestamp, RIDER, PICKUP, self.rider.id, self.rider.origin)
            travel_time = self.driver.start_ride(self.rider)
            events.append(Dropoff((self.timestamp + travel_time), self.driver, self.rider))

        else:
            self.driver.is_idle = True
            self.driver.destination = None
            events.append(DriverRequest(self.timestamp,self.driver))

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Pickup
        @rtype: str
        """

        return "{0} -- {1}: Pickup {2} ".format(self.timestamp, self.driver, self.rider)
       # return "Pickup: {0} -- Rider: {1}, Driver: {2}".format(self.timestamp, self.rider, self.driver)


class Dropoff(Event):
    """The rider is dropped off.

    === Attributes ===
    @type rider: Rider
        The rider.
    @type: driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver, rider):
        """Initialize a Dropoff event.

        @type self: Dropoff
        @type driver: Driver
        @type: rider: Rider
        @rtype: None
        """

        super().__init__(timestamp)
        self.driver = driver
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Dropoff the rider.

        A dropoff event sets the driver's location to the rider's destination, and leaves the rider satisfied.
        A new event for the driver requesting a rider is scheduled to take place immediately, and the driver
        has no destination for the moment. It also notifies the Monitor.

        @type self: Dropoff
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: None
        """

        monitor.notify(self.timestamp, DRIVER, DROPOFF, self.driver.id, self.driver.destination)
        events = []
        self.driver.end_ride()
        self.driver.destination = None
        events.append(DriverRequest(self.timestamp, self.driver))

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Dropoff
        @rtype: str
        """

        return "{0} -- {1}: Dropoff {2}".format(self.timestamp, self.driver.id, self.rider.id)

def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """

    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]

            if event_type == "DriverRequest":
                #Create DriverRequest event.
                driverObject = Driver(tokens[2], deserialize_location(tokens[3]), int(tokens[4]))
                event = DriverRequest(timestamp, driverObject)

            elif event_type == "RiderRequest":
                # Create a RiderRequest event.
                riderObject = Rider(tokens[2], deserialize_location(tokens[3]),
                                    deserialize_location(tokens[4]), int(tokens[5]))
                event = RiderRequest(timestamp, riderObject)

            events.append(event)
    return events
