from algogears.core import Point
from algogears.dynamic_hull import PathDirection, DynamicHullNode, DynamicHullTree
from AlgoGrade.dynamic_hull import DynamicHullAnswers


def test_dynamic_hull_answers():
    point = Point(coords=(1, 1))
    hull = [point]
    root = DynamicHullNode(
        data=point,
        subhull=hull,
        left_supporting=point,
        right_supporting=point
    )
    leaves = [root]
    tree = DynamicHullTree(root=root)
    optimized_tree = tree
    path = [PathDirection.right]
    modified_tree = tree

    answers_model = DynamicHullAnswers(
        leaves=leaves, tree=tree, optimized_tree=optimized_tree,
        path=path, modified_tree=modified_tree, hull=hull
    )
    answers_list = [leaves, tree, tree, tree, tree, optimized_tree, path, (modified_tree, hull)]

    assert answers_model.to_algogears_list() == answers_list
    assert DynamicHullAnswers.from_iterable(answers_list) == answers_model
    assert DynamicHullAnswers(**answers_model.model_dump()) == answers_model