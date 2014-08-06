# Generated on Tue Jul  8 15:12:38 2014
# by InvertedTauID_Normalization.py

import sys

def QCDInvertedNormalizationSafetyCheck(era):
    validForEra = "Run2012ABCD"
    if not era == validForEra:
        print "Warning, inconsistent era, normalisation factors valid for",validForEra,"but trying to use with",era
        sys.exit()

QCDInvertedNormalization = {
    # Run2012ABCD
    # Light
    # TauIdAfterCollinearCuts
    "taup_Tlt50"           : 0.061374232419,
    "taup_Teq50to60"       : 0.0582062635047,
    "taup_Teq60to70"       : 0.0503509628139,
    "taup_Teq70to80"       : 0.0525480339576,
    "taup_Teq80to100"      : 0.0517767504225,
    "taup_Teq100to120"     : 0.0499502392909,
    "taup_Teq120to150"     : 0.0521929877425,
    "taup_Tgt150"          : 0.0463719886256,
    "Inclusive"            : 0.0533604853451,
}
