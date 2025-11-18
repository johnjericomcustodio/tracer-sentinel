from pathlib import Path

import pytest

# base directory for all test scenario data
TEST_SCENARIOS_DIR = Path(__file__).parent.parent / "data" / "scenarios"


def get_test_scenarios():
    """Discovers all test case directories in the data/scenarios folder"""
    scenarios = []
    # use glob to find all directories
    for p in sorted(TEST_SCENARIOS_DIR.glob("*")):
        if p.is_dir():
            # the scenario name is the directory name
            scenario_name = p.name
            # scenario data is the absolute path to the directory
            scenarios.append(pytest.param(p, id=scenario_name))

    if not scenarios:
        raise FileNotFoundError(f"No test scenarios found in {TEST_SCENARIOS_DIR}")

    return scenarios


@pytest.fixture(scope="session", params=get_test_scenarios())
def scenario_data_path(request):
    """Fixture that yields path to scenario directory"""
    return request.param
