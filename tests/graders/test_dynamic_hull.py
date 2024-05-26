from math import isclose
from copy import deepcopy
from algogears.core import Point
from algogears.dynamic_hull import DynamicHullNode, DynamicHullTree, SubhullThreadedBinTree, PathDirection
from AlgoGrade.dynamic_hull import DynamicHullTask, DynamicHullGrader, DynamicHullAnswers
from AlgoGrade.core import Scoring


points = p2, p1, p3 = [Point.new(3, 3), Point.new(1, 1), Point.new(5, 0)]
point_to_insert = Point.new(4, 3)
givens = points, point_to_insert
task_class = DynamicHullTask
scorings = [
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.5, fine=0.25, repeat_fine=0.5),
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.5, fine=0.25, repeat_fine=0.5),
    Scoring(max_grade=0.25, fine=0.25, repeat_fine=0.5),
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.75, fine=0.25, repeat_fine=0.75)
]
correct_algogears_answers = task_class.solve_as_algogears_list(givens)
correct_answers_wrapper = task_class.solve_as_answers_wrapper(givens)


def test_dynamic_hull_grader_all_correct():
    root = DynamicHullNode(data=p2, subhull=[p1, p2, p3], left_supporting_index=1, left_supporting=p2, right_supporting=p3)
    root.left = DynamicHullNode(data=p1, subhull=[p1, p2], left_supporting=p1, right_supporting=p2)
    root.left.left = DynamicHullNode.leaf(p1)
    root.left.right = DynamicHullNode.leaf(p2)
    root.right = DynamicHullNode.leaf(p3)
    tree = DynamicHullTree(root=root)
    
    tree.root.optimized_subhull = tree.root.subhull
    
    leaves = [root.left.left, root.left.right, root.right]
    path = [PathDirection.right]
    hull = [p1, p2, point_to_insert, p3]

    modified_tree = deepcopy(tree)
    modified_tree.root.subhull = hull
    modified_tree.root.optimized_subhull = hull
    modified_tree.root.right_supporting = point_to_insert
    modified_tree.root.right = DynamicHullNode(data=point_to_insert, subhull=[point_to_insert, p3], left_supporting=point_to_insert, right_supporting=p3)
    modified_tree.root.right.left = DynamicHullNode.leaf(point_to_insert)
    modified_tree.root.right.right = DynamicHullNode.leaf(p3)

    algogears_answers = [
        leaves,
        tree,
        tree,
        tree,
        tree,
        tree,
        path,
        (modified_tree, hull)
    ]
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 3)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 3)


def test_dynamic_hull_grader_incorrect_leaves():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[1].root.left.left.data = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.75)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_left_supporting_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[1].root.left_supporting = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.75)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.75)



def test_dynamic_hull_grader_incorrect_right_supporting_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[1].root.right_supporting = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.75)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_left_and_right_supporting():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[1].root.left_supporting = Point.new(100, 100)
    algogears_answers[1].root.right_supporting = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.5)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.5)


def test_dynamic_hull_grader_incorrect_left_supporting_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[1].root.left_supporting = Point.new(100, 100) # also triggers "omitted points" grading
    algogears_answers[1].root.left.left_supporting = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.5)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.5)


def test_dynamic_hull_grader_incorrect_right_supporting_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[1].root.right_supporting = Point.new(100, 100) # also triggers "omitted points" grading
    algogears_answers[1].root.left.right_supporting = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.5)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.5)


def test_dynamic_hull_grader_incorrect_omitted_points():
    points = p2, p1, p3 = [Point.new(3, 0), Point.new(1, 1), Point.new(5, 0)] # move p2 below p1-p3 for it to be omitted
    point_to_insert = Point.new(4, 3)
    givens = points, point_to_insert
    correct_algogears_answers = task_class.solve_as_algogears_list(givens)
    correct_answers_wrapper = task_class.solve_as_answers_wrapper(givens)

    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[2].root.subhull = [p1, p2, p3]
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.5) # also triggers subhull grading (1 extra point, fine 0.25)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.5)


def test_dynamic_hull_grader_incorrect_subhull_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[3].root.left_supporting = algogears_answers[2].root.left_supporting
    algogears_answers[3].root.right_supporting = algogears_answers[2].root.right_supporting
    algogears_answers[3].root.subhull = deepcopy(algogears_answers[3].root.subhull) # to not interfere with optimized_subhull, which, in root, is a reference to subhull
    algogears_answers[3].root.subhull[0] = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.75)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_subhull_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[3].root.left_supporting = algogears_answers[2].root.left_supporting
    algogears_answers[3].root.right_supporting = algogears_answers[2].root.right_supporting
    algogears_answers[3].root.subhull = deepcopy(algogears_answers[3].root.subhull) # to not interfere with optimized_subhull, which, in root, is a reference to subhull
    algogears_answers[3].root.subhull[0] = Point.new(100, 100)

    algogears_answers[3].root.left.left_supporting = algogears_answers[2].root.left.left_supporting
    algogears_answers[3].root.left.right_supporting = algogears_answers[2].root.left.right_supporting
    algogears_answers[3].root.left.subhull[0] = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.5)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.5)


def test_dynamic_hull_grader_incorrect_left_supporting_index_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[4].root.left_supporting = algogears_answers[2].root.left_supporting # getter returns this left_supporting, not subhull[left_supporting_index]
    algogears_answers[4].root.right_supporting = algogears_answers[2].root.right_supporting
    algogears_answers[4].root.left_supporting_index = 100
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.75)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_left_supporting_index_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[4].root.left_supporting = algogears_answers[2].root.left_supporting
    algogears_answers[4].root.right_supporting = algogears_answers[2].root.right_supporting
    algogears_answers[4].root.left_supporting_index = 100

    algogears_answers[4].root.left.left_supporting = algogears_answers[2].root.left.left_supporting
    algogears_answers[4].root.left.right_supporting = algogears_answers[2].root.left.right_supporting
    algogears_answers[4].root.left.left_supporting_index = 100
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.5)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.5)


def test_dynamic_hull_grader_incorrect_optimization():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[5].root.subhull = deepcopy(algogears_answers[5].root.subhull) # to prevent being modified when optimized_subhull is modified, which, in root, is a reference to subhull
    algogears_answers[5].root.optimized_subhull[0] = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.75)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_search_path():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[6][0] = PathDirection.left
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.75)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_final_tree_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[7][0].root.point = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.75)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_final_hull_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[7] = (algogears_answers[7][0], deepcopy(algogears_answers[7][1]))
    algogears_answers[7][1][0] = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.75)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.75)


def test_dynamic_hull_grader_incorrect_final_tree_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[7][0].root.point = Point.new(100, 100)
    algogears_answers[7][0].root.left.point = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.25)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.25)


def test_dynamic_hull_grader_incorrect_final_hull_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[7][1][0] = Point.new(100, 100)
    algogears_answers[7][1][1] = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.25)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.25)


def test_dynamic_hull_grader_incorrect_final_tree_and_hull():
    algogears_answers = deepcopy(correct_algogears_answers)
    algogears_answers[7][0].root.point = Point.new(100, 100)
    algogears_answers[7][1][0] = Point.new(100, 100)
    answers_wrapper = DynamicHullAnswers.from_iterable(algogears_answers)

    total_grade, answers_grades = DynamicHullGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 2.25)

    total_grade, answers_grades = DynamicHullGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 2.25)