from functools import partial
from .core import Task, Grader, Scoring
from PyCompGeomAlgorithms.preparata import preparata


class PreparataTask(Task):
    description = "Construct the convex hull of points using Preparata's algorithm."
    algorithm = preparata


class PreparataGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [
            cls.grade_iterable,
            partial(cls.grade_iterable, grade_item_method=partial(cls.grade_iterable, grade_item_method=cls.grade_iterable)),
            partial(cls.grade_iterable, grade_item_method=cls.grade_iterable),
            partial(cls.grade_iterable, grade_item_method=(cls.grade_iterable, partial(cls.grade_iterable, grade_item_method=cls.grade_bin_tree)))
        ]
