from algogears.core import Point
from .core import GivenJSONParser


class PointListGivenJSONParser(GivenJSONParser):
    @classmethod
    def parse(cls, data):
        return ([Point.new(*item['coords']) for item in data],)


class PointListAndTargetPointGivenJSONParser(Point):
    @classmethod
    def parse(cls, data):
        points, target_point = data
        return [Point.new(*item['coords']) for item in points], Point.new(*target_point['coords'])