from PyCompGeomAlgorithms.core import Point
from AlgoGrade.parsers import PointListGivenJSONParser


def test_point_list_parser():
    points = [Point(1, 1), Point(2, 2)]
    string = '[{"coords": [1, 1]}, {"coords": [2, 2]}]'

    assert PointListGivenJSONParser.parse(string) == (points,)