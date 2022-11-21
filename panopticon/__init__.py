import argparse

from panopticon.scanner import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'module', action='store', help='Name of module you wish to scan'
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
    args = parser.parse_args()
    run(args)


__all__ = ['main']
