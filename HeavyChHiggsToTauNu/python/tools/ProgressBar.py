import sys

class ProgressBar:
    def __init__(self, width):
        self._width = width

    def draw(self, ratio):
        myResult = "["
        a = int(ratio * self._width)
        for i in range(0, a):
            myResult += "."
        for i in range(a+1, self._width):
            myResult += " "
        myResult += "]"
        sys.stdout.write("\r"+myResult)
        sys.stdout.flush()

    def finished(self):
        myResult = "["
        for i in range(0,self._width):
            myResult += "."
        myResult += "]"
        print "\r"+myResult