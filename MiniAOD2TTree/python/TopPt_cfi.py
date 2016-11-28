import FWCore.ParameterSet.Config as cms

TopPtProducer = cms.EDProducer('HplusTopPtWeightProducer',
    OutputFileName = cms.string("TopPt.root"),
#    PileupSummaryInfoSrc = cms.InputTag("addPileupInfo")
    genParticleSrc = cms.InputTag("prunedGenParticles"),
#    # These are the 8 TeV combined coefficients, which seem to agree nicely with 13 TeV data, see https://indico.cern.ch/event/463929/session/2/contribution/61/attachments/1202097/1749947/Top_Report_151209.pdf
#    # Recipy from: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
#    # Formula: exp(A-Bx)
#    parameterA = cms.double(0.156),
#    parameterB = cms.double(0.00137),
    # Updated top pt reweighting for 13 TeV
    # https://twiki.cern.ch/twiki/bin/view/CMS/TopSystematics#pt_top_Reweighting
    # Formula: exp(A-Bx)
    parameterA = cms.double(0.0615),
    parameterB = cms.double(0.0005),
)
