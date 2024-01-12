from PyCompGeomAlgorithms.core import Point
from PyCompGeomAlgorithms.graham import GrahamStepsTableRow, GrahamStepsTable
from AlgoGrade.adapters import PointPydanticAdapter
from AlgoGrade.graham import GrahamStepsTableRowPydanticAdapter, GrahamStepsTablePydanticAdapter


def test_steps_table_row_adapter():
    adapter = GrahamStepsTableRowPydanticAdapter(
        point_triple=(
            PointPydanticAdapter(coords=(1, 1)),
            PointPydanticAdapter(coords=(2, 2)),
            PointPydanticAdapter(coords=(3, 3))
        ),
        is_angle_less_than_pi=True
    )
    regular_object = GrahamStepsTableRow((Point(1, 1), Point(2, 2), Point(3, 3)), True)

    assert adapter.regular_object == regular_object
    assert GrahamStepsTableRowPydanticAdapter.from_regular_object(regular_object) == adapter


def test_steps_table_adapter():
    adapter = GrahamStepsTablePydanticAdapter(
        ordered_points=[PointPydanticAdapter(coords=(1, 1))],
        rows=[
            GrahamStepsTableRowPydanticAdapter(
                point_triple=(
                    PointPydanticAdapter(coords=(1, 1)),
                    PointPydanticAdapter(coords=(2, 2)),
                    PointPydanticAdapter(coords=(3, 3))
                ),
                is_angle_less_than_pi=True
            )
        ]
    )
    regular_object = GrahamStepsTable(
        [Point(1, 1)],
        [GrahamStepsTableRow((Point(1, 1), Point(2, 2), Point(3, 3)), True)]
    )

    assert adapter.regular_object == regular_object
    assert GrahamStepsTablePydanticAdapter.from_regular_object(regular_object) == adapter
