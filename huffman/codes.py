"""Create binary codes for letters given a huffman tree."""
from __future__ import annotations
from typing import Optional, Dict

from .tree import Node


def build_codes(
    root: Node, prefix: str = "", codes: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    """Create binary codes for letters given a huffman tree."""
    if codes is None:
        codes = {}

    if prefix is None:
        prefix = []

    if root.word is not None:
        codes[root.word] = prefix
    else:
        if root.left:
            build_codes(root.left, prefix + "0", codes)

        if root.right:
            build_codes(root.right, prefix + "1", codes)

    return codes
