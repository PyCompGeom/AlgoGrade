from typing import ClassVar
from PyCompGeomAlgorithms.graham import graham, GrahamStepsTableRow, GrahamStepsTable
from .adapters import pycga_to_pydantic, PydanticAdapter, PointPydanticAdapter
from .core import Task, Grader, Scoring, Mistake


class GrahamTask(Task):
    description = "Construct the convex hull of points using Graham's scan."
    algorithm = graham


class GrahamGrader(Grader):
    scorings = [
        Scoring(max_grade=0.25, fine=0.25),
        Scoring(max_grade=0.25, fine=0.25),
        Scoring(max_grade=0.25, fine=0.25),
        Scoring(max_grade=0.15, fine=0.15),
        Scoring(max_grade=0.15, fine=0.15),
        Scoring(max_grade=0.25, fine=0.25),
        Scoring(max_grade=0.6, fine=0.3, repeat_fine=0.6),
        Scoring(max_grade=0.1, fine=0.25)
    ]

    @classmethod
    def grade_methods(cls):
        return [
            cls.grade_default,
            cls.grade_iterable,
            cls.grade_default,
            cls.grade_iterable,
            cls.grade_iterable,
            cls.grade_angles_less_than_pi,
            cls.grade_angles_greater_than_or_equal_to_pi,
            cls.grade_finalization
        ]
    
    @classmethod
    def grade_angles_less_than_pi(cls, answer, correct_answer, scorings):
        return [
            Mistake(scorings)
            for row, next_row in zip(answer, answer[1:])
            if row.is_angle_less_than_pi and (
                row.point_triple[1] != next_row.point_triple[0] or
                row.point_triple[2] != next_row.point_triple[1] or
                next_row.point_triple[2] != cls._next_point(answer.ordered_points, row.point_triple[2])
            )
        ]
    
    @classmethod
    def grade_angles_greater_than_or_equal_to_pi(cls, answer, correct_answer, scorings):
        return [
            Mistake(scorings)
            for row, next_row in zip(answer, answer[1:])
            if not row.is_angle_less_than_pi and (
                (
                    row.point_triple[0] != next_row.point_triple[0] or
                    row.point_triple[2] != next_row.point_triple[1] or
                    next_row.point_triple[2] != cls._next_point(answer.ordered_points, next_row.point_triple[1])
                ) if row.point_triple[0] == answer.ordered_points[0] else
                (
                    row.point_triple[0] != next_row.point_triple[1] or
                    row.point_triple[2] != next_row.point_triple[2] or
                    next_row.point_triple[0] != cls._prev_point(answer.rows, next_row)
                )
            )
        ]

    @classmethod
    def grade_finalization(cls, answer, correct_answer, scorings):
        return [
            Mistake(scorings)
            for row in answer
            if row.point_triple[1] == answer.ordered_points[0]
        ]
    
    @staticmethod
    def _prev_point(rows, row):
        i = rows.index(row)

        try:
            return next(r for r in reversed(rows[:i]) if r.point_triple[1] == row.point_triple[1]).point_triple[0]
        except StopIteration:
            return None
    
    @staticmethod
    def _next_point(ordered_points, point):
        try:
            return ordered_points[(ordered_points.index(point)+1) % len(ordered_points)]
        except (IndexError, ValueError):
            return None


class GrahamStepsTableRowPydanticAdapter(PydanticAdapter):
    regular_class: ClassVar[type] = GrahamStepsTableRow
    point_triple: tuple[PointPydanticAdapter, PointPydanticAdapter, PointPydanticAdapter]
    is_angle_less_than_pi: bool

    @classmethod
    def from_regular_object(cls, obj: GrahamStepsTableRow, **kwargs):
        return cls(
            point_triple=pycga_to_pydantic(obj.point_triple),
            is_angle_less_than_pi=obj.is_angle_less_than_pi,
            **kwargs
        )


class GrahamStepsTablePydanticAdapter(PydanticAdapter):
    regular_class: ClassVar[type] = GrahamStepsTable
    ordered_points: list[PointPydanticAdapter]
    rows: list[GrahamStepsTableRowPydanticAdapter]

    @classmethod
    def from_regular_object(cls, obj: GrahamStepsTable, **kwargs):
        return cls(
            ordered_points=pycga_to_pydantic(obj.ordered_points),
            rows=pycga_to_pydantic(obj.rows),
            **kwargs
        )
