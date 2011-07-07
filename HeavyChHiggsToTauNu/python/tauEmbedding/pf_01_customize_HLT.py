import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions

def customise(process):
    options = VarParsing.VarParsing()
    options.register('overrideBeamSpot',
                     0, # default value, false
                     VarParsing.VarParsing.multiplicity.singleton,
                     VarParsing.VarParsing.varType.int,
                     "should I override beamspot in globaltag?")
    options = getOptions(options)

    # Muon isolation
    import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations
    process.muonIsolationSequence = cms.Sequence()
    muons = customisations.addMuonIsolationEmbedding(process, process.muonIsolationSequence, muons=process.tightenedMuons.src.value())
    process.tightenedMuons.src = muons
    process.ProductionFilterSequence.replace(process.tightenedMuons, process.muonIsolationSequence*process.tightenedMuons)

    # output
    outputModule = None
    outdict = process.outputModules_()
    if len(outdict) == 1:
        outputModule = outdict.values()[0]
    elif outdict.has_key("RECOSIMoutput"):
        outputModule = outdict["RECOSIMoutput"]

    #process.TFileService = cms.Service("TFileService",  fileName = cms.string("histo_simulation.root")          )

    print "TAUOLA mdtau =", process.generator.ZTauTau.TauolaOptions.InputCards.mdtau

    #process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

    processName = process.name_()

    print "Adjusting event content to RAWSIM+misc"
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.HChEventContent_cff")
    #outputModule.outputCommands = cms.untracked.vstring("keep *")
    outputModule.outputCommands = cms.untracked.vstring("drop *")
    outputModule.outputCommands.extend(process.RAWSIMEventContent.outputCommands)
    #outputModule.outputCommands.extend(process.RAWEventContent.outputCommands)
    outputModule.outputCommands.extend(process.AODEventContent.outputCommands)
    #outputModule.outputCommands.extend(process.AODSIMEventContent.outputCommands)
    outputModule.outputCommands.extend(process.HChEventContent.outputCommands)

    outputModule.outputCommands.extend([
            "keep *_generalTracks_*_*",
            "keep *_adaptedMuonsFromWmunu_*_%s" % processName,
            "keep *_dimuonsGlobal_*_%s" % processName,
            "keep *_generator_*_%s" % processName
    ])

    # Remove duplicate "drop *"
    index = 0
    for item in outputModule.outputCommands[:]:
        if item == "drop *" and index > 0:
            del outputModule.outputCommands[index]
            index -= 1
        index += 1


    # Set the empty event filter source
    process.filterEmptyEv.src.setProcessName(processName)

    # Do we have to override the beam spot for data?
    if options.overrideBeamSpot !=  0:
        bs = cms.string("BeamSpotObjects_2009_LumiBased_SigmaZ_v18_offline") # 39x data gt
        #bs = cms.string("BeamSpotObjects_2009_LumiBased_v17_offline") # 38x data gt
        process.GlobalTag.toGet = cms.VPSet(
            cms.PSet(record = cms.string("BeamSpotObjectsRcd"),
                     tag = bs,
                     connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_BEAMSPOT")
            )
        )
        print "BeamSpot in globaltag set to ", bs
    else:
        print "BeamSpot in globaltag not changed"

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
    
    return process
