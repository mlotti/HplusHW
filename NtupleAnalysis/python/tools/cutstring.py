## \package cutstring
# Logical operations for cut strings (for TTree::Draw)
#
# TCut has quite cumbersome syntax in PyROOT, and operating with
# python strings is very straightforward in the end

## Is the string empty?
#
# Intended for internal use
def _isNotEmpty(string):
    return string != ""

## Construct 'and' of the argument strings
#
# \param args   String arguments
#
# \return 'and' of arguments
#
# Empty arguments are ignored
def And(*args):
    lst = filter(_isNotEmpty, args)
    return "("+"&&".join(lst)+")"

## Construct 'not' of the argument string
#
# \param arg  String
#
# \return 'not' of argument. If argument is empty, empty string is returned.
def Not(arg):
    if _isNotEmpty(arg):
        return "(!(%s))"%arg
    else:
        return ""

## Construct 'or' of the argument strings
#
# \param args   String arguments
#
# \return 'or' of arguments
#
# Empty arguments are ignored
def Or(*args):
    lst = filter(_isNotEmpty, args)
    return "("+"||".join(lst)+")"
