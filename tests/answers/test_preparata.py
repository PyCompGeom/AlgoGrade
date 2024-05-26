from algogears.core import PathDirection, Point
from algogears.preparata import PreparataNode, PreparataThreadedBinTree
from AlgoGrade.preparata import PreparataAnswers


def test_preparata_answers():
    point = Point(coords=(1, 1))
    hull = [point]
    tree = PreparataThreadedBinTree(root=PreparataNode(data=point))
    left_paths, right_paths = [[PathDirection.left]], [[PathDirection.right]]
    left_supporting_points, right_supporting_points = [point], [point]
    deleted_points = []
    hulls, trees = [hull], [tree]

    answers_model = PreparataAnswers(
        hull=hull, tree=tree, left_paths=left_paths, right_paths=right_paths,
        left_supporting_points=left_supporting_points, right_supporting_points=right_supporting_points,
        deleted_points_lists=deleted_points, hulls=hulls, trees=trees
    )
    answers_list = [(hull, tree), ((left_paths, left_supporting_points), (right_paths, right_supporting_points)), deleted_points, (hulls, trees)]

    assert answers_model.to_algogears_list() == answers_list
    assert PreparataAnswers.from_iterable(answers_list) == answers_model
    assert PreparataAnswers(**answers_model.model_dump()) == answers_model
