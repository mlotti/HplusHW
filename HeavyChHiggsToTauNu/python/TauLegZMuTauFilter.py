import FWCore.ParameterSet.Config as cms

import PhysicsTools.PatAlgos.tools.helpers as helpers

hpsTauSelection =  "pt() > 15 && abs(eta()) < 2.5"
hpsTauSelection += " && tauID('decayModeFinding') > 0.5"
hpsTauSelection += " && (tauID('byVLooseCombinedIsolationDeltaBetaCorr') > 0.5 || tauID('byLooseCombinedIsolationDeltaBetaCorr3Hits') > 0.5 || tauID('byLooseIsolationMVA') > 0.5 || tauID('byLooseIsolationMVA2') > 0.5)"
hpsTauSelection += " && (tauID('againstElectronLoose') > 0.5 || tauID('againstElectronVLooseMVA2') > 0.5 || tauID('againstElectronLooseMVA3') > 0.5)"
hpsTauSelection += " && (tauID('againstMuonLoose') > 0.5 || tauID('againstMuonLoose2') > 0.5)"

muonSelection =  "isGlobalMuon() && isTrackerMuon()"
muonSelection += "&& pt() > 15 & abs(eta()) < 2.5 "
####muonSelection += "&& innerTrack().numberOfValidHits() > 10"
muonSelection += "&& track().hitPattern().trackerLayersWithMeasurement > 5" 
####muonSelection += "&& innerTrack().hitPattern().pixelLayersWithMeasurement() >= 1"
muonSelection += "&& innerTrack().hitPattern().numberOfValidPixelHits() > 0"
####muonSelection += "&& numberOfMatches() > 1"
muonSelection += "&& numberOfMatchedStations() > 1"
muonSelection += "&& globalTrack().normalizedChi2() < 10.0"
muonSelection += "&& globalTrack().hitPattern().numberOfValidMuonHits() > 0"

muTauPairs = cms.EDProducer("DeltaRMinCandCombiner",
    decay = cms.string('selectedPatMuons@+ selectedPatTausHpsPFTau@-'),
    checkCharge = cms.bool(False),
    cut = cms.string(''),
    name = cms.string('muTauCandidates'),
    deltaRMin = cms.double(0.7)
)

def customize(process):
    process.mutauSequence = addMuTauSelection(process)
    process.path += process.mutauSequence
    process.out.outputCommands.extend(["keep FEDRawDataCollection_*_*_*"])

    process.recoAllPFJets.replace(process.kt4PFJets, process.kt4PFJets+process.kt6PFJets)
    process.recoPFJets.replace(process.kt4PFJets, process.kt4PFJets+process.kt6PFJets)
    process.recoAllPFJets+=process.kt6PFJets

    process.patPF2PATSequenceChs.remove(process.pfTauSequenceChs)
    
    process.pfPileUpIso.PFCandidates = "particleFlowTmp"
    process.pfNoPileUpIso.bottomCollection = "particleFlowTmp"

    process.raw2digi_step = cms.Path(process.RawToDigi)
    process.L1Reco_step = cms.Path(process.L1Reco)
    process.reconstruction_step = cms.Path(process.reconstruction)
    process.endjob_step = cms.Path(process.endOfProcess)
    process.pat_step = cms.Path(process.patHplusCustomBefore)
    process.out.SelectEvents.SelectEvents = cms.vstring("path")
    process.out_step = cms.EndPath(process.out)
    process.schedule = cms.Schedule(
        process.raw2digi_step,
        process.L1Reco_step,
        process.reconstruction_step,
        process.path,
        process.endjob_step,
        process.out_step
    )

    
def addMuTauSelection(process):
    process.selectedPatTausHpsPFTau.cut = hpsTauSelection
    process.selectedPatMuons.cut = muonSelection  

    process.zmutauAllEvents = cms.EDProducer("EventCountProducer")

    process.selectedTauFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag("selectedPatTausHpsPFTau"),
        minNumber = cms.uint32(1),
    )
    process.selectedMuonFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag("selectedPatMuons"),
        minNumber = cms.uint32(1),
    )

    process.muTauPairs = muTauPairs.clone()
    process.muTauPairsFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag('muTauPairs'),
        minNumber = cms.uint32(1),
    )

    process.zmutauSelectedEvents = cms.EDProducer("EventCountProducer")
    
    return cms.Sequence(
        process.zmutauAllEvents +
        process.selectedTauFilter +
        process.selectedMuonFilter +
        process.muTauPairs +
        process.muTauPairsFilter +
        process.zmutauSelectedEvents
    )

def customizeBeforePat(process,dataVersion):
    doRECO(process,dataVersion)

def replaceInAllPathsAndSequences(process, old, new, exceptions=[]):
    for pthName, pth in process.paths_().iteritems():
        if pthName not in exceptions:
            pth.replace(old, new)
    for seqName, seq in process.sequences_().iteritems():
        if seqName not in exceptions:
            seq.replace(old, new)

def replaceInputTagInAllSequences(process, oldName, newName, exceptions=[]):
    for seqName, seq in process.sequences_().iteritems():
        if seqName not in exceptions:
            helpers.massSearchReplaceAnyInputTag(seq, cms.InputTag(oldName), cms.InputTag(newName))

def doRECO(process,dataVersion):
    # copy-pasted from embedding..
    process.load('Configuration.StandardSequences.RawToDigi_cff')
    process.load('Configuration.StandardSequences.L1Reco_cff')
    process.load('Configuration.StandardSequences.Reconstruction_cff')
    process.load('Configuration.StandardSequences.EndOfProcess_cff')

#    f = open("configDumpRECODebug.py", "w") 
#    f.write(process.dumpPython())
#    f.close()
    

    # Hacks to get PAT to work in a process with RECO
    process.recoPFJets.remove(process.kt6PFJets)
    process.recoAllPFJets.remove(process.kt6PFJets)

    origPostfix = "Orig"
    clashingSequences = [
        "muonPFIsolationSequence",
        "pfPhotonIsolationSequence",
        "pfElectronIsolationSequence",
        ]
    sequencesNoReplaceInputTag = clashingSequences+[
        "photonPFIsolationDepositsSequence",
        "electronPFIsolationDepositsSequence",
        ]
        
    modulesInClashingSequences = [
    ]
    for name in ["Charged", "ChargedAll", "Gamma", "Neutral", "PU"]:
        modulesInClashingSequences.extend([
                "muPFIsoDeposit"+name,
                "muPFIsoValue%s03"%name,
                "muPFIsoValue%s04"%name,
                "phPFIsoDeposit"+name,
                "phPFIsoValue%s03PFId"%name,
                "phPFIsoValue%s04PFId"%name,
                "elPFIsoDeposit"+name,
                "elPFIsoValue%s03PFId"%name, 
                "elPFIsoValue%s04PFId"%name,
                ])
    for name in ["Charged", "Neutral", "Photons"]:
        modulesInClashingSequences.extend([
                "isoDepPhotonWith"+name,
                "isoValPhotonWith"+name,
                "isoDepElectronWith"+name,
                "isoValElectronWith"+name,
               ])
    
    clashingModules = ["pfSelectedElectrons", "pfSelectedPhotons"]
        
    for name in clashingSequences:
        oldSeq = getattr(process, name)
        helpers.cloneProcessingSnippet(process, getattr(process, name), origPostfix)
        newSeq = getattr(process, name+origPostfix)
        
        replaceInAllPathsAndSequences(process, oldSeq, newSeq)

    for name in modulesInClashingSequences:
        replaceInputTagInAllSequences(process, name, name+origPostfix, exceptions=sequencesNoReplaceInputTag)

    for name in clashingModules:
        newName = name+origPostfix
        mod = getattr(process, name)
        newMod = mod.clone()
        setattr(process, newName, newMod)
        replaceInAllPathsAndSequences(process, mod, newMod, exceptions=sequencesNoReplaceInputTag)
        replaceInputTagInAllSequences(process, name, newName, exceptions=sequencesNoReplaceInputTag)

    if dataVersion.isData():
    #if isData:  # replace all instances of "rawDataCollector" with "source"
        from FWCore.ParameterSet import Mixins
        for module in process.__dict__.itervalues():
            if isinstance(module, Mixins._Parameterizable):
                for parameter in module.__dict__.itervalues():
                    if isinstance(parameter, cms.InputTag):
                        if parameter.moduleLabel == 'rawDataCollector':
                            parameter.moduleLabel = 'source'

#    f = open("configDumpRECODebug2.py", "w")
#    f.write(process.dumpPython())
#    f.close()

def getSelectionCounters():
    return ["zmutauAllEvents",
            "zmutauSelectedEvents"]
