from copy import deepcopy
from math import isclose
from algogears.core import Point
from algogears.graham import GrahamStepsTable, GrahamStepsTableRow
from AlgoGrade.graham import GrahamGrader, GrahamTask, GrahamAnswers
from AlgoGrade.core import Scoring


points = [
    Point.new(2, 8),
    Point.new(5, 6),
    Point.new(7, 8),
    Point.new(8, 11),
    Point.new(7, 5),
    Point.new(10, 7),
    Point.new(11, 5),
    Point.new(8, 2),
    Point.new(1, 3),
    Point.new(5, 2),
]
givens = (points,)
task_class = GrahamTask
scorings = [
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.15, fine=0.15),
    Scoring(max_grade=0.15, fine=0.15),
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.6, fine=0.3, repeat_fine=0.6),
    Scoring(max_grade=0.1, fine=0.25)
]
correct_algogears_answers = task_class.solve_as_algogears_list(givens)
correct_answers_wrapper = task_class.solve_as_answers_wrapper(givens)


def test_graham_grader_all_correct():
    centroid = Point.new(4.6667, 7.3333)
    ordered = [
        Point.new(8, 2),
        Point.new(7, 5),
        Point.new(11, 5),
        Point.new(10, 7),
        Point.new(7, 8),
        Point.new(8, 11),
        Point.new(2, 8),
        Point.new(1, 3),
        Point.new(5, 2),
        Point.new(5, 6)
    ]
    origin = Point.new(8, 2)
    steps_table = GrahamStepsTable(ordered_points=ordered)
    steps_table.extend([
        GrahamStepsTableRow(point_triple=(ordered[0], ordered[1], ordered[2]), is_angle_less_than_pi=False),
        GrahamStepsTableRow(point_triple=(ordered[0], ordered[2], ordered[3]), is_angle_less_than_pi=True),
        GrahamStepsTableRow(point_triple=(ordered[2], ordered[3], ordered[4]), is_angle_less_than_pi=True),
        GrahamStepsTableRow(point_triple=(ordered[3], ordered[4], ordered[5]), is_angle_less_than_pi=False),
        GrahamStepsTableRow(point_triple=(ordered[2], ordered[3], ordered[5]), is_angle_less_than_pi=False),
        GrahamStepsTableRow(point_triple=(ordered[0], ordered[2], ordered[5]), is_angle_less_than_pi=True),
        GrahamStepsTableRow(point_triple=(ordered[2], ordered[5], ordered[6]), is_angle_less_than_pi=True),
        GrahamStepsTableRow(point_triple=(ordered[5], ordered[6], ordered[7]), is_angle_less_than_pi=True),
        GrahamStepsTableRow(point_triple=(ordered[6], ordered[7], ordered[8]), is_angle_less_than_pi=True),
        GrahamStepsTableRow(point_triple=(ordered[7], ordered[8], ordered[9]), is_angle_less_than_pi=True),
        GrahamStepsTableRow(point_triple=(ordered[8], ordered[9], ordered[0]), is_angle_less_than_pi=False),
        GrahamStepsTableRow(point_triple=(ordered[7], ordered[8], ordered[0]), is_angle_less_than_pi=True)
    ])
    triples = [row.point_triple for row in steps_table.rows]
    are_angles_less_than_pi = [row.is_angle_less_than_pi for row in steps_table.rows]

    algogears_answers = [
        centroid,
        ordered,
        origin,
        triples,
        are_angles_less_than_pi,
        steps_table,
        steps_table,
        steps_table
    ]
    answers_wrapper = GrahamAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2)

    total_grade, answer_grades = GrahamGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2)


def test_graham_grader_incorrect_centroid():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[0] = Point.new(100, 100)
    answers_wrapper = GrahamAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.75)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.75)

    total_grade, answer_grades = GrahamGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.75)


def test_graham_grader_incorrect_ordered_points():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[1] = [
        Point.new(2000, 2000),
        Point.new(5000, 5000),
        Point.new(11, 5),
        Point.new(10, 7),
        Point.new(7, 8),
        Point.new(8, 11),
        Point.new(2, 8),
        Point.new(3000, 3000),
        Point.new(5, 2),
        Point.new(5, 6)
    ]
    answers_wrapper = GrahamAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.75)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.75)

    total_grade, answer_grades = GrahamGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.75)


def test_graham_grader_incorrect_origin():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[2] = Point.new(100, 100)
    answers_wrapper = GrahamAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.75)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.75)

    total_grade, answer_grades = GrahamGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.75)


def test_graham_grader_incorrect_triples():
    algogears_answers = deepcopy(correct_algogears_answers)
    ordered = algogears_answers[1]
    algogears_answers[3] = [
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
    answers_wrapper = GrahamAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.85)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.85)

    total_grade, answer_grades = GrahamGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.85)


def test_graham_grader_incorrect_are_angles_less_than_pi():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[4] = [False for _ in algogears_answers[4]]
    answers_wrapper = GrahamAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.85)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.85)

    total_grade, answer_grades = GrahamGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.85)


def test_graham_grader_incorrect_rows_with_angles_less_than_pi():
    algogears_answers = deepcopy(correct_algogears_answers)
    ordered = algogears_answers[1]
    incorrect_point = Point.new(1000, 1000)

    algogears_answers[5][7] = GrahamStepsTableRow(point_triple=(ordered[5], ordered[6], incorrect_point), is_angle_less_than_pi=True)
    algogears_answers[5][8] = GrahamStepsTableRow(point_triple=(ordered[6], ordered[7], incorrect_point), is_angle_less_than_pi=True)
    answers_wrapper = GrahamAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.75)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.75)

    total_grade, answer_grades = GrahamGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.75)


def test_graham_grader_incorrect_rows_with_angles_not_less_than_pi_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    ordered = algogears_answers[1]
    incorrect_point = Point.new(1000, 1000)

    algogears_answers[5][1] = GrahamStepsTableRow(point_triple=(ordered[0], ordered[2], incorrect_point), is_angle_less_than_pi=True)
    answers_wrapper = GrahamAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.45) # also triggers "rows with angles < pi" grading

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.45)

    total_grade, answer_grades = GrahamGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.45)


def test_graham_grader_incorrect_rows_with_angles_not_less_than_pi_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    incorrect_point = Point.new(1000, 1000)

    algogears_answers[5][1] = GrahamStepsTableRow(point_triple=(incorrect_point, incorrect_point, incorrect_point), is_angle_less_than_pi=True)
    algogears_answers[5][5] = GrahamStepsTableRow(point_triple=(incorrect_point, incorrect_point, incorrect_point), is_angle_less_than_pi=True)
    answers_wrapper = GrahamAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.15) # also triggers "rows with angles < pi" grading

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.15)

    total_grade, answer_grades = GrahamGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.15)


def test_graham_grader_incorrect_finalization():
    algogears_answers = deepcopy(correct_algogears_answers)
    ordered = algogears_answers[1]
    algogears_answers[6][7] = GrahamStepsTableRow(point_triple=(ordered[5], ordered[0], ordered[7]), is_angle_less_than_pi=True)
    answers_wrapper = GrahamAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.5) # also triggers "rows with angles < pi" grading

    total_grade, answer_grades = GrahamGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.5)

    total_grade, answer_grades = GrahamGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.5)


