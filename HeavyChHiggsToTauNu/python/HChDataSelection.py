import FWCore.ParameterSet.Config as cms

from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter

def addDataSelection(process, dataVersion, options):
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
    if len(options.trigger) > 0:
        print "Triggering with", " OR ".join(options.trigger)
        process.TriggerFilter = triggerResultsFilter.clone()
        process.TriggerFilter.hltResults = cms.InputTag("TriggerResults", "", dataVersion.getTriggerProcess())
        process.TriggerFilter.l1tResults = cms.InputTag("")
        process.TriggerFilter.triggerConditions = cms.vstring(options.trigger)
        if options.triggerThrow == 0:
            # Should it throw an exception if the trigger product is not found
            process.TriggerFilter.throw = False

        seq *= process.TriggerFilter

    process.passedTrigger = cms.EDProducer("EventCountProducer")
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
    # https://twiki.cern.ch/twiki/bin/view/CMS/HBHEAnomalousSignals2011
    # https://hypernews.cern.ch/HyperNews/CMS/get/hcal-noise/93.html
    process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
    process.HBHENoiseFilterResultProducer.minNumIsolatedNoiseChannels = 9999
    process.HBHENoiseFilterResultProducer.minIsolatedNoiseSumE = 9999
    process.HBHENoiseFilterResultProducer.minIsolatedNoiseSumEt = 9999
    seq *= process.HBHENoiseFilterResultProducer

    # Require a good primary vertex (we might want to do this for MC too), see
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/Collisions2010Recipes#Good_Vertex_selection
    # This is from rev. 1.4 of DPGAnalysis/Skims/python/GoodVertex_cfg.py
#    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
#    process.primaryVertexFilter = cms.EDFilter("VertexCountFilter",
#        src = cms.InputTag("goodPrimaryVertices"),
#        minNumber = cms.uint32(1),
#        maxNumber = cms.uint32(999)
#    )

#    process.passedPrimaryVertexFilter = cms.EDProducer("EventCountProducer")
#    seq *= process.goodPrimaryVertices
#    seq *= process.primaryVertexFilter
#    seq *= process.passedPrimaryVertexFilter

    return seq

dataSelectionCounters = [
    "allEvents", "passedPhysicsDeclared", "passedTrigger", "passedScrapingVeto"
#    "passedPrimaryVertexFilter"
    ]
