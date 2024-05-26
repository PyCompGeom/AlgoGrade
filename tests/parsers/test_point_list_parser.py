from algogears.core import Point
from AlgoGrade.parsers import PointListGivenJSONParser


def test_point_list_parser():
    points = [Point.new(1, 1), Point.new(2, 2)]
    data = [{"coords": [1, 1]}, {"coords": [2, 2]}]

    assert PointListGivenJSONParser.parse(data) == (points,)