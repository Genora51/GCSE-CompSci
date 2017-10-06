import mock_prerelease
import re
import pytest


@pytest.mark.parametrize("students, estimates", [
    (1, (580, 580.0)),  # Lowest case
    (7, (760, 108.57)),
    (10, (820, 82.0)),  # Check for freebie at 10, not 11
    (11, (850, 77.27)),
    (27, (1300, 48.15)),
    (45, (1780, 39.56))  # Highest case
])
def test_estimate(students, estimates):
    """
    Takes in a number of students, and an expected estimate,
    and compares this value to that produced by the `estimate`
    function.
    """
    # Get estimate
    total, average = mock_prerelease.estimate(students)
    # Round average to 2dp
    avg = round(average, 2)
    # Check correct total
    assert total == estimates[0], \
        ("Incorrect total ${} for estimating {} students: "
         "expected ${}.").format(total, students, estimates[0])
    # Check correct average
    assert avg == estimates[1], \
        ("Incorrect average ${} for estimating {} students: "
         "expected ${}").format(avg, students, estimates[1])


@pytest.mark.parametrize("string, validated", [
    ('hi', None),  # Incorrect data
    ('', None),  # Prescence data
    ('-1', None),  # Range data
    ('0', None),  # Edge case (too low)
    ('1', 1),  # Edge case (valid)
    ('2', 2),  # Normal data
    ('17', 17),
    ('45', 45),  # Edge case (valid)
    ('46', None)  # Edge case (too high)
])
def test_validate(string, validated):
    """
    Takes in a string and an expected result from validation,
    and checks whether the `validate` function returns the
    correct validated data (`None` for an invalid value,
    `int(string)` for a valid value).
    """
    # Run validation function
    validated_string = mock_prerelease.validate(string)
    # Check for valid data
    assert validated_string is validated, \
        "Incorrect validation {} of {!r}, expected {}.".format(
            validated_string, string, validated
        )


@pytest.mark.parametrize("names, has_paid, paid, unpaid", [
    (
        ['Adam', 'Beth', 'Charlie', 'Dave', 'Eve'],
        [False, True, True, False, False],
        ['Beth', 'Charlie'],
        ['Adam', 'Dave', 'Eve']
    )
])
def test_split_paid(names, has_paid, paid, unpaid):
    """
    Takes in a list of names, and whether each person has paid,
    then checks if the `split_paid` function correctly splits the
    people into 2 arrays of paid and unpaid students.
    """
    # Check for correct splitting
    assert mock_prerelease.split_paid(names, has_paid) == (paid, unpaid), \
        "Incorrect splitting of names."


@pytest.mark.parametrize("paid, unpaid, avg_est, costs", [
    (
        ['Beth', 'Charlie'],
        ['Adam', 'Dave', 'Eve'],
        108.57,
        (700, 217.14, -482.86)
    )
])
def test_cost_calculate(paid, unpaid, avg_est, costs):
    """
    Takes in a list of paid and unpaid students,
    with a previously calculated estimate for average cost,
    and checks that the total costs produced are correct.
    """
    # Runs calculation function to generate cost
    costs_to_check = mock_prerelease.calculate_cost(paid, unpaid, avg_est)
    # Checks for correct output
    assert costs_to_check == costs, \
        "Incorrect costs {} produced, expected {}".format(
            costs_to_check, costs
        )


@pytest.mark.parametrize("input_set, output_set", [
    (
        (
            "blsflh", "7a", "-7", "0", "7",  # Validation
            "Alice", "Y",  # Paid and unpaid students
            "Bob", "N",
            "Charlie", "y",
            "Dave", "Y",
            "Eve", "n",
            "Fred", "hello",
            ""  # Exit data entry
        ),
        (
            "760",  # Total estimated cost
            r"108\.57",  # Average estimated cost
            (
                r"(?<!un)paid", "Alice", "Dave",  # Paid students
                r"unpaid", "Bob", "Charlie", "Eve", "Fred"  # Unpaid students
            ),
            "730",  # Overall total cost
            r"217\.14",  # Overall amount paid
            r"512\.86",  # Overall profit/loss (in this case loss)
            "loss"  # Check for loss
        )
    )
])
def test_main(input_set, output_set, monkeypatch):
    """
    Checks that the `main` function calls other functions
    and uses them as expected, while providing opportunities
    for data input, and providing relevant outputs of computed data.
    """
    # New input function
    def inpts(*args, **kwargs):
        inpts.inpnum += 1
        return input_set[inpts.inpnum]
    inpts.inpnum = -1

    # New print function
    def prnt(*args, **kwargs):
        toprnt = " ".join(args)
        prnt.out = prnt.out + toprnt + '\n'
    prnt.out = ""
    # Assign new print/input functions
    monkeypatch.setitem(__builtins__, 'input', inpts)
    monkeypatch.setitem(__builtins__, 'print', prnt)
    # Run main function
    mock_prerelease.main()
    # Check that all required outputs are present
    for outputs_to_check in output_set:
        if isinstance(outputs_to_check, tuple):
            outputs_to_check = ".*".join(outputs_to_check)
        regex = re.compile(outputs_to_check, re.S + re.I)
        assert regex.search(prnt.out) is not None
