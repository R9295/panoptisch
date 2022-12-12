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


A minimal "sandbox" that is NOT foolproof!
see: https://redoste.xyz/2020/05/04/fr-write-up-fcsc-2020-why-not-a-sandbox/
'''
import sys

# https://docs.python.org/3/library/audit_events.html
# py version 3.11.1
'''
The following events are exlcuded from rejection as panoptisch needs them:
builtins.id
glob.glob
glob.glob/2
import
marshall.loads
os.listdir
os.scandir
sys._getframe
object.__delattr__
object.__getattr__
object.__setattr__
sys.unraisablehook
sys.excepthook",
open
exec
'''
EVENTS_TO_REJECT = [
    "builtins.input",
    "builtins.input/result",
    "code.__new__",
    "cpython.pyinterpreterstate_clear",
    "cpython.pyinterpreterstate_new",
    "cpython._pysys_clearaudithooks",
    "cpython.run_command",
    "cpython.run_file",
    "cpython.run_interactivehook",
    "cpython.run_module",
    "cpython.run_startup",
    "cpython.run_stdin",
    "ctypes.addressof",
    "ctypes.call_function",
    "ctypes.cdata",
    "ctypes.cdata/buffer",
    "ctypes.create_string_buffer",
    "ctypes.create_unicode_buffer",
    "ctypes.dlopen",
    "ctypes.dlsym",
    "ctypes.dlsym/handle",
    "ctypes.get_errno",
    "ctypes.get_last_error",
    "ctypes.seh_exception",
    "ctypes.set_errno",
    "ctypes.set_last_error",
    "ctypes.string_at",
    "ctypes.wstring_at",
    "ensurepip.bootstrap",
    "fcntl.fcntl",
    "fcntl.flock",
    "fcntl.ioctl",
    "fcntl.lockf",
    "ftplib.connect",
    "ftplib.sendcmd",
    "function.__new__",
    "gc.get_objects",
    "gc.get_referents",
    "gc.get_referrers",
    "http.client.connect",
    "http.client.send",
    "imaplib.open",
    "imaplib.send",
    "marshal.dumps",
    "marshal.load",
    "mmap.__new__",
    "msvcrt.get_osfhandle",
    "msvcrt.locking",
    "msvcrt.open_osfhandle",
    "nntplib.connect",
    "nntplib.putline",
    "os.add_dll_directory",
    "os.chdir",
    "os.chflags",
    "os.chmod",
    "os.chown",
    "os.exec",
    "os.fork",
    "os.forkpty",
    "os.fwalk",
    "os.getxattr",
    "os.kill",
    "os.killpg",
    "os.link",
    "os.listxattr",
    "os.lockf",
    "os.mkdir",
    "os.posix_spawn",
    "os.putenv",
    "os.remove",
    "os.removexattr",
    "os.rename",
    "os.rmdir",
    "os.setxattr",
    "os.spawn",
    "os.startfile",
    "os.startfile/2",
    "os.symlink",
    "os.system",
    "os.truncate",
    "os.unsetenv",
    "os.utime",
    "os.walk",
    "pathlib.path.glob",
    "pathlib.path.rglob",
    "pdb.pdb",
    "pickle.find_class",
    "poplib.connect",
    "poplib.putline",
    "pty.spawn",
    "resource.prlimit",
    "resource.setrlimit",
    "setopencodehook",
    "shutil.chown",
    "shutil.copyfile",
    "shutil.copymode",
    "shutil.copystat",
    "shutil.copytree",
    "shutil.make_archive",
    "shutil.move",
    "shutil.rmtree",
    "shutil.unpack_archive",
    "signal.pthread_kill",
    "smtplib.connect",
    "smtplib.send",
    "socket.__new__",
    "socket.bind",
    "socket.connect",
    "socket.getaddrinfo",
    "socket.gethostbyaddr",
    "socket.gethostbyname",
    "socket.gethostname",
    "socket.getnameinfo",
    "socket.getservbyname",
    "socket.getservbyport",
    "socket.sendmsg",
    "socket.sendto",
    "socket.sethostname",
    "sqlite3.connect",
    "sqlite3.connect/handle",
    "sqlite3.enable_load_extension",
    "sqlite3.load_extension",
    "subprocess.popen",
    "sys._current_exceptions",
    "sys._current_frames",
    "sys.set_asyncgen_hooks_finalizer",
    "sys.set_asyncgen_hooks_firstiter",
    "sys.setprofile",
    "sys.settrace",
    "syslog.closelog",
    "syslog.openlog",
    "syslog.setlogmask",
    "syslog.syslog",
    "telnetlib.telnet.open",
    "telnetlib.telnet.write",
    "tempfile.mkdtemp",
    "tempfile.mkstemp",
    "urllib.request",
    "webbrowser.open",
    "winreg.connectregistry",
    "winreg.createkey",
    "winreg.deletekey",
    "winreg.deletevalue",
    "winreg.disablereflectionkey",
    "winreg.enablereflectionkey",
    "winreg.enumkey",
    "winreg.enumvalue",
    "winreg.expandenvironmentstrings",
    "winreg.loadkey",
    "winreg.openkey",
    "winreg.openkey/result",
    "winreg.pyhkey.detach",
    "winreg.queryinfokey",
    "winreg.queryreflectionkey",
    "winreg.queryvalue",
    "winreg.savekey",
    "winreg.setvalue",
]


class RestrictedEventException(Exception):
    pass


def hook(event, event_args):
    # TODO: maybe reject ctypes import?
    if event in EVENTS_TO_REJECT:
        raise RestrictedEventException(
            f'A restricted function, "{event}", was run while importing a dependency. Please see the traceback to examine which dependency was calling this function. You can ignore the sandbox by adding the --no-sandbox parameter. If you have feedback about this functionality, or would like more granular filters, please submit an issue in the repo.\nAborting the scan.'  # noqa E501
        )
        sys.exit(1)


def set_audit_hooks():
    sys.addaudithook(hook)
