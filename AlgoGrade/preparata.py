from __future__ import annotations
from functools import partial
from algogears.core import PathDirection, Point
from algogears.preparata import preparata, PreparataThreadedBinTree
from .core import Task, Grader, Answers
from .parsers import PointListGivenJSONParser


class PreparataGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [
            partial(cls.grade_iterable, grade_item_method=[cls.grade_iterable, cls.grade_threaded_bin_tree]),
            # ((left_paths, left_supporting_points), (right_paths, right_supporting_points)) -> paths is a list of lists of directions, supporting points is a list of points.
            partial(cls.grade_iterable, grade_item_method=partial(cls.grade_iterable, grade_item_method=[partial(cls.grade_iterable, grade_item_method=cls.grade_iterable), cls.grade_iterable])),
            partial(cls.grade_iterable, grade_item_method=cls.grade_iterable),
            partial(cls.grade_iterable, grade_item_method=[cls.grade_iterable, partial(cls.grade_iterable, grade_item_method=cls.grade_threaded_bin_tree)])
        ]


class PreparataAnswers(Answers):
    hull: list[Point]
    tree: PreparataThreadedBinTree
    left_paths: list[list[PathDirection]]
    right_paths: list[list[PathDirection]]
    left_supporting_points: list[Point]
    right_supporting_points: list[Point]
    deleted_points_lists: list[list[Point]]
    hulls: list[list[Point]]
    trees: list[PreparataThreadedBinTree]

    @classmethod
    def from_iterable(cls, iterable):
        (hull, tree), ((left_paths, left_supporting_points), (right_paths, right_supporting_points)), deleted_points_lists, (hulls, trees), *rest = iterable
        return cls(
            hull=hull, tree=tree, left_paths=left_paths, right_paths=right_paths,
            left_supporting_points=left_supporting_points, right_supporting_points=right_supporting_points,
            deleted_points_lists=deleted_points_lists, hulls=hulls, trees=trees
        )
    
    def to_algogears_list(self):
        return [
            (self.hull, self.tree),
            ((self.left_paths, self.left_supporting_points), (self.right_paths, self.right_supporting_points)),
            self.deleted_points_lists,
            (self.hulls, self.trees)
        ]


class PreparataTask(Task):
    algorithm = preparata
    grader_class = PreparataGrader
    answers_class = PreparataAnswers
    given_parser_class = PointListGivenJSONParser
