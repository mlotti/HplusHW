## Collection of functions for adding colourful printing to shell via escapes
# Note: to end the style, call ShellStyles.NormalStyle()

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

def WarningLabel():
    return "%sWarning:%s "%(WarningStyle(),NormalStyle())

def ErrorLabel():
    return "%sError:%s "%(ErrorStyle(),NormalStyle())
