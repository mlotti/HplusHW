import FWCore.ParameterSet.Config as cms

from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter

def addDataSelection(process, dataVersion, options, calculateEventCleaning=False):
    if not dataVersion.isData():
        raise Exception("Data version is not data!")

    seq = cms.Sequence() 

    # Count all events
    process.allEvents = cms.EDProducer("EventCountProducer")
    seq *= process.allEvents

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
    # http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/RecoMET/METFilters/test/exampleICHEPrecommendation_cfg.py?revision=1.3&view=markup&pathrev=V00-00-13
    process.scrapingVeto = cms.EDFilter("FilterOutScraping",
        applyfilter = cms.untracked.bool(True),
        debugOn = cms.untracked.bool(False),
        numtrack = cms.untracked.uint32(10),
        thresh = cms.untracked.double(0.25)
    )
    process.passedScrapingVeto = cms.EDProducer("EventCountProducer")
    seq *= process.scrapingVeto
    seq *= process.passedScrapingVeto

    # Produce results for filters
    return seq

dataSelectionCounters = [
    "allEvents", "passedTrigger", "passedScrapingVeto"
    ]

def addHBHENoiseFilterResultProducer(process, sequence):
    # Reject events with anomalous HCAL noise, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/HBHEAnomalousSignals2011
    # https://hypernews.cern.ch/HyperNews/CMS/get/hcal-noise/93.html
    # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#HBHE_Noise_Filter
    process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
    sequence *= (
        process.HBHENoiseFilterResultProducer
    )
    

def addHBHENoiseFilter(process, sequence):
    process.HBHENoiseFilter = cms.EDFilter("HPlusBoolFilter",
        src = cms.InputTag("HBHENoiseFilterResultProducer", "HBHENoiseFilterResult")
    )
    process.HBHENoiseFilterAllEvents = cms.EDProducer("EventCountProducer")
    process.HBHENoiseFilterPassed = cms.EDProducer("EventCountProducer")
    sequence *= (
        process.HBHENoiseFilterAllEvents *
        process.HBHENoiseFilter *
        process.HBHENoiseFilterPassed
    )
    counters = ["HBHENoiseFilterAllEvents", "HBHENoiseFilterPassed"]
    return counters

def addPhysicsDeclaredBit(process, sequence):
    # Physics declared bit, see
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/Collisions2010Recipes#Physics_Declared_bit_selection
    process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
    process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'
    process.physicsDeclaredAllEvents = cms.EDProducer("EventCountProducer")
    process.physicsDeclaredPassed = cms.EDProducer("EventCountProducer")
    sequence *= (
        process.physicsDeclaredAllEvents *
        process.hltPhysicsDeclared *
        process.physicsDeclaredPassed
    )
    return ["physicsDeclaredAllEvents", "physicsDeclaredPassed"]

