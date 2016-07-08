from FWCore.ParameterSet.Modules import _Module
class RemoveSoftMuonVisitor:
    def __init__(self):
        self.found = []

    def enter(self, visitee):
        if isinstance(visitee, _Module) and "softMuon" in visitee.label():
            self.found.append(visitee)

    def leave(self, visitee):
        pass

    def removeFound(self, process, sequence):
        for mod in self.found:
            print "Removing '%s' from sequence '%s' and process" % (mod.label(), sequence.label())
            sequence.remove(mod)
            delattr(process, mod.label())
