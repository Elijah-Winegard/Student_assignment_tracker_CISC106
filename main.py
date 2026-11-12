
from drafter import *
from dataclasses import dataclass
from datetime import datetime #from ChatGPT


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


# HOME PAGE
@route
def index(state: State) -> Page:
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

# SAVES THE NEW ASSIGNMENT
@route
def submit_assignment(state: State, assignment_name: str,
                      assignment_course: str,
                      assignment_due_date: str) -> Page:

    state.assignment_name = assignment_name
    state.assignment_course = assignment_course
    state.assignment_due_date = assignment_due_date

    if assignment_name != "" and assignment_course != "" and assignment_due_date != "":
        new_assignment = Assignment(
            assignment_name,
            assignment_course,
            assignment_due_date,
            False
        )

        state.assignments.append(new_assignment)

        # Clear the text boxes after saving.
        state.assignment_name = ""
        state.assignment_course = ""
        state.assignment_due_date = ""

        return all_assignments(state)

    else:
        return Page(state, [
            Header("Missing Information"),
            "Please fill in all three fields.",
            Button("Go Back", "add_assignment"),
            Button("Home", "index")
        ])



# DISPLAYS ALL ASSIGNMENTS
@route
def all_assignments(state: State) -> Page:
    content = [
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
                content.append(
                    Button(
                        "Mark Completed",
                        "mark_completed",
                        [Argument("assignment_index", index)]
                    )
                )

    content.append("\n")
    content.append(Button("Home", "index"))

    return Page(state, content)


# DISPLAYS INCOMPLETE ASSIGNMENTS
# coded with AI see AI conversations in Github
@route
def upcoming_assignments(state: State) -> Page:
    content = [
        Header("Upcoming Assignments")
    ]

    found_assignment = False

    upcoming = []

    for index in range(len(state.assignments)):
        assignment = state.assignments[index]

        if assignment.completed == False:
            upcoming.append((index, assignment))

    #Sorts the upcoming assignments by due date, putting the earlies due date first.
    #The lambda function takes each item in the list,
    #accesses the assignment's due_date, and converts the date from
    #MM/DD/YYYY into a format Python uses to compare dates."""
    # item represents one assignment in the upcoming list.
    # item[1] accesses the assignment, since item[0] stores its original index.
    # .due_date accesses the assignment's due date.
    # datetime.strptime() converts the date into a format Python understands.
    # sort() uses the dates to display the closest due date first.
    upcoming.sort(
        key=lambda item: datetime.strptime(item[1].due_date, "%m/%d/%Y")
    )

    for index, assignment in upcoming:
        found_assignment = True

        content.append("\nAssignment: " + assignment.name)
        content.append("Class: " + assignment.course)
        content.append("Due Date: " + assignment.due_date)

        content.append(
            Button(
                "Mark Completed",
                "mark_completed",
                [Argument("assignment_index", index)]
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
    content = [
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
    content = [
        Header("Filter Assignments by Class")
    ]

    courses = []

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
    state.filter_course = course

    content = [
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

    if assignment_index >= 0 and assignment_index < len(state.assignments):
        state.assignments[assignment_index].completed = True

    return all_assignments(state)


# START THE WEBSITE
start_server(State([], "", "", "", ""))

