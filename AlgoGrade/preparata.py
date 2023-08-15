from functools import partial
from .core import Task, Grader, GradeParams
from PyCompGeomAlgorithms.preparata import preparata


class PreparataTask(Task):
    description = "Construct the convex hull of points using Preparata's algorithm."
    algorithm = preparata


class PreparataGrader(Grader):
    grade_params = [
        GradeParams(max_grade=0.25, fine=0.25),
        GradeParams(max_grade=0.25, fine=0.25, repeat_fine=1.5),
        GradeParams(max_grade=0.25, fine=0.25, repeat_fine=1),
        GradeParams(max_grade=0.25, fine=0.25, repeat_fine=1.5)
    ]

    @classmethod
    def grade_methods(cls):
        return [
            cls.grade_iterable,
            partial(cls.grade_iterable, grade_item_method=partial(cls.grade_iterable, grade_item_method=cls.grade_iterable)),
            partial(cls.grade_iterable, grade_item_method=cls.grade_iterable),
            partial(cls.grade_iterable, grade_item_method=(cls.grade_iterable, partial(cls.grade_iterable, grade_item_method=cls.grade_bin_tree)))
        ]
