from __future__ import annotations
from functools import partial
from algogears.core import Point
from algogears.quickhull import quickhull, QuickhullTree
from .core import Task, Grader, Mistake, Answers
from .parsers import PointListGivenJSONParser


class QuickhullGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [
            cls.grade_iterable,
            partial(cls.grade_bin_tree, grade_item_method=lambda a, c, gp: cls.grade_object(a.h, c.h, gp)),
            partial(cls.grade_bin_tree, grade_item_method=lambda a, c, gp: cls.grade_iterable(a.points, c.points, gp)),
            cls.grade_finalization,
            partial(cls.grade_bin_tree, grade_item_method=lambda a, c, gp: cls.grade_iterable(a.subhull, c.subhull, gp))
        ]
    
    @classmethod
    def grade_finalization(cls, answer, correct_answer, scorings):
        return [Mistake(scorings) for node in answer.traverse_preorder() if not node.is_leaf and len(node.points) == 2]


class QuickhullAnswers(Answers):
    leftmost_point: Point
    rightmost_point: Point
    subset1: list[Point]
    subset2: list[Point]
    tree: QuickhullTree

    @classmethod
    def from_iterable(cls, iterable):
        (leftmost_point, rightmost_point, subset1, subset2), tree, *rest = iterable
        return cls(
            leftmost_point=leftmost_point, rightmost_point=rightmost_point,
            subset1=subset1, subset2=subset2, tree=tree
        )
    
    def to_algogears_list(self):
        return [
            (self.leftmost_point, self.rightmost_point, self.subset1, self.subset2),
            self.tree, self.tree, self.tree, self.tree
        ]


class QuickhullTask(Task):
    algorithm = quickhull
    grader_class = QuickhullGrader
    answers_class = QuickhullAnswers
    given_parser_class = PointListGivenJSONParser