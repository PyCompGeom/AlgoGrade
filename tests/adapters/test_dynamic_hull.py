from pytest import fixture
from PyCompGeomAlgorithms.core import Point
from PyCompGeomAlgorithms.dynamic_hull import DynamicHullNode, DynamicHullTree, SubhullNode, SubhullThreadedBinTree
from AlgoGrade.adapters import PointPydanticAdapter
from AlgoGrade.dynamic_hull import DynamicHullNodePydanticAdapter, DynamicHullTreePydanticAdapter, SubhullNodePydanticAdapter, SubhullThreadedBinTreePydanticAdapter


@fixture
def dynamic_hull_node_adapter():
    point_adapter = PointPydanticAdapter(coords=(1, 1))
    return DynamicHullNodePydanticAdapter(
        data=point_adapter,
        subhull_points=[point_adapter],
        optimized_subhull_points=[point_adapter],
        left_supporting=point_adapter,
        right_supporting=point_adapter
    )


@fixture
def dynamic_hull_node_regular():
    point = Point(1, 1)
    return DynamicHullNode(point, [point], optimized_subhull_points=[point])


@fixture
def subhull_node_adapter():
    return SubhullNodePydanticAdapter(
        data=Point(1, 1)
    )


@fixture
def subhull_node_regular():
    return SubhullNode(Point(1, 1))


def test_dynamic_hull_node_adapter(dynamic_hull_node_adapter, dynamic_hull_node_regular):
    assert dynamic_hull_node_adapter.regular_object == dynamic_hull_node_regular


def test_dynamic_hull_tree_adapter(dynamic_hull_node_adapter, dynamic_hull_node_regular):
    adapter = DynamicHullTreePydanticAdapter(root=dynamic_hull_node_adapter)
    regular_object = DynamicHullTree(dynamic_hull_node_regular)

    assert adapter.regular_object == regular_object


def test_subhull_node_adapter(subhull_node_adapter, subhull_node_regular):
    assert subhull_node_adapter.regular_object == subhull_node_regular


def test_subhull_tree_adapter(subhull_node_adapter, subhull_node_regular):
    adapter = SubhullThreadedBinTreePydanticAdapter(root=subhull_node_adapter)
    regular_object = SubhullThreadedBinTree(root=subhull_node_regular)

    assert adapter.regular_object == regular_object
