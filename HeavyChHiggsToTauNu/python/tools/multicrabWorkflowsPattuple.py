## \package multicrabDatasetsPatTuple
# Functions for pattuple definitions

import re

from multicrabWorkflowsTools import Dataset, Workflow, WorkflowAlias, Data, Source, updatePublishName, TaskDef, updateTaskDefinitions, Disable
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
    if taskDef.triggerOR is not None and len(taskDef.triggerOR) > 1 and taskDef.triggerThrow != None and taskDef.triggerThrow == False:
        args["triggerThrow"] = 0
    if dataset.isMC() and taskDef.triggerOR is not None and len(taskDef.triggerOR) > 0:
        args["triggerMC"] = 1
    if taskDef.args != None:
        args.update(taskDef.args)

    wf = Workflow(workflowName, source=source, triggerOR=taskDef.triggerOR, args=args, output=output, **kwargs)
    if taskDef.crabLines != None:
        for line in taskDef.crabLines:
            wf.addCrabLine(line)
    return wf

def constructProcessingWorkflow_44X(dataset, taskDef, sourceWorkflow, workflowName, inputLumiMaskData="DCSONLY11", outputLumiMaskData="Nov08ReReco", **kwargs):
    # Setup input/default output lumimasks for data
    inputLumiMask = None
    outputLumiMask = None
    if dataset.isData():
        inputLumiMask = inputLumiMaskData
        outputLumiMask = outputLumiMaskData

    return _constructProcessingWorkflow_common(dataset, taskDef, sourceWorkflow, workflowName, inputLumiMask, outputLumiMask, **kwargs)

## Construct processing workflow task for a dataset 53X release
#
# \param dataset            multicrabWorkflowsTools.Dataset object
# \param taskDef            multicrabWorkflowsTools.TaskDef object, contains the task definition
# \param sourceWorkflow     String for source workflow name (i.e. input workflow)
# \param workflowName       String for the name of this workflow
# \param inputLumiMaskData  LumiMask name to be used when processing
#                           the input (allowed values are in
#                           certifiedLumi)
# \param outputLumiMaskData LumiMask name to be used by default by
#                           tasks processing the output of this
#                           workflow as an input. If None, value is
#                           deduced from the last part of the dataset
#                           name (e.g. _Jul13). To disable the
#                           outputLumiMask, give
#                           multicrabWorkflowTools.Disable object.
# \param kwargs             Keyword arguments, forwarded to _constructProcessingWorkflow_common()
def constructProcessingWorkflow_53X(dataset, taskDef, sourceWorkflow, workflowName, inputLumiMaskData="DCSONLY12", outputLumiMaskData=None, **kwargs):
    # Setup input/default output lumimasks for data
    inputLumiMask = None
    outputLumiMask = None
    if dataset.isData():
        inputLumiMask = inputLumiMaskData
        outputLumiMask = outputLumiMaskData
        if outputLumiMask is None:
            reco = dataset.getName().split("_")[-1]
            try:
                outputLumiMask = {
                    "Jul13": "13Jul2012ReReco",
                    "Aug06": "06Aug2012ReReco",
                    "Aug24": "24Aug2012ReReco",
                    "Dec11": "11Dec2012ReReco",
                    "Prompt": "PromptReco12"
                    }[reco]
            except KeyError:
                raise Exception("No output lumi mask defined for reco '%s' (dataset %s). Define one in python/tools/certifiedLumi.py, and add a 'link' to a dictionary in here" % (reco, dataset.getName()))

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
        "WJets_TuneZ2_Fall11":              TaskDefMC(njobsIn=490, njobsOut=10, args={"wjetsWeighting": 1, "wjetBin": -1}), # file size 16000 GB, 4500 files, expected output max. 37 MB/file 
        "W2Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=300, njobsOut=20, args={"wjetsWeighting": 1, "wjetBin": 2}), # expected output max. 38 MB/file, obs 38 MB / file
        "W3Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=120, njobsOut=10, args={"wjetsWeighting": 1, "wjetBin": 3}), # expected output max. 56 MB/file, obs 20-22 MB / file
        "W4Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=200, njobsOut=12, args={"wjetsWeighting": 1, "wjetBin": 4}), # expected output max. 144 MB/file, obs 20-22 MB / file
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
def addPattuple_53X(version, datasets, updateDefinitions, skim=None,
                    tauTriggers=None, quadPFJetBTagTriggers=None, quadJetBTagTriggers=None, quadJetTriggers=None):
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
    # BJetPlusX Jul13 HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v4: 1275/5000 = 0.25500
    #                 HLT_QuadJet75_55_38_20_BTagIP_VBF_v3: 858/5000 = 0.17160
    #                 OR:  1738/5000 = 0.35660

    if tauTriggers is None:
        tauTriggers = {
            "Tau_190456-190738_2012A_Jul13": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v2"],
            "Tau_190782-190949_2012A_Aug06": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v3"],
            "Tau_191043-193621_2012A_Jul13": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v3", # 191043-191411
                                              "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v4"], # 191691-191491 (193621)
            "Tau_193834-196531_2012B_Jul13": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6"],
            "Tau_198022-198523_2012C_Aug24": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7"],
            "Tau_198941-200601_2012C_Prompt": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7",  # 198941-199608
                                               "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9"],  # 199698-200161
            "Tau_200961-202504_2012C_Prompt": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9"],
            "Tau_202792-203742_2012C_Prompt": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10"],
            "Tau_198941-202504_2012C_Prompt": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7",  # 198941-199608
                                               "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9"], # 199698-202504
            "Tau_201191-201191_2012C_Dec11": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9"],
            "Tau_202972-203742_2012C_Prompt": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10"],
            "Tau_203777-208686_2012D_Prompt": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10"],
        }


    if quadPFJetBTagTriggers is None:
        quadPFJetBTagTriggers = {
            "MultiJet_190456-190738_2012A_Jul13": ["HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v2"],
            "MultiJet_190782-190949_2012A_Aug06": ["HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v3"],
            "MultiJet_191043-193621_2012A_Jul13": ["HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v3",  # 191043-191411
                                                   "HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v4"], # 191691-193621
            "BJetPlusX_193834-194225_2012B_Jul13": ["HLT_QuadPFJet75_55_38_20_BTagCSV_VBF_v4"],
        }
    if quadJetBTagTriggers is None:
        quadJetBTagTriggers = {
            "MultiJet_190456-190738_2012A_Jul13": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v2"],
            "MultiJet_190782-190949_2012A_Aug06": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v3"],
            "MultiJet_191043-193621_2012A_Jul13": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v3"],
            "BJetPlusX_193834-194225_2012B_Jul13": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v3"],
            "BJetPlusX_194270-196531_2012B_Jul13": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v3"],
            "BJetPlusX_198022-198523_2012C_Aug24": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v4"],
            "BJetPlusX_198941-203742_2012C_Prompt": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v4",  # 198941-199608
                                                     "HLT_QuadJet75_55_38_20_BTagIP_VBF_v6"], # 199698-203002
            "BJetPlusX_201191-201191_2012C_Dec11": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v6"],
            "BJetPlusX_203777-208686_2012D_Prompt": ["HLT_QuadJet75_55_38_20_BTagIP_VBF_v6",  # 203777-205238
                                                     "HLT_QuadJet75_55_38_20_BTagIP_VBF_v7"]  # 205303-208686
        }
    if quadJetTriggers is None:
        quadJetTriggers = {
            "MultiJet_190456-190738_2012A_Jul13": ["HLT_QuadJet80_v1"],
            "MultiJet_190782-190949_2012A_Aug06": ["HLT_QuadJet80_v2"],
            "MultiJet_191043-193621_2012A_Jul13": ["HLT_QuadJet80_v2"],
            "MultiJet_193834-194225_2012B_Jul13": ["HLT_QuadJet80_v2"],
            "MultiJet_194270-196531_2012B_Jul13": ["HLT_QuadJet80_v2",  # 194270-196027
                                                   "HLT_QuadJet80_v3"], # 196046-196531
            "MultiJet_198022-198523_2012C_Aug24": ["HLT_QuadJet80_v4"],
            # The following three could be combined to one
            "MultiJet_198941-200601_2012C_Prompt": ["HLT_QuadJet80_v4",  # 198941-199608
                                                    "HLT_QuadJet80_v6"], # 199698-200601
            "MultiJet_200961-202504_2012C_Prompt": ["HLT_QuadJet80_v6"],
            "MultiJet_202792-203742_2012C_Prompt": ["HLT_QuadJet80_v6"],
            # Below is a combination of the three above ones
            "MultiJet_198941-200601_2012C_Prompt": ["HLT_QuadJet80_v4",  # 198941-199608
                                                    "HLT_QuadJet80_v6"], # 199698-203002
            "MultiJet_203777-208686_2012D_Prompt": ["HLT_QuadJet80_v6"],
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
        "Tau_190456-190738_2012A_Jul13":  TaskDef(njobsIn=  35, njobsOut=  1),
        "Tau_190782-190949_2012A_Aug06":  TaskDef(njobsIn=  10, njobsOut=  1),
        "Tau_191043-193621_2012A_Jul13":  TaskDef(njobsIn= 150, njobsOut=  3),
        "Tau_193834-196531_2012B_Jul13":  TaskDef(njobsIn=2000, njobsOut= 20),
        "Tau_198022-198523_2012C_Aug24":  TaskDef(njobsIn= 200, njobsOut=  2),
        # The following three could be combined in the subsequent pattuple processings
        "Tau_198941-200601_2012C_Prompt": TaskDef(njobsIn=1500, njobsOut= 10),
        "Tau_200961-202504_2012C_Prompt": TaskDef(njobsIn=1500, njobsOut= 12),
        "Tau_202792-203742_2012C_Prompt": TaskDef(njobsIn= 150, njobsOut=  1),
        # Below is the combination of the above two, plus the third one with modified first run
        "Tau_198941-202504_2012C_Prompt": TaskDef(njobsIn=3000, njobsOut= 25),# FIXME: set njobsOut
        "Tau_202972-203742_2012C_Prompt": TaskDef(njobsIn= 150, njobsOut=  1),
        "Tau_201191-201191_2012C_Dec11":  TaskDef(njobsIn=  60, njobsOut=  1),
        "Tau_203777-208686_2012D_Prompt": TaskDef(njobsIn=4000, njobsOut= 40), # FIXME: set njobsOut

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
        "MultiJet_200961-202504_2012C_Prompt": TaskDef(njobsIn=1700, njobsOut=30),
        "MultiJet_202792-203742_2012C_Prompt": TaskDef(njobsIn= 170, njobsOut= 3),
        # Below is the combination of the above three
        "MultiJet_198941-203742_2012C_Prompt": TaskDef(njobsIn=3000, njobsOut=80), # FIXME: set njobsOut
        "MultiJet_203777-208686_2012D_Prompt": TaskDef(njobsIn=4000, njobsOut=40), # FIXME: set njobsOut

        ## BJetsPlusX
        # njobsOut is just a guess
        "BJetPlusX_193834-194225_2012B_Jul13":  TaskDef(njobsIn= 600, njobsOut= 6), # FIXME: njobsIn
        "BJetPlusX_194270-196531_2012B_Jul13":  TaskDef(njobsIn=2200, njobsOut=40), # FIXME: njobsIn
        "BJetPlusX_198022-198523_2012C_Aug24":  TaskDef(njobsIn= 250, njobsOut= 5), # FIXME: njobsIn
        "BJetPlusX_198941-203742_2012C_Prompt": TaskDef(njobsIn=3000, njobsOut=80), # FIXME: njobsIn
        "BJetPlusX_201191-201191_2012C_Dec11":  TaskDef(njobsIn=  60, njobsOut= 1), # FIXME: njobsIn
        "BJetPlusX_203777-208686_2012D_Prompt": TaskDef(njobsIn=4000, njobsOut=40), # FIXME: njosnIn, njobsOut

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
        "TTToHplusBHminusB_M90_Summer12":        TaskDefMC(njobsIn=100, njobsOut=1), # FIXME out
        "TTToHplusBHminusB_M100_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M120_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M140_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M150_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M155_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M160_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),

        "TTToHplusBHminusB_M80_ext_Summer12":    TaskDefMC(njobsIn=100, njobsOut=1), # FIXME out
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
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDefMC(njobsIn=250, njobsOut=4),
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDefMC(njobsIn=150, njobsOut=3),
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDefMC(njobsIn=850, njobsOut=14),
                                            
        "WW_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 8),
        "WZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 8),
        "ZZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut= 8),
        "TTJets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=700, njobsOut=30),
        "WJets_TuneZ2star_v1_Summer12":           TaskDefMC(njobsIn=100, njobsOut= 4, args={"wjetsWeighting": 1, "wjetBin": -1}),
        "WJets_TuneZ2star_v2_Summer12":           TaskDefMC(njobsIn=250, njobsOut= 8, args={"wjetsWeighting": 1, "wjetBin": -1}),
        "W1Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=150, njobsOut= 8, args={"wjetsWeighting": 1, "wjetBin": 1}),
        "W2Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=400, njobsOut=20, args={"wjetsWeighting": 1, "wjetBin": 2}),
        "W3Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=490, njobsOut=20, args={"wjetsWeighting": 1, "wjetBin": 3}),
        "W4Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=550, njobsOut=30, args={"wjetsWeighting": 1, "wjetBin": 4}),
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDefMC(njobsIn=350, njobsOut= 6),
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDefMC(njobsIn= 40, njobsOut= 1),
        "T_t-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn= 50, njobsOut= 2),
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 50, njobsOut= 1),
        "T_tW-channel_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 20, njobsOut= 2),
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDefMC(njobsIn= 20, njobsOut= 2),
        "T_s-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn= 10, njobsOut= 1),
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 10, njobsOut= 1),
        }

    # Set the multijet triggers on data
    for datasetName, taskDef in defaultDefinitions.iteritems():
        triggers = []
        hasOneRunRange = True
        for triggerDict in [tauTriggers, quadJetTriggers, quadPFJetBTagTriggers, quadJetBTagTriggers]:
            if datasetName in triggerDict:
                trg = triggerDict[datasetName]
                triggers.extend(trg)
                if len(trg) > 1:
                    hasOneRunRange = False
        if len(triggers) > 0:
            taskDef.update(TaskDef(triggerOR=triggers, triggerThrow=hasOneRunRange))


    # Update the default definitions from the argument
    workflowName = "pattuple_"+version
    updateTaskDefinitions(defaultDefinitions, updateDefinitions, workflowName)

    # Add pattuple Workflow for each dataset
    for datasetName, taskDef in defaultDefinitions.iteritems():
        dataset = datasets.getDataset(datasetName)

        # Construct processing workflow
        wf = constructProcessingWorkflow_53X(dataset, taskDef, sourceWorkflow="AOD", workflowName="pattuple_"+version, skimConfig=skim)

        # Setup the publish name
        name = updatePublishName(dataset, wf.source.getDataForDataset(dataset).getDatasetPath(), workflowName)
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
                found = False
                if datasetName in tauTriggers:
                    found = True
                    dataset.addWorkflow(Workflow("analysis_taumet_"+version, triggerOR=tauTriggers[datasetName], **commonArgs))
                if datasetName in quadJetTriggers:
                    found = True
                    dataset.addWorkflow(Workflow("analysis_quadjet_"+version, triggerOR=quadJetTriggers[datasetName], **commonArgs))
                if datasetName in quadJetBTagTriggers:
                    found = True
                    dataset.addWorkflow(Workflow("analysis_quadjetbtag_"+version, triggerOR=quadJetBTagTriggers[datasetName], **commonArgs))
                if datasetName in quadPFJetBTagTriggers:
                    found = True
                    dataset.addWorkflow(Workflow("analysis_quadpfjetbtag_"+version, triggerOR=quadPFJetBTagTriggers[datasetName], **commonArgs))

                if not found:
                    raise Exception("No trigger specified for dataset %s" % datasetName)
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
#
# For some reason, some of the signal samples were not triggered in
# pattuple jobs
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
        "TTToHplusBWB_M155_Fall11":         TaskDef("/TTToHplusBWB_M-155_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[]),
        "TTToHplusBWB_M160_Fall11":         TaskDef("/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),

        "TTToHplusBHminusB_M80_Fall11":     TaskDef("/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M90_Fall11":     TaskDef("/TTToHplusBHminusB_M-90_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M100_Fall11":    TaskDef("/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M120_Fall11":    TaskDef("/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M140_Fall11":    TaskDef("/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M150_Fall11":    TaskDef("/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),
        "TTToHplusBHminusB_M155_Fall11":    TaskDef("/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[]),
        "TTToHplusBHminusB_M160_Fall11":    TaskDef("/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER"),

        "HplusTB_M180_Fall11":              TaskDef("/HplusTB_M-180_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[]),
        "HplusTB_M190_Fall11":              TaskDef("/HplusTB_M-190_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[]),
        "HplusTB_M200_Fall11":              TaskDef("/HplusTB_M-200_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[]),
        "HplusTB_M220_Fall11":              TaskDef("/HplusTB_M-220_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[]),
        "HplusTB_M250_Fall11":              TaskDef("/HplusTB_M-250_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[]),
        "HplusTB_M300_Fall11":              TaskDef("/HplusTB_M-300_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[]),

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

## Add v44_4_1 pattuple production workflows
#
# These are without trigger
def addPattuple_v44_4_1(datasets):
    definitions = {
        "TTToHplusBWB_M120_Fall11":         TaskDef("/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4_1-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[]),
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDef("/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4_1-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[], njobsIn=600),
        }
    addPattuple_44X("v44_4_1", datasets, definitions)

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
        # 64775 events, 69 jobs
        # 1526.7, min 111.7, max 4328.0
        # Mean 33.7 MB, min 4.7 MB, max 66.5 MB
        "Tau_190456-190738_2012A_Jul13":          TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_190456_190738_pattuple_v53_1-00fb6a0648e9082988536b8287ce18fd/USER", njobsIn=150),
        # 42028 events, 15 jobs
        # User mean 4284.1, min 1746.4, max 6808.0
        # Mean 85.4 MB, min 37.3 MB, max 120.4 MB
        "Tau_190782-190949_2012A_Aug06":          TaskDef("/Tau/local-Run2012A_recover_06Aug2012_v1_AOD_190782_190949_pattuple_v53_1-1be0c628538f5a4dae541da3c11eb60c/USER", njobsIn=30),
        # 368031 events, 208 jobs
        # User mean 2552.0, min 490.3, max 7832.9
        # Mean 55.9 MB, min 20.1 MB, max 114.5 MB
        "Tau_191043-193621_2012A_Jul13":          TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_191043_193621_pattuple_v53_1-39e2e8832bb5d7b032f2b5c9a80e534a/USER", njobsIn=400),
        # 2822552 events, 1223 jobs
        # User mean 3862.7, min 870.5, max 12606.2
        # MEan 71.0 MB, min 30.0 MB, max 200.5 MB
        "Tau_193834-196531_2012B_Jul13":          TaskDef("/Tau/local-Run2012B_13Jul2012_v1_AOD_193834_196531_pattuple_v53_1-382e6b84ca489c093c178cfb50ba5dbe/USER"),
        # 258977 events, 123 jobs
        # User mean 3000.0, min 1023.1, max 9092.2
        # MEan 65.6 MB, min 33.8 MB, max 145.2 MB
        "Tau_198022-198523_2012C_Aug24":          TaskDef("/Tau/local-Run2012C_24Aug2012_v1_AOD_198022_198523_pattuple_v53_1-03816abcf2df69d2a2f275b0cfc9c090/USER"),
        # 1705781 events, 919 jobs
        # User mean 3198.3, min 459.2, max 10224.7
        # Mean 60.2 MB, min 12.2 MB, max 143.2 MB
        "Tau_198941-200601_2012C_Prompt":         TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_198941_200601_pattuple_v53_1-cdc21ac5d95fea9b64545e44f8ba4b15/USER"),
        # 1792819 events, 880 jobs
        # User mean 3560.7, min 165.1, max 15969.2
        # Mean 67.8 MB, min 4.1 MB, max 292.2 MB
        "Tau_200961-202504_2012C_Prompt":         TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_200961_202504_pattuple_v53_1-97851bbbf7291004b296c48e58143d74/USER"),
        # 175227 events, 88 jobs
        # User mean 3471.1, min 1106.8, max 11490.2
        # Mean 64.9 MB, min 20.3 MB, max 161.9 MB
        "Tau_202792-203742_2012C_Prompt":         TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_202792_203742_pattuple_v53_1-a6a087b1796a2a131884baa5c492e72f/USER"),

        # 466504 events, 189 jobs
        # User mean 4773.0, min 124.1, max 12608.1
        # Mean 77.8 MB, min 4.3 MB, max 165.5 MB
        "MultiJet_190456-190738_2012A_Jul13":     TaskDef("/MultiJet/local-Run2012A_13Jul2012_v1_AOD_190456_190738_pattuple_v53_1-8d229f863f3fc8a5a50f8b702ec0e1b3/USER"),
        # 313212 events, 52 jobs
        # User mean 11466.7, min 944.5, max 22526.1
        # Mean 176.9 MB, min 23.1 MB, max 245.6 MB
        "MultiJet_190782-190949_2012A_Aug06":     TaskDef("/MultiJet/local-Run2012A_recover_06Aug2012_v1_AOD_190782_190949_pattuple_v53_1-fdd3c1f4d60921e4522b1cd7c85b5f38/USER"),
        # 2954598 events, 582 jobs
        # User mean 11544.0, min 87.4, max 31691.4
        # Mean 144.6 MB, min 1.6 MB, max 309.0 MB
        "MultiJet_191043-193621_2012A_Jul13":     TaskDef("/MultiJet/local-Run2012A_13Jul2012_v1_AOD_191043_193621_pattuple_v53_1c-e7b040c48519314dbf67cfc22f9c91f7/USER"),
        # 830720 events, 230 jobs
        # User mean 6722.4, min 975.6, max 14102.3
        # Mean 115.3 MB, min 19.4 MB, max 189.1 MB
        "MultiJet_193834-194225_2012B_Jul13":     TaskDef("/MultiJet/local-Run2012B_13Jul2012_v1_AOD_193834_194225_pattuple_v53_1-7cb2cf938b8a39c78ce811004f4e1701/USER"),
        # 5766837 events, 1221 jobs
        # User mean 7562.7, min 634.7, max 22387.1
        # Mean 156.7 MB, min 19.7 MB, max 283.0 MB
        "MultiJet_194270-196531_2012B_Jul13":     TaskDef("/MultiJet/local-Run2012B_13Jul2012_v1_AOD_194270_196531_pattuple_v53_1b-13eab0232030eb0def83f54eafd8085d/USER"),
        # 715141 events, 144 jobs
        # User mean 8308.8, min 2863.4, max 18322.6
        # Mean 159.7 MB, min 67.0 MB, max 285.3 MB
        "MultiJet_198022-198523_2012C_Aug24":     TaskDef("/MultiJet/local-Run2012C_24Aug2012_v1_AOD_198022_198523_pattuple_v53_1-88f58a18bc4cc32ca93270fe01187879/USER"),
        # 4715708 events, 1014 jobs
        # User mean 10963.2, min 28.8, max 27652.1
        # Mean 152.5 MB, min 1.5 MB, max 291.0 MB
        "MultiJet_198941-200601_2012C_Prompt":    TaskDef("/MultiJet/local-Run2012C_PromptReco_v2_AOD_198941_200601_pattuple_v53_1b-8bbd8eb7290730a495ba05939e654f51/USER"),
        # 4365595 events, 951 jobs
        # User mean 9767.7, min 31.6, max 34821.4
        # Mean 156.3 MB, min 1.7 MB, max 299.6 MB
        "MultiJet_200961-202504_2012C_Prompt":    TaskDef("/MultiJet/local-Run2012C_PromptReco_v2_AOD_200961_202504_pattuple_v53_1-87325f0f572c545baf7123d89881d242/USER"),
        # 433952 events, 95 jobs
        # User mean 9729.1, min 2975.8, max 19985.4
        # Mean 149.4 MB, min 43.7 MB, max 265.8 MB
        "MultiJet_202792-203742_2012C_Prompt":    TaskDef("/MultiJet/local-Run2012C_PromptReco_v2_AOD_202792_203742_pattuple_v53_1-87325f0f572c545baf7123d89881d242/USER"),

        # 27900-37203 events, 41 jobs
        # User mean 1880.2, min 70.3, max 2354.6
        # Mean 81.3 MB, min 3.5 MB, max 89.0 MB
        "TTToHplusBWB_M80_Summer12":              TaskDef("/TTToHplusBWB_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 2402.1, min 667.7, max 3310.3
        # Mean 85.3 MB, min 35.2 MB, max 93.6 MB
        "TTToHplusBWB_M90_Summer12":              TaskDef("/TTToHplusBWB_M-90_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 1843.8, min 31.9, max 2950.7
        # Mean 74.6 MB, min 1.6 MB, max 81.0 MB
        "TTToHplusBWB_M100_Summer12":             TaskDef("/TTToHplusBWB_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 2112.0, min 69.4, max 3256.6
        # Mean 84.0 MB, min 3.0 MB, max 91.1 MB
        "TTToHplusBWB_M120_Summer12":             TaskDef("/TTToHplusBWB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 1933.6, min 833.5, max 2879.1
        # Mean 86.7 MB, min 42.5 MB, max 93.5 MB
        "TTToHplusBWB_M140_Summer12":             TaskDef("/TTToHplusBWB_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 2191.8, min 1148.9, max 3310.1
        # Mean 86.3 MB, min 46.7 MB, max 96.2 MB
        "TTToHplusBWB_M150_Summer12":             TaskDef("/TTToHplusBWB_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 2310.1, min 566.4, max 3343.5
        # Mean 89.7 MB, min 29.9 MB, max 100.3 MB
        "TTToHplusBWB_M155_Summer12":             TaskDef("/TTToHplusBWB_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40), 
        # User mean 2377.2, min 381.0, max 3628.7
        # Mean 91.1 MB, min 12.2 MB, max 101.4 MB
        "TTToHplusBWB_M160_Summer12":             TaskDef("/TTToHplusBWB_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),

        # 29908-40068 events 40 jobs
        # User mean 1864.4, min 1339.7, max 2824.3
        # Mean 78.1 MB, min 74.8 MB, max 83.1 MB
        "TTToHplusBHminusB_M80_Summer12":         TaskDef("/TTToHplusBHminusB_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 2055.7, min 1398.1, max 2986.4
        # Mean 78.3 MB, min 72.4 MB, max 84.2 MB
        "TTToHplusBHminusB_M100_Summer12":        TaskDef("/TTToHplusBHminusB_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 1849.9, min 261.0, max 2491.6
        # Mean 78.5 MB, min 13.0 MB, max 85.6 MB
        "TTToHplusBHminusB_M120_Summer12":        TaskDef("/TTToHplusBHminusB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 2086.1, min 1435.3, max 3003.0
        # Mean 82.8 MB, min 78.8 MB, max 87.2 M
        "TTToHplusBHminusB_M140_Summer12":        TaskDef("/TTToHplusBHminusB_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 2064.8, min 563.6, max 2974.9
        # Mean 82.8 MB, min 23.4 MB, max 89.4 MB
        "TTToHplusBHminusB_M150_Summer12":        TaskDef("/TTToHplusBHminusB_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 2005.8, min 1434.7, max 3196.9
        # Mean 86.4 MB, min 79.7 MB, max 91.6 MB
        "TTToHplusBHminusB_M155_Summer12":        TaskDef("/TTToHplusBHminusB_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 2016.6, min 1670.6, max 2451.4
        # Mean 88.0 MB, min 83.2 MB, max 93.5 MB        
        "TTToHplusBHminusB_M160_Summer12":        TaskDef("/TTToHplusBHminusB_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),

        # 10275-17098 events 40-41 jobs
        # User mean 709.9, min 33.7, max 973.2
        # Mean 28.6 MB, min 1.6 MB, max 33.9 MB
        "Hplus_taunu_s-channel_M80_Summer12":     TaskDef("/Hplus_taunu_s-channel_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # Mean 28.0 MB, min 1.6 MB, max 31.6 MB
        # User mean 672.5, min 31.9, max 856.0
        "Hplus_taunu_s-channel_M90_Summer12":     TaskDef("/Hplus_taunu_s-channel_M-90_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 782.6, min 69.8, max 1038.3
        # Mean 31.7 MB, min 2.8 MB, max 36.1 MB
        "Hplus_taunu_s-channel_M100_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 752.7, min 87.9, max 950.5
        # Mean 29.7 MB, min 2.8 MB, max 35.7 MB
        "Hplus_taunu_s-channel_M120_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 966.4, min 724.2, max 1137.2
        # Mean 39.9 MB, min 36.1 MB, max 43.4 MB
        "Hplus_taunu_s-channel_M140_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 995.3, min 62.8, max 1188.5
        # Mean 41.5 MB, min 2.6 MB, max 45.4 MB
        "Hplus_taunu_s-channel_M150_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 886.9, min 63.4, max 1216.1
        # Mean 40.5 MB, min 2.8 MB, max 45.6 MB
        "Hplus_taunu_s-channel_M155_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),
        # User mean 1111.6, min 885.4, max 1424.6
        # Mean 46.9 MB, min 42.2 MB, max 50.2 MB
        "Hplus_taunu_s-channel_M160_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=40),

        # 53759-78988 events, 40-43 jobs
        # User mean 3247.1, min 2359.6, max 4081.3
        # Mean 137.2 MB, min 129.2 MB, max 144.0 MB
        "HplusTB_M180_Summer12":                  TaskDef("/HplusTB_M-180_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 3518.2, min 2405.3, max 5267.8
        # Mean 142.4 MB, min 135.9 MB, max 148.7 MB
        "HplusTB_M190_Summer12":                  TaskDef("/HplusTB_M-190_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 4313.7, min 308.4, max 5847.3
        # Mean 138.3 MB, min 17.6 MB, max 153.8 MB
        "HplusTB_M200_Summer12":                  TaskDef("/HplusTB_M-200_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 3645.6, min 2859.7, max 4464.0
        # Mean 159.4 MB, min 149.1 MB, max 167.2 MB
        "HplusTB_M220_Summer12":                  TaskDef("/HplusTB_M-220_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 3862.1, min 3058.2, max 4985.0
        # Mean 173.9 MB, min 166.4 MB, max 180.4 MB
        "HplusTB_M250_Summer12":                  TaskDef("/HplusTB_M-250_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 4470.4, min 3533.4, max 6924.7
        # Mean 196.9 MB, min 189.9 MB, max 202.8 MB
        "HplusTB_M300_Summer12":                  TaskDef("/HplusTB_M-300_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),

        # 114 events, 23 jobs
        # User mean 1073.6, min 35.1, max 1520.2
        # Mean 6.0 MB, min 1.7 MB, max 7.2 MB
        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDef("/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=20),
        # 2749 events, 22 jobs
        # User mean 1422.9, min 244.0, max 2176.0
        # Mean 19.2 MB, min 4.7 MB, max 22.1 MB
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDef("/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER". njobsIn=20),
        # 21951 events, 21 jobs
        # User mean 4850.8, min 1613.3, max 6008.9
        # Mean 104.5 MB, min 32.8 MB, max 115.7 MB
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDef("/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 75972 events, 41 jobs
        # User mean 6055.0, min 2980.7, max 7870.7
        # Mean 178.4 MB, min 105.1 MB, max 190.5 MB
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDef("/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 232796 events, 82 jobs
        # User mean 8065.4, min 373.4, max 12142.1
        # Mean 280.1 MB, min 15.0 MB, max 298.4 MB
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=80),
        # 797355 events, 305 jobs
        # User mean 6733.4, min 737.7, max 17064.5
        # Mean 258.6 MB, min 27.0 MB, max 276.6 MB
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=300),
        # 616204 events, 251 jobs
        # User mean 5354.8, min 1467.4, max 8339.4
        # Mean 258.3 MB, min 85.4 MB, max 272.3 MB
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1b-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=250),
        # 359260 events, 151 jobs
        # User mean 5180.3, min 948.1, max 7609.2
        # Mean 250.5 MB, min 58.2 MB, max 265.4 MB
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=150),
        # 2045846 events, 854 jobs
        # User mean 5627.8, min 252.5, max 21303.3
        # Mean 252.4 MB, min 19.4 MB, max 269.9 MB
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v3/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=850),

        # 288671 events, 152 jobs
        # User mean 5456.2, min 173.2, max 7120.2
        # Mean 161.0 MB, min 5.9 MB, max 171.0 MB
        "WW_TuneZ2star_Summer12":                 TaskDef("/WW_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 256016 events, 153 jobs
        # User mean 3828.7, min 311.1, max 4946.5
        # Mean 146.5 MB, min 11.6 MB, max 157.1 MB
        "WZ_TuneZ2star_Summer12":                 TaskDef("/WZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 201924 events, 157 jobs
        # User mean 3534.7, min 120.2, max 6150.8
        # Mean 117.8 MB, min 4.6 MB, max 133.3 MB
        "ZZ_TuneZ2star_Summer12":                 TaskDef("/ZZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 1202301 events, 702 jobs
        # User mean 4656.1, min 107.5, max 7579.8
        # Mean 184.2 MB, min 8.8 MB, max 199.8 MB
        "TTJets_TuneZ2star_Summer12":             TaskDef("/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 94009 events, 103 jobs
        # User mean 2322.5, min 831.9, max 4019.9
        # Mean 81.3 MB, min 32.6 MB, max 88.8 MB
        "WJets_TuneZ2star_v1_Summer12":           TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=100),
        # 285149 events, 257 jobs
        # User mean 3017.1, min 231.8, max 5345.6
        # Mean 99.3 MB, min 6.2 MB, max 110.6 MB
        "WJets_TuneZ2star_v2_Summer12":           TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=250),
        # 203841 events, 154 jobs
        # User mean 2991.6, min 97.7, max 3952.6
        # Mean 107.9 MB, min 5.8 MB, max 117.0 MB
        "W1Jets_TuneZ2star_Summer12":             TaskDef("/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=150),
        # 752423 events, 407 jobs
        # User mean 3997.5, min 173.9, max 6244.6
        # Mean 153.1 MB, min 7.2 MB, max 168.7 MB
        "W2Jets_TuneZ2star_Summer12":             TaskDef("/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 616480 events, 494 jobs
        # User mean 2729.3, min 146.2, max 4887.5
        # Mean 114.8 MB, min 6.9 MB, max 125.0 MB
        "W3Jets_TuneZ2star_Summer12":             TaskDef("/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 1002056 events, 551 jobs
        # User mean 4245.6, min 1247.0, max 6472.4
        # Mean 178.0 MB, min 76.2 MB, max 194.2 MB
        "W4Jets_TuneZ2star_Summer12":             TaskDef("/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 180247 events, 354 jobs
        # User mean 1396.3, min 225.2, max 2209.5
        # Mean 52.3 MB, min 8.6 MB, max 59.7 MB
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDef("/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER", njobsIn=350),
        # 4476 events, 52 jobs
        # User mean 3143.5, min 53.1, max 7003.0
        # Mean 21.3 MB, min 1.7 MB, max 29.6 MB
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDef("/DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1b-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 222877 events, 51 jobs
        # User mean 9109.8, min 4861.2, max 12412.2
        # Mean 395.6 MB, min 161.4 MB, max 414.6 MB
        "T_t-channel_TuneZ2star_Summer12":        TaskDef("/T_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 27667 events, 51 jobs
        # User mean 5100.9, min 39.9, max 6981.7
        # Mean 191.4 MB, min 1.6 MB, max 206.7 MB
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDef("/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 61356 events, 
        # User mean 7621.3, min 101.0, max 10203.7
        # Mean 285.5 MB, min 2.8 MB, max 311.0 MB
        "T_tW-channel_TuneZ2star_Summer12":       TaskDef("/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 60272 events, 22 jobs
        # User mean 8464.9, min 309.9, max 12849.3
        # Mean 268.7 MB, min 12.9 MB, max 303.4 MB
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDef("/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 11203 events, 11 jobs
        # User mean 3459.9, min 56.5, max 4188.3
        # Mean 102.3 MB, min 1.6 MB, max 115.7 MB
        "T_s-channel_TuneZ2star_Summer12":        TaskDef("/T_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 5345 events, 11 jobs
        # User mean 1592.8, min 41.1, max 2063.5
        # Mean 52.0 MB, min 1.6 MB, max 59.9 MB
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDef("/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        }

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

    addPattuple_53X("v53_1", datasets, definitions,
                    quadPFJetBTagTriggers=quadPFJetBTagTriggers,
                    quadJetBTagTriggers=quadJetBTagTriggers,
                    quadJetTriggers=quadJetTriggers)


def addPattuple_v53_1_1(datasets):
    # Same as v53_1, but with CMSSW_5_3_6_patch1
    definitionsAlsoInV53_1 = {
        # For testing only
        "TTToHplusBWB_M120_Summer12":             TaskDef("/TTToHplusBWB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1_1-e5b7e051b5f262d92a2dca949f12e05a/USER"), # 32322 events, Mean 128.5 MB, min 2.7 MB, max 141.8 MB
        }
    definitions = {}
    definitions.update(definitionsAlsoInV53_1)

    addPattuple_53X("v53_1_1", datasets, definitions)


def addPattuple_v53_1_2(datasets):
    # Same as v53_1, but with CMSSW_5_3_7
    definitionsAlsoInV53_1 = {
        # For testing only
        "TTToHplusBWB_M120_Summer12":             TaskDef("/TTToHplusBWB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1_2-e5b7e051b5f262d92a2dca949f12e05a/USER"), # 32322 events, Mean 128.5 MB, min 2.7 MB, max 141.8 MB
        }
    definitions = {}
    definitions.update(definitionsAlsoInV53_1)

    addPattuple_53X("v53_1_2", datasets, definitions)

    # Make an alias for the analysis workflow
    # for datasetName in definitionsOnlyInV53_1_2.keys():
    #     dataset = datasets.getDataset(datasetName)
    #     if dataset.hasWorkflow("analysis_v53_1_2"):
    #         analysisWf = dataset.getWorkflow("analysis_v53_1_2")
    #         dataset.addWorkflow(WorkflowAlias("analysis_v53_1", analysisWf))

# Skeleton
def addPattuple_v53_2(datasets):
    definitions = {
        "Tau_190456-190738_2012A_Jul13":          TaskDef(""),
        "Tau_190782-190949_2012A_Aug06":          TaskDef(""),
        "Tau_191043-193621_2012A_Jul13":          TaskDef(""),
        "Tau_193834-196531_2012B_Jul13":          TaskDef(""),
        "Tau_198022-198523_2012C_Aug24":          TaskDef(""),
        "Tau_198941-202504_2012C_Prompt":         TaskDef(""),
        "Tau_201191-201191_2012C_Dec11":          TaskDef(""),
        "Tau_202972-203742_2012C_Prompt":         TaskDef(""),
        "Tau_203777-208686_2012D_Prompt":         TaskDef(""),

        "MultiJet_190456-190738_2012A_Jul13":     TaskDef(""),
        "MultiJet_190782-190949_2012A_Aug06":     TaskDef(""),
        "MultiJet_191043-193621_2012A_Jul13":     TaskDef(""),
        "MultiJet_193834-194225_2012B_Jul13":     TaskDef(""),
        "MultiJet_194270-196531_2012B_Jul13":     TaskDef(""),
        "MultiJet_198022-198523_2012C_Aug24":     TaskDef(""),
        "MultiJet_198941-203742_2012C_Prompt":    TaskDef(""),
        "MultiJet_203777-208686_2012D_Prompt":    TaskDef(""),

        "BJetPlusX_193834-194225_2012B_Jul13":    TaskDef(""),
        "BJetPlusX_194270-196531_2012B_Jul13":    TaskDef(""),
        "BJetPlusX_198022-198523_2012C_Aug24":    TaskDef(""),
        "BJetPlusX_198941-203742_2012C_Prompt":   TaskDef(""),
        "BJetPlusX_201191-201191_2012C_Dec11":    TaskDef(""),
        "BJetPlusX_203777-208686_2012D_Prompt":   TaskDef(""),

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

    addPattuple_53X("v53_2", datasets, definitions)

# Skeleton
def addPattuple_vNEXT_SKELETON_53X(datasets):
    definitions = {
        "Tau_190456-190738_2012A_Jul13":          TaskDef(""),
        "Tau_190782-190949_2012A_Aug06":          TaskDef(""),
        "Tau_191043-193621_2012A_Jul13":          TaskDef(""),
        "Tau_193834-196531_2012B_Jul13":          TaskDef(""),
        "Tau_198022-198523_2012C_Aug24":          TaskDef(""),
        "Tau_198941-202504_2012C_Prompt":         TaskDef(""),
        "Tau_201191-201191_2012C_Dec11":          TaskDef(""),
        "Tau_202972-203742_2012C_Prompt":         TaskDef(""),
        "Tau_203777-208686_2012D_Prompt":         TaskDef(""),

        "MultiJet_190456-190738_2012A_Jul13":     TaskDef(""),
        "MultiJet_190782-190949_2012A_Aug06":     TaskDef(""),
        "MultiJet_191043-193621_2012A_Jul13":     TaskDef(""),
        "MultiJet_193834-194225_2012B_Jul13":     TaskDef(""),
        "MultiJet_194270-196531_2012B_Jul13":     TaskDef(""),
        "MultiJet_198022-198523_2012C_Aug24":     TaskDef(""),
        "MultiJet_198941-203742_2012C_Prompt":    TaskDef(""),
        "MultiJet_203777-208686_2012D_Prompt":    TaskDef(""),

        "BJetPlusX_193834-194225_2012B_Jul13":    TaskDef(""),
        "BJetPlusX_194270-196531_2012B_Jul13":    TaskDef(""),
        "BJetPlusX_198022-198523_2012C_Aug24":    TaskDef(""),
        "BJetPlusX_198941-203742_2012C_Prompt":   TaskDef(""),
        "BJetPlusX_201191-201191_2012C_Dec11":    TaskDef(""),
        "BJetPlusX_203777-208686_2012D_Prompt":   TaskDef(""),

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
