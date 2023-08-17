from typing import Any, ClassVar, Optional
from pydantic import BaseModel
from PyCompGeomAlgorithms.core import Point, BinTreeNode, BinTree, ThreadedBinTreeNode, ThreadedBinTree


class PydanticAdapter(BaseModel):
    regular_class: ClassVar[type] = object

    def to_regular_object(self):
        return self.regular_class(**{
            field: value.to_regular_object() if isinstance(value, self.__class__) else value
            for field, value in self.__dict__.items()
        })
    
    def __eq__(self, other):
        return self.to_regular_object() == (other.to_regular_object() if isinstance(other, self.__class__) else other)


class PointPydanticAdapter(PydanticAdapter):
    regular_class: ClassVar[type] = Point
    coords: tuple[float, ...]

    def to_regular_object(self):
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

    def to_regular_object(self):
        return self.regular_class(
            self.data.to_regular_object() if isinstance(self.data, PydanticAdapter) else self.data,
            self.left.to_regular_object() if self.left else None,
            self.right.to_regular_object() if self.right else None
        )
        

class ThreadedBinTreePydanticAdapter(BinTreePydanticAdapter):
    regular_class: ClassVar[type] = ThreadedBinTree
    root: ThreadedBinTreeNodePydanticAdapter

    def to_regular_object(self):
        node = self.root
        while node.next is not None and node.next is not self.root:
            node = node.next
        
        is_circular = node.next is self.root
        regular_root = self.root.to_regular_object()

        return self.regular_class.from_iterable([node.data for node in regular_root.traverse_inorder()], is_circular)
