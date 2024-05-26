from algogears.core import Point
from algogears.quickhull import QuickhullNode, QuickhullTree
from AlgoGrade.quickhull import QuickhullAnswers


def test_quickhull_answers():
    point = Point(coords=(1, 1))
    leftmost_point, rightmost_point = point, point
    subset1, subset2 = [point], [point]
    tree = QuickhullTree(root=QuickhullNode(data=[point]))

    answers_model = QuickhullAnswers(
        leftmost_point=leftmost_point, rightmost_point=rightmost_point,
        subset1=subset1, subset2=subset2, tree=tree
    )
    answers_list = [(leftmost_point, rightmost_point, subset1, subset2), tree, tree, tree, tree]

    assert answers_model.to_algogears_list() == answers_list
    assert QuickhullAnswers.from_iterable(answers_list) == answers_model
    assert QuickhullAnswers(**answers_model.model_dump()) == answers_model
