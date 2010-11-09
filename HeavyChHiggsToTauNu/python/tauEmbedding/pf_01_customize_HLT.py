import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from PhysicsTools.PatAlgos.tools.coreTools import removeSpecificPATObjects, removeCleaning

import HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple as hchpat
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection

def customise(process):
    options = getOptions()
    dataVersion = "38X"
    if options.dataVersion != "":
        dataVersion = options.dataVersion
    dataVersion = DataVersion(dataVersion)

    outputModule = None
    outdict = process.outputModules_()
    if len(outdict) == 1:
        outputModule = outdict.values()[0]
    elif outdict.has_key("out"):
        outputModule = outdict["out"]

    #process.TFileService = cms.Service("TFileService",  fileName = cms.string("histo_simulation.root")          )

    processName = process.name_()

    print "Adjusting event content to RAWSIM+misc"
    #outputModule.outputCommands = cms.untracked.vstring("keep *")
    outputModule.outputCommands = cms.untracked.vstring("drop *")
    outputModule.outputCommands.extend(process.RAWSIMEventContent.outputCommands)
    #outputModule.outputCommands.extend(process.RAWEventContent.outputCommands)
    outputModule.outputCommands.extend(process.AODEventContent.outputCommands)
    #outputModule.outputCommands.extend(process.AODSIMEventContent.outputCommands)

    outputModule.outputCommands.extend([
            "keep *_generalTracks_*_*",
            "keep *_tightMuons_*_%s" % processName,
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

    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelection_cff")
    process.ProductionFilterSequence.replace(process.muonSelectionPlaceholder, process.muonSelectionSequence)

    if options.doPat != 0:
        process.collisionDataSelection = cms.Sequence()
        if dataVersion.isData():
            process.collisionDataSelection = addDataSelection(process, dataVersion, trigger)
        
        process.patSequence = hchpat.addPat(process, dataVersion, doPatTrigger=False, doPatTaus=False, doPatElectronID=False, doTauHLTMatching=False)
        removeSpecificPATObjects(process, ["Photons"], False)
        removeCleaning(process, False)    
        process.patMuons.embedTrack = False # In order to avoid transient references and generalTracks is available anyway

        process.patAndMuonSelectionSequence = cms.Sequence(
            process.collisionDataSelection * 
            process.patSequence *
            process.muonSelectionSequence
        )
        process.ProductionFilterSequence.replace(process.muonSelectionSequence, process.patAndMuonSelectionSequence)

    #process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.printGenParticles_cff")
    #process.generation_step *= process.printGenParticles

    # process.VtxSmeared = cms.EDProducer("FlatEvtVtxGenerator", 
    #     MaxZ = cms.double(0.0),
    #     MaxX = cms.double(0.0),
    #     MaxY = cms.double(0.0),
    #     MinX = cms.double(0.0),
    #     MinY = cms.double(0.0),
    #     MinZ = cms.double(0.0),
    #     TimeOffset = cms.double(0.0),
    #     src = cms.InputTag("generator")
    # )
    
    return process
