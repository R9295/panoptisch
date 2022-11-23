import importlib
import os
import time

from anytree import Node, exporter

from panopticon.imports import import_module, resolve_imports
from panopticon.util import get_file_dir


def remove_module_property(node: Node):
    delattr(node, 'module')
    for child in node.children:
        remove_module_property(child)


def get_module(module_name: str, file: str, current_root: Node):
    '''
    We don't care if we're importing a sub-module as it's not nested and
    it's imports will be scanned anyways
    '''
    if module_name != 'None':
        parent_dir = get_file_dir(file)
        is_part_of_module = file.endswith('__init__.py') or os.path.exists(
            f'{parent_dir}/__init__.py'
        )
        if os.path.isfile(f'{parent_dir}/{module_name}.py'):
            if not is_part_of_module:
                spec = importlib.util.spec_from_file_location(
                    module_name, f'{parent_dir}/{module_name}.py'
                )
                module = importlib.util.module_from_spec(spec)
                return module, module_name
            else:
                return False, module_name
        elif os.path.isdir(f'{parent_dir}/{module_name}'):
            if not is_part_of_module:
                if os.path.exists(f'{parent_dir}/{module_name}/__init__.py'):
                    spec = importlib.util.spec_from_file_location(
                        module_name, f'{parent_dir}/{module_name}/__init__.py'
                    )
                    module = importlib.util.module_from_spec(spec)
                    return module, module_name
            else:
                return False, module_name
        else:
            try:
                return importlib.import_module(module_name), module_name
            except ModuleNotFoundError:
                print(
                    f'AAAAAA Could not resolve: {module_name}, current_root = {current_root.module.__name__}'  # noqa E501
                )
    return None, module_name


def get_imports(
    current_root: Node, module_list=[], lib_dir=None, depth=0, max_depth=15
):
    depth += 1
    if depth == max_depth:
        return
    imports = resolve_imports(current_root.module)
    for item in imports:
        file = item.get('file')
        file_imports = item.get('imports')
        for module_name in file_imports:
            if module_name not in module_list:
                if lib_dir and lib_dir in file and 'site-packages' not in file:
                    continue
                module, name = get_module(module_name, file, current_root)
                if module:
                    node = Node(
                        name,
                        module=module,
                        parent=current_root,
                    )
                    module_list.append(module_name)
                    get_imports(
                        node,
                        lib_dir=lib_dir,
                        module_list=module_list,
                        depth=depth,
                        max_depth=max_depth,
                    )
                    module_list.remove(module_name)
                else:
                    if module is not False:
                        node = Node(
                            module_name,
                            parent=current_root,
                            module=None,
                            reason='ModuleNotFoundError',
                        )


def run(args):
    print(
        f'Running Panopticon on module {args.module} with maximum dependency depth of {args.max_depth}. Lib dir is {args.lib_dir}'  # noqa E501
    )
    start = time.time()
    if args.module.endswith('.py'):
        spec = importlib.util.spec_from_file_location(
            args.module.replace('.py', ''), args.module
        )
        root_module = importlib.util.module_from_spec(spec)
    else:
        root_module = import_module(args.module)
    root_node = Node(args.module.replace('.py', ''), module=root_module)
    get_imports(root_node, max_depth=args.max_depth, lib_dir=args.lib_dir)
    remove_module_property(root_node)
    with open(f'{args.out}', 'w') as f:
        f.write(exporter.JsonExporter(indent=4).export(root_node))
    end = time.time()
    elapsed = '%.2f' % (end - start)
    print(f'Done in {elapsed}')
    print(f'See {args.out}')
