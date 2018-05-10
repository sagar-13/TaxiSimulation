from location import Location

"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """A rider within the simulation.

    === Attributes ===
    @type id: str
        A unique identifier for the rider.
    @type origin: Location
        The starting location of the rider.
    @type destination: Location
        The location the rider needs to reach.
    @type status: str
        The current status of the rider, reprsented by the Constants above.
    """

    def __init__(self, name, origin, destination, patience):
        """Initialize a Rider.

        @type: self: Rider
        @type: name: str
        @type: origin: Location
        @type: destination: Location
        @type: patience: int
        @rtype: None

        >>> newRider = Rider('Bob the Builder', Location(1,2), Location(3,4), 11)
        >>> print(newRider.id)
        Bob the Builder
        >>> print(newRider.origin)
        Location Row: 1, Column: 2
        >>> print(newRider.origin)
        Location Row: 1, Column: 2
        >>> print(newRider.destination)
        Location Row: 3, Column: 4
        >>> print(newRider.patience)
        11
        """

        self.id = name
        self.origin = origin
        self.destination = destination
        self.status = WAITING
        self.patience = patience

    def __str__(self):
        """Return a string representation.

        @type: self: Rider
        @rtype: str

        >>> newRider = Rider('Martin', Location(1,2), Location(3,4), 11)
        >>> print(newRider)
        Rider: Martin

        We are choosing to display only the name, similar
        to the sample output on the discussion board
        """

        return "Rider: {}".format(self.id)
