from AlgoGrade.core import GradeParams, Grader


class MockGrader(Grader):
    grade_params = [
        GradeParams(max_grade=10, fine=5),
        GradeParams(max_grade=10, fine=5),
        GradeParams(min_grade=2, max_grade=10, fine=5, repeat_fine=7)
    ]

    @classmethod
    def grade_methods(cls):
        return [
            cls.grade_default,
            cls.grade_default,
            cls.grade_iterable   
        ]


def test_grader1():
    answers = [1, 2, (3, 4)]
    correct_answers = answers

    total_grade, answer_grades = MockGrader.grade(answers, correct_answers)
    assert total_grade == 30
    assert answer_grades == [(1, 10), (2, 10), ((3, 4), 10)]


def test_grader2():
    answers = [1, 2, (3, 4)]
    correct_answers = [1, 3, (3, 4)]

    total_grade, answer_grades = MockGrader.grade(answers, correct_answers)
    assert total_grade == 25
    assert answer_grades == [(1, 10), (2, 5), ((3, 4), 10)]


def test_grader3():
    answers = [1, 2, (3, 4)]
    correct_answers = [1, 2, (0, 0)]

    total_grade, answer_grades = MockGrader.grade(answers, correct_answers)
    assert total_grade == 23
    assert answer_grades == [(1, 10), (2, 10), ((3, 4), 3)]
