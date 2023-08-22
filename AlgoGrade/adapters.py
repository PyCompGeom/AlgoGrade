from functools import cached_property
from typing import Any, ClassVar, Optional, Iterable
from pydantic import BaseModel
from PyCompGeomAlgorithms.core import Point, BinTreeNode, BinTree, ThreadedBinTreeNode, ThreadedBinTree


class PydanticAdapter(BaseModel):
    regular_class: ClassVar[type] = object

    @cached_property
    def regular_object(self):
        return self.regular_class(**{
            field: self._regular_object(value)
            for field, value in self.__dict__.items()
        })
    
    @classmethod
    def _regular_object(cls, obj):
        if isinstance(obj, PydanticAdapter):
            return obj.regular_object
        if isinstance(obj, dict):
            return {cls._regular_object(key): cls._regular_object(value) for key, value in obj.items()}
        if isinstance(obj, Iterable):
            return obj.__class__(cls._regular_object(item) for item in obj)
        
        return obj

    def __eq__(self, other):
        return self.regular_object == (other.regular_object if isinstance(other, self.__class__) else other)


class PointPydanticAdapter(PydanticAdapter):
    regular_class: ClassVar[type] = Point
    coords: tuple[float, ...]

    @cached_property
    def regular_object(self):
        return self.regular_class(*self.coords)


class BinTreeNodePydanticAdapter(PydanticAdapter):
    regular_class: ClassVar[type] = BinTreeNode
    data: Any
    left: Optional[Any] = None
    right: Optional[Any] = None


class BinTreePydanticAdapter(PydanticAdapter):
    regular_class: ClassVar[type] = BinTree
    root: BinTreeNodePydanticAdapter


class ThreadedBinTreeNodePydanticAdapter(BinTreeNodePydanticAdapter):
    regular_class: ClassVar[type] = ThreadedBinTreeNode
    prev: Optional[Any] = None
    next: Optional[Any] = None

    @cached_property
    def regular_object(self):
        return self.regular_class(
            self.data.regular_object if isinstance(self.data, PydanticAdapter) else self.data,
            self.left.regular_object if self.left else None,
            self.right.regular_object if self.right else None
        )
        

class ThreadedBinTreePydanticAdapter(BinTreePydanticAdapter):
    regular_class: ClassVar[type] = ThreadedBinTree
    root: ThreadedBinTreeNodePydanticAdapter

    @cached_property
    def regular_object(self):
        node = self.root
        while node.next is not None and node.next is not self.root:
            node = node.next
        
        is_circular = node.next is self.root
        regular_root = self.root.regular_object

        return self.regular_class.from_iterable([node.data for node in regular_root.traverse_inorder()], is_circular)
