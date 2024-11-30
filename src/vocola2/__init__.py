"""Vocola"""

#version number now in project.toml

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
