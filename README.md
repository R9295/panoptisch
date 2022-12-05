 ## Panopticon: A recursive dependency scanner for Python projects

####  ⚠️🚨 Early stage! May not work as expected 🚨⚠️
#### What?
Panopticon scans your Python file or module to find it's imports (aka dependencies) and recursively does so for all dependencies and sub-dependencies.
It then generates a dependency tree in JSON for you to parse and enforce import policies.
Imports are resolved by mimicing Python's import system. It's completely static besides the importing of modules to find the location of its source file(s).

##### Please NOTE:
There are known **limitations and issues** at this stage. Please read this before using Panopticon.  
See: ``LIMITATIONS.md`` [LINK](LIMITATIONS.md).


#### Motivation
I was not able to find a proper dependency scanner for Python. Panopticon was born out of the need to accurately verify dependency usage accross an entire project.  
It's aim is to generate a JSON report that can be parsed and evaluated to **assert import policies**.  
For example, you may want to restrict ``os``, ``socket``, ``sys`` and ``importlib`` imports to selected packages.


#### Usage

1. Install ``Panopticon`` in the same virtual environment as your project, this is important!  
```
pip install <your_panopticon_download>.whl
```

2. Use
```
usage: panopticon <module>

positional arguments:
  module                Name of module or file you wish to scan.

options:
  -h, --help            show this help message and exit.
  --show-stdlib-dir     Prints the automatically resolved stdlib directory.
  --max-depth MAX_DEPTH
                        Maximum dependency depth.
  --out OUT             File to output report.
  --auto-stdlib-dir     Ignore stdlib modules by automatically resolving their path. MAY BE BUGGY. Try running panopticon <module_name> --show-stdlib-dir to see the directory before using this.
  --stdlib-dir STDLIB_DIR Ignore stdlib modules by providing their path.
  --omit-not-found      Do not include modules that could not be resolved in report.
```
A typical run may be
```
$ panopticon <module or file> --max-depth 5 --omit-not-found
```
3. See report
```
$ more out.json
```
#### LICENSE
All work is licensed under the [GNU General Public License Version 3](https://www.gnu.org/licenses/gpl-3.0.en.html).

#### Contributing
Feedback, contributions and issues welcome. 
