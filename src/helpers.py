import re
from dataclasses import dataclass
from datetime import datetime
from math import isnan
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


class CoordinateParser:
    """read and parse coordinates input/output files."""

    def __init__(self, input_file: Path, output_file: Path):
        self.input_file = input_file
        self.output_file = output_file
        self.rectangle_failures: List[str] = []
        self.expected_points_failures: List[str] = []
        self.actual_points_failures: List[str] = []

    # compiled regex for rectangle parsing (class-level for efficiency)
    _RECTANGLE_REGEX = re.compile(
        r"^\s*\(\s*(?P<x1>[+\-]?\d+(?:\.\d+)?)\s*,\s*(?P<y1>[+\-]?\d+(?:\.\d+)?)\s*\)\s*,\s*"
        r"\(\s*(?P<x2>[+\-]?\d+(?:\.\d+)?)\s*,\s*(?P<y2>[+\-]?\d+(?:\.\d+)?)\s*\)\s*,\s*"
        r"\(\s*(?P<x3>[+\-]?\d+(?:\.\d+)?)\s*,\s*(?P<y3>[+\-]?\d+(?:\.\d+)?)\s*\)\s*,\s*"
        r"\(\s*(?P<x4>[+\-]?\d+(?:\.\d+)?)\s*,\s*(?P<y4>[+\-]?\d+(?:\.\d+)?)\s*\)\s*$"
    )

    def _parse_rectangle(self, data) -> List[Tuple[float, float]]:
        """parse coordinates after the Rectangle keyword"""

        if data is None:
            self.rectangle_failures.append("No 'Rectangle:' keyword found.")
            return []
        data_str = data.group(1).strip()

        if not data_str:
            self.rectangle_failures.append(
                "No coordinates found between Rectangle and Points keywords."
            )
            return []

        if "\n" in data_str:
            self.rectangle_failures.append(
                "Rectangle coordinates must be on a single line."
            )
            return []

        match = self._RECTANGLE_REGEX.match(data_str)
        if not match:
            self.rectangle_failures.append("Work area is not valid/quadrilateral")
            return []

        # extract all 4 coordinates in one pass
        try:
            points = [
                (float(match.group(f"x{i}")), float(match.group(f"y{i}")))
                for i in range(1, 5)
            ]
        except (ValueError, AttributeError) as e:
            self.rectangle_failures.append(
                f"Could not convert coordinates to float in rectangle data '{data_str}': {e}"
            )
            return []

        return points

    def _parse_points(
        self, data, is_expected: bool = True
    ) -> List[Tuple[float, float]]:
        """parse points from a raw string or regex match (for output file)"""

        # select the appropriate failures dictionary
        failures_dict = (
            self.expected_points_failures
            if is_expected
            else self.actual_points_failures
        )

        # handle both re.Match object and string
        if data is None or (isinstance(data, re.Match) and data is None):
            failures_dict.append("No 'Points:' keyword found.")
            return []
        if isinstance(data, re.Match):
            data = data.group(1).strip()
        elif isinstance(data, str):
            data = data.strip()
        else:
            failures_dict.append("Data cannot be parsed")
            return []

        # regex to match a single coordinate (x, y)
        single_coord_regex = re.compile(
            r"^\s*\(\s*(?P<x>[+\-]?\d+(?:\.\d+)?)\s*,\s*(?P<y>[+\-]?\d+(?:\.\d+)?)\s*\)\s*$"
        )

        points = []
        for line in data.split("\n"):
            line = line.strip()

            # skip empty lines
            if not line:
                continue

            # check for multiple coordinates on one line
            if line.count("(") != 1:
                failures_dict.append("Multiple coordinates on one line not allowed")
                continue

            single_match = single_coord_regex.match(line)
            if single_match:
                try:
                    x = float(single_match.group("x"))
                    y = float(single_match.group("y"))
                    points.append((x, y))
                except (ValueError, AttributeError) as e:
                    failures_dict.append(
                        f"Could not convert float: '{single_match.group(0)}' - {e}"
                    )
                    points.append((float("nan"), float("nan")))  # invalid entry marker
                    continue
            else:
                failures_dict.append(f"Invalid coordinate format: '{line}'")
                points.append((float("nan"), float("nan")))  # invalid entry marker
                continue

        return points

    def _parse_input(
        self, content: str
    ) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
        """reads the input file and returns workarea points and expected points"""

        workarea_points: List[Tuple[float, float]] = []
        expected_points: List[Tuple[float, float]] = []

        # extract workarea_points (between Rectangle and Points)
        rect_match = re.search(r"Rectangle:\s*([\s\S]*?)(?=Points:|\Z)", content)
        workarea_points = self._parse_rectangle(rect_match)

        # extract expected_points (after Points)
        # note: if the Points keyword is not found or invalid,
        # the coordinates will be considered part of the Rectangle section
        # which then fails the multiple line check in _parse_rectangle
        points_match = re.search(r"Points:\s*([\s\S]*)", content)
        expected_points = self._parse_points(points_match, is_expected=True)

        return workarea_points, expected_points

    def _parse_output(self, content: str) -> List[Tuple[float, float]]:
        """reads the actual visited points from the output file"""

        # no keywords, only points and potential errors/invalid entries
        return self._parse_points(content, is_expected=False)

    def get_parsed_data(
        self,
    ) -> Tuple[
        List[Tuple[float, float]], List[Tuple[float, float]], List[Tuple[float, float]]
    ]:
        """reads and parses all necessary data from both files"""

        rectangle_coords: List[Tuple[float, float]] = []
        expected_points: List[Tuple[float, float]] = []
        actual_points: List[Tuple[float, float]] = []

        try:
            with open(self.input_file, "r", encoding="utf-8") as f:
                input_content = f.read()
            rectangle_coords, expected_points = self._parse_input(input_content)
        except FileNotFoundError as e:
            self.rectangle_failures.append(f"File not found: {e.filename}")

        try:
            with open(self.output_file, "r", encoding="utf-8") as f:
                output_content = f.read()
            actual_points = self._parse_output(output_content)
        except FileNotFoundError as e:
            self.actual_points_failures.append(f"File not found: {e.filename}")

        return rectangle_coords, expected_points, actual_points

    def get_failures(self) -> Tuple[List[str], List[str], List[str]]:
        """returns 3 lists of failures: rectangle, expected points, and actual points"""

        return (
            self.rectangle_failures,
            self.expected_points_failures,
            self.actual_points_failures,
        )


class WorkArea:  # pylint: disable=too-few-public-methods
    """models the robot arm's work environment and expected path"""

    def __init__(
        self,
        rectangle_coords: List[Tuple[float, float]],
        expected_points: List[Tuple[float, float]],
    ):

        # determine the work area bounding box (x_min, y_min, x_max, y_max)
        x_coords = [p[0] for p in rectangle_coords]
        y_coords = [p[1] for p in rectangle_coords]
        self.x_min, self.x_max = min(x_coords), max(x_coords)
        self.y_min, self.y_max = min(y_coords), max(y_coords)

        self.bounding_box = (self.x_min, self.y_min, self.x_max, self.y_max)
        self.expected_sequence = expected_points

    def point_in_bounds(self, point: Tuple[float, float]) -> bool:
        """checks if a point is within the closed rectangle work area (including boundary)"""

        x, y = point
        x_min, y_min, x_max, y_max = self.bounding_box

        # assumes the rectangle is axis-aligned
        return (x_min <= x <= x_max) and (y_min <= y <= y_max)


class TracerSentinel:  # pylint: disable=too-few-public-methods
    """performs strict sequence and geometric validation"""

    def __init__(self, work_area: WorkArea, actual_points: List[Tuple[float, float]]):

        self.work_area = work_area
        self.actual_sequence = actual_points
        self.failures: List[str] = []

    def _check_geometric_validity(self):
        """all actual points must be within the work area bounds"""

        # check if expected points are within bounds
        for point in self.work_area.expected_sequence:
            if not self.work_area.point_in_bounds(point):
                self.failures.append(
                    f"Geometric FAIL: Expected point ({point}) is outside the closed work area."
                )

    def _check_sequence_sameness(self):
        """actual sequence must match expected sequence exactly"""

        expected = self.work_area.expected_sequence
        actual = self.actual_sequence

        if len(expected) != len(actual):
            self.failures.append(
                f"Sequence FAIL: Length mismatch. Expected {len(expected)} versus {len(actual)}"
            )
        elif expected != actual:
            self.failures.append(
                "Sequence FAIL: Sequence mismatch between expected and actual points."
            )

    def run_verification(self) -> List[str]:
        """runs checks on parsed data and returns list of failures"""

        self.failures = []
        self._check_geometric_validity()
        self._check_sequence_sameness()

        return self.failures


@dataclass
class ResultsBucket:
    """container for test results data"""

    expected_points: List[Tuple[float, float]]
    actual_points: List[Tuple[float, float]]
    rectangle_failures: List[str]
    expected_points_failures: List[str]
    actual_points_failures: List[str]
    verifier_failures: List[str]
    overall_status: str = "UNKNOWN"


class ResultsWriter:
    """handles writing test results to file"""

    def __init__(
        self, scenario_path: Path, rectangle_coords: List[Tuple[float, float]]
    ):
        """initialize the writer with a scenario path"""

        self.scenario_path = scenario_path
        self.rectangle_coords = rectangle_coords
        self.output_file = scenario_path / "test_results.txt"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.plot_file = scenario_path / f"test_results_{timestamp}.png"

    def write_results(  # pylint: disable=too-many-branches
        self,
        results: ResultsBucket,
    ) -> None:
        """write test results to test_results.txt in the scenario folder"""

        with open(self.output_file, "w", encoding="utf-8") as f:
            # overall status header
            f.write("=" * 70 + "\n")
            f.write(f"OVERALL TEST STATUS: {results.overall_status}\n")
            f.write("=" * 70 + "\n\n")

            # rectangle parsing failures if any
            if results.rectangle_failures:
                f.write("RECTANGLE PARSING FAILURES:\n")
                f.write("-" * 70 + "\n")
                for error_msg in sorted(results.rectangle_failures):
                    f.write(f"  {error_msg}\n")
                f.write("\n")

            # expected points parsing failures if any
            if results.expected_points_failures:
                f.write("EXPECTED POINTS PARSING FAILURES:\n")
                f.write("-" * 70 + "\n")
                for error_msg in sorted(results.expected_points_failures):
                    f.write(f"  {error_msg}\n")
                f.write("\n")

            # actual points parsing failures if any
            if results.actual_points_failures:
                f.write("ACTUAL POINTS PARSING FAILURES:\n")
                f.write("-" * 70 + "\n")
                for error_msg in sorted(results.actual_points_failures):
                    f.write(f"  {error_msg}\n")
                f.write("\n")

            # verifier failures if any
            if results.verifier_failures:
                f.write("VERIFICATION FAILURES:\n")
                f.write("-" * 70 + "\n")
                for failure_msg in results.verifier_failures:
                    f.write(f"  {failure_msg}\n")
                f.write("\n")

            # point-by-point comparison
            f.write("POINT-BY-POINT COMPARISON:\n")
            f.write("-" * 70 + "\n")
            f.write(
                f"{'Expected Points':<20} {'Actual Points':<20} {'Assessment':<10}\n"
            )
            f.write("-" * 55 + "\n")

            # determine the longest length so we can fill up missing entries with '-'
            max_len = (
                max(len(results.expected_points), len(results.actual_points))
                if results.expected_points or results.actual_points
                else 0
            )
            for i in range(max_len):
                expected = (
                    results.expected_points[i]
                    if i < len(results.expected_points)
                    else "-"
                )
                actual = (
                    results.actual_points[i] if i < len(results.actual_points) else "-"
                )

                # format points, converting NaN tuples to "INVALID"
                def format_point(point):
                    if point == "-":
                        return "-"
                    if isinstance(point, tuple) and len(point) == 2:
                        if isnan(point[0]) or isnan(point[1]):
                            return "INVALID"
                    return str(point)

                expected_str = format_point(expected)
                actual_str = format_point(actual)

                if expected == "-" or actual == "-":
                    status = "FAIL"
                elif (
                    isinstance(expected, tuple)
                    and isinstance(actual, tuple)
                    and (isnan(expected[0]) or isnan(actual[0]))
                ):
                    status = "FAIL"
                elif expected == actual:
                    status = "PASS"
                else:
                    status = "FAIL"

                f.write(f"{expected_str:<20} {actual_str:<20} {status:<10}\n")

    def _plot_points_and_assess(self, ax, expected_points, actual_points):
        """plot points and assess if pass or fail"""

        if expected_points:
            point_xs, point_ys = zip(*expected_points)
            ax.scatter(
                point_xs,
                point_ys,
                c="blue",
                s=50,
                marker="o",
                alpha=0.7,
                label="Expected Points",
            )

        if actual_points:
            point_xs, point_ys = zip(*actual_points)
            ax.scatter(
                point_xs,
                point_ys,
                c="pink",
                s=50,
                marker="o",
                alpha=0.7,
                label="Actual Points",
            )
        return "PASS" if expected_points == actual_points else "FAIL"

    def _configure_plot_appearance(self, ax, assessment):
        """configure plot formatting and legend"""

        ax.set_title("Work Area", fontsize=14, fontweight="bold")
        ax.set_xlabel("X coordinate")
        ax.set_ylabel("Y coordinate")
        ax.grid(True, alpha=0.3)
        ax.set_aspect("equal", "box")

        handles, _ = ax.get_legend_handles_labels()

        # set assessment entry with appropriate color
        assessment_color = (
            "green"
            if assessment == "PASS"
            else "red" if assessment == "FAIL" else "gray"
        )
        assessment_handle = Line2D(
            [0],
            [0],
            marker="",
            color="white",
            markerfacecolor=assessment_color,
            label=f"Assessment: {assessment}",
            markersize=0,
            linewidth=0,
        )
        handles.append(assessment_handle)

        # better legend formatting
        ax.legend(
            handles=handles,
            bbox_to_anchor=(1.05, 1),
            loc="upper left",
            frameon=True,
            fancybox=True,
            shadow=True,
            fontsize=10,
        )

    def save_plot(
        self,
        expected_points: List[Tuple[float, float]],
        actual_points: List[Tuple[float, float]],
    ) -> Path:
        """saves plot to PNG file"""

        fig, ax = plt.subplots(figsize=(10, 8))
        closed_coords = self.rectangle_coords + [self.rectangle_coords[0]]
        xs, ys = zip(*closed_coords)
        ax.plot(xs, ys, "r-", linewidth=2, label="Work Area")

        assessment = self._plot_points_and_assess(ax, expected_points, actual_points)
        self._configure_plot_appearance(ax, assessment)

        plt.savefig(self.plot_file, format="png", dpi=150, bbox_inches="tight")
        plt.close(fig)
        return self.plot_file
