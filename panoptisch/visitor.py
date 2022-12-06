import ast
from typing import List


class Visitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.imports: List[str] = []

    def visit_Import(self, node: ast.Import):
        self.imports.extend([alias.name for alias in node.names])

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module_from = node.module
        self.imports.extend(
            [f'{module_from}.{alias.name}' for alias in node.names]
        )

    def flush_imports(self):
        self.imports = []
