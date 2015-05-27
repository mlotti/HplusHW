import FWCore.ParameterSet.Config as cms

from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter

def addMcSelection(process, dataVersion, applyTrigger, trigger):
    if not dataVersion.isMC():
        raise Exception("Data version is not MC!")

    seq = cms.Sequence()

    # Count all events
    process.allEvents = cms.EDProducer("EventCountProducer")
    seq *= process.allEvents

    # Trigger
    if applyTrigger:
        if len(trigger) == 0:
            raise Exception("triggerMC=1 and no trigger is specified!")
        print "########################################"
        print "#"
        print "# Applying trigger filter for MC"
        print "# "+" OR ".join(trigger)
        print "#"
        print "########################################"
        process.TriggerFilter = triggerResultsFilter.clone()
        process.TriggerFilter.hltResults = cms.InputTag("TriggerResults", "", dataVersion.getTriggerProcess())
        process.TriggerFilter.l1tResults = cms.InputTag("")
        #process.TriggerFilter.throw = cms.bool(False) # Should it throw an exception if the trigger product is not found
        process.TriggerFilter.triggerConditions = cms.vstring(trigger)
        seq *= process.TriggerFilter

    process.passedTrigger = cms.EDProducer("EventCountProducer")
    seq *= process.passedTrigger

    return seq

mcSelectionCounters = [
    "allEvents", "passedTrigger"
]
