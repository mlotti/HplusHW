import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion

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

    process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

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
            "keep *_tightMuons_*_*",
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
