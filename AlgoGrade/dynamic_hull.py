from functools import partial
from typing import ClassVar, Optional
from PyCompGeomAlgorithms.core import BinTree, BinTreeNode, ThreadedBinTree, ThreadedBinTreeNode
from PyCompGeomAlgorithms.dynamic_hull import upper_dynamic_hull, DynamicHullNode, DynamicHullTree, SubhullNode, SubhullThreadedBinTree
from .adapters import pycga_to_pydantic, PointPydanticAdapter, BinTreeNodePydanticAdapter, BinTreePydanticAdapter, ThreadedBinTreeNodePydanticAdapter, ThreadedBinTreePydanticAdapter
from .core import Task, Grader, GradeParams, Mistake


class DynamicHullTask(Task):
    description = "Construct the upper convex hull of points using Preparata's algorithm. Modify it by adding or deleting a specified point."
    algorithm = upper_dynamic_hull


class DynamicHullGrader(Grader):
    grade_params = [
        GradeParams(max_grade=0.25, fine=0.25),
        GradeParams(max_grade=0.5, fine=0.25, repeat_fine=0.5),
        GradeParams(max_grade=0.25, fine=0.25),
        GradeParams(max_grade=0.5, fine=0.25, repeat_fine=0.5),
        GradeParams(max_grade=0.25, fine=0.25, repeat_fine=0.5),
        GradeParams(max_grade=0.25, fine=0.25),
        GradeParams(max_grade=0.25, fine=0.25),
        GradeParams(max_grade=0.75, fine=0.25, repeat_fine=0.75)
    ]

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
                grade_item_method=lambda a, c, gp: cls.grade_iterable(
                    [n.point for n in a.subhull.traverse_inorder()],
                    [n.point for n in c.subhull.traverse_inorder()],
                    gp
                )
            ),
            partial(
                cls.grade_bin_tree,
                grade_item_method=lambda a, c, gp: cls.grade_default(a.point, c.point, gp)
            ),
            partial(
                cls.grade_bin_tree,
                grade_item_method=lambda a, c, gp: cls.grade_iterable(
                    a.optimized_subhull.traverse_inorder(),
                    c.optimized_subhull.traverse_inorder(),
                    gp
                )
            ),
            cls.grade_iterable,
            partial(cls.grade_iterable, grade_item_method=[cls.grade_bin_tree, cls.grade_iterable])
        ]
    
    @classmethod
    def grade_omitted_points(cls, answer, correct_answer, grade_params):
        def grade_item_method(a, c, gp):
            if not a.is_leaf:
                subhull = [node.point for node in a.subhull.traverse_inorder()]
                left_subhull = [node.point for node in a.left.subhull.traverse_inorder()]
                right_subhull = [node.point for node in a.right.subhull.traverse_inorder()]
                
                try:
                    left_omitted_points = set([point for point in left_subhull[left_subhull.index(a.left_supporting)+1:]])
                    right_omitted_points = set([point for point in right_subhull[:right_subhull.index(a.right_supporting)]])

                    subhull = set(subhull)
                    if subhull & (left_omitted_points | right_omitted_points):
                        return [Mistake(gp)]
                except (IndexError, ValueError):
                    return [Mistake(gp)]

            return []
        
        return cls.grade_bin_tree(answer, correct_answer, grade_params, grade_item_method)


class DynamicHullNodePydanticAdapter(BinTreeNodePydanticAdapter):
    regular_class: ClassVar[type] = DynamicHullNode
    subhull_points: list[PointPydanticAdapter]
    optimized_subhull_points: Optional[list[PointPydanticAdapter]] = None
    left_supporting_index: int = 0
    left_supporting: PointPydanticAdapter
    right_supporting: PointPydanticAdapter

    @classmethod
    def from_regular_object(cls, obj: DynamicHullNode, **kwargs):
        return super().from_regular_object(
            obj,
            subhull_points=pycga_to_pydantic(node.point for node in obj.subhull.traverse_inorder()),
            optimized_subhull_points=pycga_to_pydantic(node.point for node in obj.optimized_subhull.traverse_inorder()),
            left_supporting_index=obj.left_supporting_index,
            left_supporting=pycga_to_pydantic(obj.left_supporting),
            right_supporting=pycga_to_pydantic(obj.right_supporting),
            **kwargs
        )


class DynamicHullTreePydanticAdapter(BinTreePydanticAdapter):
    regular_class: ClassVar[type] = DynamicHullTree
    root: DynamicHullNodePydanticAdapter

    @classmethod
    def from_regular_object(cls, obj: DynamicHullTree, **kwargs):
        return super().from_regular_object(obj, **kwargs)


class SubhullNodePydanticAdapter(ThreadedBinTreeNodePydanticAdapter):
    regular_class: ClassVar[type] = SubhullNode

    @classmethod
    def from_regular_object(cls, obj: SubhullNode, **kwargs):
        return super().from_regular_object(obj, **kwargs)


class SubhullThreadedBinTreePydanticAdapter(ThreadedBinTreePydanticAdapter):
    regular_class: ClassVar[type] = SubhullThreadedBinTree
    root: SubhullNodePydanticAdapter

    @classmethod
    def from_regular_object(cls, obj: SubhullThreadedBinTree, **kwargs):
        return super().from_regular_object(obj, **kwargs)
