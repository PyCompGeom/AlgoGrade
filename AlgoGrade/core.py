from math import inf
from collections import Counter


class Task:
    description = ""
    algorithm = None

    def __init__(self, input):
        self.input = input
        self.correct_answers = list(self.__class__.algorithm(input))


class Mistake:
    def __init__(self, grade_params, description=""):
        self.grade_params = grade_params
        self.description = description
    
    @property
    def is_repeated(self):
        return self.grade_params.repeat_fine > 0
    
    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.grade_params == other.grade_params
        )
    
    def __hash__(self):
        return hash((self.__class__, self.grade_params))


class GradeParams:
    def __init__(self, min_grade=-inf, max_grade=0.0, fine=0.0, repeat_fine=0.0):
        self.min_grade = min_grade
        self.max_grade = max_grade
        self.fine = fine
        self.repeat_fine = repeat_fine
    
    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            set(self.__dict__.values()) == set(other.__dict__.values())
        )
    
    def __hash__(self):
        return hash(tuple(self.__dict__.values()))


class Grader:
    grade_params = []

    @classmethod
    def grade(cls, answers, correct_answers):
        mistake_lists = [
            grading_method(answer, correct_answer, grade_params)
            for grading_method, answer, correct_answer, grade_params
            in zip(cls.grading_methods(), answers, correct_answers, cls.grade_params)
        ]
        mistake_counters = [Counter(mistakes) for mistakes in mistake_lists]
        mistake_fines_dicts = [
            {
                mistake: mistake.grade_params.repeat_fine if mistake.is_repeated and count > 1 else mistake.grade_params.fine
                for mistake, count in mistake_counter.items()
            }
            for mistake_counter in mistake_counters
        ]

        answer_grades = [
            (answer, max(grade_params.min_grade, grade_params.max_grade-sum(mistake_fine_dict.values())))
            for answer, grade_params, mistake_fine_dict
            in zip(answers, cls.grade_params, mistake_fines_dicts)
        ]
        total_grade = sum(grade for answer, grade in answer_grades)
        
        return total_grade, answer_grades
    
    @classmethod
    def grade_default(cls, answer, correct_answer, grade_params):
        return [] if answer == correct_answer else [Mistake(grade_params, description="Items don't match")]
    
    @classmethod
    def grade_iterable(cls, answer, correct_answer, grade_params, grade_item=None, item_mistake_description=""):
        if grade_item is None:
            grade_item = cls.grade_default

        len_diff = len(correct_answer) - len(answer)
        if len_diff > 0:
            return [Mistake(grade_params, description="Too many items")] * len_diff

        return [
            Mistake(grade_params, description=item_mistake_description)
            for a, c in zip(answer, correct_answer)
            if grade_item(a, c, grade_params) != []
        ]

    @classmethod
    def grading_methods(cls):
        return [cls.grade_default for _ in cls.grade_params]
