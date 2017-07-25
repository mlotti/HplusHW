## Collection of functions for adding colourful printing to shell via escapes
# Note: to end the style, call ShellStyles.NormalStyle()

def NoteStyle():
    # White text on magent background, bold
    return "\033[0;45m\033[1;37m"

def WarningStyle():
    # White text on orange background, bold
    return "\033[0;43m\033[1;37m"

def ErrorStyle():
    # White text on red background, bold
    return "\033[0;41m\033[1;37m"

def HighlightStyle():
    # White text on black background, bold
    return "\033[0;40m\033[1;37m"

def CaptionStyle():
    # White text on blue background, bold
    return "\033[0;44m\033[1;37m"

def NormalStyle():
    # Normal text on normal background, bold
    return "\033[0;0m"

def TestPassedStyle():
    # green text, bold
    return "\033[1;32m"

def ResultStyle():
    # green text, bold
    return TestPassedStyle()

def NoteLabel():
    # white text on magenta backround
    return "%sNOTE:%s "% (NoteStyle() ,NormalStyle())

def WarningLabel():
    return "%sWARNING:%s "%(WarningStyle(),NormalStyle())

def ErrorLabel():
    return "%sERROR:%s "%(ErrorStyle(),NormalStyle())

def HighlightAltStyle():
    '''
    https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

    Foreground Code | 30 31 32 33 34 35 36 37
    Background Code | 40 41 42 43 44 45 46 47
    ==========================================
                      B  R  G  Y  B  M  C  W    
    RED   = "\033[1;31m"  
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m"
    '''
    # cyan  text on white backround
    #return "\033[;47m\033[1;36m"

    # blue text on black backround
    return "\033[;40m\033[1;34m"

def SuccessStyle():
    # green text on black backround
    # return "\033[;40m\033[1;32m"
    
    # black text on green backround
    return "\033[;40m\033[1;42m"

