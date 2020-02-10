"""Stuff about trees"""
from __future__ import annotations
from typing import List, Union, Optional, Deque
import json
from collections import deque

import attr


@attr.s(kw_only=True, auto_attribs=True)
class Node:
    """A node."""
    word: str = attr.ib(default=None, order=False)
    frequency: int = attr.ib(default=None)
    left: Optional[Node] = attr.ib(default=None, order=False)
    right: Optional[Node] = attr.ib(default=None, order=False)

    def encode(self, encoding: Optional[List[Union[None, int, str]]] = None) -> str:
        """Returns a json string representing this node and it's children, recursively."""
        # See https://opendsa-server.cs.vt.edu/ODSA/Books/CS3/html/SequentialRep.html for more
        # options on how to do this.

        if encoding is None:
            encoding = []

        if self.word is None:
            encoding.append(0)
        else:
            encoding.append(self.word)

        if self.left:
            self.left.encode(encoding=encoding)
        else:
            encoding.append(None)
        if self.right:
            self.right.encode(encoding=encoding)
        else:
            encoding.append(None)

        return json.dumps(encoding)

    @classmethod
    def decode(cls, json_str: str) -> Node:
        """Creates a node from a json string returned by `encode()`"""
        decoding = deque(json.loads(json_str))

        if not decoding:
            # this is meant to check if the decoding returns an empty list, but there are other
            # scenarios (e.g. literal null) where this branch will be taken
            raise ValueError(
                f"Passed in string ({decoding}) is either an empty list or not a list at all."
            )

        root_val = decoding.popleft()
        root = Node()
        if isinstance(root_val, str):
            root.word = root_val
        return cls._reconstruct(root, decoding)

    @classmethod
    def _reconstruct(cls, parent: Node, seq: Deque[Optional[str]]) -> Node:
        if seq:
            lval = seq.popleft()
            if lval is not None:
                lnode = Node()
                if isinstance(lval, str):
                    lnode.word = lval
                parent.left = lnode
                cls._reconstruct(parent.left, seq)
        else:
            return parent

        if seq:
            rval = seq.popleft()
            if rval is not None:
                rnode = Node()
                if isinstance(rval, str):
                    rnode.word = rval
                parent.right = rnode
                cls._reconstruct(parent.right, seq)
        else:
            return parent

        return parent
