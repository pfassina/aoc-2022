from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass
class Node:
    y: int
    x: int
    elevation: int
    neighbors: list[Node] = field(default_factory=list)

    @property
    def coord(self) -> tuple[int, int]:
        return self.y, self.x

    def add_neighbors(self, neighbors: list[Node]) -> None:
        self.neighbors += neighbors

    def __post_init__(self) -> None:
        self.end: bool = False

    def set_end(self) -> None:
        self.end = True

    def __repr__(self) -> str:
        return f"({self.y},{self.x})"


Graph = dict[tuple[int, int], Node]


@dataclass
class HeightMap:
    elevation: np.ndarray
    start: tuple[int, int]
    end: tuple[int, int]

    @property
    def shape(self) -> tuple[int, int]:
        return self.elevation.shape

    @property
    def height(self) -> int:
        return self.shape[0]

    @property
    def width(self) -> int:
        return self.shape[1]

    def print(self) -> None:
        print()
        print(self.start, "->", self.end, "\n")
        print(self.elevation, "\n")


def parse_char(char: str) -> int:
    char = "a" if char == "S" else char
    char = "z" if char == "E" else char
    return ord(char) - 97


def parse_input(input: str) -> HeightMap:
    char_lists = np.array([list(i) for i in input.splitlines()])
    sy, sx = [int(i) for i in np.where(char_lists == "S")]
    ey, ex = [int(i) for i in np.where(char_lists == "E")]

    height_map = np.vectorize(parse_char)(char_lists)

    return HeightMap(height_map, (sy, sx), (ey, ex))


def is_valid(node: Node, neighbor: Optional[Node]) -> bool:
    if not neighbor:
        return False
    if neighbor.elevation <= node.elevation:
        return True
    if neighbor.elevation - node.elevation > 1:
        return False
    return True


def create_graph(height_map: HeightMap) -> Graph:
    graph: dict[tuple[int, int], Node] = {}
    for y, x in np.ndindex(height_map.shape):
        graph[y, x] = Node(x=x, y=y, elevation=height_map.elevation[(y, x)])
        if (y, x) != height_map.end:
            continue
        graph[(y, x)].set_end()

    for node in graph.values():
        n = graph.get((node.y - 1, node.x))
        s = graph.get((node.y + 1, node.x))
        e = graph.get((node.y, node.x - 1))
        w = graph.get((node.y, node.x + 1))
        neighbors = [neighbor for neighbor in [n, s, e, w] if is_valid(node, neighbor)]
        node.add_neighbors(neighbors)  # type: ignore

    return graph


def shortest_path(
    graph: Graph, start: tuple[int, int], end: tuple[int, int]
) -> list[Node]:
    # Create a dictionary to store the shortest path to each node
    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    # Create a dictionary to store the predecessor of each node in the shortest path
    predecessors: dict[tuple[int, int], Optional[tuple[int, int]]] = {
        node: None for node in graph
    }

    # Create a priority queue to keep track of nodes to visit
    queue = [(0, start)]

    while queue:
        # Get the node with the smallest distance from the start node
        current_distance, current_node = heapq.heappop(queue)

        # Stop if we've reached the end node
        if current_node == end:
            break

        # Skip nodes we've already visited
        if current_distance > distances[current_node]:
            continue

        # Visit each neighbor of the current node
        for neighbor_node in graph[current_node].neighbors:
            neighbor = neighbor_node.coord
            # Calculate the total distance to the neighbor
            distance = current_distance + 1

            # Update the shortest distance if we've found a better path
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node

                # Add the neighbor to the priority queue
                heapq.heappush(queue, (distance, neighbor))

    # Construct the shortest path by working backwards from the end node
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = predecessors[current_node]
    path.reverse()

    return path


def find_starts(height_map: HeightMap) -> list[tuple[int, int]]:
    starts = np.where(height_map.elevation == 0)
    return [(y, x) for y, x in zip(starts[0], starts[1])]


def part_one(input: str) -> int:
    height_map = parse_input(input)
    height_map.print()

    graph = create_graph(height_map)
    path = shortest_path(graph, height_map.start, height_map.end)

    return len(path) - 1


def part_two(input: str) -> int:
    height_map = parse_input(input)
    height_map.print()

    graph = create_graph(height_map)

    paths = []
    potential_starts = find_starts(height_map)
    for start in potential_starts:
        path = shortest_path(graph, start, height_map.end)
        if len(path) == 1:
            continue
        paths.append(len(path) - 1)

    return sorted(paths)[0]


def main(p: int, s: bool) -> int:
    file_name = "sample" if s else "input"
    file_version = f"_{p}.txt"
    file_path = file_name + file_version
    with open(file_path) as file:
        input = file.read()

    if p == 1:
        return part_one(input)
    return part_two(input)


if __name__ == "__main__":
    result = main(p=2, s=False)
    print(result)
