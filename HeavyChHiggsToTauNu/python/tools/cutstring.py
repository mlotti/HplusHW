def _isNotEmpty(string):
    return string != ""

def And(*args):
    lst = filter(_isNotEmpty, args)
    return "("+"&&".join(lst)+")"

def Not(arg):
    if _isNotEmpty(arg):
        return "(!(%s))"%arg
    else:
        return ""

def Or(*args):
    lst = filter(_isNotEmpty, args)
    return "("+"||".join(lst)+")"
