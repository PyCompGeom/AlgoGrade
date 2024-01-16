from PyCompGeomAlgorithms.dynamic_hull import PathDirection
from AlgoGrade.adapters import PointPydanticAdapter, pydantic_to_pycga
from AlgoGrade.dynamic_hull import DynamicHullAnswers, DynamicHullNodePydanticAdapter, DynamicHullTreePydanticAdapter


def test_dynamic_hull_answers():
    point = PointPydanticAdapter(coords=(1, 1))
    hull = [point]
    root = DynamicHullNodePydanticAdapter(
        data=point,
        subhull_points=hull,
        left_supporting=point,
        right_supporting=point
    )
    leaves = [root]
    tree = DynamicHullTreePydanticAdapter(root=root)
    optimized_tree = tree
    path = [PathDirection.right]
    modified_tree = tree

    answers_model = DynamicHullAnswers(
        leaves=leaves, tree=tree, optimized_tree=optimized_tree,
        path=path, modified_tree=modified_tree, hull=hull
    )
    answers_list_args = [leaves, tree, optimized_tree, path, modified_tree, hull]
    answers_list_ret = [leaves, tree, tree, tree, tree, optimized_tree, path, (modified_tree, hull)]

    assert answers_model.to_pydantic_list() == answers_list_ret
    assert answers_model.to_pycga_list() == pydantic_to_pycga(answers_list_ret)
    assert DynamicHullAnswers.from_iterable(answers_list_args) == answers_model