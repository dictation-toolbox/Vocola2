"""this module performs several Vocola/Uniactions interaction actions at Natlink startup time

should be called from Vocola_main
2021-07-15, QH
Try to update: 2026-04-30
"""
#pylint:disable=C0209
import os               # access to file information
import os.path          # to parse filenames
import stat
import re
import shutil
import sys
from natlinkcore import natlinkstatus
from natlinkcore import readwritefile
status = natlinkstatus.NatlinkStatus()
#
# This function is called by natlinkmain when starting up just before
# loading grammars for the first time:
#
def start():
    """starting two features of Vocola
    """
    # print('--- natlinkvocolastartup starting...')
    updateUniactionsHeaderIfNeeded()
    create_new_language_subdirectory_if_needed()
##
## Update user's copy of Uniactions.vch if a more recent version is
## available
##

def updateUniactionsHeaderIfNeeded():
    """check the Uniactions header for include Uniactions.vch
    """
    if not status.getVocolaTakesUniactions(): 
        return
        
    destDir              = status.getVocolaUserDirectory()
    uniactionsDir          = status.getDtactionsDirectory()
    # coreFolder           = os.path.split(__file__)[0]
    # sourceDir            = os.path.normpath(os.path.join(coreFolder, "..", "..", "..",
    #                                     "Uniactions", 'vocola_compatibility'))
    sourceDir            = os.path.join(uniactionsDir, 'vocola_compatibility')
    destPath             = os.path.join(destDir,   'Uniactions.vch')
    sourcePath           = os.path.join(sourceDir, 'Uniactions.vch')
    # print(f'updateUniactionsHeaderIfNeeded\n\tsourcePath: {sourcePath}\n\tdestPath:  {destPath}\n=====')
    sourceTime, destTime = vocolaGetModTime(sourcePath), \
                           vocolaGetModTime(destPath)

    if not (sourceTime or destTime):
        print("""\n
Error: The option "Vocola Takes Uniactions Actions" is switched on, but
no file "Uniactions.vch" is found.

Please fix the configuration of Natlink/Vocola/Uniactions and restart
Dragon.  Either ensure the source file is at:
    "%s",
or switch off the option "Vocola Takes Uniactions Actions".
"""% sourceDir, file=sys.stderr)
        return
        
    if destTime < sourceTime:
        try:
            shutil.copyfile(sourcePath, destPath)
        except OSError:
            print("""\n
Warning: Could not copy example "Uniactions.vch" to:
    "%s".

There is a valid "Uniactions.vch" available, but a newer file is
available at: "%s".

Please fix the configuration of Natlink/Vocola/Uniactions and restart
Dragon, if you want to use the updated version of this file."""% (destDir, sourceDir), file=sys.stderr)
        else:
            print('Succesfully copied "Uniactions.vch" from\n\t"%s" to\n\t"%s".'% (sourceDir, destDir))

# Returns the modification time of a file or 0 if the file does not exist:
def vocolaGetModTime(file):
    """get date/time of file, 0 if not exists
    """
    #pylint:disable=C0321
    try: return os.stat(file)[stat.ST_MTIME]
    except OSError: return 0        # file not found

## 
## Quintijn's unofficial multiple language kludge:
## 

def create_new_language_subdirectory_if_needed():
    """create a language subdirectory for Vocola if needed
    
    This is the case when the user language is non-English (not "enx"), and
    the option VocolaTakesLanguages is set.
    """
    VocolaEnabled = bool(status.getVocolaUserDirectory())
    language      = status.language
    commandFolder = status.getVocolaUserDirectory()
    if not os.path.isdir(commandFolder):                      
        commandFolder = None

    if VocolaEnabled and status.getVocolaTakesLanguages():
        if language != 'enx' and commandFolder:
            uDir  = commandFolder
            uDir2 = os.path.join(uDir, language)
            if not os.path.isdir(uDir2):
                print('creating Vocola command subfolder for language %s' % language)
                os.mkdir(uDir2)
                copyToNewSubDirectory(uDir, uDir2)

def copyToNewSubDirectory(trunk, subdirectory):
    """utility function
    """
    for f in os.listdir(trunk):
        if f.endswith('.vcl'):
            copyVclFileLanguageVersion(os.path.join(trunk, f),
                                       os.path.join(subdirectory, f))

def copyVclFileLanguageVersion(Input, Output):
    """copy to another location, keeping the include files one directory above
    """
    # let include lines to relative paths point to the folder above ..\
    # so you can take the same include file for the alternate language.
    reInclude = re.compile(r'^(\s*include\b\s*[\'\"]?)([^\s;=][^;=\n]*\s*;.*)$')
    Input     = os.path.normpath(Input)
    Output    = os.path.normpath(Output)
    rwfile = readwritefile.ReadWriteFile()
    inputString = rwfile.readAnything(Input)
    # inputString = open(Input, 'r').read()

    # output    = open(Output, 'w')
    language      = status.language
    output = [f'# vocola file for alternate language: {language}\n']

    lines = list(map(lambda s: s.strip(), inputString.split('\n')))
    for line in lines:
        m = reInclude.match(line)
        if m:
            line = m.group(1) + "..\\" + m.group(2) 
        output.append(line + '\n')
    print(f'write to languageversion: {language}: {Output}')
    rwfile.writeAnything(Output, ''.join(output))

    # output.close()                

if __name__ == "__main__":
    start()
    