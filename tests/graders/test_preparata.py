from math import isclose
from copy import deepcopy
from algogears.core import Point, PathDirection
from algogears.preparata import PreparataThreadedBinTree
from AlgoGrade.preparata import PreparataGrader, PreparataTask, PreparataAnswers
from AlgoGrade.core import Scoring


points = [Point.new(1, 1), Point.new(1, 5), Point.new(5, 3), Point.new(1, 11), Point.new(6, 1), Point.new(10, 1)]
givens = (points,)
task_class = PreparataTask
scorings = [
    Scoring(max_grade=0.25, fine=0.25),
    Scoring(max_grade=0.25, fine=0.25, repeat_fine=1.5),
    Scoring(max_grade=0.25, fine=0.25, repeat_fine=1),
    Scoring(max_grade=0.25, fine=0.25, repeat_fine=1.5)
]
correct_algogears_answers = task_class.solve_as_algogears_list(givens)
correct_answers_wrapper = task_class.solve_as_answers_wrapper(givens)


def test_preparata_all_correct():
    hull0 = [Point.new(1, 1), Point.new(1, 5), Point.new(5, 3)]
    hull = [Point.new(1, 1), Point.new(1, 11), Point.new(10, 1)]
    tree0 = PreparataThreadedBinTree.from_iterable(hull0)
    left_paths = [
        [PathDirection.right],
        [PathDirection.right, PathDirection.right],
        [PathDirection.right, PathDirection.right]
    ]
    right_paths = [
        [PathDirection.left],
        [],
        []
    ]
    left_supporting_points = [
        Point.new(5, 3),
        Point.new(1, 1),
        Point.new(1, 1)
    ]
    right_supporting_points = [
        Point.new(1, 1),
        Point.new(1, 11),
        Point.new(1, 11)
    ]
    deleted_points = [[Point.new(1, 5)], [Point.new(5, 3)], [Point.new(6, 1)]]
    hulls = [
        [Point.new(1, 1), Point.new(1, 11), Point.new(5, 3)],
        [Point.new(1, 1), Point.new(1, 11), Point.new(6, 1)],
        hull
    ]
    trees = [PreparataThreadedBinTree.from_iterable(hulls[0]), PreparataThreadedBinTree.from_iterable(hulls[1])]

    algogears_answers = [(hull0, tree0), ((left_paths, left_supporting_points), (right_paths, right_supporting_points)), deleted_points, (hulls, trees)]
    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 1)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 1)


def test_preparata_grader_incorrect_first_hull():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    first_hull = algogears_answers[0][0]
    first_hull[0] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_first_tree():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    first_tree = algogears_answers[0][1]
    first_tree.root.data = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_left_paths_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    left_paths = algogears_answers[1][0][0]
    left_paths[0][0] = PathDirection.left

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_left_paths_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    left_paths = algogears_answers[1][0][0]
    left_paths[1][0] = PathDirection.left
    left_paths[1][1] = PathDirection.left

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_right_paths_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    right_paths = algogears_answers[1][1][0]
    right_paths[0][0] = PathDirection.right

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_right_paths_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    right_paths = algogears_answers[1][1][0]
    right_paths[0][0] = PathDirection.right
    right_paths[1].append(PathDirection.right)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_left_and_right_paths():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    left_paths = algogears_answers[1][0][0]
    right_paths = algogears_answers[1][1][0]
    left_paths[0][0] = PathDirection.left
    right_paths[0][0] = PathDirection.right

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_left_supporting_points_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    left_supporting_points = algogears_answers[1][0][1]
    left_supporting_points[0] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_left_supporting_points_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    left_supporting_points = algogears_answers[1][0][1]
    left_supporting_points[0] = Point.new(100, 100)
    left_supporting_points[1] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_right_supporting_points_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    right_supporting_points = algogears_answers[1][1][1]
    right_supporting_points[0] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_right_supporting_points_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    right_supporting_points = algogears_answers[1][1][1]
    right_supporting_points[0] = Point.new(100, 100)
    right_supporting_points[1] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_left_and_right_supporting_points():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    left_supporting_points = algogears_answers[1][0][1]
    right_supporting_points = algogears_answers[1][1][1]
    left_supporting_points[0] = Point.new(100, 100)
    right_supporting_points[0] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_left_paths_and_left_supporting_points():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    left_paths, left_supporting_points = algogears_answers[1][0]
    left_paths[0][0] = PathDirection.left
    left_supporting_points[0] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_left_paths_and_right_supporting_points():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    left_paths = algogears_answers[1][0][0]
    right_supporting_points = algogears_answers[1][1][1]
    left_paths[0][0] = PathDirection.left
    right_supporting_points[0] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_right_paths_and_left_supporting_points():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    right_paths = algogears_answers[1][1][0]
    left_supporting_points = algogears_answers[1][0][1]
    right_paths[0][0] = PathDirection.right
    left_supporting_points[0] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_right_paths_and_right_supporting_points():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    right_paths, right_supporting_points = algogears_answers[1][1]
    right_paths[0][0] = PathDirection.right
    right_supporting_points[0] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_deleted_points_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    deleted_points = algogears_answers[2]
    deleted_points[0][0] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_deleted_points_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    deleted_points = algogears_answers[2]
    deleted_points[0][0] = Point.new(100, 100)
    deleted_points[1][0] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 0)


def test_preparata_grader_incorrect_hulls_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    hulls = algogears_answers[3][0]
    hulls[0][0] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_hulls_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    hulls = algogears_answers[3][0]
    hulls[0][0] = Point.new(100, 100)
    hulls[1][1] = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_trees_single():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    trees = algogears_answers[3][1]
    trees[0].root.left.data = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, 0.75)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, 0.75)


def test_preparata_grader_incorrect_trees_repeated():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    trees = algogears_answers[3][1]
    trees[0].root.data = Point.new(100, 100)
    trees[0].root.left.data = Point.new(-1, -1)
    trees[1].root.data = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_incorrect_trees_and_hulls():
    algogears_answers = deepcopy(correct_algogears_answers)
    
    hulls = algogears_answers[3][0]
    hulls[0][0] = Point.new(100, 100)
    hulls[1][1] = Point.new(100, 100)
    
    trees = algogears_answers[3][1]
    trees[0].root.data = Point.new(100, 100)
    trees[0].root.left.data = Point.new(-1, -1)
    trees[1].root.data = Point.new(100, 100)

    answers_wrapper = PreparataAnswers.from_iterable(algogears_answers)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert isclose(total_grade, -0.5)

    total_grade, answer_grades = PreparataGrader.grade_answers_wrapper(answers_wrapper, correct_answers_wrapper, scorings)
    assert isclose(total_grade, -0.5)


def test_preparata_grader_jsons_correct_answers():
    answers = PreparataAnswers(**{
        "tree": {
            "root": {
                "data": {
                    "coords": [
                        3,
                        3
                    ]
                },
                "left": {
                    "data": {
                        "coords": [
                            0,
                            0
                        ]
                    },
                    "next": 1,
                    "prev": 2
                },
                "right": {
                    "data": {
                        "coords": [
                            7,
                            0
                        ]
                    },
                    "prev": 1,
                    "next": 0
                },
                "prev": 0,
                "next": 2
            }
        },
        "hull": [
            {
                "coords": [
                    0,
                    0
                ]
            },
            {
                "coords": [
                    3,
                    3
                ]
            },
            {
                "coords": [
                    7,
                    0
                ]
            }
        ],
        "trees": [
            {
                "root": {
                    "data": {
                        "coords": [
                            7,
                            9
                        ]
                    },
                    "left": {
                        "data": {
                            "coords": [
                                0,
                                0
                            ]
                        },
                        "next": 1,
                        "prev": 2
                    },
                    "right": {
                        "data": {
                            "coords": [
                                7,
                                0
                            ]
                        },
                        "prev": 1,
                        "next": 0
                    },
                    "prev": 0,
                    "next": 2
                }
            }
        ],
        "hulls": [
            [
                {
                    "coords": [
                        0,
                        0
                    ]
                },
                {
                    "coords": [
                        7,
                        9
                    ]
                },
                {
                    "coords": [
                        7,
                        0
                    ]
                }
            ],
            [
                {
                    "coords": [
                        0,
                        0
                    ]
                },
                {
                    "coords": [
                        7,
                        9
                    ]
                },
                {
                    "coords": [
                        10,
                        8
                    ]
                },
                {
                    "coords": [
                        7,
                        0
                    ]
                }
            ]
        ],
        "left_paths": [
            [
                "right"
            ],
            [
                "right"
            ]
        ],
        "right_paths": [
            [
                "left"
            ],
            []
        ],
        "left_supporting_points": [
            {
                "coords": [
                    7,
                    0
                ]
            },
            {
                "coords": [
                    7,
                    0
                ]
            }
        ],
        "right_supporting_points": [
            {
                "coords": [
                    0,
                    0
                ]
            },
            {
                "coords": [
                    7,
                    9
                ]
            }
        ],
        "deleted_points_lists": [
            [
                {
                    "coords": [
                        3,
                        3
                    ]
                }
            ],
            []
        ]
    })
    correct_answers = PreparataAnswers(**{
        "hull": [
            {
                "coords": [
                    0,
                    0
                ]
            },
            {
                "coords": [
                    3,
                    3
                ]
            },
            {
                "coords": [
                    7,
                    0
                ]
            }
        ],
        "tree": {
            "root": {
                "data": {
                    "coords": [
                        3,
                        3
                    ]
                },
                "left": {
                    "data": {
                        "coords": [
                            0,
                            0
                        ]
                    },
                    "left": None,
                    "right": None,
                    "prev": 2,
                    "next": 1
                },
                "right": {
                    "data": {
                        "coords": [
                            7,
                            0
                        ]
                    },
                    "left": None,
                    "right": None,
                    "prev": 1,
                    "next": 0
                },
                "prev": 0,
                "next": 2
            }
        },
        "left_paths": [
            [
                "right"
            ],
            [
                "right"
            ]
        ],
        "right_paths": [
            [
                "left"
            ],
            []
        ],
        "left_supporting_points": [
            {
                "coords": [
                    7,
                    0
                ]
            },
            {
                "coords": [
                    7,
                    0
                ]
            }
        ],
        "right_supporting_points": [
            {
                "coords": [
                    0,
                    0
                ]
            },
            {
                "coords": [
                    7,
                    9
                ]
            }
        ],
        "deleted_points_lists": [
            [
                {
                    "coords": [
                        3,
                        3
                    ]
                }
            ],
            []
        ],
        "hulls": [
            [
                {
                    "coords": [
                        0,
                        0
                    ]
                },
                {
                    "coords": [
                        7,
                        9
                    ]
                },
                {
                    "coords": [
                        7,
                        0
                    ]
                }
            ],
            [
                {
                    "coords": [
                        0,
                        0
                    ]
                },
                {
                    "coords": [
                        7,
                        9
                    ]
                },
                {
                    "coords": [
                        10,
                        8
                    ]
                },
                {
                    "coords": [
                        7,
                        0
                    ]
                }
            ]
        ],
        "trees": [
            {
                "root": {
                    "data": {
                        "coords": [
                            7,
                            9
                        ]
                    },
                    "left": {
                        "data": {
                            "coords": [
                                0,
                                0
                            ]
                        },
                        "left": None,
                        "right": None,
                        "prev": 2,
                        "next": 1
                    },
                    "right": {
                        "data": {
                            "coords": [
                                7,
                                0
                            ]
                        },
                        "left": None,
                        "right": None,
                        "prev": 1,
                        "next": 0
                    },
                    "prev": 0,
                    "next": 2
                }
            }
        ]
    })

    score, _ = PreparataGrader.grade_answers_wrapper(answers, correct_answers, scorings)
    assert isclose(score, 1.0)