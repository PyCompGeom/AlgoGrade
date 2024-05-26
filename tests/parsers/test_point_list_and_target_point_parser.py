from algogears.core import Point
from AlgoGrade.parsers import PointListAndTargetPointGivenJSONParser


def test_point_list_parser():
    points = [Point.new(1, 1), Point.new(2, 2)]
    target_point = Point.new(3, 3)
    data = [[{"coords": [1, 1]}, {"coords": [2, 2]}], {"coords": [3, 3]}]

    assert PointListAndTargetPointGivenJSONParser.parse(data) == (points, target_point)