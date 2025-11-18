"""Helper functions for reading files and verifying system behavior."""

import os
import re
from pathlib import Path
from typing import List, Tuple


def parse_points(data: str) -> List[Tuple[float, float]]:
    """Parses coordinate points from a given string data."""

    # regex to find valid (x, y), covers negatives and decimals
    point_regex = re.compile(
        r"\(\s*(?P<x>[+\-]?\d+(?:\.\d+)?)\s*,\s*(?P<y>[+\-]?\d+(?:\.\d+)?)\s*\)"
    )

    points = []
    for line in data.strip().split("\n"):
        line = line.strip()

        # skip empty lines only
        if not line:
            continue

        # find all valid patterns based on regex
        matches = point_regex.finditer(line)
        match_list = list(matches)
        assert len(match_list) > 0, f"Invalid coordinate format: '{line}'"

        # convert each match to float tuple
        for match in match_list:
            try:
                x = float(match.group("x"))
                y = float(match.group("y"))
                points.append((x, y))
            except (ValueError, AttributeError) as e:
                raise AssertionError(
                    f"Could not convert float: '{match.group(0)}'"
                ) from e

    return points


def read_input(
    filepath: Path,
) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
    """Reads the input file and returns workarea points and expected points."""

    workarea_points = []
    expected_points = []

    assert os.path.exists(filepath), f"Error: Input file '{filepath}' not found."
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # extract workarea_points (between Rectangle and Points)
    rect_match = re.search(r"Rectangle\s*([\s\S]*?)(?=Points|\Z)", content)
    assert (
        rect_match is not None
    ), "Failed to find 'Rectangle' keyword in the input file."
    rect_section = rect_match.group(1).strip()
    assert (
        len(rect_section) > 0
    ), "No coordinates found between Rectangle and Points keywords."
    workarea_points = parse_points(rect_section)
    assert len(workarea_points) == 4, (
        f"Work area is not quadrilateral. "
        f"Found {len(workarea_points)} points, expected 4."
    )

    # extract expected_points (after Points)
    # note: if the Points keyword is not found,
    # the coordinates will be considered part of the Rectangle section
    # which then fails the quadrilateral check above
    points_match = re.search(r"Points\s*([\s\S]*)", content)
    assert (
        points_match is not None
    ), "Failed to find 'Points' keyword in the input file."

    expected_points = parse_points(points_match.group(1).strip())

    return workarea_points, expected_points


def read_output(filepath: Path) -> List[Tuple[float, float]]:
    """Reads the actual visited points from the output file."""

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Output file '{filepath}' not found.")
        return []

    # no keywords, only points and potential errors/invalid entries
    return parse_points(content)


def point_in_rectangle(
    point: Tuple[float, float],
    rect: Tuple[float, float, float, float],
) -> bool:
    """Checks if (x, y) is within (x_min, y_min, x_max, y_max) inclusive."""

    x, y = point
    x_min, y_min, x_max, y_max = rect

    # TO INSERT: configure so that it considers non-axis aligned rectangles
    return (x_min <= x <= x_max) and (y_min <= y <= y_max)


def verify_system_behavior(
    workarea: List[Tuple[float, float]],
    expected_points: List[Tuple[float, float]],
    actual_points: List[Tuple[float, float]],
):
    """Verifies if actual points match expected points within the workarea."""

    test_status = "PASS"
    if actual_points != expected_points:
        test_status = "FAIL"

    # TO INSERT: Insert logic here to know if the points are within the rectangle inclusive
    print(workarea)

    return test_status


# TO INSERT: make a function to dump results in test_results.txt
