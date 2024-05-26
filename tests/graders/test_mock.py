from typing import Any
from AlgoGrade.core import Scoring, Grader, Answers


class MockGrader(Grader):
    @classmethod
    def grade_methods(cls):
        return [
            cls.grade_object,
            cls.grade_object,
            cls.grade_iterable   
        ]


class MockAnswers(Answers):
    list: list[Any]

    @classmethod
    def from_iterable(cls, iterable):
        return cls(list=iterable)
    
    def to_algogears_list(self):
        return self.list


scorings = [
    Scoring(max_grade=10, fine=5),
    Scoring(max_grade=10, fine=5),
    Scoring(min_grade=2, max_grade=10, fine=5, repeat_fine=7)
]


def test_grader1():
    algogears_answers = [1, 2, (3, 4)]
    correct_algogears_answers = algogears_answers

    total_grade, answer_grades = MockGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert total_grade == 30
    assert answer_grades == [(1, 10), (2, 10), ((3, 4), 10)]

    total_grade, answer_grades = MockGrader.grade_answers_wrapper(
        MockAnswers.from_iterable(algogears_answers),
        MockAnswers.from_iterable(correct_algogears_answers),
        scorings
    )
    assert total_grade == 30
    assert answer_grades == [(1, 10), (2, 10), ((3, 4), 10)]


def test_grader2():
    algogears_answers = [1, 2, (3, 4)]
    correct_algogears_answers = [1, 3, (3, 4)]

    total_grade, answer_grades = MockGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert total_grade == 25
    assert answer_grades == [(1, 10), (2, 5), ((3, 4), 10)]

    total_grade, answer_grades = MockGrader.grade_answers_wrapper(
        MockAnswers.from_iterable(algogears_answers),
        MockAnswers.from_iterable(correct_algogears_answers),
        scorings
    )
    assert total_grade == 25
    assert answer_grades == [(1, 10), (2, 5), ((3, 4), 10)]


def test_grader3():
    algogears_answers = [1, 2, (3, 4)]
    correct_algogears_answers = [1, 2, (0, 0)]

    total_grade, answer_grades = MockGrader.grade_algogears(algogears_answers, correct_algogears_answers, scorings)
    assert total_grade == 23
    assert answer_grades == [(1, 10), (2, 10), ((3, 4), 3)]

    total_grade, answer_grades = MockGrader.grade_answers_wrapper(
        MockAnswers.from_iterable(algogears_answers),
        MockAnswers.from_iterable(correct_algogears_answers),
        scorings
    )
    assert total_grade == 23
    assert answer_grades == [(1, 10), (2, 10), ((3, 4), 3)]
