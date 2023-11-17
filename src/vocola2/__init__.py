"""Vocola"""

__version__='3.1.8' #fix encoding line in outputfile
#__version__ = '3.1.6'    # bug fix/enhancing different takes languages and take unimacro actions comments for new vcl files.
## now in versions 3.1. series
# __version__ = '2.9.6'  # sendkeys again from Vocola, but via dtactions.
# __version__ = '2.9.5'  # make ready for improved pip
#             '2.9.4'  # bugfix, check for correct directories (VocolaUserDirectory, VocolaGrammarsDirectory)
#             '2.9.3'  # bugfix, typo
#             '2.9.2'  # bugfix, normpath changed into abspath
#             '2.9.1'  # initial version with python3

"""utility functions, to get calling directory of module (in site-packages),

...and to check the existence of a directory, for example .natlink in the home directory.

Note: -as user, having pipped the package, the scripts run from the site-packages directory
      -as developer, you have to clone the package, then `build_package` and,
       after a `pip uninstall vocola`, `flit install --symlink`.
       See instructions in the file README.md in the source directory of the package.

getThisDir: can be called in the calling module like:

```
try:
    from dtactions.__init__ import getThisDir, checkDirectory
except ModuleNotFoundError:
    print(f'Run this module after "build_package" and "flit install --symlink"\n')
    raise

thisDir = getThisDir(__file__)
```

checkDirectory(dirpath, create=True)
    create `dirpath` if not yet exists.
    when create=False is passed, no new directory is created, but an error is thrown if
    the directory does not exist.
"""
