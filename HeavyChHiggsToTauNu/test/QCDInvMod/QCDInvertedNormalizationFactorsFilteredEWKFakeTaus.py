# Generated on Wed Aug 13 15:50:07 2014
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
    "taup_Tlt50QCD"        : 0.0637906598414,
    "taup_Teq50to60QCD"    : 0.0614771085568,
    "taup_Teq60to70QCD"    : 0.0507851695155,
    "taup_Teq70to80QCD"    : 0.0517819571504,
    "taup_Teq80to100QCD"   : 0.0538461318351,
    "taup_Teq100to120QCD"  : 0.0493194303982,
    "taup_Tgt120QCD"       : 0.0489644134979,
    "InclusiveQCD"         : 0.053714063274,
    "taup_Tlt50EWK_GenuineTaus": 1.57369551835,
    "taup_Teq50to60EWK_GenuineTaus": 1.78280850126,
    "taup_Teq60to70EWK_GenuineTaus": 1.83717256993,
    "taup_Teq70to80EWK_GenuineTaus": 1.60683875573,
    "taup_Teq80to100EWK_GenuineTaus": 1.89657904785,
    "taup_Teq100to120EWK_GenuineTaus": 2.4305890989,
    "taup_Tgt120EWK_GenuineTaus": 1.82980209896,
    "InclusiveEWK_GenuineTaus": 1.72532700032,
    "taup_Tlt50EWK_FakeTaus": 0.0692925430542,
    "taup_Teq50to60EWK_FakeTaus": 0.0920306157198,
    "taup_Teq60to70EWK_FakeTaus": 0.106216393961,
    "taup_Teq70to80EWK_FakeTaus": 0.0813226249791,
    "taup_Teq80to100EWK_FakeTaus": 0.121028647693,
    "taup_Teq100to120EWK_FakeTaus": 0.130892419724,
    "taup_Tgt120EWK_FakeTaus": 0.0957805913665,
    "InclusiveEWK_FakeTaus": 0.0927116232936
}
