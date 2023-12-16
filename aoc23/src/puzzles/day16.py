from ..utils import parse_data


class Beam:
    def __init__(self, location, direction):
        self.initial = location, direction
        self.location = location
        self.direction = direction
        self.path = set()

    @property
    def orientation(self):
        return self.location, self.direction

    def interact(self, tile):
        match tile, self.direction:
            case ".", _:
                return None
            case "\\", d:
                mirror = {"N": "W", "W": "N", "S": "E", "E": "S"}
                self.direction = mirror[d]
                return None
            case "/", d:
                mirror = {"N": "E", "E": "N", "S": "W", "W": "S"}
                self.direction = mirror[d]
                return None
            case "|", d if d in "NS":
                return None
            case "|", d if d in "EW":
                self.direction = "N"
                return Beam(self.location, "S")
            case "-", d if d in "EW":
                return None
            case "-", d if d in "NS":
                self.direction = "E"
                return Beam(self.location, "W")

    def step(self):
        if self.direction == "N":
            self.location = self.location[0], self.location[1] - 1
        elif self.direction == "S":
            self.location = self.location[0], self.location[1] + 1
        elif self.direction == "E":
            self.location = self.location[0] + 1, self.location[1]
        elif self.direction == "W":
            self.location = self.location[0] - 1, self.location[1]


def energize(initial_beam: Beam, tiles: dict) -> int:
    beams, energized, origins = list(), set(), set()

    def add_beam(beam: Beam):
        if beam.initial not in origins:
            beams.append(beam)
            origins.add(beam.initial)

    add_beam(initial_beam)
    while beams and (current := beams.pop(0)):
        while current.location in tiles and current.orientation not in current.path:
            current.path.add(current.orientation)
            energized.add(current.location)
            if new_beam := current.interact(tiles[current.location]):
                add_beam(new_beam)

            current.step()

    return len(energized)


def solve_part1(data: str):
    input_data = parse_data(data)
    tiles = {(x, y): c for y, row in enumerate(input_data) for x, c in enumerate(row)}

    energize(Beam((0, 0), "W"), tiles)


def solve_part2(data: str):
    input_data = parse_data(data)
    tiles = {(x, y): c for y, row in enumerate(input_data) for x, c in enumerate(row)}
    exterior = {
        Beam((x, y), "E" if not x else "S" if not y else "W" if x > y else "N")
        for x, y in tiles
        if x in (0, len(input_data[0]) - 1) or y in (0, len(input_data) - 1)
    }

    return max(energize(beam, tiles) for beam in exterior)
