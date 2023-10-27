import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

import tqdm


class Input(Enum):
    PART_ONE = auto()
    PART_TWO = auto()


@dataclass
class Beacon:
    x: int
    y: int

    def __eq__(self, __o: object) -> bool:
        assert isinstance(__o, Beacon)
        return self.x == __o.x and self.y == __o.y


@dataclass
class Sensor:
    x: int
    y: int
    beacon: Beacon

    @property
    def beacon_distance(self) -> int:
        return abs(self.x - self.beacon.x) + abs(self.y - self.beacon.y)


def input_path(input: Input, sample: bool) -> str:
    file_path = {
        Input.PART_ONE: {False: "input_1.txt", True: "sample_1.txt"},
        Input.PART_TWO: {False: "input_2.txt", True: "sample_2.txt"},
    }
    return file_path[input][sample]


def get_input(input: Input, sample: bool) -> list[str]:
    with open(input_path(input, sample), "r") as file:
        return [l.strip() for l in file.readlines()]


def get_sensor(line: str) -> Sensor:
    sensor_str, beacon_str = line.split(":")
    sx_str, sy_str = sensor_str.split(",")
    sx = int(sx_str.split("=")[1])
    sy = int(sy_str.split("=")[1])

    bx_str, by_str = beacon_str.split(",")
    bx = int(bx_str.split("=")[1])
    by = int(by_str.split("=")[1])

    return Sensor(sx, sy, Beacon(bx, by))


def in_reach(row: int, sensor: Sensor) -> bool:
    distance = abs(sensor.y - row)
    return distance <= sensor.beacon_distance


def sensor_presence(
    row: int, sensor: Sensor, min_coord: int, max_coord: int
) -> list[int]:
    x = sensor.x
    distance = abs(row - sensor.y)
    cells = sensor.beacon_distance - distance
    start = max(x - cells, min_coord)
    finish = min(x + cells + 1, max_coord + 1)

    return [i for i in range(start, finish)]


def get_row(
    row: int, sensors: list[Sensor], min_coord: int, max_coord: int
) -> set[int]:
    sensors_in_reach = [s for s in sensors if in_reach(row, s)]
    cells = set()
    for s in sensors_in_reach:
        presence = sensor_presence(row, s, min_coord, max_coord)
        if len(presence) == max_coord:
            return set(presence)
        for c in presence:
            cells.add(c)
    return cells


def get_objects_in_row(row: int, sensors: list[Sensor]) -> set[int]:
    objects_in_row = set()
    for s in sensors:
        if s.y == row:
            objects_in_row.add(s.x)
        if s.beacon.y == row:
            objects_in_row.add(s.beacon.x)
    return objects_in_row


def get_row_range(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged_ranges = [sorted_ranges[0]]

    for current_range in sorted_ranges[1:]:
        previous_range = merged_ranges[-1]

        if current_range[0] <= previous_range[1]:
            merged_ranges[-1] = (
                previous_range[0],
                max(previous_range[1], current_range[1]),
            )

        else:
            merged_ranges.append(current_range)

    return merged_ranges


def part_one(row: int, sample: bool) -> int:
    input_lines = get_input(input=Input.PART_ONE, sample=sample)
    sensors = [get_sensor(l) for l in input_lines]
    cells = get_row(row, sensors, -sys.maxsize, sys.maxsize)
    objects = get_objects_in_row(row, sensors)
    return len(cells - objects)


def part_two(sample: bool, max_coord: int) -> int:
    input_lines = get_input(input=Input.PART_TWO, sample=sample)
    sensors = [get_sensor(l) for l in input_lines]
    for row in tqdm.tqdm(range(max_coord + 1)):
        sensor_ranges = []
        sensors_in_reach = [s for s in sensors if in_reach(row, s)]
        for s in sensors_in_reach:
            distance = abs(row - s.y)
            spread = s.beacon_distance - distance
            min_x = max(s.x - spread, 0)
            max_x = min(s.x + spread, max_coord)
            sensor_ranges.append((min_x, max_x))
        row_range = get_row_range(sensor_ranges)
        if row_range != [(0, max_coord)]:
            return (row_range[0][1] + 1) * 4000000 + row

    return -1


def main():
    # solution = part_one(row=2000000, sample=False)
    solution = part_two(sample=True, max_coord=20)
    print(solution)  # 11756174628223


if __name__ == "__main__":
    main()
