#
# QH, python helper functions
#     convert a print line into a formatted print line
# Quintijn Hoogenboom, 2020-08-22
#
# catches the clipboard, and pastes back if there is relevant input, and there were changes
from dtactions import natlinkclipboard
import re

rePrintLineDoubleQuote = re.compile(r'(\s*)print\((\")([^\"]+)\"%(.*$)')
rePrintLineSingleQuote = re.compile(r"(\s*)print\((\')([^\"]+)\'%(.*$)")

# Vocola function: Pythonhelpers.MakeFormattedPrintLine
def make_formatted_print_line():
    clip = natlinkclipboard.Clipboard()
    t = clip.Get_text()
    t = t.rstrip()
    print(f"make_formatted_print_line, input {t}")
    tnew = _reformat_print_line(t)
    if tnew is None:
        print("make_formatted_print_line, no processing")
        return t
    if t == tnew:
        print("make_formatted_print_line, no changes")
        return '{end}'
    return tnew

def _reformat_print_line(t):
    """from % formatted text into f"" text
>>> _reformat_print_line('    print("hello world %s"% var)')
'    print(f"hello world {var}")'
>>> _reformat_print_line('    print("hello %s more %s variables %s"% (2, world, var_name))') 
'    print(f"hello {2} more {world} variables {var_name}")'

    """
    if t.find('print(f') >= 0:
        print('print line already formatted in "f" style')
        return
    
    if t.find('\n') >= 0:
        print("use of make_formatted_print_line limited to one line")
        return
    m = rePrintLineDoubleQuote.match(t)
    if m:
        groups = m.groups()
    else:
        m = rePrintLineSingleQuote.match(t)
        if m:
            groups = m.groups
        else:
            return
    initial_spacing, quote, formatstring, rest = groups
    result = _reformat_internals(formatstring, rest)
    if result: 
        newformatstring, newrest = result
        return initial_spacing + "print(f" + quote + newformatstring + quote + newrest
    else:
        return
    
def _reformat_internals(formatstring, rest):
    """handles the internal processing, independent of ' or ""
    """
    formatparts = formatstring.split("%s")
    paren_level = 0
    more_variables = False
    ## go forward until no matching parens are found any more:
    for i, s in enumerate(rest):
        if s == "(":
            paren_level += 1
            more_variables = True
        if s == ")":
            if paren_level: paren_level -= 1
            else:
                endpos = i
                break
    else:
        print(f"invalid variables part: {rest}")
        return
    vars_part, real_rest = rest[:endpos], rest[endpos:]
    if more_variables:
        vars_part = vars_part.strip()
        vars_part = vars_part.lstrip("(")
        vars_part = vars_part.rstrip(")")
        variables = [var.strip() for var in vars_part.split(",")]
    else:
        variables = [vars_part.strip()]
    newformatparts = []
    for i, part in enumerate(formatparts):
        newformatparts.append(part)
        try:
            newformatparts.append("{%s}"% variables[i])
        except IndexError:
            pass
        
    newformatstring = ''.join(newformatparts)        
    newrest = real_rest
    return newformatstring, newrest

if __name__ == "__main__":
    import doctest
    doctest.testmod()
