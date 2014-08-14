# Generated on Wed Aug 13 16:33:40 2014
# by InvertedTauID_QCDPlusEWKFakeTaus.py

import sys

def QCDInvertedNormalizationSafetyCheck(era):
    validForEra = "Run2012ABCD"
    if not era == validForEra:
        print "Warning, inconsistent era, normalisation factors valid for",validForEra,"but trying to use with",era
        sys.exit()

QCDInvertedNormalization = {
    "taup_Tlt50" : 0.0639282069217,
    "taup_Teq50to60" : 0.0622409462359,
    "taup_Teq60to70" : 0.0521709501266,
    "taup_Teq70to80" : 0.0525204738461,
    "taup_Teq80to100" : 0.0555256947315,
    "taup_Teq100to120" : 0.0513587551313,
    "taup_Tgt120" : 0.0501348179446,
    "Inclusive" : 0.0546890022745
}
