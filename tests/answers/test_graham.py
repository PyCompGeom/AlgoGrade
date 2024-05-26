from algogears.core import Point
from algogears.graham import GrahamStepsTableRow, GrahamStepsTable
from AlgoGrade.graham import GrahamAnswers


def test_graham_answers():
    point = Point(coords=(1, 1))
    centroid = point
    ordered_points = [point]
    origin = point
    point_triples = [(point, point, point)]
    are_angles_less_than_pi = [True]
    steps_table = GrahamStepsTable(
        ordered_points=[point],
        rows=[GrahamStepsTableRow(point_triple=(point, point, point), is_angle_less_than_pi=True)]
    )

    answers_model = GrahamAnswers(
        centroid=centroid, ordered_points=ordered_points, origin=origin, point_triples=point_triples,
        are_angles_less_than_pi=are_angles_less_than_pi, steps_table=steps_table
    )
    answers_list = [
        centroid, ordered_points, origin, point_triples,
        are_angles_less_than_pi, steps_table, steps_table, steps_table
    ]

    assert answers_model.to_algogears_list() == answers_list
    assert GrahamAnswers.from_iterable(answers_list) == answers_model
    assert GrahamAnswers(**answers_model.model_dump()) == answers_model
