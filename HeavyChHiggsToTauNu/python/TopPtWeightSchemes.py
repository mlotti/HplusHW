class TopPtWeight:
    def __init__(self, **kwargs):
        if "all" in kwargs:
            self.allhadronic = kwargs["all"]
            self.leptonjets = kwargs["all"]
            self.dilepton = kwargs["all"]
        else:
            for arg in ["allhadronic", "leptonjets", "dilepton"]:
                if arg in kwargs:
                    setattr(self, arg, kwargs[arg])
                else:
                    setattr(self, arg, "1.0")


# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting#Eventweight
_TopPtReweighting = "(x<=400.0)*(exp(%s + %s*x)) + (x>400.0)*1.0"
# https://indico.cern.ch/getFile.py/access?contribId=19&sessionId=2&resId=0&materialId=slides&confId=267832, AN-2013-145
_TTH = "(x<=463.312)*(1.18246+2.10061e-6*x*(x-2*463.312)) + (x>463.312)*0.732"

schemes = {
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting#Eventweight
    "TopPtCombined": TopPtWeight(all=_TopPtReweighting % ("0.156", "-0.00137")),
    "TopPtSeparate": TopPtWeight(leptonjets=_TopPtReweighting % ("0.159", "-0.00141"),
                                 dilepton=_TopPtReweighting % ("0.148", "-0.00129")),
    "TTH" : TopPtWeight(all=_TTH),
}

defaultScheme = "TopPtCombined"
