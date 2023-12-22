import networkx as nx

from ..utils import parse_data


class Block:
    def __init__(self, id, x1, y1, z1, x2, y2, z2):
        self.id = id
        self.cubes = {
            (x, y, z)
            for x in range(x1, x2 + 1)
            for y in range(y1, y2 + 1)
            for z in range(z1, z2 + 1)
        }
        self.falling = all(z > 1 for _, _, z in self.cubes)

    def __eq__(self, other):
        return self.cubes == other.cubes

    def drops(self, others):
        down = {(x, y, z - 1) for x, y, z in self.cubes}
        if any(z == 1 for x, y, z in self.cubes):
            self.falling = False
        elif below := [o for o in others if self != o and down & o.cubes]:
            self.falling = any(o.falling for o in below)
        else:
            self.cubes = down

        return self.falling

    def supports(self, others):
        up = {(x, y, z + 1) for x, y, z in self.cubes}
        return ((self.id, o.id) for o in others if self != o and o.cubes & up)


def solve_part1(data: str):
    input_data = parse_data(data, regex=r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")
    blocks = [Block(id, *map(int, coords)) for id, coords in enumerate(input_data)]

    falling = blocks.copy()
    while falling := [block for block in falling if block.drops(blocks)]:
        print(len(falling))

    G = nx.DiGraph()
    G.add_nodes_from(block.id for block in blocks)
    for block in blocks:
        G.add_edges_from(block.supports(blocks))

    return sum(1 for block in G if not [1 for nbr in G[block] if G.in_degree(nbr) == 1])


def solve_part2(data: str):
    input_data = parse_data(data)
    print(input_data)

    return None
