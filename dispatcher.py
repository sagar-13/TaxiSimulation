from driver import Driver
from rider import Rider
from location import Location
from container import Queue


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @type waiting_riders
        @type availalbe_drivers
        @rtype: None
        """

        self._available_drivers = []
        self._waiting_riders = Queue()

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str
        """

        return "Dispatcher:\n   waiting_riders {0}, \n  availalbe_drivers {1}"\
            .format(self._waiting_riders, self._available_drivers)

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.
        If there are available drivers, return the one that can reach the driver fastest


        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None
        """

        if len(self._available_drivers) == 0:
            self._waiting_riders.add(rider)
            return None

        DriverTimes = []
        for driver in self._available_drivers:
            if driver.is_idle:
                DriverTimes.append(driver.get_travel_time(rider.origin))
        shortestTime = min(DriverTimes)

        for driver in self._available_drivers:
            if driver.get_travel_time(rider.origin) == shortestTime:
                return driver

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.
        Return None if no riders are available, otherwise return the longest waiting rider.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None
        """

        if not driver in self._available_drivers:
            self._available_drivers.append(driver)

        if self._waiting_riders.is_empty():
            return None

        # The longest waiting rider if the first element of self.waiting_riders
        return self._waiting_riders.remove()

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None

        >>> John = Dispatcher()
        >>> Bobby = Rider('Bobby', Location(1,2), Location(3,4), 10)
        >>> John._waiting_riders.items = [Bobby]
        >>> John.cancel_ride(Bobby)
        >>> print(John._waiting_riders.items)
        []

        """

        if rider in self._waiting_riders.items:
            self._waiting_riders.items.remove(rider)

