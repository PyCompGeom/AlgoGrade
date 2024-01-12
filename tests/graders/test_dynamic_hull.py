from math import isclose
from copy import deepcopy
from PyCompGeomAlgorithms.core import Point
from PyCompGeomAlgorithms.dynamic_hull import DynamicHullNode, DynamicHullTree, SubhullThreadedBinTree, PathDirection
from AlgoGrade.dynamic_hull import DynamicHullTask, DynamicHullGrader
from AlgoGrade.adapters import pycga_to_pydantic


points = p2, p1, p3 = [Point(3, 3), Point(1, 1), Point(5, 0)]
point_to_insert = Point(4, 3)
task = DynamicHullTask(points, point_to_insert)


def test_dynamic_hull_grader_all_correct():
    root = DynamicHullNode(p2, [p1, p2, p3], 1)
    root.left = DynamicHullNode(p1, [p1, p2])
    root.left.left = DynamicHullNode.leaf(p1)
    root.left.right = DynamicHullNode.leaf(p2)
    root.right = DynamicHullNode.leaf(p3)
    tree = DynamicHullTree(root)
    
    optimized_tree = deepcopy(tree)
    optimized_tree.root.optimized_subhull = optimized_tree.root.subhull
    optimized_tree.root.left.optimized_subhull = SubhullThreadedBinTree.empty()
    optimized_tree.root.left.left.optimized_subhull = SubhullThreadedBinTree.empty()
    optimized_tree.root.left.right.optimized_subhull = SubhullThreadedBinTree.empty()
    optimized_tree.root.right.optimized_subhull = SubhullThreadedBinTree.empty()
    
    leaves = [root.left.left, root.left.right, root.right]
    path = [PathDirection.right]
    hull = [p1, p2, point_to_insert, p3]

    optimized_tree2 = deepcopy(optimized_tree)
    optimized_tree2.root.subhull = SubhullThreadedBinTree.from_iterable(hull)
    optimized_tree2.root.optimized_subhull = optimized_tree2.root.subhull
    optimized_tree2.root.right = DynamicHullNode(point_to_insert, [point_to_insert, p3])
    optimized_tree2.root.right.optimized_subhull = SubhullThreadedBinTree.empty()
    optimized_tree2.root.right.left = DynamicHullNode.leaf(point_to_insert)
    optimized_tree2.root.right.left.optimized_subhull = SubhullThreadedBinTree.empty()
    optimized_tree2.root.right.right = DynamicHullNode.leaf(p3)
    optimized_tree2.root.right.right.optimized_subhull = SubhullThreadedBinTree.empty()

    answers = [
        leaves,
        tree,
        tree,
        tree,
        tree,
        optimized_tree,
        path,
        (optimized_tree2, hull)
    ]
    correct_answers = task.correct_answers

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 3)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 3)


def test_dynamic_hull_grader_incorrect_leaves():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[0] = deepcopy(answers[0])
    leaves = answers[0]
    leaves[0].data = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.75)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_left_supporting_single():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[1].root.left_supporting = Point(100, 100) # also triggers "omitted points" grading

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.5)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.5)


def test_dynamic_hull_grader_incorrect_right_supporting_single():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[1].root.right_supporting = Point(100, 100) # also triggers "omitted points" grading

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.5)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.5)


def test_dynamic_hull_grader_incorrect_left_and_right_supporting():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[1].root.left_supporting = Point(100, 100)  # also triggers "omitted points" grading
    answers[1].root.right_supporting = Point(100, 100) # also triggers "omitted points" grading

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.25)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.25)


def test_dynamic_hull_grader_incorrect_left_supporting_repeated():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[1].root.left_supporting = Point(100, 100) # also triggers "omitted points" grading
    answers[1].root.left.left_supporting = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.25)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.25)


def test_dynamic_hull_grader_incorrect_right_supporting_repeated():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[1].root.right_supporting = Point(100, 100) # also triggers "omitted points" grading
    answers[1].root.left.right_supporting = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.25)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.25)


def test_dynamic_hull_grader_incorrect_omitted_points():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[2].root.left_supporting = answers[2].root.left_supporting
    answers[2].root.right_supporting = answers[2].root.right_supporting
    correct_answers[2].root.left_supporting = correct_answers[2].root.left_supporting
    correct_answers[2].root.right_supporting = correct_answers[2].root.right_supporting
    
    answers[2], correct_answers[2] = deepcopy(answers[2]), deepcopy(correct_answers[2])
    dummy_point = Point(0, 0)
    answers[2].root.left.subhull = SubhullThreadedBinTree.from_iterable([p1, p2, dummy_point])
    correct_answers[2].root.left.subhull = SubhullThreadedBinTree.from_iterable([p1, p2, dummy_point])
    answers[2].root.subhull.root.point = dummy_point

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.75)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_subhull_single():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[3].root.left_supporting = answers[2].root.left_supporting
    answers[3].root.right_supporting = answers[2].root.right_supporting
    answers[3].root.subhull.root.point = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.75)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_subhull_repeated():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[3].root.left_supporting = answers[2].root.left_supporting
    answers[3].root.right_supporting = answers[2].root.right_supporting
    answers[3].root.subhull.root.point = Point(100, 100)

    answers[3].root.left.left_supporting = answers[2].root.left.left_supporting
    answers[3].root.left.right_supporting = answers[2].root.left.right_supporting
    answers[3].root.left.subhull.root.point = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.5)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.5)


def test_dynamic_hull_grader_incorrect_point_single():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[4].root.point = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.75)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_point_repeated():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[4].root.point = Point(100, 100)
    answers[4].root.left.point = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.5)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.5)


def test_dynamic_hull_grader_optimization():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[5].root.optimized_subhull.root.point = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.75)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_search_path():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[6][0] = PathDirection.left

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.75)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_final_tree_single():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[7][0].root.point = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.75)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_final_hull_single():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[7][1][0] = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.75)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_final_tree_repeated():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[7][0].root.point = Point(100, 100)
    answers[7][0].root.left.point = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.25)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.25)


def test_dynamic_hull_grader_incorrect_final_hull_repeated():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[7][1][0] = Point(100, 100)
    answers[7][1][1] = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.25)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.25)


def test_dynamic_hull_grader_incorrect_final_tree_and_hull():
    correct_answers = task.correct_answers
    answers = deepcopy(correct_answers)
    answers[7][0].root.point = Point(100, 100)
    answers[7][1][0] = Point(100, 100)

    total_grade, answer_grades = DynamicHullGrader.grade(answers, correct_answers)
    assert isclose(total_grade, 2.25)

    total_grade, answer_grades = DynamicHullGrader.grade(pycga_to_pydantic(answers), correct_answers, is_pydantic=True)
    assert isclose(total_grade, 2.25)