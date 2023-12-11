class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def north(self):
        return self + Point(0, -1)

    def south(self):
        return self + Point(0, 1)

    def east(self):
        return self + Point(1, 0)

    def west(self):
        return self + Point(-1, 0)

    def cardinal_neighbors(self):
        return {
            "N": self.north(),
            "S": self.south(),
            "E": self.east(),
            "W": self.west(),
        }

    def neighbor(self, direction: str):
        if direction == "N":
            return self.north()
        elif direction == "S":
            return self.south()
        elif direction == "E":
            return self.east()
        elif direction == "W":
            return self.west()

    def all_neighbors(self):
        return {
            Point(self.x, self.y - 1),
            Point(self.x, self.y + 1),
            Point(self.x - 1, self.y),
            Point(self.x + 1, self.y),
            Point(self.x - 1, self.y - 1),
            Point(self.x + 1, self.y - 1),
            Point(self.x - 1, self.y + 1),
            Point(self.x + 1, self.y + 1),
        }
