import FWCore.ParameterSet.Config as cms

PUInfo = cms.EDAnalyzer('TopPt',
    OutputFileName = cms.string("TopPt.root"),
#    PileupSummaryInfoSrc = cms.InputTag("addPileupInfo")
    genParticleSrc = cms.InputTag("prunedGenParticles"),
    # These are the 8 TeV combined coefficients, which seem to agree nicely with 13 TeV data, see https://indico.cern.ch/event/463929/session/2/contribution/61/attachments/1202097/1749947/Top_Report_151209.pdf
    # Recipy from: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
    # Formula: exp(A-Bx)
    parameterA = 0.156,
    parameterB = -0.00137,
)
