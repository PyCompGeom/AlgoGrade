import json
from PyCompGeomAlgorithms.core import Point
from .core import GivenJSONParser


class PointListGivenJSONParser(GivenJSONParser):
    @classmethod
    def parse(cls, data):
        return ([Point(*item['coords']) for item in json.loads(data)],)


class PointListAndTargetPointGivenJSONParser(Point):
    @classmethod
    def parse(cls, data):
        points, target_point = json.loads(data)
        return [Point(*item['coords']) for item in points], Point(*target_point['coords'])