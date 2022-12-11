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

import ast
from typing import List


class Visitor(ast.NodeVisitor):
    def __init__(self, module_name: str):
        super().__init__()
        self.imports: List[str] = []
        self.module_name = module_name

    def visit_Import(self, node: ast.Import):
        self.imports.extend([alias.name for alias in node.names])

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module_from = node.module
        if module_from is None:
            module_from = self.module_name
        self.imports.extend(
            [f'{module_from}.{alias.name}' for alias in node.names]
        )

    def flush_imports(self):
        self.imports = []
