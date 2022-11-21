import importlib
import time

from anytree import Node, exporter
from panopticon.imports import import_module


def remove_module_property(node: Node):
    delattr(node, 'module')
    for child in node.children:
        remove_module_property(child)


def run(args):
    print(
        f'Running Panopticon on module {args.module} with maximum dependency depth of {args.max_depth}'  # noqa E501
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
    # get_imports(root_node, max_depth=args.max_depth)
    remove_module_property(root_node)
    with open(f'{args.out}', 'w') as f:
        f.write(exporter.JsonExporter(indent=4).export(root_node))
    end = time.time()
    elapsed = '%.2f' % (end - start)
    print(f'Done in {elapsed}')
    print(f'See {args.out}')
