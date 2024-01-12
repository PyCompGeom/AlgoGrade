from functools import partial, cached_property
from typing import ClassVar, Optional

from PyCompGeomAlgorithms.core import BinTreeNode
from .adapters import pycga_to_pydantic, PointPydanticAdapter, BinTreeNodePydanticAdapter
from .core import Task, Grader, Scoring, Mistake
from PyCompGeomAlgorithms.quickhull import quickhull, QuickhullNode


class QuickhullTask(Task):
    description = "Construct the convex hull of points using Quickhull algorithm."
    algorithm = quickhull


class QuickhullGrader(Grader):
    grade_params = [
        Scoring(max_grade=0.25, fine=0.25),
        Scoring(max_grade=0.25, fine=0.25, repeat_fine=0.5),
        Scoring(max_grade=0.25, fine=0.25),
        Scoring(max_grade=0.25, fine=0.25),
        Scoring(max_grade=1, fine=1)
    ]

    @classmethod
    def grade_methods(cls):
        return [
            cls.grade_iterable,
            partial(cls.grade_bin_tree, grade_item_method=lambda a, c, gp: cls.grade_default(a.h, c.h, gp)),
            partial(cls.grade_bin_tree, grade_item_method=lambda a, c, gp: cls.grade_iterable(a.points, c.points, gp)),
            cls.grade_finalization,
            partial(cls.grade_bin_tree, grade_item_method=lambda a, c, gp: cls.grade_iterable(a.subhull, c.subhull, gp))
        ]
    
    @classmethod
    def grade_finalization(cls, answer, correct_answer, grade_params):
        return [Mistake(grade_params) for node in answer.traverse_preorder() if not node.is_leaf and len(node.points) == 2]


class QuickhullNodePydanticAdapter(BinTreeNodePydanticAdapter):
    regular_class: ClassVar[type] = QuickhullNode
    h: Optional[PointPydanticAdapter] = None
    subhull: Optional[list[PointPydanticAdapter]] = None

    @classmethod
    def from_regular_object(cls, obj: QuickhullNode, **kwargs):
        return super().from_regular_object(
            obj,
            h=pycga_to_pydantic(obj.h),
            subhull=pycga_to_pydantic(obj.subhull),
            **kwargs
        )