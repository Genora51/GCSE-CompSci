# Global Constant Storage
COACH_COST = 550
ENTRY_COST = 30

# Other Constants
FREEBIE_NUM = 10
MAX_STUDENTS = 45


def estimate(student_count):
    """Estimates the cost of a trip, given the number of students."""

    # Account for freebies
    student_count_f = student_count - (student_count // FREEBIE_NUM)
    # Cost of entry
    cost = student_count_f * ENTRY_COST
    # Add coach cost
    cost += COACH_COST
    # Average cost
    average_cost = round(cost / student_count, 2)
    # Return values
    return cost, average_cost


def validate(count_str):
    """Validates and interprets input string, returns None if invalid."""

    # Is this a valid number?
    try:
        count = int(count_str)
    except ValueError:
        return None
    # Is this number within the legal bounds?
    if 1 <= count <= MAX_STUDENTS:
        return count
    else:
        return None


def split_paid(names, has_paid):
    """Splits a list of students into 'paid' and 'unpaid'."""

    # Define final lists
    paid = []
    unpaid = []
    # Add students to lists
    for student in range(len(names)):
        if has_paid[student]:
            paid.append(names[student])
        else:
            unpaid.append(names[student])
    # Return split lists
    return paid, unpaid


def calculate_cost(paid, unpaid, average_estimate):
    """Works out final costs."""

    # Total number of students
    total_students = len(paid) + len(unpaid)
    # Total cost of trip
    total_cost, _ = estimate(total_students)
    # Amount collected from paid students
    money_collected = len(paid) * average_estimate
    # Total Profit
    total_profit = money_collected - total_cost
    # Return Values
    return total_cost, money_collected, total_profit


if __name__ == '__main__':
    print('TASK 1')
    print('-'*6)
    # Validate number of estimated students
    est_stu = None
    while est_stu is None:
        est_stu_str = input("How many students expected? ")
        est_stu = validate(est_stu_str)
    # Calculate estimates
    total_estimate, avg_estimate = estimate(est_stu)
    print('Estimated cost = ${0}'.format(total_estimate))
    print('Estimated cost per student = ${0}'.format(avg_estimate))

    print('TASK 2')
    print('-'*6)
    # Declare arrays
    names = []
    has_paid = []
    # Repeat up to the max number of times
    for student in range(MAX_STUDENTS):
        # Get name
        student_name = input('Name (ENTER to stop)? ')
        # If empty, then all names have been entered, so break
        if student_name is '':
            break
        # Add name to array
        names.append(student_name)
        # Has the student paid? Input and convert to boolean
        has_student_paid = input('Has the student paid (Y/n)? ') is 'Y'
        # Add to array
        has_paid.append(has_student_paid)
    # Split into paid and unpaid arrays based on paid/unpaid
    paid_students, unpaid_students = split_paid(names, has_paid)
    print('PAID STUDENTS:')
    for student in paid_students:
        print(student)
    print('UNPAID STUDENTS:')
    for student in unpaid_students:
        print(student)

    print('TASK 3')
    print('-'*6)
    # Calculate overall cost, money collected, and profit
    # using arrays and estimate
    (
        final_cost,
        money_collected,
        overall_profit
    ) = calculate_cost(paid_students, unpaid_students, avg_estimate)
    # Print costs and money collected
    print('Overall Cost = ${0}'.format(final_cost))
    print('Total amount collected = ${0}'.format(money_collected))
    # Has a profit or loss been made, or has the school broken even?
    if overall_profit > 0:
        # Profit
        profit_loss = 'made a profit of ${0}'.format(overall_profit)
    elif overall_profit < 0:
        # Loss
        profit_loss = 'made a loss of ${0}'.format(-overall_profit)
    else:
        # Even
        profit_loss = 'broken even'

    print('The school has {0}.'.format(profit_loss))
