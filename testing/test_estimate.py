import mock_prerelease


def test_estimate():
    estimate_checks = {
        1: (580, 580.0),
        7: (760, 108.57),
        10: (820, 82.0),
        11: (850, 77.27),
        27: (1300, 48.15),
        45: (1780, 39.56)
    }

    for students, estimates in estimate_checks.items():
        assert mock_prerelease.estimate(students) == estimates
