### Known Limitations and Issues

1. ``__import__`` statements, [a way to import modules with a function](https://docs.python.org/3/library/functions.html#import__), is not supported *yet*.
2. C Extensions for Python are not evaluated.
3. Currently, tests are also considered as source files. This can lead to false positive imports
4. Panoptisch is very new, rigourous testing is required and is currently missing!
