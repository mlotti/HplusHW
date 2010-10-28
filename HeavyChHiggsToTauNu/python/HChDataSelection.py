import FWCore.ParameterSet.Config as cms

from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter

def addDataSelection(process, dataVersion, trigger):
    if not dataVersion.isData():
        raise Exception("Data version is not data!")

    seq = cms.Sequence() 

    # Count all events
    process.allEvents = cms.EDProducer("EventCountProducer")
    seq *= process.allEvents

    # Physics declared bit, see
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/Collisions2010Recipes#Physics_Declared_bit_selection
    process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
    process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'
    process.passedPhysicsDeclared = cms.EDProducer("EventCountProducer")
    seq *= process.hltPhysicsDeclared
    seq *= process.passedPhysicsDeclared
    
    # Trigger
    process.TriggerFilter = triggerResultsFilter.clone()
    process.TriggerFilter.hltResults = cms.InputTag("TriggerResults", "", dataVersion.getTriggerProcess())
    process.TriggerFilter.l1tResults = cms.InputTag("")
    #process.TriggerFilter.throw = cms.bool(False) # Should it throw an exception if the trigger product is not found
    process.TriggerFilter.triggerConditions = cms.vstring(trigger)

    process.passedTrigger = cms.EDProducer("EventCountProducer")
    seq *= process.TriggerFilter
    seq *= process.passedTrigger

    # Filter out Beam Scraping events, see
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/Collisions2010Recipes#Removal_of_Beam_Scraping_Events
    process.scrapingVeto = cms.EDFilter("FilterOutScraping",
        applyfilter = cms.untracked.bool(True),
        debugOn = cms.untracked.bool(False),
        numtrack = cms.untracked.uint32(10),
        thresh = cms.untracked.double(0.25)
    )
    process.passedScrapingVeto = cms.EDProducer("EventCountProducer")
    seq *= process.scrapingVeto
    seq *= process.passedScrapingVeto

    # Reject events with anomalous HCAL noise, see
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/Collisions2010Recipes#Anomalous_Signals_treatment_reco
    # https://twiki.cern.ch/twiki/bin/view/CMS/HcalDPGAnomalousSignals
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/HcalNoiseInfoLibrary#How_do_I_reject_events_with_anom
    process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')
    process.passedHBHENoiseFilter = cms.EDProducer("EventCountProducer")
    seq *= process.HBHENoiseFilter
    seq *= process.passedHBHENoiseFilter

    # Require a good primary vertex (we might want to do this for MC too), see
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/Collisions2010Recipes#Good_Vertex_selection
    # This is from rev. 1.4 of DPGAnalysis/Skims/python/GoodVertex_cfg.py
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
    process.primaryVertexFilter = cms.EDFilter("VertexCountFilter",
        src = cms.InputTag("goodPrimaryVertices"),
        minNumber = cms.uint32(1),
        maxNumber = cms.uint32(999)
    )

    process.passedPrimaryVertexFilter = cms.EDProducer("EventCountProducer")
    seq *= process.goodPrimaryVertices
    seq *= process.primaryVertexFilter
    seq *= process.passedPrimaryVertexFilter

    return seq

dataSelectionCounters = ["allEvents", "passedTrigger", "passedScrapingVeto", "passedHBHENoiseFilter", "passedPrimaryVertexFilter"]
