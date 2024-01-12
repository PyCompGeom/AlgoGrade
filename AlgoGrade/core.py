from math import inf
from collections import Counter
from typing import Iterable
from .adapters import pycga_to_pydantic, pydantic_to_pycga


class Task:
    description = ""
    algorithm = None

    def __init__(self, *inputs):
        self.inputs = inputs
        self.correct_answers = list(self.__class__.algorithm(*inputs))


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


class Scoring:
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
    def grade(cls, answers, correct_answers, is_pydantic=False):
        if is_pydantic:
            answers = pydantic_to_pycga(answers)

        mistake_lists = [
            grading_method(answer, correct_answer, grade_params)
            for grading_method, answer, correct_answer, grade_params
            in zip(cls.grade_methods(), answers, correct_answers, cls.grade_params)
        ]
        mistake_counters = [Counter(mistakes) for mistakes in mistake_lists]
        mistake_fines_dicts = [
            {
                mistake: mistake.grade_params.repeat_fine if mistake.is_repeated and count > 1 else mistake.grade_params.fine
                for mistake, count in mistake_counter.items()
            }
            for mistake_counter in mistake_counters
        ]

        if is_pydantic:
            answers = pycga_to_pydantic(answers)

        answer_grades = [
            (answer, max(grade_params.min_grade, grade_params.max_grade-sum(mistake_fine_dict.values())))
            for answer, grade_params, mistake_fine_dict
            in zip(answers, cls.grade_params, mistake_fines_dicts)
        ]
        total_grade = sum(grade for answer, grade in answer_grades)
        
        return total_grade, answer_grades
    
    @classmethod
    def grade_default(cls, answer, correct_answer, grade_params, item_mistake_text=""):
        return [] if answer == correct_answer else [Mistake(grade_params, description=item_mistake_text)]
    
    @classmethod
    def grade_iterable(cls, answer, correct_answer, grade_params, grade_item_method=None, item_mistake_text=""):
        if grade_item_method is None:
            grade_item_method = cls.grade_default
        if callable(grade_item_method):
            grade_item_method = [grade_item_method] * len(correct_answer)
        elif not isinstance(grade_item_method, Iterable):
            raise TypeError(f"grade_item_method should be either a grading method, or an iterable of grading methods for each item, or None (defaults to default_grading)")

        len_diff = len(correct_answer) - len(answer)
        if len_diff == 0:
            return flatten([
                g(a, c, grade_params, item_mistake_text=item_mistake_text)
                for g, a, c in zip(grade_item_method, answer, correct_answer)
            ])

        return [Mistake(grade_params, description=f"Too {'few' if len_diff < 0 else 'many'} items")] * abs(len_diff)

    @classmethod
    def grade_bin_tree(cls, answer, correct_answer, grade_params, grade_item_method=None, item_mistake_text=""):
        if grade_item_method is None:
            grade_item_method = cls.grade_default
        
        return cls._find_mistakes_in_bin_tree(answer.root, correct_answer.root, grade_params, grade_item_method, item_mistake_text)

    @classmethod
    def _find_mistakes_in_bin_tree(
        cls, node, correct_node, grade_params,
        grade_item_method=None, item_mistake_text="", mistakes=None, extra=None, missing=None
    ):
        if mistakes is None:
            mistakes = []
        if extra is None:
            extra = []
        if missing is None:
            missing = []
        
        mistakes.extend(grade_item_method(node, correct_node, grade_params))
        
        if node.left and correct_node.left:
            cls._find_mistakes_in_bin_tree(node.left, correct_node.left, grade_params, grade_item_method, item_mistake_text, mistakes, extra, missing)
        if node.left and not correct_node.left:
            extra.extend(Mistake(grade_params, "Extra item") for _ in node.left.traverse_preorder()[1:])
        if not node.left and correct_node.left:
            missing.extend(Mistake(grade_params, "Missing item") for _ in correct_node.left.traverse_preorder()[1:])

        if node.right and correct_node.right:
            cls._find_mistakes_in_bin_tree(node.right, correct_node.right, grade_params, grade_item_method, item_mistake_text, mistakes, extra, missing)
        if node.right and not correct_node.right:
            extra.extend(Mistake(grade_params, "Extra item") for _ in node.right.traverse_preorder()[1:])
        if not node.right and correct_node.right:
            missing.extend(Mistake(grade_params, "Missing item") for _ in correct_node.right.traverse_preorder()[1:])
        
        return mistakes + extra + missing

    @classmethod
    def grade_methods(cls):
        return [cls.grade_default for _ in cls.grade_params]


def flatten(iterable):
    return list(_flatten(iterable))


def _flatten(iterable):
    for item in iterable:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for inner_item in flatten(item):
                yield inner_item
        else:
            yield item
