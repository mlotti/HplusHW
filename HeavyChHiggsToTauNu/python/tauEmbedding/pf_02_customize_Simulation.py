import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.Modules import _Module

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
    processName = process.name_()

    process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

    process.tmfTracks = cms.EDProducer("RecoTracksMixer",
        trackCol1 = cms.InputTag("dimuonsGlobal"),
        trackCol2 = cms.InputTag("generalTracks","",processName)
    )  

    process.offlinePrimaryVerticesWithBS.TrackLabel = cms.InputTag("tmfTracks")
    process.offlinePrimaryVertices.TrackLabel = cms.InputTag("tmfTracks")
    process.muons.TrackExtractorPSet.inputTrackCollection = cms.InputTag("tmfTracks")
    try:
        process.metreco.remove(process.BeamHaloId)
    except:
        pass

    outputModule = None
    outdict = process.outputModules_()
    if len(outdict) == 1:
        outputModule = outdict.values()[0]
    elif outdict.has_key("out"):
        outputModule = outdict["out"]

    recoProcessName = "RECO"
    hltProcessName = "EMBEDDINGHLT"
    processName = process.name_()

    print "Adjusting event content to GEN-SIM-RECO+misc"
    outputModule.outputCommands = cms.untracked.vstring("drop *")
    outputModule.outputCommands.extend(process.RECOSIMEventContent.outputCommands)
    outputModule.outputCommands.extend([
            "drop *_*_*_%s" % recoProcessName,
            "keep *_pfMet_*_%s" % recoProcessName,
            "keep *_offlinePrimaryVertices_*_%s" % recoProcessName,
            "keep *_generalTracks_*_%s" % recoProcessName,
            "keep *_muons_*_%s" % recoProcessName,
            "keep *_offlineBeamSpot_*_%s" % recoProcessName,

            "drop *_*_*_%s" % hltProcessName,
            "keep *_tauEmbeddingMuons_*_*",
            "keep *_generator_weight_%s" % hltProcessName,
            "keep *_genParticles_*_%s" % hltProcessName,
            "keep recoGenJets_*_*_%s" % hltProcessName,
            "keep recoGenMETs_*_*_%s" % hltProcessName,

            "drop *_*_*_%s" % processName,
            "keep *_particleFlow*_*_%s" % processName,
            "keep *_generalTracks_*_%s" % processName,
            "keep *_muons_*_%s" % processName,
    ])
    #outputModule.outputCommands.extend(process.RecoParticleFlowRECO.outputCommands)
    #outputModule.outputCommansd.extend(["keep *_%s_*_%s" % (x, processName) for x in [
    #]])

    # Remove duplicate "drop *"
    index = 0
    for item in outputModule.outputCommands[:]:
        if item == "drop *" and index > 0:
            del outputModule.outputCommands[index]
            index -= 1
        index += 1

    # Disable lumi producer
    #process.localreco_HcalNZS.remove(process.lumiProducer)
    #process.localreco.remove(process.lumiProducer)


    if  hasattr(process,"iterativeTracking"):
        process.iterativeTracking.__iadd__(process.tmfTracks)
    elif hasattr(process,"trackCollectionMerging"):
        process.trackCollectionMerging.__iadd__(process.tmfTracks)
    else:
        raise "Cannot find tracking sequence"

    process.particleFlowORG = process.particleFlow.clone()
    if hasattr(process,"famosParticleFlowSequence"):
        process.famosParticleFlowSequence.remove(process.pfElectronTranslatorSequence)
        process.famosParticleFlowSequence.remove(process.particleFlow)
        process.famosParticleFlowSequence.__iadd__(process.particleFlowORG)
        process.famosParticleFlowSequence.__iadd__(process.particleFlow)
        process.famosParticleFlowSequence.__iadd__(process.pfElectronTranslatorSequence)
    elif hasattr(process,"particleFlowReco"):
        process.particleFlowReco.remove(process.pfElectronTranslatorSequence)
        process.particleFlowReco.remove(process.particleFlow)
        process.particleFlowReco.__iadd__(process.particleFlowORG)
        process.particleFlowReco.__iadd__(process.particleFlow)
        process.particleFlowReco.__iadd__(process.pfElectronTranslatorSequence)
    else:
        raise "Cannot find tracking sequence"

    process.particleFlow =  cms.EDProducer('PFCandidateMixer',
        col1 = cms.untracked.InputTag("dimuonsGlobal","forMixing"),
        col2 = cms.untracked.InputTag("particleFlowORG", "")
    )

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


    import FWCore.ParameterSet.VarParsing as VarParsing
    options = VarParsing.VarParsing ('analysis')

    options.register ('overrideBeamSpot',
                      0, # default value, false
                      VarParsing.VarParsing.multiplicity.singleton,
                      VarParsing.VarParsing.varType.int,
                      "should I override beamspot in globaltag?")


    if options.overrideBeamSpot !=  0:
        bs = cms.string("BeamSpotObjects_2009_LumiBased_v16_offline") # 38x data gt
        #bs = cms.string("BeamSpotObjects_2009_v14_offline") # 36x data gt
        #  tag = cms.string("Early10TeVCollision_3p8cm_31X_v1_mc_START"), # 35 default
        #  tag = cms.string("Realistic900GeVCollisions_10cm_STARTUP_v1_mc"), # 36 default
        process.GlobalTag.toGet = cms.VPSet(
            cms.PSet(record = cms.string("BeamSpotObjectsRcd"),
                     tag = bs,
                     connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_BEAMSPOT")
            )
        )
        print "BeamSpot in globaltag set to ", bs
    else:
        print "BeamSpot in globaltag not changed"


    print "#############################################################"
    print " Warning! PFCandidates 'electron' collection is not mixed, "
    print "  and probably shouldnt be used. "
    print "#############################################################"
    return process
