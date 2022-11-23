import argparse

from panopticon.lib_resolver import get_stdlib_dir
from panopticon.scanner import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'module',
        action='store',
        help='Name of module or file you wish to scan',
    )
    parser.add_argument(
        '--show-stdlib-dir',
        action='store_true',
        help='Prints the automatically resolved stdlib directory.',
    )
    parser.add_argument(
        '--max-depth',
        type=int,
        action='store',
        help='Maximum dependency depth.',
        default=3,
    )
    parser.add_argument(
        '--out',
        action='store',
        help='File to output JSON',
        default='out.json',
    )
    parser.add_argument(
        '--auto-stdlib-dir',
        action='store_true',
        help='Ignore stdlib modules by automatically resolving their path. MAY BE BUGGY. try running panopticon <module_name> --show-stdlib-dir to see the directory before using this.',  # noqa E501
    )
    parser.add_argument(
        '--stdlib-dir',
        type=str,
        action='store',
        help='Ignore stdlib modules by providing their path',
    )
    args = parser.parse_args()
    if args.show_stdlib_dir:
        print(get_stdlib_dir())
    else:
        if args.auto_stdlib_dir:
            args.stdlib_dir = get_stdlib_dir()
        run(args)


__all__ = ['main']
