from functools import partial
from PyCompGeomAlgorithms.preparata import preparata
from .core import Task, Grader, Answers
from .adapters import PointPydanticAdapter, ThreadedBinTreePydanticAdapter
from .parsers import PointListGivenJSONParser


class PreparataGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [
            cls.grade_iterable,
            partial(cls.grade_iterable, grade_item_method=partial(cls.grade_iterable, grade_item_method=cls.grade_iterable)),
            partial(cls.grade_iterable, grade_item_method=cls.grade_iterable),
            partial(cls.grade_iterable, grade_item_method=(cls.grade_iterable, partial(cls.grade_iterable, grade_item_method=cls.grade_bin_tree)))
        ]


class PreparataAnswers(Answers):
    hull: list[PointPydanticAdapter]
    tree: ThreadedBinTreePydanticAdapter
    left_paths: list[PointPydanticAdapter]
    right_paths: list[PointPydanticAdapter]
    deleted_points: list[PointPydanticAdapter]
    hulls: list[list[PointPydanticAdapter]]
    trees: list[ThreadedBinTreePydanticAdapter]

    @classmethod
    def from_iterable(cls, iterable):
        hull, tree, left_paths, right_paths, deleted_points, hulls, trees, *rest = iterable
        return cls(
            hull=hull, tree=tree, left_paths=left_paths, right_paths=right_paths,
            deleted_points=deleted_points, hulls=hulls, trees=trees
        )
    
    def to_pydantic_list(self):
        return [
            (self.hull, self.tree), (self.left_paths, self.right_paths),
            self.deleted_points, (self.hulls, self.trees)
        ]


class PreparataTask(Task):
    algorithm = preparata
    grader_class = PreparataGrader
    answers_class = PreparataAnswers
    given_parser_class = PointListGivenJSONParser
