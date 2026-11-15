
from drafter import *
from dataclasses import dataclass
from datetime import datetime
from typing import Any



set_website_title("Student Assignment Tracker")
set_site_information(
    author="Elijah Winegard",
    description="Tracks student assignments",
    sources="Thanks to the Drafter docs and my study group.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/Elijah-Winegard/Student_assignment_tracker_CISC106"]
)
hide_debug_information()
set_website_framed(False)


# Stores information about one assignment
@dataclass
class Assignment:
    name: str
    course: str
    due_date: str
    completed: bool


# Stores information shared between website pages
@dataclass
class State:
    assignments: list[Assignment]
    assignment_name: str
    assignment_course: str
    assignment_due_date: str
    filter_course: str


# CHECKS WHETHER A DATE IS VALID

def is_valid_due_date(due_date: str) -> bool:
    """Checks whether a date follows the MM/DD/YYYY format."""

    try:
        # Converts the date string into a datetime object.
        # This checks whether the entered date is a real calendar date.
        parsed_date = datetime.strptime(due_date, "%m/%d/%Y")

        # Converts the date back into a string.
        # Checks whether the original date matches MM/DD/YYYY exactly.
        return parsed_date.strftime("%m/%d/%Y") == due_date

    except ValueError:
        # Returns False if Python cannot convert the entered date.
        return False



# HOME PAGE
@route
def index(state: State) -> Page:
    """Displays the home page and navigation buttons."""

    return Page(state, [
        Header("Student Assignment Tracker"),
        "Welcome! Keep track of your school assignments.",
        "\n",
        Button("Add Assignment", "add_assignment"),
        Button("View All Assignments", "all_assignments"),
        Button("Upcoming Assignments", "upcoming_assignments"),
        Button("Completed Assignments", "completed_assignments"),
        Button("Filter by Class", "classes")
    ])


# PAGE FOR ADDING AN ASSIGNMENT
@route
def add_assignment(state: State) -> Page:
    """Displays the input fields for creating a new assignment."""

    return Page(state, [
        Header("Add a New Assignment"),
        "Assignment Name:",
        TextBox("assignment_name", state.assignment_name),
        "\nClass:",
        TextBox("assignment_course", state.assignment_course),
        "\nDue Date (MM/DD/YYYY):",
        TextBox("assignment_due_date", state.assignment_due_date),
        "\n",
        Button("Save Assignment", "submit_assignment"),
        Button("Home", "index")
    ])


# SAVES THE NEW ASSIGNMENT
@route
def submit_assignment(state: State, assignment_name: str,
                      assignment_course: str,
                      assignment_due_date: str) -> Page:
    """Checks the input and saves a new assignment."""

    state.assignment_name = assignment_name.strip()
    state.assignment_course = assignment_course.strip()
    state.assignment_due_date = assignment_due_date.strip()

    if (state.assignment_name == ""
            or state.assignment_course == ""
            or state.assignment_due_date == ""):

        return Page(state, [
            Header("Missing Information"),
            "Please fill in all three fields.",
            Button("Go Back", "add_assignment"),
            Button("Home", "index")
        ])

    if not is_valid_due_date(state.assignment_due_date):

        return Page(state, [
            Header("Invalid Date"),
            "Please enter a valid date using MM/DD/YYYY.",
            "Example: 11/25/2026",
            Button("Go Back", "add_assignment"),
            Button("Home", "index")
        ])

    new_assignment = Assignment(
        state.assignment_name,
        state.assignment_course,
        state.assignment_due_date,
        False
    )

    state.assignments.append(new_assignment)

    # Clear the text boxes after saving.
    state.assignment_name = ""
    state.assignment_course = ""
    state.assignment_due_date = ""

    return all_assignments(state)


# DISPLAYS ALL ASSIGNMENTS
@route
def all_assignments(state: State) -> Page:
    """Displays every assignment and its completion status."""

    content: list[Any] = [
        Header("All Assignments")
    ]

    if len(state.assignments) == 0:
        content.append("You have not added any assignments yet.")

    else:
        for index in range(len(state.assignments)):
            assignment = state.assignments[index]

            content.append("\nAssignment: " + assignment.name)
            content.append("Class: " + assignment.course)
            content.append("Due Date: " + assignment.due_date)

            if assignment.completed == True:
                content.append("Status: Completed")

            else:
                content.append("Status: Incomplete")

                # Creates a list of button arguments.
                # The first value identifies the argument name.
                # The second value stores the assignment's list position.
                button_arguments: list[tuple[
                    str,
                    str | int | float | bool | list[Any] | dict[Any, Any] | None
                ]] = [
                    ("assignment_index", index)
                ]

                # Passes the assignment position to mark_completed.
                content.append(
                    Button(
                        "Mark Completed",
                        "mark_completed",
                        button_arguments
                    )
                )

    content.append("\n")
    content.append(Button("Home", "index"))

    return Page(state, content)


# DISPLAYS INCOMPLETE ASSIGNMENTS
# Coded with AI. See AI conversations in GitHub.
@route
def upcoming_assignments(state: State) -> Page:
    """Displays incomplete assignments sorted by their due dates."""

    content: list[Any] = [
        Header("Upcoming Assignments")
    ]

    found_assignment = False

    upcoming: list[tuple[int, Assignment]] = []

    for index in range(len(state.assignments)):
        assignment = state.assignments[index]

        if assignment.completed == False:
            upcoming.append((index, assignment))

    # Sorts upcoming assignments by due date, putting the earliest first.
    # The lambda accesses each assignment's due date.
    # datetime.strptime converts the date into a format Python can compare.
    upcoming.sort(
        key=lambda item: datetime.strptime(
            item[1].due_date, "%m/%d/%Y"
        )
    )

    for index, assignment in upcoming:
        found_assignment = True

        content.append("\nAssignment: " + assignment.name)
        content.append("Class: " + assignment.course)
        content.append("Due Date: " + assignment.due_date)

        # Passes the assignment position to mark_completed.
        button_arguments: list[tuple[
            str,
            str | int | float | bool | list[Any] | dict[Any, Any] | None
        ]] = [
            ("assignment_index", index)
        ]

        content.append(
            Button(
                "Mark Completed",
                "mark_completed",
                button_arguments
            )
        )

    if found_assignment == False:
        content.append("You have no incomplete assignments.")

    content.append("\n")
    content.append(Button("Home", "index"))

    return Page(state, content)


# DISPLAYS COMPLETED ASSIGNMENTS
@route
def completed_assignments(state: State) -> Page:
    """Displays assignments marked as completed."""

    content: list[Any] = [
        Header("Completed Assignments")
    ]

    found_assignment = False

    for assignment in state.assignments:

        if assignment.completed == True:
            found_assignment = True

            content.append("\nAssignment: " + assignment.name)
            content.append("Class: " + assignment.course)
            content.append("Due Date: " + assignment.due_date)

    if found_assignment == False:
        content.append("You have not completed any assignments.")

    content.append("\n")
    content.append(Button("Home", "index"))

    return Page(state, content)


# PAGE FOR CHOOSING A CLASS
@route
def classes(state: State) -> Page:
    """Displays a list of classes for filtering assignments."""

    content: list[Any] = [
        Header("Filter Assignments by Class")
    ]

    courses: list[str] = []

    for assignment in state.assignments:
        if assignment.course not in courses:
            courses.append(assignment.course)

    # Sorts the class names in alphabetical order.
    courses.sort()

    if len(courses) == 0:
        content.append("Add an assignment before filtering by class.")

    else:
        selected_course = courses[0]

        if state.filter_course in courses:
            selected_course = state.filter_course

        content.append("Choose a class:")
        content.append(SelectBox("course", courses, selected_course))
        content.append(Button("View Class Assignments", "filter_by_class"))

    content.append("\n")
    content.append(Button("Home", "index"))

    return Page(state, content)


# DISPLAYS ASSIGNMENTS FROM THE SELECTED CLASS
@route
def filter_by_class(state: State, course: str) -> Page:
    """Displays assignments belonging to the selected class."""

    state.filter_course = course

    content: list[Any] = [
        Header("Assignments for " + state.filter_course)
    ]

    found_assignment = False

    for assignment in state.assignments:

        if assignment.course == state.filter_course:
            found_assignment = True

            content.append("\nAssignment: " + assignment.name)
            content.append("Due Date: " + assignment.due_date)

            if assignment.completed == True:
                content.append("Status: Completed")
            else:
                content.append("Status: Incomplete")

    if found_assignment == False:
        content.append("No assignments found for this class.")

    content.append("\n")
    content.append(Button("Back to Classes", "classes"))
    content.append(Button("Home", "index"))

    return Page(state, content)


# MARKS AN ASSIGNMENT AS COMPLETED
@route
def mark_completed(state: State, assignment_index: int) -> Page:
    """Marks the selected assignment as completed."""

    if assignment_index >= 0 and assignment_index < len(state.assignments):
        state.assignments[assignment_index].completed = True

    return all_assignments(state)


# UNIT TESTS

def test_is_valid_due_date():
    """Tests valid and invalid assignment due dates."""

    assert_equal(is_valid_due_date("11/20/2026"), True)
    assert_equal(is_valid_due_date("02/15/2026"), True)
    assert_equal(is_valid_due_date("15/40/2026"), False)
    assert_equal(is_valid_due_date("November 20, 2026"), False)
    assert_equal(is_valid_due_date("11/20/26"), False)


def test_index():
    """Tests that the home page returns a Page."""

    state = State([], "", "", "", "")
    assert_equal(isinstance(index(state), Page), True)


def test_add_assignment():
    """Tests that the add assignment page returns a Page."""

    state = State([], "", "", "", "")
    assert_equal(isinstance(add_assignment(state), Page), True)


def test_submit_assignment():
    """Tests adding a new assignment."""

    state = State([], "", "", "", "")

    submit_assignment(
        state, "Math Homework", "Math", "11/20/2026"
    )

    assert_equal(len(state.assignments), 1)
    assert_equal(state.assignments[0].name, "Math Homework")
    assert_equal(state.assignments[0].course, "Math")
    assert_equal(state.assignments[0].completed, False)
    assert_equal(state.assignment_name, "")


def test_submit_invalid_assignment():
    """Tests that an invalid date does not save an assignment."""

    state = State([], "", "", "", "")

    submit_assignment(
        state, "Math Homework", "Math", "15/40/2026"
    )

    assert_equal(len(state.assignments), 0)


def test_all_assignments():
    """Tests that the all assignments page returns a Page."""

    state = State([], "", "", "", "")
    assert_equal(isinstance(all_assignments(state), Page), True)


def test_upcoming_assignments():
    """Tests that the upcoming assignments page returns a Page."""

    state = State([], "", "", "", "")
    assert_equal(isinstance(upcoming_assignments(state), Page), True)


def test_completed_assignments():
    """Tests that the completed assignments page returns a Page."""

    state = State([], "", "", "", "")
    assert_equal(isinstance(completed_assignments(state), Page), True)


def test_classes():
    """Tests that the classes page returns a Page."""

    state = State([], "", "", "", "")
    assert_equal(isinstance(classes(state), Page), True)


def test_filter_by_class():
    """Tests saving the selected class."""

    state = State([], "", "", "", "")

    filter_by_class(state, "Math")

    assert_equal(state.filter_course, "Math")


def test_mark_completed():
    """Tests marking an assignment as completed."""

    assignment = Assignment(
        "Math Homework", "Math", "11/20/2026", False
    )

    state = State([assignment], "", "", "", "")

    mark_completed(state, 0)

    assert_equal(state.assignments[0].completed, True)


def test_invalid_assignment_index():
    """Tests that an invalid index does not change assignments."""

    assignment = Assignment(
        "Math Homework", "Math", "11/20/2026", False
    )

    state = State([assignment], "", "", "", "")

    mark_completed(state, 10)

    assert_equal(state.assignments[0].completed, False)


def test_assignment_sorting():
    """Tests sorting assignments by their due dates."""

    assignments = [
        Assignment("History", "History", "11/25/2026", False),
        Assignment("Math", "Math", "11/15/2026", False),
        Assignment("Science", "Science", "11/20/2026", False)
    ]

    upcoming = []

    for index in range(len(assignments)):
        if assignments[index].completed == False:
            upcoming.append((index, assignments[index]))

    upcoming.sort(
        key=lambda item: datetime.strptime(
            item[1].due_date, "%m/%d/%Y"
        )
    )

    assert_equal(upcoming[0][1].name, "Math")
    assert_equal(upcoming[1][1].name, "Science")
    assert_equal(upcoming[2][1].name, "History")


# RUN UNIT TESTS
# The website starts after the tests pass.
if __name__ == "__main__":
    test_is_valid_due_date()
    test_index()
    test_add_assignment()
    test_submit_assignment()
    test_submit_invalid_assignment()
    test_all_assignments()
    test_upcoming_assignments()
    test_completed_assignments()
    test_classes()
    test_filter_by_class()
    test_mark_completed()
    test_invalid_assignment_index()
    test_assignment_sorting()

    start_server(State([], "", "", "", ""))
