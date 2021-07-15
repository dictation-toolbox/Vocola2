# -*- encoding: latin-1 -*-
###
### VocolaUtils.py - Code used by Vocola's generated Python code
###
###
### Copyright (c) 2002-2011 by Rick Mohr.
###
### Portions Copyright (c) 2015 by Hewlett-Packard Development Company, L.P.
###
### Permission is hereby granted, free of charge, to any person
### obtaining a copy of this software and associated documentation
### files (the "Software"), to deal in the Software without
### restriction, including without limitation the rights to use, copy,
### modify, merge, publish, distribute, sublicense, and/or sell copies
### of the Software, and to permit persons to whom the Software is
### furnished to do so, subject to the following conditions:
###
### The above copyright notice and this permission notice shall be
### included in all copies or substantial portions of the Software.
###
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
### EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
### MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
### NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
### HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
### WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
### OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
### DEALINGS IN THE SOFTWARE.
###

import re
import sys
from   types import *
import traceback  # for debugging traceback code in handle_error

import natlink
import natlinkutils

##
## Global variables:
##

# DNS short name of current SystemLanguage being used, set by _vocola_main.py:
SystemLanguage = None
Language = "enx"  ## for the moment QH




##
## Handling <_anything>:
##

#
# Massage recognition results to make a single entry for each
# <dgndictation> result.
#
def combineDictationWords(fullResults):
    i = 0
    inDictation = 0
    while i < len(fullResults):
        if fullResults[i][1] == "dgndictation":
            # This word came from a "recognize anything" rule.
            # Convert to written form if necessary, e.g. "@\at-sign" --> "@"
            word = fullResults[i][0]
            backslashPosition = word.find("\\")
            if backslashPosition > 0:
                word = word[:backslashPosition]
            if inDictation:
                fullResults[i-1] = [fullResults[i-1][0] + " " + word,
                                    "converted dgndictation"]
                del fullResults[i]
            else:
                fullResults[i] = [word, "converted dgndictation"]
                i = i + 1
            inDictation = 1
        else:
            i = i + 1
            inDictation = 0
    return fullResults



##
## Runtime error handling:
##

class VocolaRuntimeError(Exception):
    pass

# raise this to abort current utterance without error:
class VocolaRuntimeAbort(Exception):
    pass


def handle_error(filename, line, command, exception):
    if isinstance(exception, VocolaRuntimeAbort):
        return

    print()
    print("While executing the following Vocola command:", file=sys.stderr)
    print("    " + command, file=sys.stderr)
    print("defined at line " + str(line) + " of " + filename +",", file=sys.stderr)
    print("the following error occurred:", file=sys.stderr)
    print("    " + exception.__class__.__name__ + ": " \
        + str(exception), file=sys.stderr)
    #traceback.print_exc()
    #raise exception


def to_long(string):
    try:
        return int(string)
    except ValueError:
        raise VocolaRuntimeError("unable to convert '"
                                 + "'".replace("''")
                                 + "' into an integer")

def do_flush(functional_context, buffer):
    if functional_context:
        raise VocolaRuntimeError(
            'attempt to call Unimacro, Dragon, or a Vocola extension ' +
            'procedure in a functional context!')
    if buffer != '':
        natlinkutils.playString(convert_keys(buffer))
    return ''



##
## Dragon built-ins:
##

dragon_prefix = ""

def convert_keys(keys):
    # Roughly, {<keyname>_<count>}'s -> {<keyname> <count>}:
    #   (is somewhat generous about what counts as a key name)
    #
    # Because we can't be sure of the current code page, treat all non-ASCII
    # characters as potential accented letters for now.
    keys = re.sub(r"""(?x)
                      \{ ( (?: [a-zA-Z\x80-\xff]+ \+ )*
                           (?:[^}]|[-a-zA-Z0-9/*+.\x80-\xff]+) )
                      [ _]
                      (\d+) \}""", r'{\1 \2}', keys)

    # prefix with current SystemLanguage appropriate version of {shift}
    # to prevent doubling/dropping bug:
    shift = name_for_shift()
    if shift:
        keys = "{" + shift + "}" + keys

    return keys

def name_for_shift():
    if SystemLanguage == "enx":
        return "shift"
    elif SystemLanguage == "nld":
        return "shift"
    elif SystemLanguage == "fra":
        return "Maj"
    elif SystemLanguage == "deu":
        return "Umschalt"
    elif SystemLanguage == "ita":
        return "MAIUSC"
    elif SystemLanguage == "esp":
        return "MAY�S"
    else:
        return None

def call_Dragon(function_name, argument_types, arguments):
    global dragon_prefix

    def quoteAsVisualBasicString(argument):
        q = argument
        q = q.replace('"', '""')
        q = q.replace("\n", '" + chr$(10) + "')
        q = q.replace("\r", '" + chr$(13) + "')
        return '"' + q + '"'

    script = ""
    for argument in arguments:
        argument_type = argument_types[0]
        argument_types = argument_types[1:]

        if argument_type == 'i':
            argument = str(to_long(argument))
        elif argument_type == 's':
            if function_name == "SendDragonKeys" or function_name == "SendKeys" \
                    or function_name == "SendSystemKeys":
                argument = convert_keys(argument)
            argument = quoteAsVisualBasicString(str(argument))
        else:
            # there is a vcl2py.pl bug if this happens:
            raise VocolaRuntimeError("Vocola compiler error: unknown data type "
                                     + " specifier '" + argument_type +
                                     "' supplied for a Dragon procedure argument")

        if script != '':
            script += ','
        script += ' ' + argument

    script = dragon_prefix + function_name + script
    dragon_prefix = ""
    #print '[' + script + ']'
    try:
        if function_name == "SendDragonKeys":
            natlink.playString(convert_keys(arguments[0]))
        elif function_name == "ShiftKey":
            dragon_prefix = script + chr(10)
        else:
            natlink.execScript(script)
    except Exception as e:
        m = "when Vocola called Dragon to execute:\n" \
            + '        ' + script + '\n' \
            + '    Dragon reported the following error:\n' \
            + '        ' + type(e).__name__ + ": " + str(e)
        raise VocolaRuntimeError(m)



##
## Unimacro built-in:
##

# attempt to import Unimacro, suppressing errors, and noting success status:
unimacro_available = False
try:
    import unimacro.actions
    unimacro_available = True
except ImportError:
    pass
except OSError:
    # print 'cannot open Unimacro actions file'
    pass

def call_Unimacro(argumentString):
    if unimacro_available:
        #print '[' + argumentString + ']'
        try:
            actions.doAction(argumentString)
        except Exception as e:
            # traceback.print_exc()
            m = "when Vocola called Unimacro to execute:\n" \
                + '        Unimacro(' + argumentString + ')\n' \
                + '    Unimacro reported the following error:\n' \
                + '        ' + type(e).__name__ + ": " + str(e) 
                
            raise VocolaRuntimeError(m)
    else:
        m = '\n'.join(['Unimacro call failed because ',
                       '    the link with Unimacro is unavailable.',
                       '    You can fix this by switching on the option:',
                       '    "Vocola takes Unimacro Actions" in the',
                       '    program "Configure Natlink via GUI".'])
        raise VocolaRuntimeError(m)



##
## EvalTemplate built-in function:
##

def eval_template(template, *arguments):
    variables = {}

    waiting = list(arguments)
    def get_argument():
        if len(waiting) == 0:
            raise VocolaRuntimeError(
                "insufficient number of arguments passed to Eval[Template]")
        return waiting.pop(0)

    def get_variable(value):
        argument_number = len(arguments)-len(waiting)
        name = "v" + str(argument_number)
        variables[name] = value
        return name

    # is string the canonical representation of a long?
    def isCanonicalNumber(string):
        try:
            return str(int(string)) == string
        except ValueError:
            return 0

    def handle_descriptor(m):
        descriptor = m.group()
        if descriptor == "%%":
            return "%"
        elif descriptor == "%s":
            return get_variable(str(get_argument()))
        elif descriptor == "%i":
            return get_variable(to_long(get_argument()))
        elif descriptor == "%a":
            a = get_argument()
            if isCanonicalNumber(a):
                return get_variable(int(a))
            else:
                return get_variable(str(a))
        else:
            return descriptor

    expression = re.sub(r'%.', handle_descriptor, template)
    try:
        return eval('str(' + expression + ')', variables.copy())
    except VocolaRuntimeAbort:
        raise
    except Exception as e:
        m = "when Eval[Template] called Python to evaluate:\n" \
            + '        str(' + expression + ')\n' \
            + '    under the following bindings:\n'
        names = list(variables.keys())
        names.sort()
        for v in names:
            m += '        ' + str(v) + ' -> ' + repr(variables[v]) + '\n'
        m += '    Python reported the following error:\n' \
            + '        ' + type(e).__name__ + ": " + str(e)
        raise VocolaRuntimeError(m)
