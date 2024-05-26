from copy import deepcopy
from functools import partial
from math import isclose
from pytest import fixture
from algogears.core import BinTree, BinTreeNode, ThreadedBinTree, ThreadedBinTreeNode
from AlgoGrade.core import Grader, Scoring


single_mistake_fine_scoring = Scoring(min_grade=0, max_grade=1, fine=0.5, repeat_fine=0)
repeated_mistake_fine_scoring = Scoring(min_grade=0, max_grade=1, fine=0.5, repeat_fine=1)


class ObjectGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [cls.grade_object]


class ApproximateEqualityObjectGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [partial(cls.grade_object, custom_eq=isclose)]


class IterableGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [cls.grade_iterable]


class BinTreeGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [cls.grade_bin_tree]


class ThreadedBinTreeGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [cls.grade_threaded_bin_tree]


def test_grade_object_regular_equality_correct_with_single_mistake_scoring():
    answers = [1]
    correct_answers = [1]

    total_score, _ = ObjectGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 1)


def test_grade_object_regular_equality_correct_with_repeated_mistake_scoring():
    answers = [1]
    correct_answers = [1]

    total_score, _ = ObjectGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 1)


def test_grade_object_regular_equality_incorrect_with_single_mistake_scoring():
    answers = [0]
    correct_answers = [1]

    total_score, _ = ObjectGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_object_regular_equality_incorrect_with_repeated_mistake_scoring():
    answers = [0]
    correct_answers = [1]

    total_score, _ = ObjectGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_object_custom_equality_with_single_mistake_scoring():
    answers = [1.33333333333]
    correct_answers = [1.333333333332]

    total_score, _ = ApproximateEqualityObjectGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 1)


def test_grade_object_custom_equality_with_repeated_mistake_scoring():
    answers = [1.33333333333]
    correct_answers = [1.333333333332]

    total_score, _ = ApproximateEqualityObjectGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 1)


def test_grade_iterable_correct_with_single_mistake_scoring():
    answers = [[1, 2, 3, 4]]
    correct_answers = [[1, 2, 3, 4]]

    total_score, _ = IterableGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 1)


def test_grade_iterable_correct_with_repeated_mistake_scoring():
    answers = [[1, 2, 3, 4]]
    correct_answers = [[1, 2, 3, 4]]

    total_score, _ = IterableGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 1)


def test_grade_iterablle_incorrect_single_with_single_mistake_scoring():
    answers = [[0, 2, 3, 4]]
    correct_answers = [[1, 2, 3, 4]]

    total_score, _ = IterableGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_iterablle_incorrect_single_with_repeated_mistake_scoring():
    answers = [[0, 2, 3, 4]]
    correct_answers = [[1, 2, 3, 4]]

    total_score, _ = IterableGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_iterable_incorrect_repeated_with_single_mistake_scoring():
    answers = [[0, 2, 0, 4]]
    correct_answers = [[1, 2, 3, 4]]

    total_score, _ = IterableGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_iterable_incorrect_repeated_with_repeated_mistake_scoring():
    answers = [[0, 2, 0, 4]]
    correct_answers = [[1, 2, 3, 4]]

    total_score, _ = IterableGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0)


def test_grade_bin_tree_correct_with_single_mistake_scoring():
    answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))]
    correct_answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 1)


def test_grade_bin_tree_correct_with_repeated_mistake_scoring():
    answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))]
    correct_answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 1)


def test_grade_bin_tree_incorrect_contents_single_with_single_mistake_scoring():
    answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=0), right=BinTreeNode(data=3)))]
    correct_answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_bin_tree_incorrect_contents_single_with_repeated_mistake_scoring():
    answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=0), right=BinTreeNode(data=3)))]
    correct_answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_bin_tree_incorrect_contents_repeated_with_single_mistake_scoring():
    answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=0), right=BinTreeNode(data=0)))]
    correct_answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_bin_tree_incorrect_contents_repeated_with_repeated_mistake_scoring():
    answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=0), right=BinTreeNode(data=0)))]
    correct_answers = [BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0)


def test_grade_bin_tree_extra_nodes_single_with_single_mistake_scoring():
    correct_tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree.root.left.left = BinTreeNode(data="extra")

    answers = [tree]
    correct_answers = [correct_tree]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_bin_tree_extra_nodes_single_with_repeated_mistake_scoring():
    correct_tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree.root.left.left = BinTreeNode(data="extra")

    answers = [tree]
    correct_answers = [correct_tree]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_bin_tree_extra_nodes_repeated_with_single_mistake_scoring():
    correct_tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree.root.left.left = BinTreeNode(data="extra")
    tree.root.right.left = BinTreeNode(data="extra")
    tree.root.right.left.left = BinTreeNode(data="extra")

    answers = [tree]
    correct_answers = [correct_tree]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_bin_tree_extra_nodes_repeated_with_repeated_mistake_scoring():
    correct_tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree.root.left.left = BinTreeNode(data="extra")
    tree.root.right.left = BinTreeNode(data="extra")
    tree.root.right.left.left = BinTreeNode(data="extra")

    answers = [tree]
    correct_answers = [correct_tree]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0)


def test_grade_bin_tree_missing_nodes_single_with_single_mistake_scoring():
    correct_tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2)))

    answers = [tree]
    correct_answers = [correct_tree]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_bin_tree_missing_nodes_single_with_repeated_mistake_scoring():
    correct_tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2)))

    answers = [tree]
    correct_answers = [correct_tree]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_bin_tree_missing_nodes_repeated_with_single_mistake_scoring():
    correct_tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree = BinTree(root=BinTreeNode(data=1))

    answers = [tree]
    correct_answers = [correct_tree]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_bin_tree_missing_nodes_repeated_with_repeated_mistake_scoring():
    correct_tree = BinTree(root=BinTreeNode(data=1, left=BinTreeNode(data=2), right=BinTreeNode(data=3)))
    tree = BinTree(root=BinTreeNode(data=1))

    answers = [tree]
    correct_answers = [correct_tree]

    total_score, _ = BinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0)


@fixture
def correct_circular_tbt():
    root = ThreadedBinTreeNode(data=3)
    root.left = ThreadedBinTreeNode(data=0)
    root.left.right = ThreadedBinTreeNode(data=2)
    root.left.right.left = ThreadedBinTreeNode(data=1)
    root.right = ThreadedBinTreeNode(data=4)
    root.right.right = ThreadedBinTreeNode(data=5)

    root.prev = root.left.right
    root.next = root.right

    root.left.prev = root.right.right
    root.left.next = root.left.right.left

    root.left.right.prev = root.left.right.left
    root.left.right.next = root

    root.left.right.left.prev = root.left
    root.left.right.left.next = root.left.right

    root.right.prev = root
    root.right.next = root.right.right

    root.right.right.prev = root.right
    root.right.right.next = root.left

    return ThreadedBinTree(root=root)


@fixture
def correct_non_circular_tbt(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.prev = None
    tbt.root.right.right.next = None

    return tbt


def test_grade_threaded_bin_tree_correct_with_single_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 1)


def test_grade_threaded_bin_tree_correct_with_repeated_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 1)


def test_grade_threaded_bin_tree_incorrect_contents_single_with_single_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.data = 100

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_incorrect_contents_single_with_repeated_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.data = 100

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_incorrect_contents_repeated_with_single_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.data = 100
    tbt.root.right.data = 100

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_incorrect_contents_repeated_with_repeated_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.data = 100
    tbt.root.right.data = 100

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0)


def test_grade_threaded_bin_tree_extra_nodes_single_with_single_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.left = ThreadedBinTreeNode(data="extra1")

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_extra_nodes_single_with_repeated_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.left = ThreadedBinTreeNode(data="extra1")

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_extra_nodes_repeated_with_single_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.left = ThreadedBinTreeNode(data="extra1")
    tbt.root.left.right.right = ThreadedBinTreeNode(data="extra2")

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_extra_nodes_repeated_with_repeated_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.left = ThreadedBinTreeNode(data="extra1")
    tbt.root.left.right.right = ThreadedBinTreeNode(data="extra2")

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0)


def test_grade_threaded_bin_tree_missing_nodes_single_with_single_mistake_scoring(correct_circular_tbt):
    # Note that this test also triggers missing threads by necessity, so there are actually 3 mistakes here (1 for node, 2 for threads)
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.right.left = None
    tbt.root.left.right.prev = None
    tbt.root.left.next = None

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_missing_nodes_single_with_repeated_mistake_scoring(correct_circular_tbt):
    # Note that this test also triggers missing threads by necessity, so there are actually 3 mistakes here (1 for node, 2 for threads)
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.right.left = None
    tbt.root.left.right.prev = None
    tbt.root.left.next = None

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.0)


def test_grade_threaded_bin_tree_missing_nodes_repeated_with_single_mistake_scoring(correct_circular_tbt):
    # Note that this test also triggers missing threads by necessity, so there are actually 6 mistakes here (2 for nodes, 4 for threads)
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.right.left = None
    tbt.root.left.right.prev = None
    tbt.root.left.next = None

    tbt.root.right.right = None
    tbt.root.left.prev = None
    tbt.root.right.next = None

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_missing_nodes_repeated_with_repeated_mistake_scoring(correct_circular_tbt):
    # Note that this test also triggers missing threads by necessity, so there are actually 6 mistakes here (2 for nodes, 4 for threads)
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.left.right.left = None
    tbt.root.left.right.prev = None
    tbt.root.left.next = None

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.0)


def test_grade_threaded_bin_tree_extra_threads_in_incorrect_part_of_tree_single_with_single_mistake_scoring(correct_non_circular_tbt):
    # Note that this test also triggers extra nodes by necessity, so there are actually 2 mistakes here (1 for node, 1 for thread)
    tbt = deepcopy(correct_non_circular_tbt)
    tbt.root.left.right.right = ThreadedBinTreeNode(data="extra1")
    tbt.root.left.right.right.prev = tbt.root.right.right
    tbt.root.right.right.next = tbt.root.left.right.right

    answers = [tbt]
    correct_answers = [correct_non_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_extra_threads_in_incorrect_part_of_tree_single_with_repeated_mistake_scoring(correct_non_circular_tbt):
    # Note that this test also triggers extra nodes by necessity, so there are actually 2 mistakes here (1 for node, 1 for thread)
    tbt = deepcopy(correct_non_circular_tbt)
    tbt.root.left.right.right = ThreadedBinTreeNode(data="extra1")
    tbt.root.left.right.right.prev = tbt.root.right.right
    tbt.root.right.right.next = tbt.root.left.right.right

    answers = [tbt]
    correct_answers = [correct_non_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.0)


def test_grade_threaded_bin_tree_extra_threads_in_incorrect_part_of_tree_repeated_with_single_mistake_scoring(correct_non_circular_tbt):
    # Note that this test also triggers extra nodes by necessity, so there are actually 4 mistakes here (2 for nodes, 2 for threads)
    tbt = deepcopy(correct_non_circular_tbt)
    tbt.root.left.right.right = ThreadedBinTreeNode(data="extra1")
    tbt.root.left.right.right.prev = tbt.root.right.right
    tbt.root.right.right.next = tbt.root.left.right.right

    tbt.root.left.right.right.right = ThreadedBinTreeNode(data="extra2")
    tbt.root.left.right.right.next = tbt.root.left.right.right.right
    tbt.root.left.right.right.right.prev = tbt.root.left.right.right

    answers = [tbt]
    correct_answers = [correct_non_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_extra_threads_in_incorrect_part_of_tree_repeated_with_repeated_mistake_scoring(correct_non_circular_tbt):
    # Note that this test also triggers extra nodes by necessity, so there are actually 4 mistakes here (2 for nodes, 2 for threads)
    tbt = deepcopy(correct_non_circular_tbt)
    tbt.root.left.right.right = ThreadedBinTreeNode(data="extra1")
    tbt.root.left.right.right.prev = tbt.root.right.right
    tbt.root.right.right.next = tbt.root.left.right.right

    answers = [tbt]
    correct_answers = [correct_non_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.0)


def test_grade_threaded_bin_tree_missing_threads_in_correct_subtree_single_with_single_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.prev = None

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_missing_threads_in_correct_subtree_single_with_repeated_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.prev = None

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_missing_threads_in_correct_subtree_repeated_with_single_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.prev = None
    tbt.root.left.right.next = None

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_missing_threads_in_correct_subtree_repeated_with_repeated_mistake_scoring(correct_circular_tbt):
    tbt = deepcopy(correct_circular_tbt)
    tbt.root.prev = None
    tbt.root.left.right.next = None

    answers = [tbt]
    correct_answers = [correct_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0)


def test_grade_threaded_bin_tree_extra_thread_in_correct_subtree_with_single_mistake_scoring(correct_non_circular_tbt):
    # There can be only one extra thread in a correct subtree, and it's the one that connects the extreme nodes in a non-circular TBT (which shouldn't be connected).
    tbt = deepcopy(correct_non_circular_tbt)
    tbt.root.left.prev = tbt.root.right.right
    tbt.root.right.right.next = tbt.root.left

    answers = [tbt]
    correct_answers = [correct_non_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_extra_thread_in_correct_subtree_with_repeated_mistake_scoring(correct_non_circular_tbt):
    # There can be only one extra thread in a correct subtree, and it's the one that connects the extreme nodes in a non-circular TBT (which shouldn't be connected).
    tbt = deepcopy(correct_non_circular_tbt)
    tbt.root.left.prev = tbt.root.right.right
    tbt.root.right.right.next = tbt.root.left

    answers = [tbt]
    correct_answers = [correct_non_circular_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


@fixture
def correct_shallow_tbt():
    root = ThreadedBinTreeNode(data=1)
    root.left = ThreadedBinTreeNode(data=0)
    root.right = ThreadedBinTreeNode(data=2)

    root.prev = root.left
    root.next = root.right

    root.left.prev = root.right
    root.left.next = root

    root.right.prev = root
    root.right.next = root.left

    return ThreadedBinTree(root=root)


@fixture
def incorrect_shallow_tbt():
    root = ThreadedBinTreeNode(data=1)
    root.left = ThreadedBinTreeNode(data=0)
    root.right = ThreadedBinTreeNode(data=2)

    root.prev = root.right
    root.right.next = root

    root.left.next = None
    root.left.prev = None

    return ThreadedBinTree(root=root)


def test_grade_threaded_bin_tree_threads_in_correct_subtree_in_wrong_direction_single_with_single_mistake_scoring(correct_shallow_tbt, incorrect_shallow_tbt):
    # Note that this test also triggers missing threads in correct subtree by necessity, so there are actually 3 mistakes (1 thread in wrong direction and 2 missing threads)
    answers = [incorrect_shallow_tbt]
    correct_answers = [correct_shallow_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_threads_in_correct_subtree_in_wrong_direction_single_with_repeated_mistake_scoring(correct_shallow_tbt, incorrect_shallow_tbt):
    # Note that this test also triggers missing threads in correct subtree by necessity, so there are actually 3 mistakes (1 thread in wrong direction and 2 missing threads)
    answers = [incorrect_shallow_tbt]
    correct_answers = [correct_shallow_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0)


def test_grade_threaded_bin_tree_threads_in_correct_subtree_in_wrong_direction_repeated_with_single_mistake_scoring(correct_shallow_tbt):
    tbt = deepcopy(correct_shallow_tbt)
    tbt.root.prev = tbt.root.right
    tbt.root.next = tbt.root.left

    tbt.root.left.prev = tbt.root
    tbt.root.left.next = tbt.root.right

    tbt.root.right.prev = tbt.root.left
    tbt.root.right.next = tbt.root
    
    answers = [tbt]
    correct_answers = [correct_shallow_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [single_mistake_fine_scoring])
    assert isclose(total_score, 0.5)


def test_grade_threaded_bin_tree_threads_in_correct_subtree_in_wrong_direction_repeated_with_repeated_mistake_scoring(correct_shallow_tbt):
    tbt = deepcopy(correct_shallow_tbt)
    tbt.root.prev = tbt.root.right
    tbt.root.next = tbt.root.left

    tbt.root.left.prev = tbt.root
    tbt.root.left.next = tbt.root.right

    tbt.root.right.prev = tbt.root.left
    tbt.root.right.next = tbt.root
    
    answers = [tbt]
    correct_answers = [correct_shallow_tbt]

    total_score, _ = ThreadedBinTreeGrader.grade_algogears(answers, correct_answers, [repeated_mistake_fine_scoring])
    assert isclose(total_score, 0)