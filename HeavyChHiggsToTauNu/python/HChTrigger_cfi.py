import FWCore.ParameterSet.Config as cms

import sys

# HLT8E29 = cms.EDFilter('HPlusTriggering',
# #    TriggerResultsName = cms.InputTag("TriggerResults::HLT"),
#     TriggerResultsName = cms.InputTag("TriggerResults::HLT8E29"),
#     TriggersToBeApplied = cms.vstring(
#     ),
#     TriggersToBeSaved = cms.vstring(
# 	"HLT_SingleLooseIsoTau20",
# 	"HLT_MET45",
# 	"HLT_MET100",
# 	"HLT_Jet15U",
# 	"HLT_Jet30U",
# 	"HLT_Jet50U",
# 	"HLT_QuadJet15U",
# 	"HLT_Mu9"
#     ),
#     PrintTriggerNames = cms.bool(False)
# )

# HLT = cms.EDFilter('HPlusTriggering',
#     TriggerResultsName = cms.InputTag("TriggerResults::HLT"),
#     TriggersToBeApplied = cms.vstring(
#     ),
#     TriggersToBeSaved = cms.vstring(
#         #"HLT_Jet30",
#         #"HLT_DiJetAve15U_1E31",
#         #"HLT_DiJetAve30U_1E31",
#         #"HLT_QuadJet30",
#         "HLT_SingleIsoTau30_Trk5",
#         #"HLT_Mu15",
#         #"HLT_Ele15_SW_L1R",
#         #"HLT_Ele15_SW_EleId_L1R",
#         #"HLT_MET35",
#     ),
#     PrintTriggerNames = cms.bool(False)
# )


#HChTriggers = cms.Sequence( HLT8E29 * HLT )
#HChTriggers = cms.Sequence( HLT8E29 )

def addSpring10(process):
    process.patTrigger.processName = "HLT"
    process.patTriggerEvent.processName = "HLT"

    process.HLTREDIGI = cms.EDFilter('HPlusTriggering',
        TriggerResultsName = cms.InputTag("TriggerResults::HLT"),
        TriggersToBeApplied = cms.vstring(
        ),
        TriggersToBeSaved = cms.vstring(
        "HLT_SingleLooseIsoTau20",
        "HLT_MET45",
        "HLT_MET100",
        "HLT_Jet15U",
        "HLT_Jet30U",
        "HLT_Jet50U",
        "HLT_QuadJet15U",
        "HLT_Mu9"
        ),
        PrintTriggerNames = cms.bool(False)
    )

def addSpring10redigi(process):
    process.patTrigger.processName = "REDIGI"
    process.patTriggerEvent.processName = "REDIGI"

    process.HLTREDIGI = cms.EDFilter('HPlusTriggering',
        TriggerResultsName = cms.InputTag("TriggerResults::REDIGI"),
        TriggersToBeApplied = cms.vstring(
        ),
        TriggersToBeSaved = cms.vstring(
    	"HLT_SingleLooseIsoTau20",
    	"HLT_MET45",
    	"HLT_MET100",
    	"HLT_Jet15U",
    	"HLT_Jet30U",
    	"HLT_Jet50U",
    	"HLT_QuadJet15U",
    	"HLT_Mu9"
        ),
        PrintTriggerNames = cms.bool(False)
    )

def addSummer10(process):
    process.patTrigger.processName = "REDIGI36X"
    process.patTriggerEvent.processName = "REDIGI36X"

    process.HLTREDIGI = cms.EDFilter('HPlusTriggering',
        TriggerResultsName = cms.InputTag("TriggerResults::REDIGI36X"),
        TriggersToBeApplied = cms.vstring(
        ),
        TriggersToBeSaved = cms.vstring(
    	"HLT_SingleLooseIsoTau20",
    	"HLT_MET45",
    	"HLT_MET100",
    	"HLT_Jet15U",
    	"HLT_Jet30U",
    	"HLT_Jet50U",
    	"HLT_QuadJet15U",
    	"HLT_Mu9"
        ),
        PrintTriggerNames = cms.bool(False)
    )

def addSummer10_37X(process):
    process.patTrigger.processName = "REDIGI37X"
    process.patTriggerEvent.processName = "REDIGI37X"

    process.HLTREDIGI = cms.EDFilter('HPlusTriggering',
        TriggerResultsName = cms.InputTag("TriggerResults::REDIGI37X"),
        TriggersToBeApplied = cms.vstring(
        ),
        TriggersToBeSaved = cms.vstring(
    	"HLT_SingleLooseIsoTau20",
    	"HLT_MET45",
    	"HLT_MET100",
    	"HLT_Jet15U",
    	"HLT_Jet30U",
    	"HLT_Jet50U",
    	"HLT_QuadJet15U",
    	"HLT_Mu9"
        ),
        PrintTriggerNames = cms.bool(False)
    )

def customise(process, dataVersion):
    if dataVersion == "35Xredigi":
        addSpring10redigi(process)
    elif dataVersion == "35X":
        addSpring10(process)
    elif dataVersion == "36X":
        addSummer10(process)
    elif dataVersion == "37X":
        addSummer10_37X(process)
    else:
        print "Incorrect data version '%s'" % dataVersion
        sys.exit(1)

    process.HChTriggers = cms.Sequence( process.HLTREDIGI )

    return process

def extendEventContent(content, process):
#    content.append("keep *_HLTREDIGI36X_*_"+process.name_())
    content.append("keep *_HLTREDIGI_*_"+process.name_())
    return content
