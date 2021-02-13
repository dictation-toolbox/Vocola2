Place your Vocola2 extension files in the "extensions" subdirectory of the VocolaUserDirectory.

A few samples are in the Vocola2/extensions directory.

At start of _vocola_main.py, these samples are copied to the extensions subdirectory of the VocolaUserDirectory,
if needed. The directory is created at first run, and at each start of _vocola_main (Dragon),
files are checked for possible updates, and copied to the VocolaUserDirectory/extensions directory without further warning.

So if you make changes to one of the sample extension files, make a copy of the sample files first.

User defined extensions should be put directly in the VocolaUserDirectory/extensions directory.

See http://vocola.net/v2/UsingExtensions.asp for more information.
