#!/usr/bin/env python

from HiggsAnalysis.NtupleAnalysis.main import PSet
import HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors


#====== General parameters
histoLevel = "Debug"  # Options: Systematics, Vital, Informative, Debug

#====== Trigger
trg = PSet(
  # No need to specify version numbers, they are automatically scanned in range 1--100 (remove the '_v' suffix)
  L1ETM = 80,
  triggerOR = ["HLT_LooseIsoPFTau50_Trk30_eta2p1_MET90"
               ],
  triggerOR2 = [],
)

#====== MET filter
metFilter = PSet(
  discriminators = ["hbheNoiseTokenRun2Loose", # Loose is recommended
#                    "hbheIsoNoiseToken", # under scrutiny
                    "Flag_HBHENoiseIsoFilter",
                    "Flag_EcalDeadCellTriggerPrimitiveFilter",
                    "Flag_CSCTightHaloFilter",
                    "Flag_eeBadScFilter",
                    "Flag_goodVertices",
                    "Flag_globalTightHalo2016Filter",
                    "badPFMuonFilter",
                    "badChargedCandidateFilter"]
)

#====== Tau selection
tauSelection = PSet(
  applyTriggerMatching = True,
   triggerMatchingCone = 0.1,   # DeltaR for matching offline tau with trigger tau
              tauPtCut = 60.0, #for heavy H+, overriden in signalAnalysis.py for light H+
             tauEtaCut = 2.1,
        tauLdgTrkPtCut = 30.0,
                prongs = 13,    # options: 1, 2, 3, 12, 13, 23, 123 or -1 (all)
                  rtau = 0.0,   # to disable set to 0.0
  againstElectronDiscr = "againstElectronTightMVA6",
#  againstElectronDiscr = "",
      againstMuonDiscr = "againstMuonLoose3",
#        isolationDiscr = "byMediumIsolationMVA3oldDMwLT",
        isolationDiscr = "byLooseCombinedIsolationDeltaBetaCorr3Hits",
)
# tau misidentification scale factors
scaleFactors.assignTauMisidentificationSF(tauSelection, "eToTau", "full", "nominal")
scaleFactors.assignTauMisidentificationSF(tauSelection, "muToTau", "full", "nominal")
scaleFactors.assignTauMisidentificationSF(tauSelection, "jetToTau", "full", "nominal")
# tau trigger SF
scaleFactors.assignTauTriggerSF(tauSelection, "nominal")

#====== Electron veto
eVeto = PSet(
         electronPtCut = 15.0,
        electronEtaCut = 2.5,
#            electronID = "mvaEleID_PHYS14_PU20bx25_nonTrig_V1_wp90", # highest (wp90) for vetoing (2012: wp95)
            electronID = "cutBasedElectronID_Spring15_25ns_V1_standalone_veto",
     electronIsolation = "veto", # loosest possible for vetoing ("veto"), "tight" for selecting
)

#====== Muon veto
muVeto = PSet(
             muonPtCut = 10.0,
            muonEtaCut = 2.5,
                muonID = "muIDLoose", # loosest option for vetoing (options: muIDLoose, muIDMedium, muIDTight)
         muonIsolation = "veto", # loosest possible for vetoing ("veto"), "tight" for selecting
)

#====== Jet selection
jetSelection = PSet(
               jetType = "Jets", # options: Jets (AK4PFCHS), JetsPuppi (AK4Puppi)
              jetPtCut = 30.0,
             jetEtaCut = 4.7,
     tauMatchingDeltaR = 0.4,
  numberOfJetsCutValue = 3,
  numberOfJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
            jetIDDiscr = "IDloose", # options: IDloose, IDtight, IDtightLeptonVeto
          jetPUIDDiscr = "", # does not work at the moment 
)
 
#====== Angular cuts / collinear
angularCutsCollinear = PSet(
       nConsideredJets = 3,    # Number of highest-pt jets to consider (excluding jet corresponding to tau)
enableOptimizationPlots = True, # 2D histograms for optimizing angular cuts
        cutValueJet1 = 0.0,   # Cut value in degrees (circular cut)
        cutValueJet2 = 0.0,   # Cut value in degrees (circular cut)
        cutValueJet3 = 0.0,   # Cut value in degrees (circular cut)
        cutValueJet4 = 0.0,   # Cut value in degrees (circular cut)
)
 
#====== B-jet selection
bjetSelection = PSet(
              jetPtCut = 30.0,
             jetEtaCut = 2.5,
             #bjetDiscr = "combinedInclusiveSecondaryVertexV2BJetTags",
             bjetDiscr = "pfCombinedInclusiveSecondaryVertexV2BJetTags",
 bjetDiscrWorkingPoint = "Loose",
 numberOfBJetsCutValue = 1,
 numberOfBJetsCutDirection = ">=", # options: ==, !=, <, <=, >, >=
)

scaleFactors.setupBtagSFInformation(btagPset=bjetSelection, 
                                    btagPayloadFilename="CSVv2.csv",
                                    #btagEfficiencyFilename="btageff_TTJets.json",
                                    #btagEfficiencyFilename="btageff_WJetsHT.json",
                                    btagEfficiencyFilename="btageff_hybrid.json",
                                    direction="nominal")

#====== MET selection
metSelection = PSet(
           METCutValue = 100.0, #for heavy H+, overriden in signalAnalysis.py for light H+
       METCutDirection = ">", # options: ==, !=, <, <=, >, >=
  METSignificanceCutValue = -1000.0,
  METSignificanceCutDirection = ">", # options: ==, !=, <, <=, >, >=
               METType = "MET_Type1", # options: MET_Type1, MET_Type1_NoHF, MET_Puppi, GenMET, L1MET, HLTMET, CaloMET
   applyPhiCorrections = False  # FIXME: no effect yet
)
# MET trigger SF
scaleFactors.assignMETTriggerSF(metSelection, bjetSelection.bjetDiscrWorkingPoint, "nominal")

#====== Angular cuts / back-to-back
angularCutsBackToBack = PSet(
       nConsideredJets = 3,    # Number of highest-pt jets to consider (excluding jet corresponding to tau)
enableOptimizationPlots = True, # 2D histograms for optimizing angular cuts
        cutValueJet1 = 0.0,   # Cut value in degrees (circular cut)
        cutValueJet2 = 0.0,   # Cut value in degrees (circular cut)
        cutValueJet3 = 0.0,   # Cut value in degrees (circular cut)
        cutValueJet4 = 0.0,   # Cut value in degrees (circular cut)
)
#====== Experimental
jetCorrelations = PSet (

)


def setAngularCutsWorkingPoint(pset, workingPoint):
    if workingPoint == "NoCut":
        pset.cutValueJet1 = 0.0
        pset.cutValueJet2 = 0.0
        pset.cutValueJet3 = 0.0
        pset.cutValueJet4 = 0.0
    elif workingPoint == "Loose":
        pset.cutValueJet1 = 40.0
        pset.cutValueJet2 = 40.0
        pset.cutValueJet3 = 40.0
        pset.cutValueJet4 = 40.0
    elif workingPoint == "Medium":
        pset.cutValueJet1 = 60.0
        pset.cutValueJet2 = 60.0
        pset.cutValueJet3 = 60.0
        pset.cutValueJet4 = 60.0
    elif workingPoint == "Tight":
        pset.cutValueJet1 = 80.0
        pset.cutValueJet2 = 80.0
        pset.cutValueJet3 = 80.0
        pset.cutValueJet4 = 80.0
    elif workingPoint == "VTight":
        pset.cutValueJet1 = 100.0
        pset.cutValueJet2 = 100.0
        pset.cutValueJet3 = 100.0
        pset.cutValueJet4 = 100.0
    else:
        raise Exception("Error: Unknown working point '%s' requested!"%workingPoint)

#====== Common plots options
commonPlotsOptions = PSet(
  # Splitting of histograms as function of one or more parameters
  # Example: histogramSplitting = [PSet(label="tauPt", binLowEdges=[60, 70, 80, 100, 120], useAbsoluteValues=False)],
  histogramSplitting = [],
  # By default, inclusive (i.e. fake tau+genuine tau) and fake tau histograms are produced. Set to true to also produce genuine tau histograms (Note: will slow down running and enlarge resulting files).
  enableGenuineTauHistograms = False, 
  # Bin settings (final bin setting done in datacardGenerator, there also variable bin width is supported)
       nVerticesBins = PSet(nBins=60, axisMin=0., axisMax=60.),
              ptBins = PSet(nBins=500, axisMin=0., axisMax=5000.),
             etaBins = PSet(nBins=60, axisMin=-3.0, axisMax=3.0),
             phiBins = PSet(nBins=72, axisMin=-3.1415926, axisMax=3.1415926),
        deltaPhiBins = PSet(nBins=18, axisMin=0., axisMax=180.), # used in 2D plots, i.e. putting high number of bins here will cause troubles
            rtauBins = PSet(nBins=55, axisMin=0., axisMax=1.1),
           njetsBins = PSet(nBins=20, axisMin=0., axisMax=20.),
             metBins = PSet(nBins=1000, axisMin=0., axisMax=10000.), # please use 10 GeV bin width because of QCD measurement
       bjetDiscrBins = PSet(nBins=20, axisMin=-1.0, axisMax=1.0),
   angularCuts1DBins = PSet(nBins=52, axisMin=0., axisMax=260.),
         topMassBins = PSet(nBins=60, axisMin=0., axisMax=600.),
           WMassBins = PSet(nBins=60, axisMin=0., axisMax=300.),
              mtBins = PSet(nBins=2000, axisMin=0., axisMax=10000.), # 5 GeV bin width for tail fitter
         invmassBins = PSet(nBins=1000, axisMin=0., axisMax=10000.),
  # Enable/Disable some debug-level plots
       enablePUDependencyPlots = True,
)

#====== Build all selections group
allSelections = PSet(
 histogramAmbientLevel = histoLevel,
               Trigger = trg,
             METFilter = metFilter,
          TauSelection = tauSelection,
     ElectronSelection = eVeto,
         MuonSelection = muVeto,
          JetSelection = jetSelection,
  AngularCutsCollinear = angularCutsCollinear,
         BJetSelection = bjetSelection,
          METSelection = metSelection,
 AngularCutsBackToBack = angularCutsBackToBack,
       JetCorrelations = jetCorrelations,
           CommonPlots = commonPlotsOptions,
)


## Parses command line parameters and returns suffix for analysis
def obtainAnalysisSuffix(argv):
    suffix = "" 
    if "1prong" in argv or "1pr" in argv:
        suffix = "1pr"
        print "Running on 1-prong taus"
    elif "2prong" in argv or "2pr" in argv:
        suffix = "2pr"
        print "Running on 2-prong taus"
    elif "3prong" in argv or "3pr" in argv:
        suffix = "3pr"
        print "Running on 3-prong taus"
    return suffix

## Parses command line parameters and adjusts the parameters accordingly
def applyAnalysisCommandLineOptions(argv, config):
    if len(argv) < 3:
        return
    print "Applying command line options"
    if "1prong" in argv or "1pr" in argv:
        config.TauSelection.prongs = 1
    elif "2prong" in argv or "2pr" in argv:
        config.TauSelection.prongs = 2
    elif "3prong" in argv or "3pr" in argv:
        config.TauSelection.prongs = 3

    scaleFactors.assignTauTriggerSF(config.TauSelection, "nominal")

