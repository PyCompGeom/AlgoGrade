from copy import deepcopy
from pytest import fixture
from PyCompGeomAlgorithms.core import Point, BinTreeNode, BinTree, ThreadedBinTreeNode, ThreadedBinTree
from AlgoGrade.proxies import PointProxy, BinTreeNodeProxy, BinTreeProxy, ThreadedBinTreeNodeProxy, ThreadedBinTreeProxy


def test_point_proxy():
    coords = 1, 2, 3
    proxy = PointProxy(coords=coords)
    regular = Point(*coords)
    assert proxy.to_regular_object() == regular


@fixture
def proxy_root():
    proxy_root = BinTreeNodeProxy(data=1)
    proxy_left = BinTreeNodeProxy(data=2)
    proxy_right = BinTreeNodeProxy(data=3)
    proxy_root.left = proxy_left
    proxy_root.right = proxy_right

    return proxy_root


@fixture
def regular_root():
    return BinTreeNode(1, left=BinTreeNode(2), right=BinTreeNode(3))


def test_bin_tree_node_proxy(proxy_root, regular_root):
    assert proxy_root.to_regular_object() == regular_root


def test_bin_tree_proxy(proxy_root, regular_root):
    proxy_tree = BinTreeProxy(root=proxy_root)
    regular_tree = BinTree(regular_root)
    assert proxy_tree.to_regular_object() == regular_tree


@fixture
def proxy_tbt_root_circular():
    proxy_root = ThreadedBinTreeNodeProxy(data=1)
    proxy_left = ThreadedBinTreeNodeProxy(data=2)
    proxy_right =ThreadedBinTreeNodeProxy(data=3)
    proxy_root.left = proxy_left
    proxy_root.right = proxy_right

    proxy_root.prev = proxy_root.left
    proxy_root.next = proxy_root.right
    proxy_left.prev = proxy_right
    proxy_left.next = proxy_root
    proxy_right.prev = proxy_root
    proxy_right.next = proxy_left

    return proxy_root


@fixture
def regular_tbt_root_circular():
    left = ThreadedBinTreeNode(2)
    right = ThreadedBinTreeNode(3)
    root = ThreadedBinTreeNode(1, left, right)
    root.prev = left
    root.next = right
    left.prev = right
    left.next = root
    right.prev = root
    right.next = left

    return root


@fixture
def proxy_tbt_root(proxy_tbt_root_circular):
    proxy_tbt_root = deepcopy(proxy_tbt_root_circular)
    proxy_tbt_root.left.prev = None
    proxy_tbt_root.right.next = None

    return proxy_tbt_root


@fixture
def regular_tbt_root(regular_tbt_root_circular):
    regular_tbt_root = deepcopy(regular_tbt_root_circular)
    regular_tbt_root.left.prev = None
    regular_tbt_root.right.next = None

    return regular_tbt_root


def test_threaded_bin_tree_node_proxy(proxy_tbt_root, regular_tbt_root):
    assert proxy_tbt_root.to_regular_object() == regular_tbt_root


def test_threaded_bin_tree_proxy(proxy_tbt_root, regular_tbt_root):
    proxy_tbt = ThreadedBinTreeProxy(root=proxy_tbt_root)
    regular_tbt = ThreadedBinTree(regular_tbt_root)
    assert proxy_tbt.to_regular_object() == regular_tbt


def test_threaded_bin_tree_node_proxy_circular(proxy_tbt_root_circular, regular_tbt_root_circular):
    assert proxy_tbt_root_circular.to_regular_object() == regular_tbt_root_circular


def test_threaded_bin_tree_proxy_circular(proxy_tbt_root_circular, regular_tbt_root_circular):
    proxy_tbt = ThreadedBinTreeProxy(root=proxy_tbt_root_circular)
    regular_tbt = ThreadedBinTree(regular_tbt_root_circular)
    assert proxy_tbt.to_regular_object() == regular_tbt
