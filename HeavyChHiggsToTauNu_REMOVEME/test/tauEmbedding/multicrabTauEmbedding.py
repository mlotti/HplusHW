#!/usr/bin/env python

import os
import re
import time
from optparse import OptionParser

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

# Default processing step
#defaultStep = "skim"
defaultStep = "embedding"
#defaultStep = "analysis"
#defaultStep = "analysisTau"
#defaultStep = "signalAnalysis"
#defaultStep = "signalAnalysisGenTau"
#defaultStep = "muonAnalysis"
#defaultStep = "caloMetEfficiency"

# Default embedding version(s) to use
defaultVersions = [
# "v13"
# "v13_1"
# "v13_2"
# "v13_2_seedTest1"
# "v13_2_seedTest2"
# "v13_2_seedTest3"
#    "v13_3",
#    "v13_3_seedTest1",
#    "v13_3_seedTest2",
#    "v13_3_seedTest3",
#    "v13_3_seedTest4",
#    "v13_3_seedTest5",
#    "v13_3_seedTest6",
#    "v13_3_seedTest7",
#    "v13_3_seedTest8",
#    "v13_3_seedTest9",
#    "v13_3_seedTest10",
#    "v14"
#    "v44_3_seed0",
#    "v44_3_seed1",
#    "v44_3_seed2",
    #"v44_2fix", # for hybrid event production only
    #"v44_2fix_seed1", # for hybrid event production only
    #"v44_2fix_seed2", # for hybrid event production only
#    "v44_4_seed0",

#    "v44_4_2" # skim version

#    "v44_4_2_muiso0"
#    "v44_4_2_muiso1"

#    "v44_4_2_seed0",
#    "v44_4_2_seed1"

#    "v44_5_notrg2"
#    "v44_5_1_notrg2",
#    "v44_5_1",
#    "v44_5_1_tauhad",
#    "v44_5_1_tauhad_vispt10",
#    "v44_5_1_tauhad_vispt20",
#    "v44_5_1_tauhad_vispt30",
    "v53_3" # skim version   
]

skimVersion = "v53_3"
genTauSkimVersion = "v53_3"

# Define the processing steps: input dataset, configuration file, output file
config = {"skim":                 {"workflow": "tauembedding_skim_"+skimVersion,         "config": "muonSkim_cfg.py"},
          "embedding":            {"workflow": "tauembedding_embedding_%s",              "config": "embed.py"},
          "analysis":             {"workflow": "tauembedding_analysis_%s",               "config": "embeddingAnalysis_cfg.py"},
#          "analysis":             {"workflow": "tauembedding_analysis_%s",               "config": "debugAnalysis_cfg.py"},
          "genTauSkim":           {"workflow": "tauembedding_gentauskim_"+genTauSkimVersion,     "config": "../pattuple/patTuple_cfg.py"},
          "analysisTau":          {"workflow": "tauembedding_gentauanalysis_"+genTauSkimVersion, "config": "tauAnalysis_cfg.py"},
#          "analysisTau":          {"workflow": "tauembedding_gentauanalysis_"+genTauSkimVersion, "config": "genTauDebugAnalysis_cfg.py"},
#          "analysisTau":          {"workflow": "tauembedding_gentauanalysis_"+genTauSkimVersion, "config": "genTauDebugAnalysisNtuple_cfg.py"},
          "analysisTauAod":       {"workflow": "embeddingAodAnalysis_44X",               "config": "tauAnalysis_cfg.py"},
          "muonDebugAnalysisAod": {"workflow": "embeddingAodAnalysis_44X",               "config": "genMuonDebugAnalysisAOD_cfg.py"},
          "muonDebugAnalysisNtupleAod": {"workflow": "embeddingAodAnalysis_44X",         "config": "genMuonDebugAnalysisNtupleAOD_cfg.py"},
          "signalAnalysis":       {"workflow": "tauembedding_analysis_%s",               "config": "../signalAnalysis_cfg.py"},
          "signalAnalysisGenTau": {"workflow": "analysis_taumet_v53_3",                         "config": "../signalAnalysis_cfg.py"},
          "signalAnalysisGenTauSkim": {"workflow": "tauembedding_gentauanalysis_"+genTauSkimVersion, "config": "../signalAnalysis_cfg.py"},
          "EWKMatching":          {"workflow": "tauembedding_analysis_%s",               "config": "../EWKMatching_cfg.py"},
          "muonAnalysis":         {"workflow": "tauembedding_skimAnalysis_"+skimVersion, "config": "muonAnalysisFromSkim_cfg.py"},
#          "muonAnalysis":         {"workflow": "tauembedding_skimAnalysis_"+skimVersion, "config": "genMuonDebugAnalysis_cfg.py"},
          "caloMetEfficiency":    {"workflow": "tauembedding_skimAnalysis_"+skimVersion, "config": "caloMetEfficiency_cfg.py"},
          "ewkBackgroundCoverageAnalysis":    {"workflow": "analysis_v44_5",             "config": "ewkBackgroundCoverageAnalysis_cfg.py"},
          "ewkBackgroundCoverageAnalysisAod": {"workflow": "embeddingAodAnalysis_44X",   "config": "ewkBackgroundCoverageAnalysis_cfg.py"},
          }

updateNjobs = {
    "muonDebugAnalysisAod": {
        "TTJets_TuneZ2_Fall11": 100,
    },
    "muonDebugAnalysisNtupleAod": {
        "TTJets_TuneZ2_Fall11": 500,
    },
}


# "Midfix" for multicrab directory name
dirPrefix = ""
#dirPrefix = "_vital"
#dirPrefix += "_Met50"
if defaultStep in ["signalAnalysis", "signalAnalysisGenTau"]:
    dirPrefix += "_systematics"

#dirPrefix += "_test"
#dirPrefix += "_debug"

datasetsData2012 = [
    "SingleMu_190456-193621_2012A_Jan22",
    "SingleMu_193834-196531_2012B_Jan22",
    "SingleMu_198022-200381_2012C_Jan22",
    "SingleMu_200466-203742_2012C_Jan22",
    "SingleMu_203777-205834_2012D_Jan22",
    "SingleMu_205908-207100_2012D_Jan22",
    "SingleMu_207214-208686_2012D_Jan22",
]
datasetsMCTT = [
#    "TTJets_TuneZ2star_Summer12",
    "TTJets_FullLept_TuneZ2star_Summer12",
    "TTJets_SemiLept_TuneZ2star_Summer12",
    "TTJets_Hadronic_TuneZ2star_ext_Summer12",
]
datasetsMCWDY = [
    "WJets_TuneZ2star_v1_Summer12",
    "WJets_TuneZ2star_v2_Summer12",
    "W1Jets_TuneZ2star_Summer12",
    "W2Jets_TuneZ2star_Summer12",
    "W3Jets_TuneZ2star_Summer12",
    "W4Jets_TuneZ2star_Summer12",
    "DYJetsToLL_M50_TuneZ2star_Summer12",
]
datasetsMCSTVV = [
    "T_t-channel_TuneZ2star_Summer12",
    "Tbar_t-channel_TuneZ2star_Summer12",
    "T_tW-channel_TuneZ2star_Summer12",
    "Tbar_tW-channel_TuneZ2star_Summer12",
    "T_s-channel_TuneZ2star_Summer12",
    "Tbar_s-channel_TuneZ2star_Summer12",
    "WW_TuneZ2star_Summer12",
    "WZ_TuneZ2star_Summer12",
    "ZZ_TuneZ2star_Summer12",
]
datasetsMCQCD = [
    "QCD_Pt20_MuEnriched_TuneZ2star_Summer12",
]
datasetsMCSignal = [
    "TTToHplusBWB_M80_ext_Summer12",
    "TTToHplusBWB_M90_ext_Summer12",
    "TTToHplusBWB_M100_ext_Summer12",
    "TTToHplusBWB_M120_ext_Summer12",
    "TTToHplusBWB_M140_ext_Summer12",
    "TTToHplusBWB_M150_ext_Summer12",
    "TTToHplusBWB_M155_ext_Summer12",
    "TTToHplusBWB_M160_ext_Summer12",
    "TTToHplusBHminusB_M80_ext_Summer12",
    "TTToHplusBHminusB_M90_Summer12",
    "TTToHplusBHminusB_M100_ext_Summer12",
    "TTToHplusBHminusB_M120_ext_Summer12",
    "TTToHplusBHminusB_M140_ext_Summer12",
    "TTToHplusBHminusB_M150_ext_Summer12",
    "TTToHplusBHminusB_M155_ext_Summer12",
    "TTToHplusBHminusB_M160_ext_Summer12",
]

#datasetsData2012 = []
#datasetsMCTT = []
#datasetsMCWDY = []
#datasetsMCSTVV = []
#datasetsMCnoQCD = []
#datasetsMCQCD = []
datasetsMCSignal = []

datasetsMCnoQCD = datasetsMCTT + datasetsMCWDY + datasetsMCSTVV
#datasetsMCnoQCD = ["TTJets_TuneZ2star_Summer12"]
#datasetsMCnoQCD = ["W4Jets_TuneZ2star_Summer12"]
#datasetsMCnoQCD = ["DYJetsToLL_M50_TuneZ2star_Summer12"]
#datasetsMCnoQCD = ["W1Jets_TuneZ2star_Summer12"]
#datasetsMCnoQCD = [
#    "TTJets_FullLept_TuneZ2star_Summer12",
#    "TTJets_SemiLept_TuneZ2star_Summer12",
#    "TTJets_Hadronic_TuneZ2star_ext_Summer12",
#]

def main():
    parser = OptionParser(usage="Usage: %prog [options]")
    allSteps = config.keys()
    allSteps.sort()
    parser.add_option("--step", dest="step", default=defaultStep,
                      help="Processing step, one of %s (default: %s)" % (", ".join(allSteps), defaultStep))
    parser.add_option("--version", dest="version", action="append", default=[],
                      help="Data version(s) to use as an input for 'analysis', 'signalAnalysis', or output for 'skim', 'embedding' (default: %s)" % ", ".join(defaultVersions))
    parser.add_option("--midfix", dest="midfix", default=dirPrefix,
                      help="String to add in the middle of the multicrab directory name (default: %s)" % dirPrefix)
    parser.add_option("--configOnly", dest="configOnly", action="store_true", default=False,
                      help="Generate multicrab configurations only, do not create crab jobs (default is to create crab jobs)")
    parser.add_option("--dataOnly", dest="dataOnly", action="store_true", default=False,
                      help="Use only data datasets (default is to use data+MC, or an applicable subset)")
    parser.add_option("--ttbarOnly", dest="ttbarOnly", action="store_true", default=False,
                      help="Use only TTJets datasets")
    parser.add_option("--pickEvents", dest="pickEvents", action="store_true", default=False,
                      help="Retrieve also pickEvents.txt")
    parser.add_option("--dest", dest="destdir", default=None,
                      help="Directory to generate the multicrab directory to (default .)")
    (opts, args) = parser.parse_args()
    if opts.ttbarOnly and opts.dataOnly:
        parser.error("Only one of --dataOnly and --ttbarOnly can be given")

    step = opts.step
    versions = opts.version
    if len(versions) == 0:
        versions = defaultVersions

    tmp = "Processing step %s" % step
    if step in ["skim", "embedding", "analysis", "signalAnalysis","EWKMatching", "ewkBackgroundCoverageAnalysis", "ewkBackgroundCoverageAnalysisAod"]:
        inputOutput = "input"
        if step in ["skim", "embedding"]:
            inputOutput = "output"
        if step == "skim" and len(versions) > 1:
            raise Exception("There should be no need to run skim with multiple output versions, you specified %d versions" % len(versions))

        tmp += ", embedded versions '%s' as %s" % (", ".join(versions), inputOutput)
        print tmp

        for v in versions:
            print "########################################"
            print
            print " Creating tasks for embedding %s %s" % (inputOutput, v)
            print
            print "########################################"

            createTasks(opts, step, v)
    else:
        print tmp
        createTasks(opts, step)


def createTasks(opts, step, version=None):
    # Pick crab.cfg
    crabcfg = "crab.cfg"
    crabcfgtemplate = None
    scheduler = "arc"
    if "HOST" in os.environ and "lxplus" in os.environ["HOST"]:
        scheduler = "remoteGlidein"
    if step in ["genTauSkim"]:
        crabcfg = "../pattuple/crab_pat.cfg"
    elif step in ["signalAnalysisGenTau", "signalAnalysisGenTauSkim"]:
        crabcfg = "../crab_analysis.cfg"
    elif step in ["analysis", "analysisTau", "analysisTauAod", "muonDebugAnalysisAod", "muonDebugAnalysisNtupleAod", "signalAnalysis", "muonAnalysis", "caloMetEfficiency","EWKMatching", "ewkBackgroundCoverageAnalysis", "ewkBackgroundCoverageAnalysisAod"]:
        crabcfg = None
        args = {}
        if step in ["analysisTauAod", "ewkBackgroundCoverageAnalysisAod"]:
            args["copy_data"] = True
            args["userLines"] = [
                "user_remote_dir = %s_%s" % (step, time.strftime("%y%m%d_%H%M%S")),
                "storage_element = T2_FI_HIP"
                ]
        else:
            args["return_data"] = True
        crabcfgtemplate = crabCfgTemplate(scheduler=scheduler, **args)

    # Setup directory naming
    dirName = ""
    if step in ["skim", "embedding", "analysis", "signalAnalysis", "EWKMatching"]:
        dirName += "_"+version
    if step in ["genTauSkim", "analysisTau"]:
        dirName += "_"+genTauSkimVersion
    dirName += opts.midfix

    # Select the datasets based on the processing step and data era
    tasks = []
    global datasetsData2012, datasetsMCTT, datasetsMCTTWJets, datasetsMCWDY, datasetsMCSTVV, datasetsMCQCD, datasetsMCnoQCD, datasetsMCSignal
    if step == "skim":
        def app(name, lst):
            if len(lst) > 0:
                tasks.append( (name, lst) )
        app("Data", datasetsData2012)
        app("TT", datasetsMCTT)
        app("W_DY", datasetsMCWDY)
        app("ST_VV_QCD", datasetsMCSTVV+datasetsMCQCD)
        app("Signal", datasetsMCSignal)        
    else:
        datasets = []
        if opts.dataOnly:
            datasetsMCnoQCD = []
            datasetsMCTTWJets = []
            datasetsMCTT = []
            datasetsMCQCD = []
            datasetsMCSignal = []
        if opts.ttbarOnly:
            datasetsMCnoQCD = datasetsMCTT
            datasetsMCTTWJets = datasetsMCTT
            datasetsMCQCD = []
            datasetsMCSignal = []
            datasetsData2012 = []

        if step in ["analysisTauAod", "muonDebugAnalysisAod", "muonDebugAnalysisNtupleAod", "signalAnalysisGenTau", "genTauSkim", "analysisTau"]:
            datasets.extend(datasetsMCnoQCD)
        elif step in ["ewkBackgroundCoverageAnalysis", "ewkBackgroundCoverageAnalysisAod"]:
            datasets.extend(datasetsMCTTWJets)
        elif step in ["signalAnalysisGenTauSkim"]:
            datasets.extend(datasetsMCTT)
        else:
            datasets.extend(datasetsData2012)
            datasets.extend(datasetsMCnoQCD)
            datasets.extend(datasetsMCQCD)
        if step in ["embedding", "signalAnalysis","EWKMatching"]:
            datasets.extend(datasetsMCSignal)
        tasks.append( ("", datasets) )

    # Setup the version number for tauembedding_{embedding,analysis} workflows
    workflow = config[step]["workflow"]
    if step in ["embedding", "analysis", "signalAnalysis", "EWKMatching"]:
        workflow = workflow % version

    taskDirs = []
    for midfix, datasets in tasks:
        # Create multicrab
        multicrab = Multicrab(crabcfg, config[step]["config"], lumiMaskDir="..", crabConfigTemplate=crabcfgtemplate,
                              ignoreMissingDatasets=True
                          )

        if step in ["skim", "embedding", "genTauSkim"]:
            multicrab.addCommonLine("USER.user_remote_dir = /store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_5_3_X")

        multicrab.extendDatasets(workflow, datasets)

        if scheduler == "arc":
            multicrab.addCommonLine("GRID.maxtarballsize = 50")
#        if not step in ["skim", "genTauSkim", "analysisTauAod"]:
#            multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])
        if step in ["analysisTauAod", "muonDebugAnalysisAod", "muonDebugAnalysisNtupleAod", "signalAnalysisGenTau", "analysisTau", "signalAnalysisGenTauSkim", "signalAnalysis", "ewkBackgroundCoverageAnalysis", "ewkBackgroundCoverageAnalysisAod"]:
            outputFiles = "histograms.root"
            if opts.pickEvents:
                outputFiles += ",pickEvents.txt"
            multicrab.addCommonLine("CMSSW.output_file = "+outputFiles)

        # Let's do the naming like this until we get some answer from crab people
        #if step in ["skim", "embedding"]:
        #    multicrab.addCommonLine("USER.publish_data_name = Tauembedding_%s_%s" % (step, version))
    
        # For this workflow we need one additional command line argument
        if step in ["signalAnalysisGenTau", "signalAnalysisGenTauSkim"]:
            multicrab.appendArgAll("doTauEmbeddingLikePreselection=1")
    
        if step in ["skim"]:
            multicrab.extendBlackWhiteListAll("se_black_list", defaultSeBlacklist)
        else:
            multicrab.extendBlackWhiteListAll("se_black_list", defaultSeBlacklist_noStageout)
    
        if step == "embedding":
            multicrab.addCommonLine("GRID.max_rss = 3000")
    
        # Override number of jobs if asked
        if updateNjobs.has_key(step):
            for dname, njobs in updateNjobs[step].iteritems():
                try:
                    md = multicrab.getDataset(dname)
                except KeyError:
                    continue
                md.setNumberOfJobs(njobs)

#        if step in ["skim", "embedding", "genTauSkim"]:
#            def addCopyConfig(dataset):
#                dataset.appendLine("USER.additional_input_files = copy_cfg.py")
#                dataset.appendCopyFile("../copy_cfg.py")
#            multicrab.forEachDataset(addCopyConfig)
    
        # Create multicrab task(s)
        prefix = "multicrab_"+step+dirName
        if midfix != "":
            prefix += "_"+midfix
        taskDirs.extend(multicrab.createTasks(configOnly = opts.configOnly, prefix=prefix, path=opts.destdir))
            
        # patch CMSSW.sh
#        if not opts.configOnly and step in ["skim", "embedding", "genTauSkim"]:
#            import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crabPatchCMSSWsh as patch
#            for td, dsets in taskDirs:
#                os.chdir(td)
#                patch.main(Wrapper(dirs=dsets, input={"skim": "skim",
#                                                      "embedding": "embedded",
#                                                      "genTauSkim": "pattuple",
#                                                      }[step]))
#                os.chdir("..")
    
    if len(taskDirs) > 1:
        print 
        print "Created multicrab directories"
        print "\n".join( [x[0] for x in taskDirs] )

# patch CMSSW.sh
class Wrapper:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

if __name__ == "__main__":
    main()
