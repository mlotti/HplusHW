# Generated on Mon Oct 12 12:50:11 2015
# by InvertedTauID_Normalization_QCDandFakeTausFromData.py

import sys

def QCDInvertedNormalizationSafetyCheck(era):
    validForEra = "Run2015"
    if not era == validForEra:
        print "Warning, inconsistent era, normalisation factors valid for",validForEra,"but trying to use with",era
        sys.exit()

QCDInvertedNormalization = {
    # Run2015
    # 80to1000
    # AfterStdSelections
    "tauPtlt60QCD"                                               : -0.00591932365234,
    "tauPteq60to70QCD"                                           : 0.0172620204843,
    "tauPteq70to80QCD"                                           : 0.00840942348102,
    "tauPteq80to100QCD"                                          : 0.0675809395946,
    "tauPteq100to120QCD"                                         : 0.00866687751,
    "tauPtgt120QCD"                                              : 0.0116310738099,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveQCD"  : 0.00896873175383,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveQCD"  : 0.00896873175383,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveQCD"  : 0.00896873175383,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveQCD"  : 0.00896873175383,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveQCD"  : 0.00896873175383,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveQCD"  : 0.00896873175383,
    "tauPtlt60EWK_GenuineTaus": 1.70232848059,
    "tauPteq60to70EWK_GenuineTaus": 1.660955766,
    "tauPteq70to80EWK_GenuineTaus": 1.31127927998,
    "tauPteq80to100EWK_GenuineTaus": 1.69684714971,
    "tauPteq100to120EWK_GenuineTaus": 1.216558854,
    "tauPtgt120EWK_GenuineTaus": 2.27783181568,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_GenuineTaus": 1.6371398641,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_GenuineTaus": 1.6371398641,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_GenuineTaus": 1.6371398641,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_GenuineTaus": 1.6371398641,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_GenuineTaus": 1.6371398641,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_GenuineTaus": 1.6371398641,
    "tauPtlt60EWK_FakeTaus": 0.0556403109838,
    "tauPteq60to70EWK_FakeTaus": 0.0483551682998,
    "tauPteq70to80EWK_FakeTaus": 0.057001110609,
    "tauPteq80to100EWK_FakeTaus": 0.0274985214988,
    "tauPteq100to120EWK_FakeTaus": 0.0474458833334,
    "tauPtgt120EWK_FakeTaus": 0.00911106399377,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_FakeTaus": 0.0357697584282,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_FakeTaus": 0.0357697584282,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_FakeTaus": 0.0357697584282,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_FakeTaus": 0.0357697584282,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_FakeTaus": 0.0357697584282,
    "NormalizationMETBaselineTauAfterStdSelectionsInclusiveEWK_FakeTaus": 0.0357697584282
}
