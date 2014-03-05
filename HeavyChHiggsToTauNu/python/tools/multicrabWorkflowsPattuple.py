## \package multicrabDatasetsPatTuple
# Functions for pattuple definitions

import re

from multicrabWorkflowsTools import Dataset, Workflow, Data, Source, updatePublishName, TaskDef, updateTaskDefinitions, Disable
import multicrabDatasetsCommon as common

def constructProcessingWorkflow_44X(dataset, taskDef, sourceWorkflow, workflowName, inputLumiMaskData="DCSONLY11", outputLumiMaskData="Nov08ReReco", **kwargs):
    # Setup input/default output lumimasks for data
    inputLumiMask = None
    outputLumiMask = None
    if dataset.isData():
        inputLumiMask = inputLumiMaskData
        outputLumiMask = outputLumiMaskData

    # Setup the Source for pattuple Workflow
    source = Source(sourceWorkflow,
                    # These are exclusive, but the default values of None and a check in Workflow ensure correctness
                    number_of_jobs=taskDef.njobsIn, events_per_job=taskDef.neventsPerJobIn, lumis_per_job=taskDef.nlumisPerJobIn,
                    lumiMask=inputLumiMask)
    # If taskDef contains the DBS-path of the pattuple, setup also the Data for the pattuple
    output = None
    if taskDef.outputPath != None and len(taskDef.outputPath) > 0:
        dbs_url = taskDef.dbs
        if dbs_url is None:
            dbs_url = common.pattuple_dbs
        output = Data(taskDef.outputPath,
                      # These are exclusive, but the default values of None and a check in Workflow ensure correctness
                      number_of_jobs=taskDef.njobsOut, events_per_job=taskDef.neventsPerJobOut, lumis_per_job=taskDef.nlumisPerJobOut,
                      lumiMask=outputLumiMask, dbs_url=dbs_url)

    # Additional, necessary command line arguments relaring to trigger
    args = {}
    if taskDef.triggerOR is not None and len(taskDef.triggerOR) > 1 and taskDef.triggerThrow != None and taskDef.triggerThrow == False:
        args["triggerThrow"] = 0
    if dataset.isMC() and taskDef.triggerOR is not None and len(taskDef.triggerOR) > 0:
        args["triggerMC"] = 1
    if taskDef.args != None:
        args.update(taskDef.args)
        
    wf = Workflow(workflowName, source=source, triggerOR=taskDef.triggerOR, args=args, output=output, dataVersionAppend=taskDef.dataVersionAppend, **kwargs)
    if taskDef.crabLines != None:
        for line in taskDef.crabLines:
            wf.addCrabLine(line)
    return wf

## Main function for generating 44X pattuples
#
# \param version        String for pattuple version
# \param datasets       List of Dataset objects
# \param updateDefinitions  Dictionary from Dataset names to TaskDef
#                       objects. These override the default values
#                       specified in the body of this function
#                       (usually the DBS-path of pattuples, but others
#                       are possible too)
# \param skim           List of strings for skim configuration files (if given)
#
# It is a matter of taste how the responsibilites are divided by the
# addPattuple_44X() and other addPattuple_v*() functions. Here I tried
# to catch the commonalities such that the other addPattuple_v*()
# functions would be as short as possible.
def addPattuple_44X(version, datasets, updateDefinitions, skim=None):
    mcTrigger = "HLT_MediumIsoPFTau35_Trk20_MET60_v1"
    def TaskDefMC(**kwargs):
        if "triggerOR" in kwargs:
            return TaskDef(**kwargs)
        else:
            return TaskDef(triggerOR=[mcTrigger], **kwargs)

    # Specifies the default
    # - number of jobs in pattuple processing
    # - number of jobs for those who read pattuples
    # - triggers
    # for all relevant Datasets
    defaultDefinitions = {
        "Tau_160431-167913_2011A_Nov08": TaskDef(njobsIn=800, njobsOut=15, triggerOR=[
                                                    "HLT_IsoPFTau35_Trk20_MET45_v1", # 160431-161176
                                                    "HLT_IsoPFTau35_Trk20_MET45_v2", # 161216-163261
                                                    "HLT_IsoPFTau35_Trk20_MET45_v4", # 163270-163869
                                                    "HLT_IsoPFTau35_Trk20_MET45_v6", # 165088-165633
                                                    "HLT_IsoPFTau35_Trk20_MET60_v2", # 165970-166164, 166374-167043
                                                    "HLT_IsoPFTau35_Trk20_MET60_v3", # 166346
                                                    "HLT_IsoPFTau35_Trk20_MET60_v4", # 167078-167913
                                                ], triggerThrow=False),
        "Tau_170722-173198_2011A_Nov08": TaskDef(njobsIn=500, njobsOut=3, triggerOR=["HLT_IsoPFTau35_Trk20_MET60_v6"]),
        "Tau_173236-173692_2011A_Nov08": TaskDef(njobsIn=250, njobsOut=2, triggerOR=["HLT_MediumIsoPFTau35_Trk20_MET60_v1"]),
        "Tau_175832-180252_2011B_Nov19": TaskDef(njobsIn=650, njobsOut=20, triggerOR=[
                                                    "HLT_MediumIsoPFTau35_Trk20_MET60_v1", # 175832-178380
                                                    "HLT_MediumIsoPFTau35_Trk20_MET60_v5", # 178420-179889
                                                    "HLT_MediumIsoPFTau35_Trk20_MET60_v6", # 179959-180252
                                              ], triggerThrow=False),

        # MC, triggered with mcTrigger
        "TTToHplusBWB_M80_Fall11":        TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBWB_M90_Fall11":        TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBWB_M100_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBWB_M120_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBWB_M140_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBWB_M150_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBWB_M155_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBWB_M160_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),

        "TTToHplusBHminusB_M80_Fall11":        TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBHminusB_M90_Fall11":        TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBHminusB_M100_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBHminusB_M120_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBHminusB_M140_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBHminusB_M150_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBHminusB_M155_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),
        "TTToHplusBHminusB_M160_Fall11":       TaskDefMC(njobsIn=15, njobsOut=1),

        # These are at T2_FI_HIP, hence a smaller njobsIn (file size
        # is not that big of a problem)
        "HplusTB_M180_Fall11":       TaskDefMC(njobsIn=5, njobsOut=1),
        "HplusTB_M190_Fall11":       TaskDefMC(njobsIn=5, njobsOut=1),
        "HplusTB_M200_Fall11":       TaskDefMC(njobsIn=5, njobsOut=1),
        "HplusTB_M220_Fall11":       TaskDefMC(njobsIn=5, njobsOut=1),
        "HplusTB_M250_Fall11":       TaskDefMC(njobsIn=5, njobsOut=1),
        "HplusTB_M300_Fall11":       TaskDefMC(njobsIn=5, njobsOut=1),

        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDefMC(njobsIn=20, njobsOut=1),
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDefMC(njobsIn=40, njobsOut=1),
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDefMC(njobsIn=100, njobsOut=3),
                                            
        "WW_TuneZ2_Fall11":                 TaskDefMC(njobsIn=40, njobsOut=1),
        "WZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=40, njobsOut=1),
        "ZZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=40, njobsOut=1),
        "TTJets_TuneZ2_Fall11":             TaskDefMC(njobsIn=2000, njobsOut=50),
        "WJets_TuneZ2_Fall11":              TaskDefMC(njobsIn=400, njobsOut=4, args={"wjetsWeighting": 1}),
        "W1Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=300, njobsOut=6, args={"wjetsWeighting": 1}),
        "W2Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=200, njobsOut=5, args={"wjetsWeighting": 1}),
        "W3Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=100, njobsOut=10, args={"wjetsWeighting": 1}),
        "W3Jets_TuneZ2_v2_Fall11":          TaskDefMC(njobsIn=100, njobsOut=4, args={"wjetsWeighting": 1}),
        "W4Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=300, njobsOut=10, args={"wjetsWeighting": 1}),
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDefMC(njobsIn=200, njobsOut=2),
        "DYJetsToLL_M10to50_TuneZ2_Fall11": TaskDefMC(njobsIn=200, njobsOut=1),
        "T_t-channel_TuneZ2_Fall11":        TaskDefMC(njobsIn=40, njobsOut=1),
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDefMC(njobsIn=20, njobsOut=1),
        "T_tW-channel_TuneZ2_Fall11":       TaskDefMC(njobsIn=30, njobsOut=1),
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDefMC(njobsIn=30, njobsOut=1),
        "T_s-channel_TuneZ2_Fall11":        TaskDefMC(njobsIn=5, njobsOut=1),
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDefMC(njobsIn=5, njobsOut=1),

        }

    # Update the default definitions from the argument
    updateTaskDefinitions(defaultDefinitions, updateDefinitions)

    # Add pattuple Workflow for each dataset
    for datasetName, taskDef in defaultDefinitions.iteritems():
        dataset = datasets.getDataset(datasetName)

        # Construct processing workflow
        wf = constructProcessingWorkflow_44X(dataset, taskDef, sourceWorkflow="AOD", workflowName="pattuple_"+version, skimConfig=skim)

        # Setup the publish name
        name = updatePublishName(dataset, wf.source.getDataForDataset(dataset).getDatasetPath(), "pattuple_"+version)
        wf.addCrabLine("USER.publish_data_name = "+name)

        # For MC, split by events, for data, split by lumi
        if dataset.isMC():
            wf.addCrabLine("CMSSW.total_number_of_events = -1")
        else:
            wf.addCrabLine("CMSSW.total_number_of_lumis = -1")

        # Add the pattuple Workflow to Dataset
        dataset.addWorkflow(wf)
        # If DBS-dataset of the pattuple has been specified, add also analysis Workflow to Dataset
        if wf.output != None:
            dataset.addWorkflow(Workflow("analysis_"+version, source=Source("pattuple_"+version), triggerOR=taskDef.triggerOR, args=wf.args, dataVersionAppend=wf.dataVersionAppend, skimConfig=skim))

## Add v44_5 pattuple production workflows
def addPattuple_v44_5(datasets):
    definitions = {
        # 7650822 events, 504 jobs
        # User mean 13304.5, min 2532.2, max 37588.4
        # Mean 224.6 MB, min 60.5 MB, max 505.2 MB
        "Tau_160431-167913_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_160431_167913_pattuple_v44_5-5b9e06707f537e1145c67b2d6e11cbbd/USER"),
        # 914344 events
        # User mean 4100.7, min 751.5, max 11620.2
        # Mean 72.7 MB, min 20.1 MB, max 154.9 MB
        "Tau_170722-173198_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_170722_173198_pattuple_v44_5-29dd66960ccb0c43b9b01919e28657bd/USER"),
        # 470476 events
        # User mean 4748.7, min 1443.0, max 10400.2
        # Mean 82.7 MB, min 35.0 MB, max 166.1 MB
        "Tau_173236-173692_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_173236_173692_pattuple_v44_5-1b3ed6acb33bc8106ac34fb558c6831f/USER"),
        # 6298060 events
        # User mean 18182.0, min 4722.5, max 37545.8
        # Mean 321.7 MB, min 83.2 MB, max 529.7 MB
        "Tau_175832-180252_2011B_Nov19":    TaskDef("/Tau/local-Run2011B_19Nov2011_v1_AOD_175832_180252_pattuple_v44_5-b5ff496274cc2d624fc6fce769142e2a/USER"),

        # 18274-32151 events, 15-17 jobs
        # User mean 1325.4, min 162.2, max 1946.4
        # Mean 87.1 MB, min 10.4 MB, max 102.4 MB
        "TTToHplusBWB_M80_Fall11":          TaskDef("/TTToHplusBWB_M-80_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 1739.5, min 34.5, max 2191.1
        # Mean 97.2 MB, min 1.9 MB, max 108.0 MB
        "TTToHplusBWB_M90_Fall11":          TaskDef("/TTToHplusBWB_M-90_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 1711.1, min 20.5, max 2329.7
        # Mean 101.5 MB, min 1.9 MB, max 112.9 MB
        "TTToHplusBWB_M100_Fall11":         TaskDef("/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 2110.6, min 1690.4, max 2525.6
        # Mean 120.6 MB, min 116.2 MB, max 124.1 MB
        "TTToHplusBWB_M120_Fall11":         TaskDef("/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 2117.1, min 1378.2, max 2770.5
        # Mean 131.4 MB, min 88.3 MB, max 144.6 MB
        "TTToHplusBWB_M140_Fall11":         TaskDef("/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 2035.1, min 725.4, max 2895.7
        # Mean 139.5 MB, min 55.1 MB, max 152.9 MB
        "TTToHplusBWB_M150_Fall11":         TaskDef("/TTToHplusBWB_M-150_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 2494.2, min 909.9, max 3100.0
        # Mean 142.8 MB, min 55.1 MB, max 154.9 MB
        "TTToHplusBWB_M155_Fall11":         TaskDef("/TTToHplusBWB_M-155_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 2845.7, min 2141.5, max 3300.1
        # Mean 155.2 MB, min 150.9 MB, max 159.5 MB
        "TTToHplusBWB_M160_Fall11":         TaskDef("/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),

        # 23781-46586 events, 15-17 jobs
        # User mean 1673.4, min 574.6, max 2414.5
        # Mean 111.6 MB, min 41.2 MB, max 121.1 MB
        "TTToHplusBHminusB_M80_Fall11":     TaskDef("/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 1837.1, min 1630.5, max 2533.7
        # Mean 123.8 MB, min 117.5 MB, max 128.0 MB
        "TTToHplusBHminusB_M90_Fall11":     TaskDef("/TTToHplusBHminusB_M-90_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 2068.6, min 226.8, max 2684.8
        # Mean 116.4 MB, min 12.1 MB, max 134.0 MB
        "TTToHplusBHminusB_M100_Fall11":    TaskDef("/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 2179.3, min 767.0, max 3004.3
        # Mean 138.4 MB, min 57.0 MB, max 151.8 MB
        "TTToHplusBHminusB_M120_Fall11":    TaskDef("/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 2577.2, min 1912.3, max 3523.5
        # Mean 161.4 MB, min 106.6 MB, max 179.3 MB
        "TTToHplusBHminusB_M140_Fall11":    TaskDef("/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 2598.3, min 1127.2, max 3609.8
        # Mean 171.9 MB, min 80.3 MB, max 189.0 MB
        "TTToHplusBHminusB_M150_Fall11":    TaskDef("/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 3107.8, min 1203.1, max 3873.1
        # Mean 175.7 MB, min 70.1 MB, max 193.0 MB
        "TTToHplusBHminusB_M155_Fall11":    TaskDef("/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 2664.3, min 958.2, max 4995.6
        # Mean 169.6 MB, min 49.6 MB, max 197.8 MB
        "TTToHplusBHminusB_M160_Fall11":    TaskDef("/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),

        # 43034-64331 events, 5-6 jobs
        # User mean 7573.2, min 20.0, max 9332.1
        # Mean 529.3 MB, min 1.9 MB, max 646.5 MB
        "HplusTB_M180_Fall11":              TaskDef("/HplusTB_M-180_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 13527.9, min 13385.7, max 13809.7
        # Mean 674.9 MB, min 673.1 MB, max 677.4 MB
        "HplusTB_M190_Fall11":              TaskDef("/HplusTB_M-190_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 11980.5, min 10111.3, max 14455.7
        # Mean 720.0 MB, min 711.7 MB, max 737.7 MB
        "HplusTB_M200_Fall11":              TaskDef("/HplusTB_M-200_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 15097.0, min 14518.4, max 15456.7
        # Mean 754.3 MB, min 737.1 MB, max 767.8 MB
        "HplusTB_M220_Fall11":              TaskDef("/HplusTB_M-220_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 14018.3, min 11712.5, max 22224.1
        # Mean 834.4 MB, min 827.1 MB, max 840.8 MB
        "HplusTB_M250_Fall11":              TaskDef("/HplusTB_M-250_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # User mean 14045.9, min 19.9, max 19703.3
        # Mean 796.5 MB, min 1.9 MB, max 970.8 MB
        "HplusTB_M300_Fall11":              TaskDef("/HplusTB_M-300_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),

        # 32 events, 11 jobs
        # User mean 3099.7, min 40.3, max 3883.3
        # Mean 5.8 MB, min 1.9 MB, max 6.7 MB
        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDef("/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 677 events, 11 jobs
        # User mean 3475.8, min 101.3, max 4757.8
        # Mean 10.3 MB, min 2.0 MB, max 11.8 MB
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDef("/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 6152 events, 11 jobs
        # User mean 4673.3, min 1898.5, max 5300.7
        # Mean 46.6 MB, min 20.9 MB, max 53.2 MB
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDef("/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 26243 events, 21 jobs
        # User mean 4800.8, min 193.4, max 5764.3
        # Mean 89.9 MB, min 5.3 MB, max 97.5 MB
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDef("/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 83237 events, 41 jobs
        # User mean 4989.9, min 1710.9, max 6474.6
        # Mean 144.4 MB, min 57.7 MB, max 154.4 MB
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDef("/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 220338 events, 101 jobs
        # User mean 4556.6, min 129.1, max 5261.4
        # Mean 159.4 MB, min 3.3 MB, max 168.1 MB
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDef("/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),

        # 77684 events, 41 jobs
        # User mean 3842.1, min 143.5, max 4664.9
        # Mean 118.6 MB, min 3.0 MB, max 126.7 MB
        "WW_TuneZ2_Fall11":                 TaskDef("/WW_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 68886 events, 41 jobs
        # User mean 3675.4, min 1405.0, max 4130.6
        # Mean 106.5 MB, min 43.4 MB, max 113.2 MB
        "WZ_TuneZ2_Fall11":                 TaskDef("/WZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 58071 events, 42 jobs
        # User mean 2956.5, min 238.9, max 3601.0
        # Mean 87.6 MB, min 9.3 MB, max 95.1 MB
        "ZZ_TuneZ2_Fall11":                 TaskDef("/ZZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 3358608 events, 2003 jobs
        # User mean 3018.3, min 693.0, max 4590.2
        # Mean 139.4 MB, min 30.5 MB, max 151.1 MB
        "TTJets_TuneZ2_Fall11":             TaskDef("/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 301748 events, 407 jobs
        # User mean 2419.0, min 176.7, max 3345.0
        # Mean 49.3 MB, min 3.3 MB, max 54.2 MB
        "WJets_TuneZ2_Fall11":              TaskDef("/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 501106 events, 307 jobs
        # User mean 2651.9, min 78.9, max 6659.2
        # Mean 91.9 MB, min 3.2 MB, max 99.6 MB
        "W1Jets_TuneZ2_Fall11":             TaskDef("/W1Jet_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 404002 events, 202 events
        # User mean 4932.9, min 381.0, max 5728.2
        # Mean 122.7 MB, min 9.3 MB, max 131.3 MB
        "W2Jets_TuneZ2_Fall11":             TaskDef("/W2Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 208523 events, 101 jobs
        # User mean 4009.9, min 126.6, max 5742.2
        # Mean 143.6 MB, min 3.1 MB, max 152.2 MB
        "W3Jets_TuneZ2_v2_Fall11":          TaskDef("/W3Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v2_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 604144 events, 303 jobs
        # User mean 5153.5, min 239.9, max 8819.9
        # Mean 149.4 MB, min 4.8 MB, max 162.4 MB
        "W4Jets_TuneZ2_Fall11":             TaskDef("/W4Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 71235 events, 201 jobs
        # User mean 1521.7, min 584.8, max 2864.9
        # Mean 29.0 MB, min 9.3 MB, max 33.1 MB
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDef("/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 61815 events, 43 jobs
        # User mean 3090.9, min 259.1, max 3932.5
        # Mean 102.2 MB, min 9.8 MB, max 116.6 MB
        "T_t-channel_TuneZ2_Fall11":        TaskDef("/T_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 29028 events, 23 jobs
        # User mean 2648.3, min 372.8, max 3845.4
        # Mean 89.9 MB, min 12.5 MB, max 108.1 MB
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDef("/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 41707 events, 31 jobs
        # User mean 2648.8, min 1291.2, max 3468.4
        # Mean 104.2 MB, min 52.0 MB, max 111.9 MB
        "T_tW-channel_TuneZ2_Fall11":       TaskDef("/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 41142 events, 32 jobs
        # User mean 2530.8, min 128.8, max 4528.9
        # Mean 100.0 MB, min 5.2 MB, max 110.3 MB
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDef("/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 4241 events, 6 jobs
        # User mean 1643.2, min 1103.8, max 2191.3
        # Mean 55.3 MB, min 35.6 MB, max 66.4 MB
        "T_s-channel_TuneZ2_Fall11":        TaskDef("/T_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        # 1986 events, 7 jobs
        # User mean 696.4, min 303.2, max 1101.2
        # Mean 24.7 MB, min 8.4 MB, max 34.3 MB
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDef("/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5-778bc6993dea1b89668515c3036cbe70/USER"),
        }

    addPattuple_44X("v44_5", datasets, definitions)

# Skeleton
def addPattuple_vNEXT_SKELETON(datasets):
    definitions = {
        "Tau_160431-167913_2011A_Nov08":    TaskDef(""),
        "Tau_170722-173198_2011A_Nov08":    TaskDef(""),
        "Tau_173236-173692_2011A_Nov08":    TaskDef(""),
        "Tau_175832-180252_2011B_Nov19":    TaskDef(""),

        "TTToHplusBWB_M80_Fall11":          TaskDef(""),
        "TTToHplusBWB_M90_Fall11":          TaskDef(""),
        "TTToHplusBWB_M100_Fall11":         TaskDef(""),
        "TTToHplusBWB_M120_Fall11":         TaskDef(""),
        "TTToHplusBWB_M140_Fall11":         TaskDef(""),
        "TTToHplusBWB_M150_Fall11":         TaskDef(""),
        "TTToHplusBWB_M155_Fall11":         TaskDef(""),
        "TTToHplusBWB_M160_Fall11":         TaskDef(""),

        "TTToHplusBHminusB_M80_Fall11":     TaskDef(""),
        "TTToHplusBHminusB_M90_Fall11":     TaskDef(""),
        "TTToHplusBHminusB_M100_Fall11":    TaskDef(""),
        "TTToHplusBHminusB_M120_Fall11":    TaskDef(""),
        "TTToHplusBHminusB_M140_Fall11":    TaskDef(""),
        "TTToHplusBHminusB_M150_Fall11":    TaskDef(""),
        "TTToHplusBHminusB_M155_Fall11":    TaskDef(""),
        "TTToHplusBHminusB_M160_Fall11":    TaskDef(""),

        "HplusTB_M180_Fall11":              TaskDef(""),
        "HplusTB_M190_Fall11":              TaskDef(""),
        "HplusTB_M200_Fall11":              TaskDef(""),
        "HplusTB_M220_Fall11":              TaskDef(""),
        "HplusTB_M250_Fall11":              TaskDef(""),
        "HplusTB_M300_Fall11":              TaskDef(""),

        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDef(""),
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDef(""),
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDef(""),
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDef(""),
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDef(""),
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDef(""),

        "WW_TuneZ2_Fall11":                 TaskDef(""),
        "WZ_TuneZ2_Fall11":                 TaskDef(""),
        "ZZ_TuneZ2_Fall11":                 TaskDef(""),
        "TTJets_TuneZ2_Fall11":             TaskDef(""),
        "WJets_TuneZ2_Fall11":              TaskDef(""),
        "W1Jets_TuneZ2_Fall11":             TaskDef(""),
        "W2Jets_TuneZ2_Fall11":             TaskDef(""),
        "W3Jets_TuneZ2_v2_Fall11":          TaskDef(""),
        "W4Jets_TuneZ2_Fall11":             TaskDef(""),
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDef(""),
        "T_t-channel_TuneZ2_Fall11":        TaskDef(""),
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDef(""),
        "T_tW-channel_TuneZ2_Fall11":       TaskDef(""),
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDef(""),
        "T_s-channel_TuneZ2_Fall11":        TaskDef(""),
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDef(""),
        }

    #addPattuple_44X("VERSION", datasets, definitions)
