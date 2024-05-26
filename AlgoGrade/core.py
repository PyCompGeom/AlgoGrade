from collections import Counter
from functools import partial
from operator import eq
from typing import Iterable, Generator, Type, Any
from pydantic import BaseModel
from algogears.core import SerializablePydanticModelWithPydanticFields


class Answers(SerializablePydanticModelWithPydanticFields):
    @classmethod
    def from_iterable(cls, iterable):
        raise NotImplementedError
    
    def to_algogears_list(self):
        raise NotImplementedError


class Mistake:
    def __init__(self, scorings, description=""):
        self.scorings = scorings
        self.description = description
    
    @property
    def is_repeated(self):
        return self.scorings.repeat_fine > 0
    
    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.scorings == other.scorings
        )
    
    def __hash__(self):
        return hash((self.__class__, self.scorings))


class Scoring(BaseModel, frozen=True):
    min_grade: float = -1000.0
    max_grade: float = 0.0
    fine: float = 0.0
    repeat_fine: float = 0.0


class Grader:
    @classmethod
    def grade_methods(cls):
        """List of grading methods for each step of the task. Redefine in the derived class"""
        raise NotImplementedError

    @classmethod
    def grade_algogears(cls, answers, correct_answers, scorings):
        """
            Compare answers to correct_answers (both in AlgoGEARS format) an return a tuple
            `(total_grade, answers_grades)`, where answers_grades is a list of tuples--grades for each answer `(answer, grade)` in AlgoGEARS format.
        """
        mistake_lists = [
            grading_method(answer, correct_answer, scorings)
            for grading_method, answer, correct_answer, scorings
            in zip(cls.grade_methods(), answers, correct_answers, scorings)
        ]
        mistake_counters = [Counter(mistakes) for mistakes in mistake_lists]
        mistake_fines_dicts = [
            {
                mistake: mistake.scorings.repeat_fine if mistake.is_repeated and count > 1 else mistake.scorings.fine
                for mistake, count in mistake_counter.items()
            }
            for mistake_counter in mistake_counters
        ]

        answers_grades = [
            (answer, max(scorings.min_grade, scorings.max_grade-sum(mistake_fine_dict.values())))
            for answer, scorings, mistake_fine_dict
            in zip(answers, scorings, mistake_fines_dicts)
        ]
        total_grade = sum(grade for answer, grade in answers_grades)
        
        return total_grade, answers_grades
    
    @classmethod
    def grade_answers_wrapper(cls, answers: Answers, correct_answers: Answers, scorings):
        """
            Compare answers to correct_answers (both in Answers format) and return a tuple
            `(total_grade, answers_grades)`, where answers_grades is a list of tuples--grades for each answer `(answer, grade)` in Answers format.
        """
        return cls.grade_algogears(answers.to_algogears_list(), correct_answers.to_algogears_list(), scorings)
    
    @classmethod
    def grade_object(cls, answer, correct_answer, scorings, custom_eq=eq):
        """
            The most basic method for grading an object compared to the correct one, using customizable equality.
            
            By default, grades `answer` compared to `correct_answer` based on whether `answer == correct_answer` (`answer.__eq__(correct_answer)`).

            Returns an empty list if the equality holds, and a list containing a mistake otherwise.
        """
        return [] if custom_eq(answer, correct_answer) else [Mistake(scorings, "Objects don't match")]

    @classmethod
    def grade_iterable(cls, answer, correct_answer, scorings, grade_item_method=None):
        if grade_item_method is None:
            grade_item_method = cls.grade_object
        if callable(grade_item_method):
            grade_item_method = [grade_item_method] * len(correct_answer)
        elif not isinstance(grade_item_method, Iterable):
            raise TypeError(f"grade_item_method should be either a grading method, or an iterable of grading methods for each item, or None (defaults to default_grading)")

        len_diff = len(correct_answer) - len(answer)
        if len_diff == 0:
            return flatten([
                g(a, c, scorings)
                for g, a, c in zip(grade_item_method, answer, correct_answer)
            ])

        return [Mistake(scorings, description=f"Too {'few' if len_diff < 0 else 'many'} items")] * abs(len_diff)

    @classmethod
    def grade_bin_tree(cls, answer, correct_answer, scorings, grade_item_method=None):
        if grade_item_method is None:
            grade_item_method = partial(cls.grade_object, custom_eq=lambda a, c: c.weak_equal(a))
        
        return cls._find_mistakes_in_bin_tree(answer.root, correct_answer.root, scorings, grade_item_method)

    @classmethod
    def _find_mistakes_in_bin_tree(
        cls, node, correct_node, scorings,
        grade_item_method=None, mistakes=None, mistakes_extra=None, mistakes_missing=None
    ):
        if mistakes is None:
            mistakes = []
        if mistakes_extra is None:
            mistakes_extra = []
        if mistakes_missing is None:
            mistakes_missing = []
        
        mistakes.extend(grade_item_method(node, correct_node, scorings))

        cls._find_mistakes_in_subtree(node.left, correct_node.left, scorings, grade_item_method, mistakes, mistakes_extra, mistakes_missing)
        cls._find_mistakes_in_subtree(node.right, correct_node.right, scorings, grade_item_method, mistakes, mistakes_extra, mistakes_missing)

        return mistakes + mistakes_extra + mistakes_missing

    @classmethod
    def _find_mistakes_in_subtree(cls, node, correct_node, scorings, grade_item_method, mistakes, extra, missing):
        if node and correct_node:
            cls._find_mistakes_in_bin_tree(node, correct_node, scorings, grade_item_method, mistakes, extra, missing)
        if node and not correct_node:
            extra.extend(Mistake(scorings, "Extra item") for _ in node.traverse_inorder())
        if not node and correct_node:
            missing.extend(Mistake(scorings, "Missing item") for _ in correct_node.traverse_inorder())

    @classmethod
    def grade_threaded_bin_tree(cls, answer, correct_answer, scorings, grade_item_method=None):
        if grade_item_method is None:
            grade_item_method = partial(cls.grade_object, custom_eq=lambda a, c: c.weak_equal(a))

        nodes = answer.traverse_inorder()
        correct_nodes = correct_answer.traverse_inorder()

        cls._set_nodes_indices(nodes)
        cls._set_nodes_indices(correct_nodes)
        
        matching_nodes, correct_matching_nodes = [], []
        seen_threads = set()
        mistakes = cls._find_mistakes_in_threaded_bin_tree(
            node=answer.root, correct_node=correct_answer.root, scorings=scorings, grade_item_method=grade_item_method,
            matching_nodes=matching_nodes, correct_matching_nodes=correct_matching_nodes, seen_threads=seen_threads
        )

        for node, correct_node in zip(matching_nodes, correct_matching_nodes):
            mistakes.extend(cls._find_thread_mistakes_in_correct_subtree(node, node.prev, correct_node.prev, seen_threads, scorings))
            mistakes.extend(cls._find_thread_mistakes_in_correct_subtree(node, node.next, correct_node.next, seen_threads, scorings))
        
        return mistakes

    @classmethod
    def _set_nodes_indices(cls, nodes):
        for i, node in enumerate(nodes):
                node.matching_node_index = None
                node.inorder_index = i
        for node in nodes:
            if node.prev is not None:
                node.prev_index = node.prev.inorder_index
            else:
                node.prev_index = None
            if node.next is not None:
                node.next_index = node.next.inorder_index
            else:
                node.next_index = None

    @classmethod
    def _find_mistakes_in_threaded_bin_tree(
        cls, node, correct_node, scorings,
        grade_item_method=None, mistakes=None, mistakes_extra=None, mistakes_missing=None,
        matching_nodes_counter=None, matching_nodes=None, correct_matching_nodes=None, seen_threads=None
    ):
        if mistakes is None:
            mistakes = []
        if mistakes_extra is None:
            mistakes_extra = []
        if mistakes_missing is None:
            mistakes_missing = []
        if matching_nodes_counter is None:
            matching_nodes_counter = [0]
        if matching_nodes is None:
            matching_nodes = []
        if correct_matching_nodes is None:
            correct_matching_nodes = []
        if seen_threads is None:
            seen_threads = set()

        mistakes.extend(grade_item_method(node, correct_node, scorings))
        
        matching_nodes_counter[0] += 1
        node.matching_node_index = matching_nodes_counter[0]
        correct_node.matching_node_index = matching_nodes_counter[0]
        
        matching_nodes.append(node)
        correct_matching_nodes.append(correct_node)

        cls._find_mistakes_in_threaded_subtree(node.left, correct_node.left, scorings, grade_item_method, mistakes, mistakes_extra, mistakes_missing, matching_nodes_counter, matching_nodes, correct_matching_nodes, seen_threads)
        cls._find_mistakes_in_threaded_subtree(node.right, correct_node.right, scorings, grade_item_method, mistakes, mistakes_extra, mistakes_missing, matching_nodes_counter, matching_nodes, correct_matching_nodes, seen_threads)
        
        return mistakes + mistakes_extra + mistakes_missing

    @classmethod
    def _find_mistakes_in_threaded_subtree(cls, subtree_root, correct_subtree_root, scorings, grade_item_method, mistakes, mistakes_extra, mistakes_missing, matching_nodes_counter, matching_nodes, correct_matching_nodes, seen_threads):
        if subtree_root and correct_subtree_root:
            cls._find_mistakes_in_threaded_bin_tree(subtree_root, correct_subtree_root, scorings, grade_item_method, mistakes, mistakes_extra, mistakes_missing, matching_nodes_counter, matching_nodes, correct_matching_nodes, seen_threads)
        if subtree_root and not correct_subtree_root:
            extra_nodes = subtree_root.traverse_inorder()
            mistakes_extra.extend(Mistake(scorings, "Extra node") for _ in extra_nodes)            
            
            # Here threads can be set by student in an unpredictably wrong way, so we need to traverse them all to find their number
            connected_threads = cls._connected_threads(extra_nodes)
            mistakes_extra.extend(Mistake(scorings, "Extra thread") for _ in connected_threads)
            seen_threads |= connected_threads
        if not subtree_root and correct_subtree_root:
            missing_nodes = correct_subtree_root.traverse_inorder()
            mistakes_missing.extend(Mistake(scorings, "Missing node") for _ in missing_nodes)

            # Here the number of threads can be found without traversing.
            # If len(missing_nodes) is N > 0, then there is necessarily 1 thread between the parent of correct_subtree_root and the left/right extreme node of its (parent's) right/left subtree, respectively.
            # There are also N - 1 threads between N nodes in the subtree.
            # For circular TBT, there is 1 additional thread from that subtree's extreme node to either correct_node's parent or, if the extreme node is also globally extreme, to the other globally extreme node.
            # For non-circular TBT, there is no thread between globally leftmost node and globally rightmost node.
            n_missing_threads = len(missing_nodes) + (0 if missing_nodes[0].prev is None else 1)
            mistakes_missing.extend(Mistake(scorings, "Missing thread") for _ in range(n_missing_threads))

    @classmethod
    def _connected_threads(cls, nodes):
        seen_threads = set()
        for node in nodes:
            if node.prev_index is not None:
                seen_threads.add((node.prev_index, node.inorder_index))
            if node.next_index is not None:
                seen_threads.add((node.inorder_index, node.next_index))
        
        return seen_threads

    @classmethod
    def _find_thread_mistakes_in_correct_subtree(cls, node, neighbor, correct_neighbor, seen_threads, scorings):
        mistakes = []
        if neighbor is None and correct_neighbor is not None:
            mistakes.append(Mistake(scorings, "Missing thread"))
        elif neighbor is not None and (neighbor.inorder_index, node.inorder_index) not in seen_threads and (node.inorder_index, neighbor.inorder_index) not in seen_threads:
            if correct_neighbor is None:
                mistakes.append(Mistake(scorings, "Extra thread"))
                seen_threads.add((node.inorder_index, neighbor.inorder_index) if node.next is neighbor else (neighbor.inorder_index, node.inorder_index))
            else:
                threads_exist_and_dont_match = (
                    neighbor.matching_node_index is not None
                    and correct_neighbor.matching_node_index is not None
                    and neighbor.matching_node_index != correct_neighbor.matching_node_index
                )

                if threads_exist_and_dont_match:
                    mistakes.append(Mistake(scorings, "Thread doesn't match the correct one"))
                    seen_threads.add((node.inorder_index, neighbor.inorder_index) if node.next is neighbor else (neighbor.inorder_index, node.inorder_index))
                            
        return mistakes


class GivenJSONParser:
    """Parses a JSON-represented (list) givens as a tuple of arguments to be fed into the respective PyCGA task solving method."""
    @classmethod
    def parse(cls, data) -> list[Any]:
        """Parses a JSON-represented (list) givens as a tuple of arguments to be fed into the respective PyCGA task solving method."""
        raise NotImplementedError


class Task:
    algorithm: Generator = None
    grader_class: Type[Grader] = None
    answers_class: Type[Answers] = None
    given_parser_class: Type[GivenJSONParser] = None
    
    @classmethod
    def solve_as_algogears_list(cls, givens: Iterable):
        """Solves a task with the givens provided in AlgoGEARS format and returns a list of answers in PyCGA format."""
        return list(cls.algorithm(*givens))
    
    @classmethod
    def solve_as_answers_wrapper(cls, givens: Iterable):
        """Solves a task with the givens provided in PyCGA format and returns answers in form of the respective Answers wrapper."""
        algogears_answers = cls.solve_as_algogears_list(givens)
        return cls.answers_class.from_iterable(algogears_answers)


def flatten(iterable):
    return list(_flatten(iterable))


def _flatten(iterable):
    for item in iterable:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for inner_item in flatten(item):
                yield inner_item
        else:
            yield item
