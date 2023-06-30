from math import isclose
from PyCompGeomAlgorithms.core import Point
from PyCompGeomAlgorithms.graham import GrahamStepsTable, GrahamStepsTableRow
from AlgoGrade.graham import GrahamGrader, GrahamTask


points = [
    Point(2, 8),
    Point(5, 6),
    Point(7, 8),
    Point(8, 11),
    Point(7, 5),
    Point(10, 7),
    Point(11, 5),
    Point(8, 2),
    Point(1, 3),
    Point(5, 2),
]
task = GrahamTask(points)


def test_graham_grader_all_correct():
    centroid = Point(4.6667, 7.3333)
    ordered = [
        Point(8, 2),
        Point(7, 5),
        Point(11, 5),
        Point(10, 7),
        Point(7, 8),
        Point(8, 11),
        Point(2, 8),
        Point(1, 3),
        Point(5, 2),
        Point(5, 6)
    ]
    origin = Point(8, 2)
    steps_table = GrahamStepsTable(ordered)
    steps_table.extend([
        GrahamStepsTableRow((ordered[0], ordered[1], ordered[2]), False),
        GrahamStepsTableRow((ordered[0], ordered[2], ordered[3]), True),
        GrahamStepsTableRow((ordered[2], ordered[3], ordered[4]), True),
        GrahamStepsTableRow((ordered[3], ordered[4], ordered[5]), False),
        GrahamStepsTableRow((ordered[2], ordered[3], ordered[5]), False),
        GrahamStepsTableRow((ordered[0], ordered[2], ordered[5]), True),
        GrahamStepsTableRow((ordered[2], ordered[5], ordered[6]), True),
        GrahamStepsTableRow((ordered[5], ordered[6], ordered[7]), True),
        GrahamStepsTableRow((ordered[6], ordered[7], ordered[8]), True),
        GrahamStepsTableRow((ordered[7], ordered[8], ordered[9]), True),
        GrahamStepsTableRow((ordered[8], ordered[9], ordered[0]), False),
        GrahamStepsTableRow((ordered[7], ordered[8], ordered[0]), True)
    ])
    triples = [row.point_triple for row in steps_table]
    are_angles_less_than_pi = [row.is_angle_less_than_pi for row in steps_table]

    answers = [
        centroid,
        ordered,
        origin,
        triples,
        are_angles_less_than_pi,
        steps_table,
        steps_table,
        steps_table
    ]
    correct_answers = task.correct_answers

    total_grade, answer_grades = GrahamGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2)


def test_graham_grader_incorrect_centroid():
    correct_answers = task.correct_answers
    answers = correct_answers[:]
    answers[0] = Point(100, 100)

    total_grade, answer_grades = GrahamGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 1.75)


def test_graham_grader_incorrect_ordered_points():
    correct_answers = task.correct_answers
    answers = correct_answers[:]
    answers[1] = [
        Point(2000, 2000),
        Point(5000, 5000),
        Point(11, 5),
        Point(10, 7),
        Point(7, 8),
        Point(8, 11),
        Point(2, 8),
        Point(3000, 3000),
        Point(5, 2),
        Point(5, 6)
    ]

    total_grade, answer_grades = GrahamGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 1.75)


def test_graham_grader_incorrect_origin():
    correct_answers = task.correct_answers
    answers = correct_answers[:]
    answers[2] = Point(100, 100)

    total_grade, answer_grades = GrahamGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 1.75)


def test_graham_grader_incorrect_triples():
    correct_answers = task.correct_answers
    answers = correct_answers[:]
    ordered = answers[1]
    answers[3] = [
        (ordered[0], ordered[0], ordered[0]),
        (ordered[0], ordered[0], ordered[0]),
        (ordered[2], ordered[3], ordered[4]),
        (ordered[3], ordered[4], ordered[5]),
        (ordered[2], ordered[3], ordered[5]),
        (ordered[0], ordered[2], ordered[5]),
        (ordered[2], ordered[5], ordered[6]),
        (ordered[5], ordered[6], ordered[7]),
        (ordered[6], ordered[7], ordered[8]),
        (ordered[7], ordered[8], ordered[9]),
        (ordered[8], ordered[9], ordered[0]),
        (ordered[7], ordered[8], ordered[0])
    ]

    total_grade, answer_grades = GrahamGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 1.85)


def test_graham_grader_incorrect_are_angles_less_than_pi():
    correct_answers = task.correct_answers
    answers = correct_answers[:]
    answers[4] = [False for _ in answers[4]]

    total_grade, answer_grades = GrahamGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 1.85)


def test_graham_grader_incorrect_rows_with_angles_less_than_pi():
    correct_answers = task.correct_answers
    answers = correct_answers[:]
    ordered = answers[1]
    incorrect_point = Point(1000, 1000)

    answers[5][7] = GrahamStepsTableRow((ordered[5], ordered[6], incorrect_point), True)
    answers[5][8] = GrahamStepsTableRow((ordered[6], ordered[7], incorrect_point), True)
    
    total_grade, answer_grades = GrahamGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 1.75)


def test_graham_grader_incorrect_rows_with_angles_not_less_than_pi_single():
    correct_answers = task.correct_answers
    answers = correct_answers[:]
    ordered = answers[1]
    incorrect_point = Point(1000, 1000)

    answers[5][1] = GrahamStepsTableRow((ordered[0], ordered[2], incorrect_point), True)
    
    total_grade, answer_grades = GrahamGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 1.45) # also triggers "rows with angles < pi" grading


def test_graham_grader_incorrect_rows_with_angles_not_less_than_pi_repeated():
    correct_answers = task.correct_answers
    answers = correct_answers[:]
    incorrect_point = Point(1000, 1000)

    answers[5][1] = GrahamStepsTableRow((incorrect_point, incorrect_point, incorrect_point), True)
    answers[5][5] = GrahamStepsTableRow((incorrect_point, incorrect_point, incorrect_point), True)
    
    total_grade, answer_grades = GrahamGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 1.15) # also triggers "rows with angles < pi" grading


def test_graham_grader_incorrect_finalization():
    correct_answers = task.correct_answers
    answers = correct_answers[:]
    ordered = answers[1]
    answers[6][7] = GrahamStepsTableRow((ordered[5], ordered[0], ordered[7]), True)

    total_grade, answer_grades = GrahamGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 1.5) # also triggers "rows with angles <pi" grading
