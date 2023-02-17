'''
Copyright (C) 2022 Aarnav Bos
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
from typing import List, Tuple

from anytree import Node

cache = {}
to_cache = []


def add_reason_attr(node: Node, cloned_node: Node) -> None:
    if hasattr(node, 'reason'):
        cloned_node.reason = node.reason


def clone_children(child: Node, cloned_child: Node) -> None:
    '''
    Recursively adds children to the cloned_child
    '''
    for node in child.children:
        cloned = Node(
            node.name,
            parent=cloned_child,
        )
        add_reason_attr(node, cloned)
        if len(node.children) > 0:
            return clone_children(node, cloned)


def apply_cache(to_cache: List[Tuple[Node, str]], cache) -> None:
    for item in to_cache:
        parent = item[0]
        child = cache.get(item[1])
        cloned_child = Node(
            child.name,
            parent=parent,
        )
        add_reason_attr(child, cloned_child)
        clone_children(child, cloned_child)
