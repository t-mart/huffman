"""Huffman encoding and decoding."""
from __future__ import annotations
from typing import List, Dict, Generator
from collections import Counter
import heapq

import attr

from .tree import Node
from .codes import build_codes


@attr.s(kw_only=True, auto_attribs=True, order=False, frozen=True)
class Compression:
    tree: str
    data: bytes
    data_len: int

    @classmethod
    def compress(cls, text: str) -> Compression:
        """
        Returns a Compression object that represents a huffman-encoded body of text.
        """

        heap: List[Node] = []
        for char, freq in reversed(Counter(text).most_common()):
            heapq.heappush(heap, Node(word=char, frequency=freq))

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            combiner = Node(
                frequency=left.frequency + right.frequency, left=left, right=right
            )
            heapq.heappush(heap, combiner)

        root = heap[0]

        codes: Dict[str, str] = build_codes(root)

        data: bytearray = bytearray()
        buffer: str = ""  # it's probably expensive to create new strings. bytearray might be better

        for char in text:
            code = codes[char]
            buffer += code

            while len(buffer) >= 8:
                bytestring, buffer = buffer[:8], buffer[8:]
                byte = int(bytestring, 2).to_bytes(1, byteorder="big")
                data += byte

        data_len = len(data) * 8

        if buffer:
            data_len += len(buffer)
            buffer += "0" * (8 - len(buffer))
            byte = int(buffer, 2).to_bytes(1, byteorder="big")
            data += byte

        return Compression(tree=root.encode(), data=data, data_len=data_len)

    def _iterbits(self) -> Generator[int, None, None]:
        for byte in self.data:
            mask = 128
            for _ in range(8):
                yield 1 if byte & mask else 0
                mask >>= 1

    def decompress(self) -> str:
        """Returns the body of text that this object compresses."""
        root = Node.decode(self.tree)
        string: bytearray = bytearray()
        location = root

        for bit, _ in zip(self._iterbits(), range(self.data_len)):
            if bit:
                location = location.right  # type: ignore
            else:
                location = location.left  # type: ignore

            if location.word is not None:
                string += location.word.encode('utf-8')
                location = root

        return string.decode('utf-8')
