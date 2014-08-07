# Generated on Fri Aug  1 10:26:44 2014
# by InvertedTauID_QCDPlusEWKFakeTaus.py

import sys

def QCDInvertedNormalizationSafetyCheck(era):
    validForEra = "Run2012ABCD"
    if not era == validForEra:
        print "Warning, inconsistent era, normalisation factors valid for",validForEra,"but trying to use with",era
        sys.exit()

QCDInvertedNormalization = {
    "taup_Tlt50" : 0.0710877239962,
    "taup_Teq50to60" : 0.0630555279202,
    "taup_Teq60to70" : 0.0659717329909,
    "taup_Teq70to80" : 0.0601066119323,
    "taup_Teq80to100" : 0.0808117618569,
    "taup_Teq100to120" : 0.0553467487457,
    "taup_Tgt120" : 0.0534324176531,
    "Inclusive" : 0.0627937529475
}
