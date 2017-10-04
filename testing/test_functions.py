import mock_prerelease
import re
import pytest


@pytest.mark.parametrize("students, estimates", [
    (1, (580, 580.0)),
    (7, (760, 108.57)),
    (10, (820, 82.0)),
    (11, (850, 77.27)),
    (27, (1300, 48.15)),
    (45, (1780, 39.56))
])
def test_estimate(students, estimates):
    total, average = mock_prerelease.estimate(students)
    assert total == estimates[0]
    assert round(average, 2) == estimates[1]


@pytest.mark.parametrize("string, validated", [
    ('hi', None),
    ('', None),
    ('-1', None),
    ('0', None),
    ('1', 1),
    ('2', 2),
    ('17', 17),
    ('45', 45),
    ('46', None)
])
def test_validate(string, validated):
    assert mock_prerelease.validate(string) is validated


@pytest.mark.parametrize("names, has_paid, paid, unpaid", [
    (
        ['Adam', 'Beth', 'Charlie', 'Dave', 'Eve'],
        [False, True, True, False, False],
        ['Beth', 'Charlie'],
        ['Adam', 'Dave', 'Eve']
    )
])
def test_split_paid(names, has_paid, paid, unpaid):
    assert mock_prerelease.split_paid(names, has_paid) == (paid, unpaid)


def test_cost_calculate():
    paids = [
        ['Beth', 'Charlie']
    ]
    unpaids = [
        ['Adam', 'Dave', 'Eve']
    ]
    average_estimates = [
        108.57
    ]
    costs_list = [
        (700, 217.14, -482.86)
    ]
    for index in range(len(paids)):
        paid = paids[index]
        unpaid = unpaids[index]
        avg_est = average_estimates[index]
        costs = costs_list[index]
        assert mock_prerelease.calculate_cost(paid, unpaid, avg_est) == costs


def test_main(monkeypatch):
    inputs = [
        [
            "blsflh", "7a", "-7", "0", "7",
            "Alice", "Y",
            "Bob", "N",
            "Charlie", "y",
            "Dave", "Y",
            "Eve", "n",
            "Fred", "hello",
            ""
        ]
    ]

    outputs = [
        [
            ("760",),
            (r"108\.57",),
            (
                r"(?<!un)paid", "Alice", "Dave",
                r"unpaid", "Bob", "Charlie", "Eve", "Fred"
            ),
            ("730",),
            (r"217\.14",),
            (r"512\.86",),
            ("loss",)
        ]
    ]

    for test in range(len(inputs)):

        def inpts(*args, **kwargs):
            inpts.inpnum += 1
            return inputs[test][inpts.inpnum]
        inpts.inpnum = -1

        def prnt(*args, **kwargs):
            toprnt = " ".join(args)
            prnt.out = prnt.out + toprnt + '\n'
        prnt.out = ""
        # print('hi')
        monkeypatch.setitem(mock_prerelease.__builtins__, 'input', inpts)
        monkeypatch.setitem(mock_prerelease.__builtins__, 'print', prnt)
        mock_prerelease.main()

        for outputsets in outputs:
            for outputset in outputsets:
                if not isinstance(outputset, str):
                    outputset = ".*".join(outputset)
                regex = re.compile(outputset, re.S + re.I)
                assert regex.search(prnt.out) is not None

        # mock_prerelease.print = prnt
