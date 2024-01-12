from PyCompGeomAlgorithms.core import Point
from PyCompGeomAlgorithms.quickhull import QuickhullNode
from AlgoGrade.adapters import PointPydanticAdapter
from AlgoGrade.quickhull import QuickhullNodePydanticAdapter


def test_quickhull_node_adapter():
    adapter = QuickhullNodePydanticAdapter(
        data=[
            PointPydanticAdapter(coords=(1, 1)),
            PointPydanticAdapter(coords=(2, 2))
        ],
        subhull=[
            PointPydanticAdapter(coords=(1, 1)),
            PointPydanticAdapter(coords=(2, 2))
        ]
    )
    regular_object = QuickhullNode([Point(1, 1), Point(2, 2)], subhull=[Point(1, 1), Point(2, 2)])

    assert adapter.regular_object == regular_object
    assert QuickhullNodePydanticAdapter.from_regular_object(regular_object) == adapter