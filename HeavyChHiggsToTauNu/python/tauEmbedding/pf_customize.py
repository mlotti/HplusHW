import re

import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.Modules import _Module

import FWCore.ParameterSet.VarParsing as VarParsing

from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

# Searches for self.lookFor module in cms.Path. When found, next and prev module is stored
class SeqVisitor(object):
    def __init__(self, lookFor):
	self.lookFor=lookFor
	self.nextInChain="NONE"
	self.prevInChain="NONE"
	self.prevInChainCandidate="NONE"
	self.catch=0   # 1 - we have found self.lookFor, at next visit write visitee
	self.found=0

    def prepareSearch(self): # this should be called on beggining of each iteration 
	self.found=0 
      
    def setLookFor(self, lookFor):
	self.lookFor = lookFor
      
    def giveNext(self):
	return self.nextInChain
    def givePrev(self):
	return self.prevInChain
      
    def enter(self,visitee):
	if isinstance(visitee, _Module):
	  if self.catch == 1:
	      self.catch=0
	      self.nextInChain=visitee
	      self.found=1
	  if visitee == self.lookFor:
	      self.catch=1
	      self.prevInChain=self.prevInChainCandidate
	      
	  self.prevInChainCandidate=visitee
	
    def leave(self,visitee):
	    pass


def customise(process):
    # Command line arguments
    import FWCore.ParameterSet.VarParsing as VarParsing
    options = VarParsing.VarParsing ('analysis')
    options.register ('overrideBeamSpot',
                      0, # default value, false
                      VarParsing.VarParsing.multiplicity.singleton,
                      VarParsing.VarParsing.varType.int,
                      "should I override beamspot in globaltag?")

    options, dataVersion = getOptionsDataVersion("42Xmc", options)

    hltProcessName = dataVersion.getTriggerProcess()
    recoProcessName = dataVersion.getRecoProcess()
    processName = process.name_()

    # Tighten muon selection w.r.t. skim
    import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations
    process.muonIsolationSequence = cms.Sequence()
    muons = customisations.addMuonIsolationEmbedding(process, process.muonIsolationSequence, muons=process.tightenedMuons.src.value())
    process.tightenedMuons.src = muons
    process.ProductionFilterSequence.replace(process.tightenedMuons, process.muonIsolationSequence*process.tightenedMuons)

    # Setup output
    outputModule = None
    outdict = process.outputModules_()
    if len(outdict) == 1:
        outputModule = outdict.values()[0]
    elif outdict.has_key("RECOSIMoutput"):
        outputModule = outdict["RECOSIMoutput"]

    print "Adjusting event content to GEN-SIM-RECO+misc"
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.HChEventContent_cff")
    #outputModule.outputCommands = cms.untracked.vstring("keep *")
    outputModule.outputCommands = cms.untracked.vstring("drop *")
    outputModule.outputCommands.extend(process.RECOSIMEventContent.outputCommands)
    outputModule.outputCommands.extend([
            "drop *_*_*_%s" % recoProcessName,
            "keep *_genParticles_*_%s" % recoProcessName,
            "keep recoGenJets_*_*_%s" % recoProcessName,
            "keep recoGenMETs_*_*_%s" % recoProcessName,
            "keep *_pfMet_*_%s" % recoProcessName,
            "keep *_offlinePrimaryVertices_*_%s" % recoProcessName,
            "keep *_generalTracks_*_%s" % recoProcessName,
            "keep *_muons_*_%s" % recoProcessName,
            "keep *_globalMuons_*_%s" % recoProcessName,
            "keep *_offlineBeamSpot_*_%s" % recoProcessName,
            "keep *_gtDigis_*_%s" % recoProcessName,
            "keep *_l1GtTriggerMenuLite_*_%s" % recoProcessName, # in run block
            "keep *_conditionsInEdm_*_%s" % recoProcessName, # in run block
            "keep *_addPileupInfo*_*_%s" % recoProcessName, # for MC

            "drop *_*_*_%s" % processName,
            "keep *_dimuonsGlobal_*_%s" % processName,
            "keep *_generator_weight_%s" % processName,
            "keep *_genParticles_*_%s" % processName,
            "keep recoGenJets_*_*_%s" % processName,
            "keep recoGenMETs_*_*_%s" % processName,
            "keep edmMergeableCounter_*_*_%s" % processName,
            "keep *_particleFlow*_*_%s" % processName,
            "keep *_generalTracks_*_%s" % processName,
            "keep *_tmfTracks_*_%s" % processName,
            "keep *_muons_*_%s" % processName,
            "keep *_globalMuons_*_%s" % processName,
            "keep *_offlinePrimaryVertices_*_%s" % processName,
            "keep edmMergeableCounter_*_*_%s" % processName,
    ])
#    re_procName = re.compile("_\*$")
#    outputModule.outputCommands.extend([re_procName.sub("_"+processName, x) for x in process.RECOSIMEventContent.outputCommands])
    outputModule.outputCommands.extend(process.HChEventContent.outputCommands)
    #outputModule.outputCommands.extend(process.RecoParticleFlowRECO.outputCommands)
    #outputModule.outputCommands.extend(["keep *_%s_*_%s" % (x, processName) for x in [
    #]])


    # Remove duplicate "drop *"
    index = 0
    for item in outputModule.outputCommands[:]:
        if item == "drop *" and index > 0:
            del outputModule.outputCommands[index]
            index -= 1
        index += 1


    # Disable gen vertex smearing
    process.VtxSmeared = cms.EDProducer("FlatEvtVtxGenerator", 
        MaxZ = cms.double(0.0),
        MaxX = cms.double(0.0),
        MaxY = cms.double(0.0),
        MinX = cms.double(0.0),
        MinY = cms.double(0.0),
        MinZ = cms.double(0.0),
        TimeOffset = cms.double(0.0),
        src = cms.InputTag("generator")
    )


    print "TAUOLA mdtau =", process.generator.ZTauTau.TauolaOptions.InputCards.mdtau

    # Do we have to override the beam spot for data?
    if options.overrideBeamSpot !=  0:
        bs = cms.string("BeamSpotObjects_2009_LumiBased_SigmaZ_v21_offline") # 42x data gt
        process.GlobalTag.toGet = cms.VPSet(
            cms.PSet(record = cms.string("BeamSpotObjectsRcd"),
                     tag = bs,
                     connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_BEAMSPOT")
            )
        )
        print "BeamSpot in globaltag set to ", bs
    else:
        print "BeamSpot in globaltag not changed"


    # Merge tracks
    process.tmfTracks = cms.EDProducer("RecoTracksMixer",
        trackCol1 = cms.InputTag("dimuonsGlobal"),
        trackCol2 = cms.InputTag("generalTracks", "", processName)
    )
    process.offlinePrimaryVerticesWithBS.TrackLabel = cms.InputTag("tmfTracks")
    process.offlinePrimaryVertices.TrackLabel = cms.InputTag("tmfTracks")
    process.muons.TrackExtractorPSet.inputTrackCollection = cms.InputTag("tmfTracks")

    if  hasattr(process, "iterativeTracking"):
        process.iterativeTracking *= process.tmfTracks
    elif hasattr(process, "trackCollectionMerging"):
        process.trackCollectionMerging *= process.tmfTracks
    else:
        raise Exception("Cannot find tracking sequence")


    # it should be the best solution to take the original beam spot for the
    # reconstruction of the new primary vertex
    # use the  one produced earlier, do not produce your own
    for s in process.sequences:
        seq =  getattr(process,s)
        seq.remove(process.offlineBeamSpot) 

    try:
        process.metreco.remove(process.BeamHaloId)
    except:
        pass


    # Disable lumi producer
    process.localreco_HcalNZS.remove(process.lumiProducer)
    process.localreco.remove(process.lumiProducer)

    # PFCandidate embedding
    process.particleFlowORG = process.particleFlow.clone()
    if hasattr(process,"famosParticleFlowSequence"):
        process.famosParticleFlowSequence.remove(process.pfPhotonTranslatorSequence)
        process.famosParticleFlowSequence.remove(process.pfElectronTranslatorSequence)
        process.famosParticleFlowSequence.remove(process.particleFlow)
        process.famosParticleFlowSequence.__iadd__(process.particleFlowORG)
        process.famosParticleFlowSequence.__iadd__(process.particleFlow)
        process.famosParticleFlowSequence.__iadd__(process.pfElectronTranslatorSequence)
        process.famosParticleFlowSequence.__iadd__(process.pfPhotonTranslatorSequence)
    elif hasattr(process,"particleFlowReco"):
        process.particleFlowReco.remove(process.pfPhotonTranslatorSequence)
        process.particleFlowReco.remove(process.pfElectronTranslatorSequence)
        process.particleFlowReco.remove(process.particleFlow)
        process.particleFlowReco.__iadd__(process.particleFlowORG)
        process.particleFlowReco.__iadd__(process.particleFlow)
        process.particleFlowReco.__iadd__(process.pfElectronTranslatorSequence)
        process.particleFlowReco.__iadd__(process.pfPhotonTranslatorSequence)
    else:
        raise "Cannot find pflow sequence"

    process.particleFlow =  cms.EDProducer('PFCandidateMixer',
        col1 = cms.untracked.InputTag("dimuonsGlobal","forMixing"),
        col2 = cms.untracked.InputTag("particleFlowORG", ""),
        trackCol = cms.untracked.InputTag("tmfTracks")
    )

    # Set the empty event filter source
    process.filterEmptyEv.src.setProcessName(processName)

    # Find all modules having particleFlow as their input
    pfInputNeeded = {}
    for p in process.paths:
        i =  getattr(process,p)
        target = process.particleFlow

        lookForPFInput = ["particleFlow"]
     
        seqVis = SeqVisitor(target)
        seqVis.prepareSearch()
        seqVis.setLookFor(target)
        i.visit(seqVis)
        while seqVis.catch != 1 and seqVis.found == 1: 
            target = seqVis.giveNext()

            pfInput = []

            targetAttributes =  dir(target)
            for targetAttribute in targetAttributes:
                attr=getattr(target,targetAttribute) # get actual attribute, not just  the name
                if isinstance(attr, cms.InputTag):
                    if attr.getModuleLabel()=="particleFlow" and attr.getProductInstanceLabel()!="":
                        print "Changing: ", target, " ", targetAttribute, " ", attr, " to particleFlowORG"
                        attr.setModuleLabel("particleFlowORG")
                    if attr.getModuleLabel() in lookForPFInput:
                        pfInput.append(attr)

            if len(pfInput) > 0:
                lookForPFInput.append(target.label())
                pfInputNeeded[target.label()] = pfInput


            #i.replace(target, source) 
            seqVis.prepareSearch()
            seqVis.setLookFor(target)
            i.visit(seqVis)

        #if (seqVis.catch==1):
            #seqVis.catch=0
            #i.__iadd__(source)

    pfOutputCommands = []
    for label in pfInputNeeded.keys():
        print "particleFlow as input in module %s, InputTags: %s" % (label, ", ".join(str(x) for x in pfInputNeeded[label]))
        pfOutputCommands.append("keep *_%s_*_%s" % (label, processName))
    outputModule.outputCommands.extend(pfOutputCommands)

    process.pfSelectedElectrons.src = "particleFlowORG"
    process.pfSelectedPhotons.src = "particleFlowORG"


    # Setup/remove some HLT/DQM stuff whcih doesn't work
    if hasattr(process, "hltTrigReport"):
        process.hltTrigReport.HLTriggerResults.setProcessName(processName)
    if hasattr(process, "DQM_FEDIntegrity_v2"):
        process.schedule.remove(process.DQM_FEDIntegrity_v2)
    if hasattr(process, "DQM_FEDIntegrity_v3"):
        process.schedule.remove(process.DQM_FEDIntegrity_v3)
    if hasattr(process, "HLTAnalyzerEndpath"):
        process.schedule.remove(process.HLTAnalyzerEndpath)
        del process.HLTAnalyzerEndpath

    #process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.printGenParticles_cff")
    #process.generation_step *= process.printGenParticles

    print "#############################################################"
    print " Warning! PFCandidates 'electron' collection is not mixed, "
    print "  and probably shouldnt be used. "
    print "#############################################################"


    return process
