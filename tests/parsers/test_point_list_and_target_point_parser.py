from PyCompGeomAlgorithms.core import Point
from AlgoGrade.parsers import PointListAndTargetPointGivenJSONParser


def test_point_list_parser():
    points = [Point(1, 1), Point(2, 2)]
    target_point = Point(3, 3)
    string = '[[{"coords": [1, 1]}, {"coords": [2, 2]}], {"coords": [3, 3]}]'

    assert PointListAndTargetPointGivenJSONParser.parse(string) == (points, target_point)