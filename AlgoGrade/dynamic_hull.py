from __future__ import annotations
from functools import partial
from algogears.core import PathDirection, Point
from algogears.dynamic_hull import upper_dynamic_hull, DynamicHullTree
from .core import Task, Grader, Answers, Mistake
from .parsers import PointListAndTargetPointGivenJSONParser


class DynamicHullGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [
            cls.grade_iterable,
            partial(
                cls.grade_bin_tree,
                grade_item_method=lambda a, c, gp: cls.grade_iterable(
                    (a.left_supporting, a.right_supporting),
                    (c.left_supporting, c.right_supporting),
                    gp
                )
            ),
            cls.grade_omitted_points,
            partial(
                cls.grade_bin_tree,
                grade_item_method=lambda a, c, gp: cls.grade_iterable(a.subhull, c.subhull, gp)
            ),
            partial(
                cls.grade_bin_tree,
                grade_item_method=lambda a, c, gp: cls.grade_object(a.left_supporting_index, c.left_supporting_index, gp)
            ),
            partial(
                cls.grade_bin_tree,
                grade_item_method=lambda a, c, gp: cls.grade_iterable(a.optimized_subhull, c.optimized_subhull, gp)
            ),
            cls.grade_iterable,
            partial(cls.grade_iterable, grade_item_method=[cls.grade_modified_tree, cls.grade_iterable])
        ]
    
    @classmethod
    def grade_omitted_points(cls, answer, correct_answer, scorings):
        def grade_item_method(a, c, gp):
            if not a.is_leaf:
                correct_subhull = set(c.subhull)
                correct_left_subhull = set(c.left.subhull)
                correct_right_subhull = set(c.right.subhull)
                correct_omitted_points = (correct_left_subhull | correct_right_subhull) - correct_subhull

                subhull = set(a.subhull)
                if non_omitted_points := subhull & correct_omitted_points:
                    return [Mistake(gp)] * len(non_omitted_points)

            return []
        
        return cls.grade_bin_tree(answer, correct_answer, scorings, grade_item_method)
    
    @classmethod
    def grade_modified_tree(cls, answer, correct_answer, scorings):
        def grade_item_method(a, c, gp):
            return cls.grade_iterable(
                [a.data, a.subhull, a.optimized_subhull, a.left_supporting_index, a.left_supporting, a.right_supporting],
                [c.data, c.subhull, c.optimized_subhull, c.left_supporting_index, c.left_supporting, c.right_supporting],
                gp,
                grade_item_method=[cls.grade_iterable, cls.grade_iterable, cls.grade_object, cls.grade_object, cls.grade_object]
            )
        
        return cls.grade_bin_tree(answer, correct_answer, scorings, grade_item_method)
            



class DynamicHullAnswers(Answers):
    tree: DynamicHullTree
    path: list[PathDirection]
    modified_tree: DynamicHullTree
    hull: list[Point]

    @classmethod
    def from_iterable(cls, iterable):
        _, tree, _, _, _, _, path, (modified_tree, hull), *rest = iterable
        return cls(tree=tree, path=path, modified_tree=modified_tree, hull=hull)
    
    def to_algogears_list(self):
        return [
            self.tree.leaves_inorder(), self.tree, self.tree, self.tree, self.tree,
            self.tree, self.path, (self.modified_tree, self.hull)
        ]


class DynamicHullTask(Task):
    algorithm = upper_dynamic_hull
    grader_class = DynamicHullGrader
    answers_class = DynamicHullAnswers
    given_parser_class = PointListAndTargetPointGivenJSONParser
