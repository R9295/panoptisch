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
import importlib
import os
import time
from types import ModuleType
from typing import Tuple, Union

from anytree import Node, exporter

from panoptisch.sandbox import set_audit_hooks
from panoptisch.util import get_file_dir

from panoptisch.imports import (  # isort:skip
    import_file_module,
    import_module,
    resolve_imports,
)


def remove_module_property(node: Node) -> None:
    delattr(node, 'module')
    for child in node.children:
        remove_module_property(child)


def resolve_module(
    module_name: str, parent_file: str, parent_module: ModuleType
) -> Tuple[Union[bool, None], str]:
    '''
    This function resolves a module by imported by the parent_file.
    The resolver behaves like Python's import system.
    If the imported module is a submodule of the parent module,
    the function returns False because:
    1. It is a nested module, not a dependency of the parent.
    2. The files from the submodule as included in the parent module,
    so it's imports will be parsed and factored in as the parent's imports.
    TODO: handle None
    '''
    parent_dir = get_file_dir(parent_file)
    is_part_of_module = parent_file.endswith('__init__.py') or os.path.exists(
        f'{parent_dir}/__init__.py'
    )
    module_as_dir = f'{parent_dir}/{module_name}'
    module_as_file = f'{module_as_dir}.py'
    if os.path.isfile(module_as_file):
        if not is_part_of_module:
            module = import_file_module(module_name, module_as_file)
            return module, module_name
        else:
            return False, module_name
    elif os.path.isdir(module_as_dir):
        if not is_part_of_module:
            # this check matters as a simple script cannot
            # import another script in a folder if the folder does not have
            # an __init__.py (making it a module)
            if os.path.exists(f'{module_as_dir}/__init__.py'):
                module = import_file_module(
                    module_name, f'{module_as_dir}/__init__.py'
                )
                return module, module_name
            else:
                return False, module_name
    try:
        return import_module(module_name), module_name
    except ModuleNotFoundError:
        print(
            f'AAAAA Could not resolve: {module_name}, parent = {parent_module.__name__}'  # noqa E501
        )
    return None, module_name


def get_imports(
    current_root: Node,
    stdlib_dir=None,
    depth=-1,
    max_depth=3,
    omit_not_found=False,
):
    depth += 1
    if depth == max_depth:
        return
    imports = resolve_imports(current_root.module)
    for item in imports:
        file = item.get('file')
        file_imports = item.get('imports')
        for module_name in file_imports:
            if module_name != current_root.module.__name__:
                if (
                    stdlib_dir
                    and stdlib_dir in file
                    and 'site-packages' not in file
                ):
                    continue
                module, name = resolve_module(
                    module_name, file, current_root.module
                )
                if module:
                    node = Node(
                        name,
                        module=module,
                        parent=current_root,
                    )
                    get_imports(
                        node,
                        stdlib_dir=stdlib_dir,
                        depth=depth,
                        max_depth=max_depth,
                        omit_not_found=omit_not_found,
                    )
                else:
                    if module is not False and omit_not_found is False:
                        node = Node(
                            module_name,
                            parent=current_root,
                            module=None,
                            reason='ModuleNotFoundError',
                        )


def run(args):
    print('-' * 50)
    print(f'Running Panopticon on module {args.module}')
    print('-' * 50)
    print(f'maximum dependency depth: {args.max_depth}')
    print(f'stdlib dir is {args.stdlib_dir}')
    print(f'omit not found: {args.omit_not_found}')
    print('-' * 50)
    start = time.time()
    if args.module.endswith('.py'):
        spec = importlib.util.spec_from_file_location(
            args.module.replace('.py', ''), args.module
        )
        root_module = importlib.util.module_from_spec(spec)
    else:
        root_module = import_module(args.module)
    root_node = Node(root_module.__name__, module=root_module)
    if not args.no_sandbox:
        set_audit_hooks()
    get_imports(
        root_node,
        max_depth=args.max_depth,
        stdlib_dir=args.stdlib_dir,
        omit_not_found=args.omit_not_found,
    )
    remove_module_property(root_node)
    with open(f'{args.out}', 'w') as f:
        f.write(exporter.JsonExporter(indent=4).export(root_node))
    end = time.time()
    elapsed = '%.2fs' % (end - start)
    print('-' * 50)
    print(f'Done in {elapsed}')
    print(f'See {args.out}')
