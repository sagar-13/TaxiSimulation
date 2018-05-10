class Location:

    def __init__(self, row, column):
        """Initialize a location.

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None

        >>> new_location = Location(1,2)
        >>> print(new_location.row)
        1
        >>> print(new_location.column)
        2
        """

        self.row = int(row)
        self.column = int(column)

    def __str__(self):
        """Return a string representation.

        @rtype: str

        >>> new_location = Location(1,2)
        >>> print(new_location)
        Location Row: 1, Column: 2
        """

        return "Location Row: {0}, Column: {1}".format(self.row, self.column)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool

        >>> new_location1 = Location(1,2)
        >>> new_location2 = Location(3,4)
        >>> new_location3 = Location(1,2)
        >>> new_location1 == new_location2
        False
        >>> new_location1 == new_location3
        True
        """

        return self.row == other.row and self.column == other.column


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int

    >>> test_origin = Location(1,2)
    >>> test_destination = Location(3,4)
    >>> manhattan_distance(test_origin, test_destination)
    4
    """

    return abs((origin.row - destination.row)) + abs((origin.column - destination.column))


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location

    >>> print(deserialize_location('1,2'))
    Location Row: 1, Column: 2
    """

    row_column_lst = location_str.split(',')
    return Location(row_column_lst[0], row_column_lst[1])
