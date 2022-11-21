import sys


def get_lib_dir():
    major = sys.version_info.major
    minor = sys.version_info.minor
    if sys.platform not in ['win32', 'cygwin']:
        for path in sys.path:
            if path.endswith(f'/lib/python{major}.{minor}'):
                return path
    raise Exception(
        "Panopticon cannot automatically resolve Python's lib directory. Please provide it yourself with --lib-dir."
    )
