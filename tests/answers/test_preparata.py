from AlgoGrade.adapters import PointPydanticAdapter, ThreadedBinTreePydanticAdapter, ThreadedBinTreeNodePydanticAdapter, pydantic_to_pycga
from AlgoGrade.preparata import PreparataAnswers


def test_preparata_answers():
    point = PointPydanticAdapter(coords=(1, 1))
    hull = [point]
    tree = ThreadedBinTreePydanticAdapter(root=ThreadedBinTreeNodePydanticAdapter(data=point))
    left_paths, right_paths = [point], [point]
    deleted_points = []
    hulls, trees = [hull], [tree]

    answers_model = PreparataAnswers(
        hull=hull, tree=tree, left_paths=left_paths, right_paths=right_paths,
        deleted_points=deleted_points, hulls=hulls, trees=trees
    )
    answers_list_args = [hull, tree, left_paths, right_paths, deleted_points, hulls, trees]
    answers_list_ret = [(hull, tree), (left_paths, right_paths), deleted_points, (hulls, trees)]

    assert answers_model.to_pydantic_list() == answers_list_ret
    assert answers_model.to_pycga_list() == pydantic_to_pycga(answers_list_ret)
    assert PreparataAnswers.from_iterable(answers_list_args) == answers_model
