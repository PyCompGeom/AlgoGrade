from functools import cached_property
from typing import Any, ClassVar, Optional, Iterable, Generator
from enum import Enum
from pydantic import BaseModel
from PyCompGeomAlgorithms.core import PyCGAObject, Point, BinTreeNode, BinTree, ThreadedBinTreeNode, ThreadedBinTree
from PyCompGeomAlgorithms.dynamic_hull import DynamicHullNode, DynamicHullTree, SubhullNode, SubhullThreadedBinTree
from PyCompGeomAlgorithms.graham import GrahamStepsTableRow, GrahamStepsTable
from PyCompGeomAlgorithms.quickhull import QuickhullNode


class PydanticAdapter(BaseModel):
    regular_class: ClassVar[type] = object

    @classmethod
    def from_regular_object(cls, obj, **kwargs):
        raise NotImplementedError

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
        if isinstance(obj, Iterable) and not isinstance(obj, str):
            generator = (cls._regular_object(item) for item in obj)
            return generator if isinstance(obj, Generator) else obj.__class__(generator)
        
        return obj

    def __eq__(self, other):
        return self.regular_object == (other.regular_object if isinstance(other, self.__class__) else other)
    
    def __hash__(self):
        return hash(self.regular_object)


class PointPydanticAdapter(PydanticAdapter):
    regular_class: ClassVar[type] = Point
    coords: tuple[float, ...]

    @classmethod
    def from_regular_object(cls, obj: Point, **kwargs):
        return cls(coords=obj.coords, **kwargs)

    @cached_property
    def regular_object(self):
        return self.regular_class(*self.coords)


class BinTreeNodePydanticAdapter(PydanticAdapter):
    regular_class: ClassVar[type] = BinTreeNode
    data: Any
    left: Optional[Any] = None
    right: Optional[Any] = None

    @classmethod
    def from_regular_object(cls, obj: BinTreeNode, **kwargs):
        return cls(
            data=pycga_to_pydantic(obj.data),
            left=pycga_to_pydantic(obj.left),
            right=pycga_to_pydantic(obj.right),
            **kwargs
        )
    
    def traverse_inorder(self, node=None, nodes=None):
        if node is None:
            node = self
        if nodes is None:
            nodes = []
        
        if node.left:
            self.traverse_inorder(node.left, nodes)
        
        nodes.append(node)

        if node.right:
            self.traverse_inorder(node.right, nodes)
        
        return nodes


class BinTreePydanticAdapter(PydanticAdapter):
    regular_class: ClassVar[type] = BinTree
    root: BinTreeNodePydanticAdapter

    @classmethod
    def from_regular_object(cls, obj: BinTree, **kwargs):
        return cls(root=pycga_to_pydantic(obj.root), **kwargs)
    
    def traverse_inorder(self):
        return self.root.traverse_inorder() if self.root else []


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
    
    @classmethod
    def from_regular_object(cls, obj: ThreadedBinTreeNode, **kwargs):
        return super().from_regular_object(obj, prev=None, next=None, **kwargs)
        

class ThreadedBinTreePydanticAdapter(BinTreePydanticAdapter):
    regular_class: ClassVar[type] = ThreadedBinTree
    root: ThreadedBinTreeNodePydanticAdapter

    @classmethod
    def from_regular_object(cls, obj: ThreadedBinTree, **kwargs):
        root = obj.root
        is_circular = root.leftmost_node.prev is root.rightmost_node or root.rightmost_node.next is root.leftmost_node
        root = pycga_to_pydantic(obj.root)
        nodes = root.traverse_inorder()

        for i, node in enumerate(nodes):
            node.prev = node.left if node.left else nodes[i-1]
            node.next = node.right if node.right else nodes[(i+1)%len(nodes)]
        
        if not is_circular and nodes:
            nodes[0].prev = None
            nodes[-1].next = None
        
        return cls(root=root, **kwargs)

    @cached_property
    def regular_object(self):
        node = self.root
        while node.next is not None and node.next is not self.root:
            node = node.next
        
        is_circular = node.next is self.root
        regular_root = self.root.regular_object

        return self.regular_class.from_iterable([node.data for node in regular_root.traverse_inorder()], is_circular)


def pydantic_to_pycga(obj: Any | PydanticAdapter | Iterable):    
    if isinstance(obj, PydanticAdapter):
        return obj.regular_object

    if isinstance(obj, dict):
        return {pydantic_to_pycga(key): pydantic_to_pycga(value) for key, value in obj.items()}
    
    if isinstance(obj, Iterable) and not isinstance(obj, str):
        generator = (pydantic_to_pycga(obj) for obj in obj)
        return generator if isinstance(obj, Generator) else obj.__class__(generator)
    
    return obj


def pycga_to_pydantic(obj: Any | type | PyCGAObject | Iterable):
    if isinstance(obj, type):
        try:
            from .dynamic_hull import DynamicHullNodePydanticAdapter, DynamicHullTreePydanticAdapter, SubhullNodePydanticAdapter, SubhullThreadedBinTreePydanticAdapter
            from .graham import GrahamStepsTableRowPydanticAdapter, GrahamStepsTablePydanticAdapter
            from .quickhull import QuickhullNodePydanticAdapter
            
            return {
                Point: PointPydanticAdapter,
                BinTreeNode: BinTreeNodePydanticAdapter,
                BinTree: BinTreePydanticAdapter,
                ThreadedBinTreeNode: ThreadedBinTreeNodePydanticAdapter,
                ThreadedBinTree: ThreadedBinTreePydanticAdapter,
                DynamicHullNode: DynamicHullNodePydanticAdapter,
                DynamicHullTree: DynamicHullTreePydanticAdapter,
                SubhullNode: SubhullNodePydanticAdapter,
                SubhullThreadedBinTree: SubhullThreadedBinTreePydanticAdapter,
                GrahamStepsTableRow: GrahamStepsTableRowPydanticAdapter,
                GrahamStepsTable: GrahamStepsTablePydanticAdapter,
                QuickhullNode: QuickhullNodePydanticAdapter
            }[obj]
        except KeyError as e:
            raise KeyError("unknown PyCGA type") from e

    if isinstance(obj, PyCGAObject) and not isinstance(obj, Enum):
        return pycga_to_pydantic(obj.__class__).from_regular_object(obj)

    if isinstance(obj, dict):
        return {pycga_to_pydantic(key): pycga_to_pydantic(value) for key, value in obj.items()}
    
    if isinstance(obj, Iterable) and not isinstance(obj, str):
        generator = (pycga_to_pydantic(item) for item in obj)
        return generator if isinstance(obj, Generator) else obj.__class__(generator)
    
    return obj