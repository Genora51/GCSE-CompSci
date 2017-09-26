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


def test_validate():
    validation_checks = {
        'hi': None,
        '': None,
        '-1': None,
        '0': None,
        '1': 1,
        '2': 2,
        '17': 17,
        '45': 45,
        '46': None
    }

    for string, validated in validation_checks.items():
        assert mock_prerelease.validate(string) == validated


def test_split_paid():
    names_lists = [
        ['Adam', 'Beth', 'Charlie', 'Dave', 'Eve']
    ]
    has_paids = [
        [False, True, True, False, False]
    ]
    paids = [
        ['Beth', 'Charlie']
    ]
    unpaids = [
        ['Adam', 'Dave', 'Eve']
    ]
    for index in range(len(names_lists)):
        names = names_lists[index]
        has_paid = has_paids[index]
        assert mock_prerelease.split_paid(names, has_paid) == (paids[index],
                                                               unpaids[index])
