import ast
import glob
import importlib
from types import ModuleType
from typing import Dict, List, Literal, Union

from panopticon.util import get_file_dir
from panopticon.visitor import Visitor


def get_module_files(module: ModuleType) -> List[str]:
    try:
        entry = module.__file__
    except AttributeError:
        return []  # frozen module
    if entry.endswith('__init__.py'):
        entry_folder = get_file_dir(entry)
        return glob.glob(f'{entry_folder}/**/*.py', recursive=True)
    else:
        return [entry]


def get_ast_from_file(filename: str) -> ast.Module:
    with open(filename) as f:
        try:
            return ast.parse(f.read())
        # ast module has test files that are bad syntax
        # to test unicode & syntax parsing
        # so the errors are ignored.
        # TODO: ignore test files
        except UnicodeDecodeError:
            return ast.Module()
        except SyntaxError:
            return ast.Module()


RESOLVED_IMPORT_LIST = List[
    Dict[Union[Literal['file'], Literal['imports']], Union[str, List[str]]]
]


def resolve_imports(module: ModuleType) -> RESOLVED_IMPORT_LIST:
    visitor = Visitor()
    files = get_module_files(module)
    imports: RESOLVED_IMPORT_LIST = []
    for file in files:
        if not file.endswith('.so'):  # c extension
            file_ast = get_ast_from_file(file)
            visitor.visit(file_ast)
            imports.append({'file': file, 'imports': visitor.imports})
            visitor.flush_imports()
    imports = simplify_imports(imports)
    return imports


def simplify_imports(imports: RESOLVED_IMPORT_LIST) -> RESOLVED_IMPORT_LIST:
    simplified = []
    existing = []
    for item in imports:
        copy = item.copy()
        root_modules = map(
            lambda x: x if len(x.split('.')) == 0 else x.split('.')[0],
            item['imports'],
        )
        copy['imports'] = list(
            set(filter(lambda x: x not in existing, root_modules))
        )
        simplified.append(copy)
        existing.extend(copy['imports'])
    return simplified


def import_module(name: str) -> ModuleType:
    return importlib.import_module(name)
