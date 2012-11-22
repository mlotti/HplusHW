## \package multicrabDatasetsPatTuple
# Functions for pattuple definitions

import re

from multicrabWorkflowsTools import Dataset, Workflow, Data, Source, updatePublishName, TaskDef, updateTaskDefinitions
import multicrabDatasetsCommon as common

def _constructProcessingWorkflow_common(dataset, taskDef, sourceWorkflow, workflowName, inputLumiMask, outputLumiMask, **kwargs):
    # Setup the Source for pattuple Workflow
    source = Source(sourceWorkflow,
                    # These are exclusive, but the default values of None and a check in Workflow ensure correctness
                    number_of_jobs=taskDef.njobsIn, events_per_job=taskDef.neventsPerJobIn, lumis_per_job=taskDef.nlumisPerJobIn,
                    lumiMask=inputLumiMask)
    # If taskDef contains the DBS-path of the pattuple, setup also the Data for the pattuple
    output = None
    if taskDef.outputPath != None and len(taskDef.outputPath) > 0:
        output = Data(taskDef.outputPath,
                      # These are exclusive, but the default values of None and a check in Workflow ensure correctness
                      number_of_jobs=taskDef.njobsOut, events_per_job=taskDef.neventsPerJobOut, lumis_per_job=taskDef.nlumisPerJobOut,
                      lumiMask=outputLumiMask, dbs_url=common.pattuple_dbs)

    # Additional, necessary command line arguments relaring to trigger
    args = {}
    if len(taskDef.triggerOR) > 1 and taskDef.triggerThrow != None and taskDef.triggerThrow == False:
        args["triggerThrow"] = 0
    if dataset.isMC() and taskDef.triggerOR != None:
        args["triggerMC"] = 1
    if taskDef.args != None:
        args.update(taskDef.args)

    wf = Workflow(workflowName, source=source, triggerOR=taskDef.triggerOR, args=args, output=output, **kwargs)
    if taskDef.crabLines != None:
        for line in taskDef.crabLines:
            wf.addCrabLine(line)
    return wf

def constructProcessingWorkflow_44X(dataset, taskDef, sourceWorkflow, workflowName, **kwargs):
    # Setup input/default output lumimasks for data
    inputLumiMask = None
    outputLumiMask = None
    if dataset.isData():
        inputLumiMask = "DCSONLY11"
        outputLumiMask = "Nov08ReReco"

    return _constructProcessingWorkflow_common(dataset, taskDef, sourceWorkflow, workflowName, inputLumiMask, outputLumiMask, **kwargs)

def constructProcessingWorkflow_53X(dataset, taskDef, sourceWorkflow, workflowName, **kwargs):
    # Setup input/default output lumimasks for data
    inputLumiMask = None
    outputLumiMask = None
    if dataset.isData():
        inputLumiMask = "DCSONLY12"
        reco = dataset.getName().split("_")[-1]
        outputLumiMask = {
            "Jul13": "13Jul2012ReReco",
            "Aug06": "06Aug2012ReReco",
            "Aug24": "24Aug2012ReReco",
            "Prompt": "PromptReco12"
            }[reco]

    return _constructProcessingWorkflow_common(dataset, taskDef, sourceWorkflow, workflowName, inputLumiMask, outputLumiMask, **kwargs)


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
        return TaskDef(triggerOR=[mcTrigger], **kwargs)

    # Specifies the default
    # - number of jobs in pattuple processing
    # - number of jobs for those who read pattuples
    # - triggers
    # for all relevant Datasets
    defaultDefinitions = {
        "Tau_160431-167913_2011A_Nov08": TaskDef(njobsIn=300, njobsOut=15, triggerOR=[
                                                    "HLT_IsoPFTau35_Trk20_MET45_v1", # 160431-161176
                                                    "HLT_IsoPFTau35_Trk20_MET45_v2", # 161216-163261
                                                    "HLT_IsoPFTau35_Trk20_MET45_v4", # 163270-163869
                                                    "HLT_IsoPFTau35_Trk20_MET45_v6", # 165088-165633
                                                    "HLT_IsoPFTau35_Trk20_MET60_v2", # 165970-166164, 166374-167043
                                                    "HLT_IsoPFTau35_Trk20_MET60_v3", # 166346
                                                    "HLT_IsoPFTau35_Trk20_MET60_v4", # 167078-167913
                                                ], triggerThrow=False),
        "Tau_170722-173198_2011A_Nov08": TaskDef(njobsIn=70, njobsOut=3, triggerOR=["HLT_IsoPFTau35_Trk20_MET60_v6"]),
        "Tau_173236-173692_2011A_Nov08": TaskDef(njobsIn=30, njobsOut=2, triggerOR=["HLT_MediumIsoPFTau35_Trk20_MET60_v1"]),
        "Tau_175832-180252_2011B_Nov19": TaskDef(njobsIn=300, njobsOut=30, triggerOR=[
                                                    "HLT_MediumIsoPFTau35_Trk20_MET60_v1", # 175832-178380
                                                    "HLT_MediumIsoPFTau35_Trk20_MET60_v5", # 178420-179889
                                                    "HLT_MediumIsoPFTau35_Trk20_MET60_v6", # 179959-180252
                                              ], triggerThrow=False),

        # MC, triggered with mcTrigger
        "TTToHplusBWB_M80_Fall11":        TaskDefMC(njobsIn=50, njobsOut=2), # 53 GB, 19 files
        "TTToHplusBWB_M90_Fall11":        TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBWB_M100_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBWB_M120_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBWB_M140_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBWB_M150_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBWB_M155_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBWB_M160_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),

        "TTToHplusBHminusB_M80_Fall11":        TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBHminusB_M90_Fall11":        TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBHminusB_M100_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBHminusB_M120_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBHminusB_M140_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBHminusB_M150_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBHminusB_M155_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "TTToHplusBHminusB_M160_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),

        "HplusTB_M180_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "HplusTB_M190_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "HplusTB_M200_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "HplusTB_M220_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "HplusTB_M250_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),
        "HplusTB_M300_Fall11":       TaskDefMC(njobsIn=50, njobsOut=2),

        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDefMC(njobsIn=20, njobsOut=1),
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDefMC(njobsIn=40, njobsOut=4),
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDefMC(njobsIn=40, njobsOut=10),
                                            
        "WW_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),   # file size 890 GB, 252-275 files, expected output max. 185 MB/file
        "WZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),   # expected output max. 185 MB/file
        "ZZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),   # expected output max. 185 MB/file
        "TTJets_TuneZ2_Fall11":             TaskDefMC(njobsIn=490, njobsOut=50), # file size 15214; 3938 files, expected output max. 266 MB/file, obs 60 MB / file
        "WJets_TuneZ2_Fall11":              TaskDefMC(njobsIn=490, njobsOut=10), # file size 16000 GB, 4500 files, expected output max. 37 MB/file 
        "W2Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=300, njobsOut=20), # expected output max. 38 MB/file, obs 38 MB / file
        "W3Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=120, njobsOut=10), # expected output max. 56 MB/file, obs 20-22 MB / file
        "W4Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=200, njobsOut=12), # expected output max. 144 MB/file, obs 20-22 MB / file
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDefMC(njobsIn=350, njobsOut=2),  # file size 6945 GB, 1964 files, expected output max. 46 MB/file, obs 40 MB / file
        "DYJetsToLL_M10to50_TuneZ2_Fall11": TaskDefMC(njobsIn=300, njobsOut=1),  # file size 5900 GB, 1420 files, expected output max. 47 MB/file, obs 21 MB / file
        "T_t-channel_TuneZ2_Fall11":        TaskDefMC(njobsIn=50, njobsOut=2),   # 866 GB, 395 files, expected output max. 47 MB/file, obs 15-20 MB / file
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDefMC(njobsIn=50, njobsOut=1),   # expected output max. 47 MB/file, obs 15-20 MB / file
        "T_tW-channel_TuneZ2_Fall11":       TaskDefMC(njobsIn=20, njobsOut=1),   # 210 GB, 69 files, expected output max. 28 MB/file, obs 15-20 MB / file
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDefMC(njobsIn=20, njobsOut=1),   # expected output max. 15 MB/file, obs 15-20 MB / file
        "T_s-channel_TuneZ2_Fall11":        TaskDefMC(njobsIn=10, njobsOut=1),      # 59 GB, 19 files, expected output max. 57 MB/file, obs 15-20 MB / file
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDefMC(njobsIn=10, njobsOut=1),

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
            dataset.addWorkflow(Workflow("analysis_"+version, source=Source("pattuple_"+version), triggerOR=taskDef.triggerOR, args=wf.args, skimConfig=skim))


## Main function for generating 53X pattuples
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
def addPattuple_53X(version, datasets, updateDefinitions, skim=None):
    mcTriggerTauMET = "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6"
    mcTriggerQuadJet = "HLT_QuadJet80_v2"
    mcTriggerQuadJetBTag = "HLT_QuadJet75_55_35_20_BTagIP_VBF_v3"
    mcTriggerQuadPFJet78BTag = "HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v1"
    mcTriggerQuadPFJet82BTag = "HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v1"
    mcTriggers = [
        mcTriggerTauMET,
        mcTriggerQuadJet,
        mcTriggerQuadJetBTag,
        mcTriggerQuadPFJet78BTag,
        mcTriggerQuadPFJet82BTag,
        ]
    def TaskDefMC(**kwargs):
        return TaskDef(triggerOR=mcTriggers, **kwargs)

    # Trigger selection efficiency for WH signal M120
    # HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6: 605/6048 = 0.10003
    # HLT_QuadJet80_v2: 199/6048 = 0.032903
    # HLT_QuadJet75_55_35_20_BTagIP_VBF_v3: 162/6048 = 0.026786
    # HLT_QuadJet75_55_38_20_BTagIP_VBF_v3: 141/6048 = 0.023313
    # HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v1: 149/6048 = 0.024636
    # HLT_QuadPFJet82_65_48_35_BTagCSV_VBF_v1: 125/6048 = 0.020668
    #
    # HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6 OR
    # HLT_QuadJet75_55_35_20_BTagIP_VBF_v3 OR
    # HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v1 OR
    # HLT_QuadPFJet82_65_48_35_BTagCSV_VBF_v1: 807/6048 = 0.13343

    # HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6 OR
    # HLT_QuadJet80_v2 OR
    # HLT_QuadJet75_55_35_20_BTagIP_VBF_v3 OR
    # HLT_QuadPFJet78_61_44_31_BTagCSV_VBF_v1 OR
    # HLT_QuadPFJet82_65_48_35_BTagCSV_VBF_v1: 958/6048 = 0.15840

    # Trigger selection efficiency for Data
    # Tau Aug24 (HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7): 984/7489 = 0.13139
    # MultiJet Jul13 HLT_QuadJet80_v2: 453/5000 = 0.090600
    #                HLT_QuadJet75_55_38_20_BTagIP_VBF_v3: 440/5000 = 0.088000
    #                HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v4: 537/5000 = 0.10740
    #                OR: 1222/5000 = 0.24440


    quadPFJetBTagTriggers = {
        "MultiJet_190456-190738_2012A_Jul13": ["HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v2"],
        "MultiJet_190782-190949_2012A_Aug06": ["HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v3"],
        "MultiJet_191043-193621_2012A_Jul13": ["HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v3",  # 191043-191411
                                               "HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v4"], # 191691-193621
        "MultiJet_193834-194225_2012B_Jul13": ["HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v4"],
    }
    quadJetBTagTriggers = {
        "MultiJet_190456-190738_2012A_Jul13": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v2"],
        "MultiJet_190782-190949_2012A_Aug06": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v3"],
        "MultiJet_191043-193621_2012A_Jul13": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v3"],
        "MultiJet_193834-194225_2012B_Jul13": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v3"],
        "MultiJet_194270-196531_2012B_Jul13": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v3"],
        "MultiJet_198022-198523_2012C_Aug24": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v4"],
        "MultiJet_198941-200601_2012C_Prompt": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v4",  # 198941-199608
                                                "HLT_QuadJet75_55_38_20_BTagIP_VBF_v6"], # 199698-200601
        "MultiJet_200961-202504_2012C_Prompt": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v6"],
        "MultiJet_202792-203742_2012C_Prompt": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v6"],
    }
    quadJetTriggers = {
        "MultiJet_190456-190738_2012A_Jul13": ["HLT_QuadJet80_v1"],
        "MultiJet_190782-190949_2012A_Aug06": ["HLT_QuadJet80_v2"],
        "MultiJet_191043-193621_2012A_Jul13": ["HLT_QuadJet80_v2"],
        "MultiJet_193834-194225_2012B_Jul13": ["HLT_QuadJet80_v2"],
        "MultiJet_194270-196531_2012B_Jul13": ["HLT_QuadJet80_v2",  # 194270-196027
                                               "HLT_QuadJet80_v3"], # 196046-196531
        "MultiJet_198022-198523_2012C_Aug24": ["HLT_QuadJet80_v4"],
        "MultiJet_198941-200601_2012C_Prompt": ["HLT_QuadJet80_v4",  # 198941-199608
                                                "HLT_QuadJet80_v6"], # 199698-200601
        "MultiJet_200961-202504_2012C_Prompt": ["HLT_QuadJet80_v6"],
        "MultiJet_202792-203742_2012C_Prompt": ["HLT_QuadJet80_v6"],
    }

    # Specifies the default
    # - number of jobs in pattuple processing
    # - number of jobs for those who read pattuples
    # - triggers
    # for all relevant Datasets
    #
    # Goal is to have ~200 MB output/job for pattuples
    # - This works quite well over Atlantic
    # - Also smaller outputs are somewhat problematic, because then
    #   there is potential to reduce the number of jobs
    #   * -getotput and -publish steps take longer with large number of jobs
    #
    # Goal is to have ~150kevents/job for analysis phase
    defaultDefinitions = {
        # njobsOut is just a guess
        "Tau_190456-190738_2012A_Jul13":  TaskDef(njobsIn=  35, njobsOut=  1, triggerOR=["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v2"]),
        "Tau_190782-190949_2012A_Aug06":  TaskDef(njobsIn=  10, njobsOut=  1, triggerOR=["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v3"]),
        "Tau_191043-193621_2012A_Jul13":  TaskDef(njobsIn= 150, njobsOut=  3, triggerOR=[
                                                      "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v3", # 191043-191411
                                                      "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v4", # 191691-191491 (193621)
                                                  ], triggerThrow=False),

        "Tau_193834-196531_2012B_Jul13":  TaskDef(njobsIn=2000, njobsOut= 20, triggerOR=["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6"]),
        "Tau_198022-198523_2012C_Aug24":  TaskDef(njobsIn= 200, njobsOut=  2, triggerOR=["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7"]),
        # FIXME: the following three could be combined in the subsequent pattuple processings
        "Tau_198941-200601_2012C_Prompt": TaskDef(njobsIn=1500, njobsOut= 12, triggerOR=[
                                                     "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7",  # 198941-199608
                                                     "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9",  # 199698-200161
                                                 ], triggerThrow=False),
        "Tau_200961-202504_2012C_Prompt": TaskDef(njobsIn=1500, njobsOut= 12, triggerOR=["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9"]),
        "Tau_202792-203742_2012C_Prompt": TaskDef(njobsIn= 150, njobsOut=  2, triggerOR=["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10"]),

        ## MultiJet
        # njobsOut is just a guess
        "MultiJet_190456-190738_2012A_Jul13":  TaskDef(njobsIn= 490, njobsOut= 4),
        "MultiJet_190782-190949_2012A_Aug06":  TaskDef(njobsIn= 120, njobsOut= 2),
        "MultiJet_191043-193621_2012A_Jul13":  TaskDef(njobsIn=1200, njobsOut=20),
        "MultiJet_193834-194225_2012B_Jul13":  TaskDef(njobsIn= 600, njobsOut= 6),
        "MultiJet_194270-196531_2012B_Jul13":  TaskDef(njobsIn=2200, njobsOut=40),
        "MultiJet_198022-198523_2012C_Aug24":  TaskDef(njobsIn= 250, njobsOut= 5),
        # FIXME: the following three could be combined in the subsequent pattuple processings
        "MultiJet_198941-200601_2012C_Prompt": TaskDef(njobsIn=1700, njobsOut=35),
        "MultiJet_200961-202504_2012C_Prompt": TaskDef(njobsIn=1700, njobsOut=35),
        "MultiJet_202792-203742_2012C_Prompt": TaskDef(njobsIn= 170, njobsOut= 3),

        # MC, triggered with mcTrigger
        "TTToHplusBWB_M80_Summer12":        TaskDefMC(njobsIn=25, njobsOut=1),
        "TTToHplusBWB_M90_Summer12":        TaskDefMC(njobsIn=25, njobsOut=1),
        "TTToHplusBWB_M100_Summer12":       TaskDefMC(njobsIn=25, njobsOut=1),
        "TTToHplusBWB_M120_Summer12":       TaskDefMC(njobsIn=25, njobsOut=1),
        "TTToHplusBWB_M140_Summer12":       TaskDefMC(njobsIn=25, njobsOut=1),
        "TTToHplusBWB_M150_Summer12":       TaskDefMC(njobsIn=25, njobsOut=1),
        "TTToHplusBWB_M155_Summer12":       TaskDefMC(njobsIn=25, njobsOut=1),
        "TTToHplusBWB_M160_Summer12":       TaskDefMC(njobsIn=25, njobsOut=1),

        "TTToHplusBWB_M80_ext_Summer12":    TaskDefMC(njobsIn=130, njobsOut=1), # FIXME out
        "TTToHplusBWB_M90_ext_Summer12":    TaskDefMC(njobsIn=130, njobsOut=1), # FIXME out
        "TTToHplusBWB_M100_ext_Summer12":   TaskDefMC(njobsIn=130, njobsOut=1), # FIXME out
        "TTToHplusBWB_M120_ext_Summer12":   TaskDefMC(njobsIn=130, njobsOut=1), # FIXME out
        "TTToHplusBWB_M140_ext_Summer12":   TaskDefMC(njobsIn=130, njobsOut=1), # FIXME out
        "TTToHplusBWB_M150_ext_Summer12":   TaskDefMC(njobsIn=130, njobsOut=1), # FIXME out
        "TTToHplusBWB_M155_ext_Summer12":   TaskDefMC(njobsIn=130, njobsOut=1), # FIXME out
        "TTToHplusBWB_M160_ext_Summer12":   TaskDefMC(njobsIn=130, njobsOut=1), # FIXME out

        "TTToHplusBHminusB_M80_Summer12":        TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M90_Summer12":        TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M100_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M120_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M140_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M150_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M155_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M160_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),

        "TTToHplusBHminusB_M80_ext_Summer12":    TaskDefMC(njobsIn=100, njobsOut=1), # FIXME out
        "TTToHplusBHminusB_M90_ext_Summer12":    TaskDefMC(njobsIn=100, njobsOut=1), # FIXME out
        "TTToHplusBHminusB_M100_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=1), # FIXME out
        "TTToHplusBHminusB_M120_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=1), # FIXME out
        "TTToHplusBHminusB_M140_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=1), # FIXME out
        "TTToHplusBHminusB_M150_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=1), # FIXME out
        "TTToHplusBHminusB_M155_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=1), # FIXME out
        "TTToHplusBHminusB_M160_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=1), # FIXME out

        "Hplus_taunu_t-channel_M80_Summer12":    TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_t-channel_M90_Summer12":    TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_t-channel_M100_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_t-channel_M120_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_t-channel_M140_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_t-channel_M150_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_t-channel_M155_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_t-channel_M160_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out

        "Hplus_taunu_tW-channel_M80_Summer12":    TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_tW-channel_M90_Summer12":    TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_tW-channel_M100_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_tW-channel_M120_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_tW-channel_M140_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_tW-channel_M150_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_tW-channel_M155_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out
        "Hplus_taunu_tW-channel_M160_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1), # FIXME out

        "Hplus_taunu_s-channel_M80_Summer12":       TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M90_Summer12":       TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M100_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M120_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M140_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M150_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M155_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M160_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),

        "HplusTB_M180_Summer12":       TaskDefMC(njobsIn=40, njobsOut=2),
        "HplusTB_M190_Summer12":       TaskDefMC(njobsIn=40, njobsOut=2),
        "HplusTB_M200_Summer12":       TaskDefMC(njobsIn=40, njobsOut=2),
        "HplusTB_M220_Summer12":       TaskDefMC(njobsIn=40, njobsOut=2),
        "HplusTB_M250_Summer12":       TaskDefMC(njobsIn=40, njobsOut=2),
        "HplusTB_M300_Summer12":       TaskDefMC(njobsIn=40, njobsOut=2),
        "HplusTB_M400_Summer12":       TaskDefMC(njobsIn=200, njobsOut=2), # FIXME out
        "HplusTB_M500_Summer12":       TaskDefMC(njobsIn=200, njobsOut=2), # FIXME out
        "HplusTB_M600_Summer12":       TaskDefMC(njobsIn=200, njobsOut=2), # FIXME out

        "HplusTB_M180_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=2), # FIXME out
        "HplusTB_M190_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=2), # FIXME out
        "HplusTB_M200_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=2), # FIXME out
        "HplusTB_M220_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=2), # FIXME out
        "HplusTB_M250_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=2), # FIXME out
        "HplusTB_M300_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=2), # FIXME out

        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut=1),
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut=1),
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDefMC(njobsIn= 20, njobsOut=1),
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 40, njobsOut=1),
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 80, njobsOut=2),
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDefMC(njobsIn=300, njobsOut=6),
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDefMC(njobsIn=250, njobsOut=5),
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDefMC(njobsIn=150, njobsOut=3),
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDefMC(njobsIn=850, njobsOut=14),
                                            
        "WW_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut=10),
        "WZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut=10),
        "ZZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut=10),
        "TTJets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=700, njobsOut=50),
        "WJets_TuneZ2star_v1_Summer12":           TaskDefMC(njobsIn=100, njobsOut=10),
        "WJets_TuneZ2star_v2_Summer12":           TaskDefMC(njobsIn=250, njobsOut=10),
        "W1Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=150, njobsOut=20),
        "W2Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=400, njobsOut=20),
        "W3Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=490, njobsOut=10),
        "W4Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=550, njobsOut=12),
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDefMC(njobsIn=350, njobsOut= 2),
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDefMC(njobsIn= 40, njobsOut= 1),
        "T_t-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn= 50, njobsOut= 2),
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 50, njobsOut= 1),
        "T_tW-channel_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut= 1),
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDefMC(njobsIn= 20, njobsOut= 1),
        "T_s-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn= 10, njobsOut= 1),
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 10, njobsOut= 1),
        }

    # Set the multijet triggers on data
    for datasetName, taskDef in defaultDefinitions.iteritems():
        if datasetName.split("_")[0] != "MultiJet":
            continue

        triggers = []
        hasOneRunRange = True
        for triggerDict in [quadJetTriggers, quadPFJetBTagTriggers, quadJetBTagTriggers]:
            if datasetName in triggerDict:
                trg = triggerDict[datasetName]
                triggers.extend(trg)
                if len(trg) > 1:
                    hasOneRunRange = False
        taskDef.update(TaskDef(triggerOR=triggers, triggerThrow=hasOneRunRange))

    # Update the default definitions from the argument
    updateTaskDefinitions(defaultDefinitions, updateDefinitions)

    # Add pattuple Workflow for each dataset
    for datasetName, taskDef in defaultDefinitions.iteritems():
        dataset = datasets.getDataset(datasetName)

        # Construct processing workflow
        wf = constructProcessingWorkflow_53X(dataset, taskDef, sourceWorkflow="AOD", workflowName="pattuple_"+version, skimConfig=skim)

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
            commonArgs = {
                "source": Source("pattuple_"+version),
                "args": wf.args,
                "skimConfig": skim
                }

            if dataset.isData():
                # For data, construct one analysis workflow per trigger type
                pd = datasetName.split("_")[0]
                if pd == "Tau":
                    dataset.addWorkflow(Workflow("analysis_taumet_"+version, triggerOR=wf.triggerOR, **commonArgs))
                elif pd == "MultiJet":
                    if datasetName in quadJetTriggers:
                        dataset.addWorkflow(Workflow("analysis_quadjet_"+version, triggerOR=quadJetTriggers[datasetName], **commonArgs))
                    if datasetName in quadJetBTagTriggers:
                        dataset.addWorkflow(Workflow("analysis_quadjetbtag_"+version, triggerOR=quadJetBTagTriggers[datasetName], **commonArgs))
                    if datasetName in quadPFJetBTagTriggers:
                        dataset.addWorkflow(Workflow("analysis_quadpfjetbtag_"+version, triggerOR=quadPFJetBTagTriggers[datasetName], **commonArgs))
                else:
                    raise Exception("Unsupported PD name %s" % pd)
            else:
                # For MC, also construct one analysis workflow per trigger type
                dataset.addWorkflow(Workflow("analysis_taumet_"+version, triggerOR=[mcTriggerTauMET], **commonArgs))
                dataset.addWorkflow(Workflow("analysis_quadjet_"+version, triggerOR=[mcTriggerQuadJet], **commonArgs))
                dataset.addWorkflow(Workflow("analysis_quadjetbtag_"+version, triggerOR=[mcTriggerQuadJetBTag], **commonArgs))
                dataset.addWorkflow(Workflow("analysis_quadpfjet78btag_"+version, triggerOR=[mcTriggerQuadPFJet78BTag], **commonArgs))
                dataset.addWorkflow(Workflow("analysis_quadpfjet82btag_"+version, triggerOR=[mcTriggerQuadPFJet82BTag], **commonArgs))


## Add v25b pattuples
def addPattuple_v25b(datasets):
    definitions = {
        "Tau_160431-167913_2011A_Nov08":    TaskDef("/Tau/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_Tau_160431-167913_2011A_Nov08-6a35806d4ee51a0fcded80eb169c9c26/USER", njobsOut=15), # 4629090 evt, 40-80 MB / file
        "Tau_170722-173198_2011A_Nov08":    TaskDef("/Tau/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_Tau_170722-173198_2011A_Nov08-bf69bd8220530b9ba3ad7a1d882490f3/USER"), # 754860 evt, 30 MB / file
        "Tau_173236-173692_2011A_Nov08":    TaskDef("/Tau/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_Tau_173236-173692_2011A_Nov08-466fa79a18d5f55ecd74f61a06585be0/USER"), # 407038 evt
        "Tau_175832-180252_2011B_Nov19":    TaskDef("/Tau/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_Tau_175860-180252_2011B_Nov19-b2a9ba9a3b361daafe58fb023a257e1b/USER"), # 5691371 evt, 30 MB / file

        "TTToHplusBWB_M80_Fall11":          TaskDef("/TTToHplusBWB_M-80_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M80_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218200 evt, 15-18 MB / file
        "TTToHplusBWB_M90_Fall11":          TaskDef("/TTToHplusBWB_M-90_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M90_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218200 evt
        "TTToHplusBWB_M100_Fall11":         TaskDef("/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_TTToHplusBWB_M100_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218200 evt
        "TTToHplusBWB_M120_Fall11":         TaskDef("/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218200 evt
        "TTToHplusBWB_M140_Fall11":         TaskDef("/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M140_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218200 evt
        "TTToHplusBWB_M150_Fall11":         TaskDef("/TTToHplusBWB_M-150_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M150_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218900 evt
        "TTToHplusBWB_M155_Fall11":         TaskDef("/TTToHplusBWB_M-155_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M155_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218900 evt
        "TTToHplusBWB_M160_Fall11":         TaskDef("/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M160_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218400 evt

        "TTToHplusBHminusB_M80_Fall11":     TaskDef("/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBHminusB_M80_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218400 evt
        "TTToHplusBHminusB_M90_Fall11":     TaskDef("/TTToHplusBHminusB_M-90_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBHminusB_M90_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218900 evt
        "TTToHplusBHminusB_M100_Fall11":    TaskDef("/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25bfix_nojetskim_TTToHplusBHminusB_M100_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 217600 evt
        "TTToHplusBHminusB_M120_Fall11":    TaskDef("/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBHminusB_M120_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218800 evt
        "TTToHplusBHminusB_M140_Fall11":    TaskDef("/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBHminusB_M140_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218800 evt
        "TTToHplusBHminusB_M150_Fall11":    TaskDef("/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBHminusB_M150_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 218800 evt
        "TTToHplusBHminusB_M155_Fall11":    TaskDef("/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBHminusB_M155_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 217400 evt
        "TTToHplusBHminusB_M160_Fall11":    TaskDef("/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBHminusB_M160_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 220000 evt

        "HplusTB_M180_Fall11":              TaskDef("/HplusTB_M-180_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_HplusTB_M180_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 210823 evt
        "HplusTB_M190_Fall11":              TaskDef("/HplusTB_M-190_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_HplusTB_M190_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 209075 evt
        "HplusTB_M200_Fall11":              TaskDef("/HplusTB_M-200_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_HplusTB_M200_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 214140 evt
        "HplusTB_M220_Fall11":              TaskDef("/HplusTB_M-220_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_HplusTB_M220_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 199960 evt
        "HplusTB_M250_Fall11":              TaskDef("/HplusTB_M-250_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_HplusTB_M250_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 202450 evt
        "HplusTB_M300_Fall11":              TaskDef("/HplusTB_M-300_7TeV-pythia6-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_HplusTB_M300_Fall11-867f8948ab405c5cced92453543fca46/USER"), # 201457 evt

        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDef("/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_QCD_Pt30to50_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 32 evt
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDef("/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_QCD_Pt50to80_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 677 evt
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDef("/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_QCD_Pt80to120_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 6152 evt
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDef("/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_QCD_Pt120to170_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 26115 evt
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDef("/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_QCD_Pt170to300_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 83237 evt
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDef("/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_QCD_Pt300to470_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 219207 evt

        "WW_TuneZ2_Fall11":                 TaskDef("/WW_TuneZ2_7TeV_pythia6_tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_WW_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 50032 evt
        "WZ_TuneZ2_Fall11":                 TaskDef("/WZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_WZ_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 44675 evt
        "ZZ_TuneZ2_Fall11":                 TaskDef("/ZZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_ZZ_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"),
        "TTJets_TuneZ2_Fall11":             TaskDef("/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTJets_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 3125473 evt
        "WJets_TuneZ2_Fall11":              TaskDef("/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_WJets_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 180088
        "W2Jets_TuneZ2_Fall11":             TaskDef("/W2Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_W2Jets_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 267079
        "W3Jets_TuneZ2_Fall11":             TaskDef("/W3Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_W3Jets_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 185741 evt
        "W4Jets_TuneZ2_Fall11":             TaskDef("/W4Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_W4Jets_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 580556 
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDef("/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_DYJetsToLL_M50_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 51916 evt
        "T_t-channel_TuneZ2_Fall11":        TaskDef("/T_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_T_t-channel_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 49900 evt
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDef("/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_Tbar_t-channel_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 23601 evt
        "T_tW-channel_TuneZ2_Fall11":       TaskDef("/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_T_tW-channel_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 36882 evt
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDef("/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_Tbar_tW-channel_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 36369 evt
        "T_s-channel_TuneZ2_Fall11":        TaskDef("/T_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_T_s-channel_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 3618 evt
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDef("/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_Tbar_s-channel_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER"), # 1685 evt
        }

    addPattuple_44X("v25b", datasets, definitions)

## Add v25c pattuples
def addPattuple_v25c(datasets):
    definitions = {
        "Tau_160431-167913_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_160431_pattuple_v25c-71def38b05f792f2273b1e28fc6e4f12/USER"), # 7650822 evt, 40-80 MB / file
        "Tau_170722-173198_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_170722_pattuple_v25c-1997d8885939481988a1e591798fb84f/USER"), # 914344 evt, 30 MB / file
        "Tau_173236-173692_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_173236_pattuple_v25c-847c5b91b10d6ca1cca97c3366bcb9ca/USER"), # 470476 evt
        "Tau_175832-180252_2011B_Nov19":    TaskDef("/Tau/local-Run2011B_19Nov2011_v1_AOD_175835_pattuple_v25c-ab60dfb18d7993779cd7c862a842fc97/USER"), # 6284525 evt, 30 MB / file

        "TTToHplusBWB_M80_Fall11":          TaskDef("/TTToHplusBWB_M-80_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 18274 evt, 31 MB / file
        "TTToHplusBWB_M90_Fall11":          TaskDef("/TTToHplusBWB_M-90_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 19323 evt, 33 MB / file
        "TTToHplusBWB_M100_Fall11":         TaskDef("/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 20376 evt, 35 MB / file
        "TTToHplusBWB_M120_Fall11":         TaskDef("/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 23189 evt, 39 MB / file
        "TTToHplusBWB_M140_Fall11":         TaskDef("/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 27563 evt, 44 MB / file
        "TTToHplusBWB_M150_Fall11":         TaskDef("/TTToHplusBWB_M-150_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 29846 evt, 47 MB / file
        "TTToHplusBWB_M155_Fall11":         TaskDef("/TTToHplusBWB_M-155_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 31034 evt, 48 MB / file
        "TTToHplusBWB_M160_Fall11":         TaskDef("/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 32151 evt, 50 MB / file

        "TTToHplusBHminusB_M80_Fall11":     TaskDef("/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 23781 evt, 39 MB / file
        "TTToHplusBHminusB_M90_Fall11":     TaskDef("/TTToHplusBHminusB_M-90_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"),
        "TTToHplusBHminusB_M100_Fall11":    TaskDef("/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"),
        "TTToHplusBHminusB_M120_Fall11":    TaskDef("/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"),
        "TTToHplusBHminusB_M140_Fall11":    TaskDef("/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"),
        "TTToHplusBHminusB_M150_Fall11":    TaskDef("/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"),
        "TTToHplusBHminusB_M155_Fall11":    TaskDef("/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"),
        "TTToHplusBHminusB_M160_Fall11":    TaskDef("/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"),

#        "HplusTB_M180_Fall11":              TaskDef(""), # FIXME: not at T2
        "HplusTB_M190_Fall11":              TaskDef("/HplusTB_M-190_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 45737 evt, 67 MB / file
        "HplusTB_M200_Fall11":              TaskDef("/HplusTB_M-200_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"),
        "HplusTB_M220_Fall11":              TaskDef("/HplusTB_M-220_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"),
        "HplusTB_M250_Fall11":              TaskDef("/HplusTB_M-250_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"),
#        "HplusTB_M300_Fall11":              TaskDef(""), # FIXME: not at T2

        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDef("/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 32 evt
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDef("/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 677 evt
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDef("/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 6152 evt
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDef("/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 26243 evt
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDef("/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 83237 evt
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDef("/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 186974 evt (missing few jobs)

        "WW_TuneZ2_Fall11":                 TaskDef("/WW_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 77684 evt
        "WZ_TuneZ2_Fall11":                 TaskDef("/WZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 67793
        "ZZ_TuneZ2_Fall11":                 TaskDef("/ZZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 57239
        "TTJets_TuneZ2_Fall11":             TaskDef("/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 3327519 evt
        "WJets_TuneZ2_Fall11":              TaskDef("/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 299195
        "W2Jets_TuneZ2_Fall11":             TaskDef("/W2Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 404002
        "W3Jets_TuneZ2_Fall11":             TaskDef("/W3Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 221655
        "W4Jets_TuneZ2_Fall11":             TaskDef("/W4Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 604144
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDef("/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 71235 evt
        "T_t-channel_TuneZ2_Fall11":        TaskDef("/T_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 61815 evt
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDef("/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 29028 evt
        "T_tW-channel_TuneZ2_Fall11":       TaskDef("/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 41707 evt
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDef("/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 41142 evt
        "T_s-channel_TuneZ2_Fall11":        TaskDef("/T_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 4241
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDef("/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v25c-792142e4d0984f6b86a1b0c2d38da119/USER"), # 1986 evt
        }

    addPattuple_44X("v25c", datasets, definitions)

## Add v44_4 pattuple production workflows, no output yet
def addPattuple_v44_4(datasets):
    definitions = {
        "Tau_160431-167913_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_160431_pattuple_v44_4-22fa40c1fbac4684dd3ccb0e713bd4b5/USER"), # 7694502 evt, 40-80 MB / file
        "Tau_170722-173198_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_170722_pattuple_v44_4-9ec211af2ee07b45d4ecbc81a3a92e63/USER"), # 914344 evt, 30 MB / file
        "Tau_173236-173692_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_173236_pattuple_v44_4-525b16261b70f8b500033d7d0afaba83/USER"), # 470476 evt
        "Tau_175832-180252_2011B_Nov19":    TaskDef("/Tau/local-Run2011B_19Nov2011_v1_AOD_175860_pattuple_v44_4-af466d5c64c42a78ca457d4da73a4b82/USER"), # 6298060 evt, 30 MB / file

        "TTToHplusBWB_M80_Fall11":          TaskDef("/TTToHplusBWB_M-80_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBWB_M90_Fall11":          TaskDef("/TTToHplusBWB_M-90_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBWB_M100_Fall11":         TaskDef("/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBWB_M120_Fall11":         TaskDef("/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBWB_M140_Fall11":         TaskDef("/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBWB_M150_Fall11":         TaskDef("/TTToHplusBWB_M-150_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBWB_M155_Fall11":         TaskDef("/TTToHplusBWB_M-155_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER"),
        "TTToHplusBWB_M160_Fall11":         TaskDef("/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),

        "TTToHplusBHminusB_M80_Fall11":     TaskDef("/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M90_Fall11":     TaskDef("/TTToHplusBHminusB_M-90_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M100_Fall11":    TaskDef("/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M120_Fall11":    TaskDef("/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M140_Fall11":    TaskDef("/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M150_Fall11":    TaskDef("/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M155_Fall11":    TaskDef("/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER"),
        "TTToHplusBHminusB_M160_Fall11":    TaskDef("/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),

        "HplusTB_M180_Fall11":              TaskDef("/HplusTB_M-180_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER"),
        "HplusTB_M190_Fall11":              TaskDef("/HplusTB_M-190_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER"),
        "HplusTB_M200_Fall11":              TaskDef("/HplusTB_M-200_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER"),
        "HplusTB_M220_Fall11":              TaskDef("/HplusTB_M-220_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER"),
        "HplusTB_M250_Fall11":              TaskDef("/HplusTB_M-250_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER"),
        "HplusTB_M300_Fall11":              TaskDef("/HplusTB_M-300_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER"),

        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDef("/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDef("/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDef("/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDef("/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDef("/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDef("/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),

        "WW_TuneZ2_Fall11":                 TaskDef("/WW_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "WZ_TuneZ2_Fall11":                 TaskDef("/WZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "ZZ_TuneZ2_Fall11":                 TaskDef("/ZZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "TTJets_TuneZ2_Fall11":             TaskDef("/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "WJets_TuneZ2_Fall11":              TaskDef("/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "W2Jets_TuneZ2_Fall11":             TaskDef("/W2Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "W3Jets_TuneZ2_Fall11":             TaskDef("/W3Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "W4Jets_TuneZ2_Fall11":             TaskDef("/W4Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDef("/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "T_t-channel_TuneZ2_Fall11":        TaskDef("/T_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDef("/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "T_tW-channel_TuneZ2_Fall11":       TaskDef("/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDef("/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "T_s-channel_TuneZ2_Fall11":        TaskDef("/T_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDef("/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),
    }
    addPattuple_44X("v44_4", datasets, definitions)

# Skeleton
def addPattuple_vNEXT_SKELETON_44X(datasets):
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
        "W2Jets_TuneZ2_Fall11":             TaskDef(""),
        "W3Jets_TuneZ2_Fall11":             TaskDef(""),
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

def addPattuple_v53_1_test1(datasets):
    definitions = {
        "Tau_190456-190738_2012A_Jul13":          TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_pattuple_v53_1_190456_190738_test1-00fb6a0648e9082988536b8287ce18fd/USER", njobsOut=1),

        "MultiJet_190456-190738_2012A_Jul13":     TaskDef("/MultiJet/local-Run2012A_13Jul2012_v1_AOD_pattuple_v53_1_190456_190738_test1-8d229f863f3fc8a5a50f8b702ec0e1b3/USER", njobsOut=1),

        "TTToHplusBWB_M120_Summer12":             TaskDef("/TTToHplusBWB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1_test1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=50, njobsOut=1),

        "TTJets_TuneZ2star_Summer12":             TaskDef("/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1_test1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=490, njobsOut=1),
        "WJets_TuneZ2star_v1_Summer12":           TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1_test1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=200, njobsOut=1),
        "WJets_TuneZ2star_v2_Summer12":           TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1_test1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=490, njobsOut=1),
        "W1Jets_TuneZ2star_Summer12":             TaskDef("/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1_test1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=300, njobsOut=1),
        "W2Jets_TuneZ2star_Summer12":             TaskDef("/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1_test1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsOut=1),
        "W3Jets_TuneZ2star_Summer12":             TaskDef("/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1_test1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsOut=1),
        "W4Jets_TuneZ2star_Summer12":             TaskDef("/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1_test1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=490, njobsOut=1),
        }

    addPattuple_53X("v53_1_test1", datasets, definitions)

def addPattuple_v53_1(datasets):
    definitions = {
        "Tau_190456-190738_2012A_Jul13":          TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_190456_190738_pattuple_v53_1-00fb6a0648e9082988536b8287ce18fd/USER", njobsIn=150), # 64775 events, Mean 33.7 MB, min 4.7 MB, max 66.5 MB
        "Tau_190782-190949_2012A_Aug06":          TaskDef("/Tau/local-Run2012A_recover_06Aug2012_v1_AOD_190782_190949_pattuple_v53_1-1be0c628538f5a4dae541da3c11eb60c/USER", njobsIn=30), # 42028 events, Mean 85.4 MB, min 37.3 MB, max 120.4 MB
        "Tau_191043-193621_2012A_Jul13":          TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_191043_193621_pattuple_v53_1-39e2e8832bb5d7b032f2b5c9a80e534a/USER", njobsIn=400), # 368031 events, 55.9 MB, min 20.1 MB, max 114.5 MB
        "Tau_193834-196531_2012B_Jul13":          TaskDef("/Tau/local-Run2012B_13Jul2012_v1_AOD_193834_196531_pattuple_v53_1-382e6b84ca489c093c178cfb50ba5dbe/USER"), # 2822552 events, 71.0 MB, min 30.0 MB, max 200.5 MB
        "Tau_198022-198523_2012C_Aug24":          TaskDef("/Tau/local-Run2012C_24Aug2012_v1_AOD_198022_198523_pattuple_v53_1-03816abcf2df69d2a2f275b0cfc9c090/USER"), # 258977 events, 65.6 MB, min 33.8 MB, max 145.2 MB
        "Tau_198941-200601_2012C_Prompt":         TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_198941_200601_pattuple_v53_1-cdc21ac5d95fea9b64545e44f8ba4b15/USER"), # 1705781 events, 60.2 MB, min 12.2 MB, max 143.2 MB
        "Tau_200961-202504_2012C_Prompt":         TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_200961_202504_pattuple_v53_1-97851bbbf7291004b296c48e58143d74/USER"), # 1792819 events, Mean 67.8 MB, min 4.1 MB, max 292.2 MB
        "Tau_202792-203742_2012C_Prompt":         TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_202792_203742_pattuple_v53_1-a6a087b1796a2a131884baa5c492e72f/USER"), # 175227 events, 64.9 MB, min 20.3 MB, max 161.9 MB

        "MultiJet_190456-190738_2012A_Jul13":     TaskDef("/MultiJet/local-Run2012A_13Jul2012_v1_AOD_190456_190738_pattuple_v53_1-8d229f863f3fc8a5a50f8b702ec0e1b3/USER"), # 466504 events, Mean 77.8 MB, min 4.3 MB, max 165.5 MB
        "MultiJet_190782-190949_2012A_Aug06":     TaskDef("/MultiJet/local-Run2012A_recover_06Aug2012_v1_AOD_190782_190949_pattuple_v53_1-fdd3c1f4d60921e4522b1cd7c85b5f38/USER"), # 313212 events, Mean 176.9 MB, min 23.1 MB, max 245.6 MB
        "MultiJet_191043-193621_2012A_Jul13":     TaskDef("/MultiJet/local-Run2012A_13Jul2012_v1_AOD_191043_193621_pattuple_v53_1c-e7b040c48519314dbf67cfc22f9c91f7/USER"), # 2954598 events, Mean 144.6 MB, min 1.6 MB, max 309.0 MB
        "MultiJet_193834-194225_2012B_Jul13":     TaskDef("/MultiJet/local-Run2012B_13Jul2012_v1_AOD_193834_194225_pattuple_v53_1-7cb2cf938b8a39c78ce811004f4e1701/USER"), # 830720 events, Mean 115.3 MB, min 19.4 MB, max 189.1 MB
        "MultiJet_194270-196531_2012B_Jul13":     TaskDef("/MultiJet/local-Run2012B_13Jul2012_v1_AOD_194270_196531_pattuple_v53_1b-13eab0232030eb0def83f54eafd8085d/USER"), # 5766837 events, Mean 156.7 MB, min 19.7 MB, max 283.0 MB
        "MultiJet_198022-198523_2012C_Aug24":     TaskDef("/MultiJet/local-Run2012C_24Aug2012_v1_AOD_198022_198523_pattuple_v53_1-88f58a18bc4cc32ca93270fe01187879/USER"), # 715141 events, Mean 159.7 MB, min 67.0 MB, max 285.3 MB
        "MultiJet_198941-200601_2012C_Prompt":    TaskDef("/MultiJet/local-Run2012C_PromptReco_v2_AOD_198941_200601_pattuple_v53_1b-8bbd8eb7290730a495ba05939e654f51/USER"), # 4715708 events, Mean 152.5 MB, min 1.5 MB, max 291.0 MB
        "MultiJet_200961-202504_2012C_Prompt":    TaskDef("/MultiJet/local-Run2012C_PromptReco_v2_AOD_200961_202504_pattuple_v53_1-87325f0f572c545baf7123d89881d242/USER"), # 4365595 events, Mean 156.3 MB, min 1.7 MB, max 299.6 MB
        "MultiJet_202792-203742_2012C_Prompt":    TaskDef("/MultiJet/local-Run2012C_PromptReco_v2_AOD_202792_203742_pattuple_v53_1-87325f0f572c545baf7123d89881d242/USER"), # 433952 events, Mean 149.4 MB, min 43.7 MB, max 265.8 MB

        # 27900-37203 events, max 
        "TTToHplusBWB_M80_Summer12":              TaskDef("/TTToHplusBWB_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),  # Mean 81.3 MB, min 3.5 MB, max 89.0 MB
        "TTToHplusBWB_M90_Summer12":              TaskDef("/TTToHplusBWB_M-90_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),  # Mean 85.3 MB, min 35.2 MB, max 93.6 MB
        "TTToHplusBWB_M100_Summer12":             TaskDef("/TTToHplusBWB_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 74.6 MB, min 1.6 MB, max 81.0 MB
        "TTToHplusBWB_M120_Summer12":             TaskDef("/TTToHplusBWB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 84.0 MB, min 3.0 MB, max 91.1 MB
        "TTToHplusBWB_M140_Summer12":             TaskDef("/TTToHplusBWB_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 86.7 MB, min 42.5 MB, max 93.5 MB
        "TTToHplusBWB_M150_Summer12":             TaskDef("/TTToHplusBWB_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 86.3 MB, min 46.7 MB, max 96.2 MB
        "TTToHplusBWB_M155_Summer12":             TaskDef("/TTToHplusBWB_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 89.7 MB, min 29.9 MB, max 100.3 MB
        "TTToHplusBWB_M160_Summer12":             TaskDef("/TTToHplusBWB_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 91.1 MB, min 12.2 MB, max 101.4 MB

        # 29908-40068 events
        "TTToHplusBHminusB_M80_Summer12":         TaskDef("/TTToHplusBHminusB_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),  # Mean 78.1 MB, min 74.8 MB, max 83.1 MB
#        "TTToHplusBHminusB_M90_Summer12":         TaskDef(""),
        "TTToHplusBHminusB_M100_Summer12":        TaskDef("/TTToHplusBHminusB_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 78.3 MB, min 72.4 MB, max 84.2 MB
        "TTToHplusBHminusB_M120_Summer12":        TaskDef("/TTToHplusBHminusB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 78.5 MB, min 13.0 MB, max 85.6 MB
        "TTToHplusBHminusB_M140_Summer12":        TaskDef("/TTToHplusBHminusB_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 82.8 MB, min 78.8 MB, max 87.2 M
        "TTToHplusBHminusB_M150_Summer12":        TaskDef("/TTToHplusBHminusB_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 82.8 MB, min 23.4 MB, max 89.4 MB
        "TTToHplusBHminusB_M155_Summer12":        TaskDef("/TTToHplusBHminusB_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 86.4 MB, min 79.7 MB, max 91.6 MB
        "TTToHplusBHminusB_M160_Summer12":        TaskDef("/TTToHplusBHminusB_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 88.0 MB, min 83.2 MB, max 93.5 MB

        # 10275-17098 events
        "Hplus_taunu_s-channel_M80_Summer12":     TaskDef("/Hplus_taunu_s-channel_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),  # Mean 28.6 MB, min 1.6 MB, max 33.9 MB
        "Hplus_taunu_s-channel_M90_Summer12":     TaskDef("/Hplus_taunu_s-channel_M-90_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),  # Mean 28.0 MB, min 1.6 MB, max 31.6 MB
        "Hplus_taunu_s-channel_M100_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 31.7 MB, min 2.8 MB, max 36.1 MB
        "Hplus_taunu_s-channel_M120_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 29.7 MB, min 2.8 MB, max 35.7 MB
        "Hplus_taunu_s-channel_M140_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 39.9 MB, min 36.1 MB, max 43.4 MB
        "Hplus_taunu_s-channel_M150_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 41.5 MB, min 2.6 MB, max 45.4 MB
        "Hplus_taunu_s-channel_M155_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 40.5 MB, min 2.8 MB, max 45.6 MB
        "Hplus_taunu_s-channel_M160_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), # Mean 46.9 MB, min 42.2 MB, max 50.2 MB

        # 53759-78988 events
        "HplusTB_M180_Summer12":                  TaskDef("/HplusTB_M-180_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # Mean 137.2 MB, min 129.2 MB, max 144.0 MB
        "HplusTB_M190_Summer12":                  TaskDef("/HplusTB_M-190_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # Mean 142.4 MB, min 135.9 MB, max 148.7 MB
        "HplusTB_M200_Summer12":                  TaskDef("/HplusTB_M-200_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # Mean 138.3 MB, min 17.6 MB, max 153.8 MB
        "HplusTB_M220_Summer12":                  TaskDef("/HplusTB_M-220_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # Mean 159.4 MB, min 149.1 MB, max 167.2 MB
        "HplusTB_M250_Summer12":                  TaskDef("/HplusTB_M-250_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # Mean 173.9 MB, min 166.4 MB, max 180.4 MB
        "HplusTB_M300_Summer12":                  TaskDef("/HplusTB_M-300_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # Mean 196.9 MB, min 189.9 MB, max 202.8 MB

        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDef("/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 114 events, Mean 6.0 MB, min 1.7 MB, max 7.2 MB
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDef("/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 2749 events, Mean 19.2 MB, min 4.7 MB, max 22.1 MB
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDef("/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 21951 events, Mean 104.5 MB, min 32.8 MB, max 115.7 MB
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDef("/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 75972 events, Mean 178.4 MB, min 105.1 MB, max 190.5 MB
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 232796 events, Mean 280.1 MB, min 15.0 MB, max 298.4 MB
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 797355 events, Mean 258.6 MB, min 27.0 MB, max 276.6 MB
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1b-cad8d1056ca20d363262a3efa1d97a74/USER"), # 616204 events, Mean 258.3 MB, min 85.4 MB, max 272.3 MB
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 359260 events, Mean 250.5 MB, min 58.2 MB, max 265.4 MB
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v3/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 2045846 events, Mean 252.4 MB, min 19.4 MB, max 269.9 MB

        "WW_TuneZ2star_Summer12":                 TaskDef("/WW_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 288671 events, Mean 161.0 MB, min 5.9 MB, max 171.0 MB
        "WZ_TuneZ2star_Summer12":                 TaskDef("/WZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 256016 events, Mean 146.5 MB, min 11.6 MB, max 157.1 MB
        "ZZ_TuneZ2star_Summer12":                 TaskDef("/ZZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 201924 events, Mean 117.8 MB, min 4.6 MB, max 133.3 MB
        "TTJets_TuneZ2star_Summer12":             TaskDef("/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 1202301 events, Mean 184.2 MB, min 8.8 MB, max 199.8 MB
        "WJets_TuneZ2star_v1_Summer12":           TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 94009 events, Mean 81.3 MB, min 32.6 MB, max 88.8 MB
        "WJets_TuneZ2star_v2_Summer12":           TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 285149 events, Mean 99.3 MB, min 6.2 MB, max 110.6 MB
        "W1Jets_TuneZ2star_Summer12":             TaskDef("/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 203841 events, Mean 107.9 MB, min 5.8 MB, max 117.0 MB
        "W2Jets_TuneZ2star_Summer12":             TaskDef("/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 752423 events, Mean 153.1 MB, min 7.2 MB, max 168.7 MB
        "W3Jets_TuneZ2star_Summer12":             TaskDef("/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 616480 events, Mean 114.8 MB, min 6.9 MB, max 125.0 MB
        "W4Jets_TuneZ2star_Summer12":             TaskDef("/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 1002056 events, Mean 178.0 MB, min 76.2 MB, max 194.2 MB
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDef("/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 180247 events, Mean 52.3 MB, min 8.6 MB, max 59.7 MB
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDef("/DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1b-cad8d1056ca20d363262a3efa1d97a74/USER"), # 4476 events, Mean 21.3 MB, min 1.7 MB, max 29.6 MB
        "T_t-channel_TuneZ2star_Summer12":        TaskDef("/T_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 222877, Mean 395.6 MB, min 161.4 MB, max 414.6 MB
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDef("/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 27667, Mean 191.4 MB, min 1.6 MB, max 206.7 MB
        "T_tW-channel_TuneZ2star_Summer12":       TaskDef("/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 61356 events, Mean 285.5 MB, min 2.8 MB, max 311.0 MB
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDef("/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 60272 events, Mean 268.7 MB, min 12.9 MB, max 303.4 MB
        "T_s-channel_TuneZ2star_Summer12":        TaskDef("/T_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 11203 events, Mean 102.3 MB, min 1.6 MB, max 115.7 MB
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDef("/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), # 5345 events, Mean 52.0 MB, min 1.6 MB, max 59.9 MB
        }

    addPattuple_53X("v53_1", datasets, definitions)


def addPattuple_v53_1_1(datasets):
    # Same as v53_1, but with CMSSW_5_3_6_patch1
    definitionsAlsoInV53_1 = {
        # For testing only
        "TTToHplusBWB_M120_Summer12":             TaskDef(""),
        }
    definitionsOnlyInV53_1_1 = {
        "TTToHplusBWB_M80_ext_Summer12":          TaskDef(""),
        "TTToHplusBWB_M90_ext_Summer12":          TaskDef(""),
        "TTToHplusBWB_M100_ext_Summer12":         TaskDef(""),
        "TTToHplusBWB_M120_ext_Summer12":         TaskDef(""),
#        "TTToHplusBWB_M140_ext_Summer12":         TaskDef(""),
        "TTToHplusBWB_M150_ext_Summer12":         TaskDef(""),
        "TTToHplusBWB_M155_ext_Summer12":         TaskDef(""),
        "TTToHplusBWB_M160_ext_Summer12":         TaskDef(""),

        "TTToHplusBHminusB_M80_ext_Summer12":     TaskDef(""),
#        "TTToHplusBHminusB_M90_ext_Summer12":     TaskDef(""),
        "TTToHplusBHminusB_M100_ext_Summer12":    TaskDef(""),
        "TTToHplusBHminusB_M120_ext_Summer12":    TaskDef(""),
        "TTToHplusBHminusB_M140_ext_Summer12":    TaskDef(""),
        "TTToHplusBHminusB_M150_ext_Summer12":    TaskDef(""),
        "TTToHplusBHminusB_M155_ext_Summer12":    TaskDef(""),
        "TTToHplusBHminusB_M160_ext_Summer12":    TaskDef(""),

        "Hplus_taunu_t-channel_M80_Summer12":     TaskDef(""),
        "Hplus_taunu_t-channel_M90_Summer12":     TaskDef(""),
        "Hplus_taunu_t-channel_M100_Summer12":    TaskDef(""),
        "Hplus_taunu_t-channel_M120_Summer12":    TaskDef(""),
        "Hplus_taunu_t-channel_M140_Summer12":    TaskDef(""),
        "Hplus_taunu_t-channel_M150_Summer12":    TaskDef(""),
        "Hplus_taunu_t-channel_M155_Summer12":    TaskDef(""),
        "Hplus_taunu_t-channel_M160_Summer12":    TaskDef(""),

        "Hplus_taunu_tW-channel_M80_Summer12":    TaskDef(""),
        "Hplus_taunu_tW-channel_M90_Summer12":    TaskDef(""),
        "Hplus_taunu_tW-channel_M100_Summer12":   TaskDef(""),
        "Hplus_taunu_tW-channel_M120_Summer12":   TaskDef(""),
        "Hplus_taunu_tW-channel_M140_Summer12":   TaskDef(""),
        "Hplus_taunu_tW-channel_M150_Summer12":   TaskDef(""),
        "Hplus_taunu_tW-channel_M155_Summer12":   TaskDef(""),
        "Hplus_taunu_tW-channel_M160_Summer12":   TaskDef(""),

        "HplusTB_M400_Summer12":                  TaskDef(""),
#        "HplusTB_M500_Summer12":                  TaskDef(""),
        "HplusTB_M600_Summer12":                  TaskDef(""),

        "HplusTB_M180_ext_Summer12":              TaskDef(""),
        "HplusTB_M190_ext_Summer12":              TaskDef(""),
        "HplusTB_M200_ext_Summer12":              TaskDef(""),
        "HplusTB_M220_ext_Summer12":              TaskDef(""),
#        "HplusTB_M250_ext_Summer12":              TaskDef(""),
        "HplusTB_M300_ext_Summer12":              TaskDef(""),
        }
    definitions = {}
    definitions.update(definitionsAlsoInV53_1)
    definitions.update(definitionsOnlyInV53_1_1)

    addPattuple_53X("v53_1_1", datasets, definitions)

        

# Skeleton
def addPattuple_vNEXT_SKELETON_53X(datasets):
    definitions = {
        "Tau_190456-190738_2012A_Jul13":          TaskDef(""),
        "Tau_190782-190949_2012A_Aug06":          TaskDef(""),
        "Tau_191043-193621_2012A_Jul13":          TaskDef(""),
        "Tau_193834-196531_2012B_Jul13":          TaskDef(""),
        "Tau_198022-198523_2012C_Aug24":          TaskDef(""),
        "Tau_198941-200601_2012C_Prompt":         TaskDef(""),
        "Tau_200961-202504_2012C_Prompt":         TaskDef(""),
        "Tau_202792-203742_2012C_Prompt":         TaskDef(""),

        "MultiJet_190456-190738_2012A_Jul13":     TaskDef(""),
        "MultiJet_190782-190949_2012A_Aug06":     TaskDef(""),
        "MultiJet_191043-193621_2012A_Jul13":     TaskDef(""),
        "MultiJet_193834-194225_2012B_Jul13":     TaskDef(""),
        "MultiJet_194270-196531_2012B_Jul13":     TaskDef(""),
        "MultiJet_198022-198523_2012C_Aug24":     TaskDef(""),
        "MultiJet_198941-200601_2012C_Prompt":    TaskDef(""),
        "MultiJet_200961-202504_2012C_Prompt":    TaskDef(""),
        "MultiJet_202792-203742_2012C_Prompt":    TaskDef(""),

        "TTToHplusBWB_M80_Summer12":              TaskDef(""),
        "TTToHplusBWB_M90_Summer12":              TaskDef(""),
        "TTToHplusBWB_M100_Summer12":             TaskDef(""),
        "TTToHplusBWB_M120_Summer12":             TaskDef(""),
        "TTToHplusBWB_M140_Summer12":             TaskDef(""),
        "TTToHplusBWB_M150_Summer12":             TaskDef(""),
        "TTToHplusBWB_M155_Summer12":             TaskDef(""),
        "TTToHplusBWB_M160_Summer12":             TaskDef(""),

        "TTToHplusBWB_M80_ext_Summer12":          TaskDef(""),
        "TTToHplusBWB_M90_ext_Summer12":          TaskDef(""),
        "TTToHplusBWB_M100_ext_Summer12":         TaskDef(""),
        "TTToHplusBWB_M120_ext_Summer12":         TaskDef(""),
        "TTToHplusBWB_M140_ext_Summer12":         TaskDef(""),
        "TTToHplusBWB_M150_ext_Summer12":         TaskDef(""),
        "TTToHplusBWB_M155_ext_Summer12":         TaskDef(""),
        "TTToHplusBWB_M160_ext_Summer12":         TaskDef(""),

        "TTToHplusBHminusB_M80_Summer12":         TaskDef(""),
        "TTToHplusBHminusB_M90_Summer12":         TaskDef(""),
        "TTToHplusBHminusB_M100_Summer12":        TaskDef(""),
        "TTToHplusBHminusB_M120_Summer12":        TaskDef(""),
        "TTToHplusBHminusB_M140_Summer12":        TaskDef(""),
        "TTToHplusBHminusB_M150_Summer12":        TaskDef(""),
        "TTToHplusBHminusB_M155_Summer12":        TaskDef(""),
        "TTToHplusBHminusB_M160_Summer12":        TaskDef(""),

        "TTToHplusBHminusB_M80_ext_Summer12":     TaskDef(""),
        "TTToHplusBHminusB_M90_ext_Summer12":     TaskDef(""),
        "TTToHplusBHminusB_M100_ext_Summer12":    TaskDef(""),
        "TTToHplusBHminusB_M120_ext_Summer12":    TaskDef(""),
        "TTToHplusBHminusB_M140_ext_Summer12":    TaskDef(""),
        "TTToHplusBHminusB_M150_ext_Summer12":    TaskDef(""),
        "TTToHplusBHminusB_M155_ext_Summer12":    TaskDef(""),
        "TTToHplusBHminusB_M160_ext_Summer12":    TaskDef(""),

        "Hplus_taunu_t-channel_M80_Summer12":     TaskDef(""),
        "Hplus_taunu_t-channel_M90_Summer12":     TaskDef(""),
        "Hplus_taunu_t-channel_M100_Summer12":    TaskDef(""),
        "Hplus_taunu_t-channel_M120_Summer12":    TaskDef(""),
        "Hplus_taunu_t-channel_M140_Summer12":    TaskDef(""),
        "Hplus_taunu_t-channel_M150_Summer12":    TaskDef(""),
        "Hplus_taunu_t-channel_M155_Summer12":    TaskDef(""),
        "Hplus_taunu_t-channel_M160_Summer12":    TaskDef(""),

        "Hplus_taunu_tW-channel_M80_Summer12":    TaskDef(""),
        "Hplus_taunu_tW-channel_M90_Summer12":    TaskDef(""),
        "Hplus_taunu_tW-channel_M100_Summer12":   TaskDef(""),
        "Hplus_taunu_tW-channel_M120_Summer12":   TaskDef(""),
        "Hplus_taunu_tW-channel_M140_Summer12":   TaskDef(""),
        "Hplus_taunu_tW-channel_M150_Summer12":   TaskDef(""),
        "Hplus_taunu_tW-channel_M155_Summer12":   TaskDef(""),
        "Hplus_taunu_tW-channel_M160_Summer12":   TaskDef(""),

        "Hplus_taunu_s-channel_M80_Summer12":     TaskDef(""),
        "Hplus_taunu_s-channel_M90_Summer12":     TaskDef(""),
        "Hplus_taunu_s-channel_M100_Summer12":    TaskDef(""),
        "Hplus_taunu_s-channel_M120_Summer12":    TaskDef(""),
        "Hplus_taunu_s-channel_M140_Summer12":    TaskDef(""),
        "Hplus_taunu_s-channel_M150_Summer12":    TaskDef(""),
        "Hplus_taunu_s-channel_M155_Summer12":    TaskDef(""),
        "Hplus_taunu_s-channel_M160_Summer12":    TaskDef(""),

        "HplusTB_M180_Summer12":                  TaskDef(""),
        "HplusTB_M190_Summer12":                  TaskDef(""),
        "HplusTB_M200_Summer12":                  TaskDef(""),
        "HplusTB_M220_Summer12":                  TaskDef(""),
        "HplusTB_M250_Summer12":                  TaskDef(""),
        "HplusTB_M300_Summer12":                  TaskDef(""),
        "HplusTB_M400_Summer12":                  TaskDef(""),
        "HplusTB_M500_Summer12":                  TaskDef(""),
        "HplusTB_M600_Summer12":                  TaskDef(""),

        "HplusTB_M180_ext_Summer12":              TaskDef(""),
        "HplusTB_M190_ext_Summer12":              TaskDef(""),
        "HplusTB_M200_ext_Summer12":              TaskDef(""),
        "HplusTB_M220_ext_Summer12":              TaskDef(""),
        "HplusTB_M250_ext_Summer12":              TaskDef(""),
        "HplusTB_M300_ext_Summer12":              TaskDef(""),

        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDef(""),
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDef(""),
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDef(""),
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDef(""),
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDef(""),
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDef(""),
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDef(""),
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDef(""),
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDef(""),

        "WW_TuneZ2star_Summer12":                 TaskDef(""),
        "WZ_TuneZ2star_Summer12":                 TaskDef(""),
        "ZZ_TuneZ2star_Summer12":                 TaskDef(""),
        "TTJets_TuneZ2star_Summer12":             TaskDef(""),
        "WJets_TuneZ2star_v1_Summer12":           TaskDef(""),
        "WJets_TuneZ2star_v2_Summer12":           TaskDef(""),
        "W1Jets_TuneZ2star_Summer12":             TaskDef(""),
        "W2Jets_TuneZ2star_Summer12":             TaskDef(""),
        "W3Jets_TuneZ2star_Summer12":             TaskDef(""),
        "W4Jets_TuneZ2star_Summer12":             TaskDef(""),
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDef(""),
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDef(""),
        "T_t-channel_TuneZ2star_Summer12":        TaskDef(""),
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDef(""),
        "T_tW-channel_TuneZ2star_Summer12":       TaskDef(""),
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDef(""),
        "T_s-channel_TuneZ2star_Summer12":        TaskDef(""),
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDef(""),
        }

    #addPattuple_53X("VERSION", datasets, definitions)
