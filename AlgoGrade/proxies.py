from typing import Any, ClassVar, Optional
from pydantic import BaseModel
from PyCompGeomAlgorithms.core import Point, BinTreeNode, BinTree, ThreadedBinTreeNode, ThreadedBinTree


class PydanticProxy(BaseModel):
    regular_class: ClassVar[type] = object

    def to_regular_object(self):
        return self.__class__.regular_class(**{
            field: (value.to_regular_object() if isinstance(value, PydanticProxy) else value)
            for field, value in self.__dict__.items()
        })


class PointProxy(PydanticProxy):
    regular_class: ClassVar[type] = Point
    coords: tuple[float, ...]

    def to_regular_object(self):
        return self.__class__.regular_class(*self.coords)


class BinTreeNodeProxy(PydanticProxy):
    regular_class: ClassVar[type] = BinTreeNode
    data: Any
    left: Optional[Any] = None
    right: Optional[Any] = None


class BinTreeProxy(PydanticProxy):
    regular_class: ClassVar[type] = BinTree
    root: BinTreeNodeProxy


class ThreadedBinTreeNodeProxy(BinTreeNodeProxy):
    regular_class: ClassVar[type] = ThreadedBinTreeNode
    prev: Optional[Any] = None
    next: Optional[Any] = None

    def to_regular_object(self):
        return self.__class__.regular_class(
            self.data.to_regular_object() if isinstance(self.data, PydanticProxy) else self.data,
            self.left.to_regular_object() if self.left else None,
            self.right.to_regular_object() if self.right else None
        )
        

class ThreadedBinTreeProxy(BinTreeProxy):
    regular_class: ClassVar[type] = ThreadedBinTree
    root: ThreadedBinTreeNodeProxy

    def to_regular_object(self):
        node = self.root
        while node.next is not None and node.next is not self.root:
            node = node.next
        
        is_circular = node.next is self.root
        regular_root = self.root.to_regular_object()

        return self.__class__.regular_class.from_iterable([node.data for node in regular_root.traverse_inorder()], is_circular)
