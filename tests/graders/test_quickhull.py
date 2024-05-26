from math import isclose
from copy import deepcopy
from algogears.core import Point
from algogears.quickhull import QuickhullNode, QuickhullTree
from AlgoGrade.quickhull import QuickhullGrader, QuickhullTask, QuickhullAnswers
from AlgoGrade.core import Scoring


points = [
    Point.new(0, 6),
    Point.new(8, 11),
    Point.new(10, 4),
    Point.new(7, 13),
    Point.new(6, 3),
    Point.new(3, 0),
    Point.new(4, 2),
    Point.new(12, 1),
    Point.new(14, 10),
    Point.new(5, 9),
    Point.new(3, 11),
    Point.new(1, 4),
]
givens = (points,)
hull = [points[0], points[10], points[3], points[8], points[7], points[5]]
task_class = QuickhullTask
scorings = [
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.25, fine=0.25, repeat_fine=0.5),
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=1, fine=1)
]
correct_algogears_answers = task_class.solve_as_algogears_list(givens)
correct_answers_wrapper = task_class.solve_as_answers_wrapper(givens)


def test_quickhull_grader_all_correct():
    tree = QuickhullTree(
        root=QuickhullNode(
            data=[
                points[0],
                points[10],
                points[9],
                points[3],
                points[1],
                points[8],
                points[7],
                points[2],
                points[4],
                points[6],
                points[5],
                points[11],
            ],
            subhull=hull
        )
    )

    tree.root.left = QuickhullNode(
        data=[points[0], points[10], points[9], points[3], points[1], points[8]],
        h=points[3],
        subhull=[points[0], points[10], points[3], points[8]]
    )
    tree.root.right = QuickhullNode(
        data=[points[8], points[7], points[2], points[4], points[6], points[5], points[11], points[0]],
        h=points[7],
        subhull=[points[8], points[7], points[5], points[0]]
    )

    tree.root.left.left = QuickhullNode(data=[points[0], points[10], points[3]], h=points[10], subhull=[points[0], points[10], points[3]])
    tree.root.left.right = QuickhullNode(data=[points[3], points[8]], subhull=[points[3], points[8]])
    tree.root.left.left.left = QuickhullNode(data=[points[0], points[10]], subhull=[points[0], points[10]])
    tree.root.left.left.right = QuickhullNode(data=[points[10], points[3]], subhull=[points[10], points[3]])

    tree.root.right.left = QuickhullNode(data=[points[8], points[7]], subhull=[points[8], points[7]])
    tree.root.right.right = QuickhullNode(
        data=[points[7], points[4], points[6], points[5], points[11], points[0]],
        h=points[5],
        subhull=[points[7], points[5], points[0]]
    )
    tree.root.right.right.left = QuickhullNode(data=[points[7], points[5]], subhull=[points[7], points[5]])
    tree.root.right.right.right = QuickhullNode(data=[points[5], points[0]], subhull=[points[5], points[0]])

    leftmost_point, rightmost_point = points[0], points[8]
    s1, s2 = tree.root.left.points, tree.root.right.points

    algogears_answers = [(leftmost_point, rightmost_point, s1, s2), tree, tree, tree, tree]
    answers_wrapper = QuickhullAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = QuickhullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2)

    total_grade, answer_grades = QuickhullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2)


def test_quickhull_grader_incorrect_first_step():
    algogears_answers = deepcopy(correct_algogears_answers)
    first_step_list = list(algogears_answers[0])
    first_step_list[0] = Point.new(100, 100)
    algogears_answers[0] = tuple(first_step_list)
    answers_wrapper = QuickhullAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = QuickhullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.75)

    total_grade, answer_grades = QuickhullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.75)


def test_quickhull_grader_incorrect_h_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[1].root.h = Point.new(100, 100)
    answers_wrapper = QuickhullAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = QuickhullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.75)

    total_grade, answer_grades = QuickhullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.75)


def test_quickhull_grader_incorrect_h_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[1].root.h = Point.new(100, 100)
    algogears_answers[1].root.left.h = Point.new(100, 100)
    answers_wrapper = QuickhullAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = QuickhullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.5)

    total_grade, answer_grades = QuickhullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.5)


def test_quickhull_grader_incorrect_points():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[2].root.left.left.points[0] = Point.new(100, 100)
    answers_wrapper = QuickhullAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = QuickhullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1.75)

    total_grade, answer_grades = QuickhullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1.75)


def test_quickhull_grader_incorrect_finalization():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[3].root.left.right.left = QuickhullNode(data=[]) # leaf node w/ 2 points is now not a leaf
    answers_wrapper = QuickhullAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = QuickhullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.25) # this test also triggers four node-related gradings: 0.25, 0.25, 0.25, 1

    total_grade, answer_grades = QuickhullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 0.25)


def test_quickhull_grader_incorrect_merge():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[4].root.left.right.subhull = [Point.new(100, 100)]
    answers_wrapper = QuickhullAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = QuickhullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1)

    total_grade, answer_grades = QuickhullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1)
