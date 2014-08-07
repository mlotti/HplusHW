# Generated on Fri Aug  1 09:24:49 2014
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
    "taup_Tlt50QCD"        : 0.063198745369,
    "taup_Teq50to60QCD"    : 0.0593405803646,
    "taup_Teq60to70QCD"    : 0.0537393363565,
    "taup_Teq70to80QCD"    : 0.0534628529326,
    "taup_Teq80to100QCD"   : 0.0581344895955,
    "taup_Teq100to120QCD"  : 0.0458454966738,
    "taup_Tgt120QCD"       : 0.0484729056085,
    "InclusiveQCD"         : 0.053044862261,
    "taup_Tlt50EWK_GenuineTaus": 1.5673733527,
    "taup_Teq50to60EWK_GenuineTaus": 1.90410535047,
    "taup_Teq60to70EWK_GenuineTaus": 1.74332911083,
    "taup_Teq70to80EWK_GenuineTaus": 1.35705636979,
    "taup_Teq80to100EWK_GenuineTaus": 2.13833851708,
    "taup_Teq100to120EWK_GenuineTaus": 2.10006152634,
    "taup_Tgt120EWK_GenuineTaus": 2.41424249765,
    "InclusiveEWK_GenuineTaus": 1.77298341889,
    "taup_Tlt50EWK_FakeTaus": 0.0947546598777,
    "taup_Teq50to60EWK_FakeTaus": 0.0742003705869,
    "taup_Teq60to70EWK_FakeTaus": 0.102668922894,
    "taup_Teq70to80EWK_FakeTaus": 0.0800378889312,
    "taup_Teq80to100EWK_FakeTaus": 0.148843578641,
    "taup_Teq100to120EWK_FakeTaus": 0.0838505049615,
    "taup_Tgt120EWK_FakeTaus": 0.0683109537868,
    "InclusiveEWK_FakeTaus": 0.0920404250071
}
