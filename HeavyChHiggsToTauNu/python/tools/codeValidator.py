from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from sys import stdout

class CodeValidator:
    def __init__(self):
        self._n = 0
        self._package = None

    def setPackage(self, packageName):
        self._package = packageName
        print "\r- testing package: %s%s%s                "%(HighlightStyle(), self._package, NormalStyle())

    def finish(self):
        print "\r                                                                 "
        print HighlightStyle()+"All %d tests have been passed!              "%(self._n)+NormalStyle()

    def test(self, title, a, b):
        myStatus = False
        if isinstance(a, float) or isinstance(b, float):
            myStatus = abs(a-b) < 0.00001
        else:
            myStatus = a == b
        if myStatus:
            self._n += 1
            stdout.write("\r... testing ... %d    "%self._n)
            stdout.flush()
        else:
            print "\r... %s%s: test '%s' failed! value="%(ErrorLabel(), self._package, title), a, "correct=", b
            print "\n"
            raise Exception()

