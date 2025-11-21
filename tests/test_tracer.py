"""Main test program for Sentinel"""

from pathlib import Path

from src.helpers import (
    CoordinateParser,
    ResultsWriter,
    ResultsBucket,
    TracerSentinel,
    WorkArea,
)


# conftest provides the scenario_data_path fixture
def test_system_verification_scenarios(
    scenario_data_path: Path,
):  # pylint: disable=too-many-locals
    """sequence run test each scenario"""

    scenario = scenario_data_path.name

    # parse input and output files and check for parsing failures
    parser = CoordinateParser(
        input_file=scenario_data_path / "system_input_file.txt",
        output_file=scenario_data_path / "system_output_file.txt",
    )
    rectangle_coords, expected_points, actual_points = parser.get_parsed_data()
    rectangle_failures, expected_points_failures, actual_points_failures = (
        parser.get_failures()
    )

    verifier_failures = []
    parsing_successful = not (
        rectangle_failures or expected_points_failures or actual_points_failures
    )

    # proceed only if parsing was successful
    if parsing_successful:
        # create work area based on input file
        work_area = WorkArea(rectangle_coords, expected_points)

        # verify that the actual points match expected within the work area
        verifier = TracerSentinel(work_area, actual_points)
        verifier_failures = verifier.run_verification()

    # calculate overall test status
    has_any_failures = not parsing_successful or bool(verifier_failures)
    overall_status = "FAIL" if has_any_failures else "PASS"

    # write test results to file
    results_writer = ResultsWriter(
        scenario_data_path, rectangle_coords if rectangle_coords else []
    )

    test_results = ResultsBucket(
        expected_points=expected_points,
        actual_points=actual_points,
        rectangle_failures=rectangle_failures,
        expected_points_failures=expected_points_failures,
        actual_points_failures=actual_points_failures,
        verifier_failures=verifier_failures,
        overall_status=overall_status,
    )
    results_writer.write_results(test_results)

    is_fail_case = "fail" in scenario.lower()
    if is_fail_case:
        # for fail scenarios, we expect failures
        assert has_any_failures, f"Scenario '{scenario}' expected to fail but passed."
    else:
        # for pass scenarios, we expect no failures
        assert (
            not has_any_failures
        ), f"Scenario '{scenario}' expected to pass but failed."

    # save png
    if parsing_successful:
        results_writer.save_plot(expected_points, actual_points)
