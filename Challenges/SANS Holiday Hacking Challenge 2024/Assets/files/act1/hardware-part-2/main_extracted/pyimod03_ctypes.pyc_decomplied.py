# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: PyInstaller/loader/pyimod03_ctypes.py
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

"""
Hooks to make ctypes.CDLL, .PyDLL, etc. look in sys._MEIPASS first.
"""
import sys

def install():
    """
    Install the hooks.

    This must be done from a function as opposed to at module-level, because when the module is imported/executed,
    the import machinery is not completely set up yet.
    """
    import os
    try:
        import ctypes
    except ImportError:
        return None
    else:

        def _frozen_name(name):
            if name and (not os.path.isfile(name)):
                frozen_name = os.path.join(sys._MEIPASS, os.path.basename(name))
                if os.path.isfile(frozen_name):
                    name = frozen_name
            return name

        class PyInstallerImportError(OSError):

            def __init__(self, name):
                self.msg = 'Failed to load dynlib/dll %r. Most likely this dynlib/dll was not found when the application was frozen.' % name
                self.args = (self.msg,)

        class PyInstallerCDLL(ctypes.CDLL):

            def __init__(self, name, *args, **kwargs):
                name = _frozen_name(name)
                try:
                    super().__init__(name, *args, **kwargs)
                except Exception as base_error:
                    raise PyInstallerImportError(name) from base_error
        ctypes.CDLL = PyInstallerCDLL
        ctypes.cdll = ctypes.LibraryLoader(PyInstallerCDLL)

        class PyInstallerPyDLL(ctypes.PyDLL):

            def __init__(self, name, *args, **kwargs):
                name = _frozen_name(name)
                try:
                    super().__init__(name, *args, **kwargs)
                except Exception as base_error:
                    raise PyInstallerImportError(name) from base_error
        ctypes.PyDLL = PyInstallerPyDLL
        ctypes.pydll = ctypes.LibraryLoader(PyInstallerPyDLL)
        if sys.platform.startswith('win'):

            class PyInstallerWinDLL(ctypes.WinDLL):

                def __init__(self, name, *args, **kwargs):
                    name = _frozen_name(name)
                    try:
                        super().__init__(name, *args, **kwargs)
                    except Exception as base_error:
                        raise PyInstallerImportError(name) from base_error
            ctypes.WinDLL = PyInstallerWinDLL
            ctypes.windll = ctypes.LibraryLoader(PyInstallerWinDLL)

            class PyInstallerOleDLL(ctypes.OleDLL):

                def __init__(self, name, *args, **kwargs):
                    name = _frozen_name(name)
                    try:
                        super().__init__(name, *args, **kwargs)
                    except Exception as base_error:
                        raise PyInstallerImportError(name) from base_error
            ctypes.OleDLL = PyInstallerOleDLL
            ctypes.oledll = ctypes.LibraryLoader(PyInstallerOleDLL)
            try:
                import ctypes.util
            except ImportError:
                return None
            else:

                def pyinstaller_find_library(name):
                    if name in ['c', 'm']:
                        return ctypes.util.find_msvcrt()
                    search_dirs = [sys._MEIPASS] + os.environ['PATH'].split(os.pathsep)
                    for directory in search_dirs:
                        fname = os.path.join(directory, name)
                        if os.path.isfile(fname):
                            return fname
                        if fname.lower().endswith('.dll'):
                            continue
                        fname = fname + '.dll'
                        if os.path.isfile(fname):
                            return fname
                    else:
                        return None
                ctypes.util.find_library = pyinstaller_find_library
if sys.platform.startswith('darwin'):
    try:
        from ctypes.macholib import dyld
        dyld.DEFAULT_LIBRARY_FALLBACK.insert(0, sys._MEIPASS)
    except ImportError:
        pass