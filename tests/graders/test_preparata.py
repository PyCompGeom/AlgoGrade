from math import isclose
from copy import deepcopy
from PyCompGeomAlgorithms.core import Point, ThreadedBinTree
from AlgoGrade.preparata import PreparataGrader, PreparataTask
from AlgoGrade.adapters import pycga_to_pydantic
from AlgoGrade.core import Scoring


points = [Point(1, 1), Point(1, 5), Point(5, 3), Point(1, 11), Point(6, 1), Point(10, 1)]
task = PreparataTask(points)
scorings = [
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.25, fine=0.25, repeat_fine=1.5),
    Scoring(max_grade=0.25, fine=0.25, repeat_fine=1),
    Scoring(max_grade=0.25, fine=0.25, repeat_fine=1.5)
]


def test_preparata_all_correct():
    hull0 = [Point(1, 1), Point(1, 5), Point(5, 3)]
    hull = [Point(1, 1), Point(1, 11), Point(10, 1)]
    tree0 = ThreadedBinTree.from_iterable(hull0)
    left_paths = [
        [Point(1, 5), Point(5, 3)],
        [Point(1, 11), Point(5, 3), Point(1, 1)],
        [Point(1, 11), Point(6, 1), Point(1, 1)]
    ]
    right_paths = [
        [Point(1, 5), Point(1, 1)],
        [Point(1, 11)],
        [Point(1, 11)]
    ]
    deleted_points = [[Point(1, 5)], [Point(5, 3)], [Point(6, 1)]]
    hulls = [
        [Point(1, 1), Point(1, 11), Point(5, 3)],
        [Point(1, 1), Point(1, 11), Point(6, 1)],
        hull
    ]
    trees = [ThreadedBinTree.from_iterable(hulls[0]), ThreadedBinTree.from_iterable(hulls[1])]

    answers = [(hull0, tree0), (left_paths, right_paths), deleted_points, (hulls, trees)]
    correct_answers = task.correct_answers

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, 1)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, 1)


def test_preparata_grader_incorrect_first_hull():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    first_hull = answers[0][0]
    first_hull[0] = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_first_tree():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    first_tree = answers[0][1]
    first_tree.root.data = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_left_paths_single():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    left_paths = answers[1][0]
    left_paths[0][0] = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_left_paths_repeated():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    left_paths = answers[1][0]
    left_paths[0][0] = Point(100, 100)
    left_paths[0][1] = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_right_paths_single():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    right_paths = answers[1][1]
    right_paths[0][0] = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_right_paths_repeated():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    right_paths = answers[1][1]
    right_paths[0][0] = Point(100, 100)
    right_paths[0][1] = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_left_and_right_paths():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    left_paths = answers[1][0]
    right_paths = answers[1][1]
    left_paths[0][0] = Point(100, 100)
    right_paths[0][0] = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_deleted_points_single():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    deleted_points = answers[2]
    deleted_points[0][0] = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_deleted_points_repeated():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    deleted_points = answers[2]
    deleted_points[0][0] = Point(100, 100)
    deleted_points[1][0] = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, 0)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, 0)


def test_preparata_grader_incorrect_hulls_single():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    hulls = answers[3][0]
    hulls[0][0] = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_hulls_repeated():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    hulls = answers[3][0]
    hulls[0][0] = Point(100, 100)
    hulls[1][1] = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_trees_single():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    trees = answers[3][1]
    trees[0].root.data = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_trees_repeated():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    trees = answers[3][1]
    trees[0].root.data = Point(100, 100)
    trees[0].root.left.data = None
    trees[1].root.data = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_trees_and_hulls():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    
    hulls = answers[3][0]
    hulls[0][0] = Point(100, 100)
    hulls[1][1] = Point(100, 100)
    
    trees = answers[3][1]
    trees[0].root.data = Point(100, 100)
    trees[0].root.left.data = None
    trees[1].root.data = Point(100, 100)

    total_grade, answer_grades = PreparataGrader.grade(answers, correct_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade(pycga_to_pydantic(answers), correct_answers, scorings, is_pydantic=True)
    assert isclose(total_grade, -0.5)
