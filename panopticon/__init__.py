import argparse

from panopticon.lib_resolver import get_lib_dir
from panopticon.scanner import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'module', action='store', help='Name of module you wish to scan'
    )
    parser.add_argument(
        '--show-lib-dir',
        action='store_true',
        help='Prints the automatically resolved builtin source directory.',
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
        '--auto-lib-dir',
        action='store_true',
        help='Automatically ignore builtin modules by lib path. MAY BE BUGGY!',
    )
    parser.add_argument(
        '--lib-dir',
        type=str,
        action='store',
        help='Ignore builtin modules by providing their path',
    )
    args = parser.parse_args()
    if args.show_lib_dir:
        print(get_lib_dir())
    else:
        if args.auto_lib_dir:
            args.lib_dir = get_lib_dir()
        run(args)


__all__ = ['main']
