"""Main test program for Sentinel"""

from pathlib import Path

from src.helpers import read_input, read_output, verify_system_behavior


# the scenario_data_path fixture provides the Path object to the data dir
def test_system_verification_scenarios(scenario_data_path: Path):
    """Test system using various scenarios."""

    # Define file paths based on the test scenario's directory
    input_file = scenario_data_path / "system_input_file.txt"
    output_file = scenario_data_path / "system_output_file.txt"
    scenario = scenario_data_path.name

    # Extract work area and expected/actual points
    workarea, expected_points = read_input(input_file)
    actual_points = read_output(output_file)

    # Verify system behavior
    test_status = verify_system_behavior(workarea, expected_points, actual_points)

    # Scenarios categorized by name as PASS/FAIL
    is_fail_case = "fail" in scenario.lower()

    if is_fail_case:
        assert (
            test_status == "FAIL"
        ), f"Scenario {scenario} failed: Expected FAIL but got PASS."
    else:
        assert (
            test_status == "PASS"
        ), f"Scenario {scenario} failed: Expected PASS but got FAIL."
