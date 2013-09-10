## Package for all systematic uncertainties in the analysis

# List of shape uncertainties

shapeUncertaintiesWithoutBtag = ["JER", "TES", "JES", "MET", "TauTrgSF", "METTrgSF", "PUWeight"]
shapeUncertainties = shapeUncertaintiesWithoutBtag.copy().extend(["BTagSF"])

shapeUncertaintiesQCDMeasurementWithoutBtag = shapeUncertaintiesWithoutBtag.copy().extend(["QCDNorm"])
shapeUncertaintiesQCDMeasurement = shapeUncertainties.copy().extend(["QCDNorm"])

scalarUncertaintiesBase = {
    "Lepton veto": 0.002,
    "xsectionPlus": 0.062, # 7 TeV ttbar xsection (use it for all MC samples as conservative approximation)
    "xsectionMinus": 0.053, # 7 TeV ttbar xsection (use it for all MC samples as conservative approximation)
}

scalarUncertaintiesGenuineTau = scalarUncertaintiesBase.copy()
scalarUncertaintiesGenuineTau["tau ID"] = 0.07

scalarUncertaintiesFakeTau = scalarUncertaintiesBase.copy()
scalarUncertaintiesFakeTau["tau misID"] = 0.15

scalarUncertaintiesForEmbedding = scalarUncertaintiesBase.copy()
#scalarUncertaintiesForEmbedding[...] = ...:
# FIXME: Add embedding specific uncertainties here


#######################################
# List of considered uncertainties
#######################################
# Tau trg SF uncertainty:         shape
# MET trg SF uncertainty:         shape
# tau ID uncertainty:             scalar
# tau mis-ID uncertainty:         scalar
# fake tau SF uncertainty:        FIXME
# tau energy scale (TES):         shape
# jet energy scale (JES):         shape
# MET (unclustered) energy scale: shape
# jet energy resolution (JER):    shape
# e/mu reco and ID:               scalar
# btag SF:                        shape
# top pT reweight SF uncertainty: FIXME is this needed?
# QCD method normalization:       shape
# Embedding specific:             scalar
# pileup uncertainty:             shape
# luminosity uncertainty:         shape
# cross section uncertainties:    scalar
# (statistical uncertainties:     shape)
#######################################



