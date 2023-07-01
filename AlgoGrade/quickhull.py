from functools import partial
from .core import Task, Grader, GradeParams, Mistake
from PyCompGeomAlgorithms.quickhull import quickhull


class QuickhullTask(Task):
    description = "Construct the convex hull of points using Quickhull algorithm."
    algorithm = quickhull


class QuickhullGrader(Grader):
    grade_params = [
        GradeParams(max_grade=0.25, fine=0.25),
        GradeParams(max_grade=0.25, fine=0.25, repeat_fine=0.5),
        GradeParams(max_grade=0.25, fine=0.25),
        GradeParams(max_grade=0.25, fine=0.25),
        GradeParams(max_grade=1, fine=1)
    ]

    @classmethod
    def grade_methods(cls):
        return [
            cls.grade_iterable,
            partial(cls.grade_bin_tree, grade_item=lambda a, c, gp: cls.grade_default(a.h, c.h, gp)),
            partial(cls.grade_bin_tree, grade_item=lambda a, c, gp: cls.grade_iterable(a.points, c.points, gp)),
            cls.grade_finalization,
            partial(cls.grade_bin_tree, grade_item=lambda a, c, gp: cls.grade_iterable(a.subhull, c.subhull, gp))
        ]
    
    @classmethod
    def grade_finalization(cls, answer, correct_answer, grade_params):
        return [Mistake(grade_params) for node in answer.traverse_preorder() if not node.is_leaf and len(node.points) == 2]
