# Generated on Fri May 23 10:54:50 2014
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
    "0"           : 0.0676020214328,
    "1"       : 0.0679528325628,
    "2"       : 0.0606206961163,
    "3"       : 0.0629403891595,
    "4"      : 0.0609005601053,
    "5"     : 0.0564183875353,
    "6"     : 0.049831912837,
    "7"          : 0.0497258200166,
    "Inclusive"            : 0.0555065566008,
    "0EWK": 0.763317652608,
    "1EWK": 0.788890661569,
    "2EWK": 0.833138360478,
    "3EWK": 0.699736947122,
    "4EWK": 0.901115546282,
    "5EWK": 0.802318349228,
    "6EWK": 0.708215871453,
    "7EWK": 0.720851083854,
    "InclusiveEWK": 0.784712669879
}
