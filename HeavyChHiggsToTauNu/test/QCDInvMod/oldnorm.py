# Generated on Sun Jul 20 15:00:50 2014
# by InvertedTauID_NormalizationWithFakeTaus.py

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
    "0"             : 0.0618941091,
    "1"             : 0.0565069427358,
    "2"             : 0.0511387170788,
    "3"             : 0.0522396219738,
    "4"             : 0.050964213702,
    "5"             : 0.0525152351566,
    "6"             : 0.0542860035726,
    "7"             : 0.0463090475819,
    "Inclusive"     : 0.0526625347039,
    "0EWK_GenuineTaus": 1.50818549934,
    "1EWK_GenuineTaus": 1.50596037458,
    "2EWK_GenuineTaus": 1.51761090263,
    "3EWK_GenuineTaus": 1.34768039612,
    "4EWK_GenuineTaus": 1.75385285917,
    "5EWK_GenuineTaus": 1.70935851638,
    "6EWK_GenuineTaus": 1.33996232198,
    "7EWK_GenuineTaus": 2.08380995911,
    "InclusiveEWK_GenuineTaus": 1.53323341092,
    "0EWK_FakeTaus": 0.0893856104567,
    "1EWK_FakeTaus": 0.104349623105,
    "2EWK_FakeTaus": 0.109551476433,
    "3EWK_FakeTaus": 0.0946315250502,
    "4EWK_FakeTaus": 0.116610852797,
    "5EWK_FakeTaus": 0.091912842879,
    "6EWK_FakeTaus": 0.118418968284,
    "7EWK_FakeTaus": 0.0468091525714,
    "InclusiveEWK_FakeTaus": 0.0980493796973
}
