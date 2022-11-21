import ast
import glob
import importlib
from types import ModuleType
from typing import Dict, List, Literal, Union

from panopticon.visitor import Visitor


def get_module_files(module: ModuleType) -> List[str]:
    try:
        entry = module.__file__
    except AttributeError:
        return []  # frozen module
    if entry.endswith('__init__.py'):
        entry_folder = entry.replace('/__init__.py', '')
        return glob.glob(f'{entry_folder}/**/*.py', recursive=True)
    else:
        return [entry]


def get_ast_from_file(filename: str) -> ast.Module:
    with open(filename) as f:
        try:
            return ast.parse(f.read())
        #     except SyntaxError as e:
        #            raise Exception(
        #               f'Failed parsing AST for {filename}. There appears to be a SyntaxError on line {e.lineno}!'  # noqa E501
        #          )
        except UnicodeDecodeError:
            # ast has test files that are bad syntax to test unicode parsing
            # so this is required
            # TODO: ignore test files
            return ast.Module()
        except SyntaxError:
            return ast.Module()


def resolve_imports(module: ModuleType) -> List[str]:
    visitor = Visitor()
    files = get_module_files(module)
    imports: List[Dict[Union[Literal['file'], Literal['imports']]]] = []
    for file in files:
        if not file.endswith('.so'):  # c extension
            file_ast = get_ast_from_file(file)
            visitor.visit(file_ast)
            imports.append({'file': file, 'imports': visitor.imports})
            visitor.flush_imports()
    imports = simplify_imports(imports)
    return imports


def simplify_imports(imports: List[Dict[str, List[str]]]) -> List[str]:
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


def import_module(module_name: str) -> ModuleType:
    return importlib.import_module(module_name)
