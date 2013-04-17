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
                    "Prompt": "PromptReco12",
                    # Winter13 Rereco
                    "Jan22": "22Jan2013ReReco",
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
                                            
        "WW_TuneZ2_Fall11":                 TaskDefMC(njobsIn=40, njobsOut=3),
        "WZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=40, njobsOut=3),
        "ZZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=40, njobsOut=3),   
        "TTJets_TuneZ2_Fall11":             TaskDefMC(njobsIn=2000, njobsOut=50),
        "WJets_TuneZ2_Fall11":              TaskDefMC(njobsIn=400, njobsOut=4, args={"wjetsWeighting": 1, "wjetBin": -1}),
        "W1Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=300, njobsOut=6, args={"wjetsWeighting": 1, "wjetBin": 1}),
        "W2Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=200, njobsOut=5, args={"wjetsWeighting": 1, "wjetBin": 2}),
        "W3Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=100, njobsOut=10, args={"wjetsWeighting": 1, "wjetBin": 3}),
        "W3Jets_TuneZ2_v2_Fall11":          TaskDefMC(njobsIn=100, njobsOut=4, args={"wjetsWeighting": 1, "wjetBin": 3}),
        "W4Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=300, njobsOut=10, args={"wjetsWeighting": 1, "wjetBin": 4}),
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

            # Winter13 Reprocessing
            "Tau_190456-193621_2012A_Jan22": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v2", # 190456-190738
                                              "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v3", # 190782-191411
                                              "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v4"],# 191691-193621
            "TauParked_193834-196531_2012B_Jan22": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6"],
            "TauParked_198022-202504_2012C_Jan22": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7",  # 198022-199608
                                                    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9"],  # 199698-202504
            "TauParked_202972-203742_2012C_Jan22": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10"],
            "TauParked_203777-208686_2012D_Jan22": ["HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10"],
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
            "MultiJet_198941-203742_2012C_Prompt": ["HLT_QuadJet80_v4",  # 198941-199608
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
        "Tau_190456-190738_2012A_Jul13":  TaskDef(njobsIn=  25, njobsOut=  1), # aim 22
        "Tau_190782-190949_2012A_Aug06":  TaskDef(njobsIn=  15, njobsOut=  1), # aim 10
        "Tau_191043-193621_2012A_Jul13":  TaskDef(njobsIn= 130, njobsOut=  4), # aim 90
        "Tau_193834-196531_2012B_Jul13":  TaskDef(nlumisPerJobIn=1, njobsOut= 25),
        "Tau_198022-198523_2012C_Aug24":  TaskDef(njobsIn= 130, njobsOut=  3), # aim 85
        # The following three could be combined in the subsequent pattuple processings
        "Tau_198941-200601_2012C_Prompt": TaskDef(njobsIn=1500, njobsOut= 10),
        "Tau_200961-202504_2012C_Prompt": TaskDef(njobsIn=1500, njobsOut= 12),
        "Tau_202792-203742_2012C_Prompt": TaskDef(njobsIn= 150, njobsOut=  1),
        # Below is the combination of the above two, plus the third one with modified first run
        "Tau_198941-202504_2012C_Prompt": TaskDef(njobsIn=2800, njobsOut= 40), # aim 1700
        "Tau_201191-201191_2012C_Dec11":  TaskDef(njobsIn=20,   njobsOut=  1), # aim 18
        "Tau_202972-203742_2012C_Prompt": TaskDef(njobsIn=40,   njobsOut=  1), # aim 34
        "Tau_203777-208686_2012D_Prompt": TaskDef(nlumisPerJobIn=1, njobsOut= 50),

        ## MultiJet
        "MultiJet_190456-190738_2012A_Jul13":  TaskDef(nlumisPerJobIn=1, njobsOut= 2),
        "MultiJet_190782-190949_2012A_Aug06":  TaskDef(nlumisPerJobIn=1, njobsOut= 1),
        "MultiJet_191043-193621_2012A_Jul13":  TaskDef(nlumisPerJobIn=1, njobsOut=15),
        "MultiJet_193834-194225_2012B_Jul13":  TaskDef(nlumisPerJobIn=1, njobsOut= 5),
        "MultiJet_194270-196531_2012B_Jul13":  TaskDef(nlumisPerJobIn=1, njobsOut=30),
        "MultiJet_198022-198523_2012C_Aug24":  TaskDef(nlumisPerJobIn=1, njobsOut= 4),
        # The following three could be combined in the subsequent pattuple processings
        "MultiJet_198941-200601_2012C_Prompt": TaskDef(njobsIn=1700, njobsOut=35),
        "MultiJet_200961-202504_2012C_Prompt": TaskDef(njobsIn=1700, njobsOut=30),
        "MultiJet_202792-203742_2012C_Prompt": TaskDef(njobsIn= 170, njobsOut= 3),
        # Below is the combination of the above three
        "MultiJet_198941-203742_2012C_Prompt": TaskDef(nlumisPerJobIn=1, njobsOut=50),
        "MultiJet_203777-208686_2012D_Prompt": TaskDef(nlumisPerJobIn=1, njobsOut=60),

        ## BJetsPlusX
        "BJetPlusX_193834-194225_2012B_Jul13":  TaskDef(nlumisPerJobIn=1, njobsOut= 6),
        "BJetPlusX_194270-196531_2012B_Jul13":  TaskDef(nlumisPerJobIn=1, njobsOut=30),
        "BJetPlusX_198022-198523_2012C_Aug24":  TaskDef(nlumisPerJobIn=1, njobsOut= 3),
        "BJetPlusX_198941-203742_2012C_Prompt": TaskDef(nlumisPerJobIn=1, njobsOut=40),
        "BJetPlusX_201191-201191_2012C_Dec11":  TaskDef(nlumisPerJobIn=1, njobsOut= 1),
        "BJetPlusX_203777-208686_2012D_Prompt": TaskDef(nlumisPerJobIn=1, njobsOut=50),

        # Winter13 Reprocessing
        ## Tau
        "Tau_190456-193621_2012A_Jan22":       TaskDef(njobsIn= 300, njobsOut= 6), # aim 200, FIXME: set njobsOut
        "TauParked_193834-196531_2012B_Jan22": TaskDef(njobsIn=2500, njobsOut=25), # aim 1800, FIXME: set njobsOut
        "TauParked_198022-202504_2012C_Jan22": TaskDef(njobsIn=3000, njobsOut=40), # aim 2200, FIXME: set njobsOut
        "TauParked_202972-203742_2012C_Jan22": TaskDef(njobsIn=  50, njobsOut= 1), # aim 40, FIXME: set njobsOut
        "TauParked_203777-208686_2012D_Jan22": TaskDef(njobsIn=7000, njobsOut=50), # aim 4000, FIXME: set njobsOut

        # MC, triggered with mcTrigger
        "TTToHplusBWB_M80_Summer12":        TaskDefMC(njobsIn=25, njobsOut=1),
        "TTToHplusBWB_M90_Summer12":        TaskDefMC(njobsIn=25, njobsOut=1),
        "TTToHplusBWB_M100_Summer12":       TaskDefMC(njobsIn=25, njobsOut=1),
        "TTToHplusBWB_M120_Summer12":       TaskDefMC(njobsIn=25, njobsOut=1),
        "TTToHplusBWB_M140_Summer12":       TaskDefMC(njobsIn=25, njobsOut=2),
        "TTToHplusBWB_M150_Summer12":       TaskDefMC(njobsIn=25, njobsOut=2),
        "TTToHplusBWB_M155_Summer12":       TaskDefMC(njobsIn=25, njobsOut=2),
        "TTToHplusBWB_M160_Summer12":       TaskDefMC(njobsIn=25, njobsOut=2),

        "TTToHplusBWB_M80_ext_Summer12":    TaskDefMC(njobsIn=90, njobsOut=7),
        "TTToHplusBWB_M90_ext_Summer12":    TaskDefMC(njobsIn=90, njobsOut=7),
        "TTToHplusBWB_M100_ext_Summer12":   TaskDefMC(njobsIn=90, njobsOut=15),
        "TTToHplusBWB_M120_ext_Summer12":   TaskDefMC(njobsIn=90, njobsOut=7),
        "TTToHplusBWB_M140_ext_Summer12":   TaskDefMC(njobsIn=90, njobsOut=9),
        "TTToHplusBWB_M150_ext_Summer12":   TaskDefMC(njobsIn=90, njobsOut=9),
        "TTToHplusBWB_M155_ext_Summer12":   TaskDefMC(njobsIn=90, njobsOut=9),
        "TTToHplusBWB_M160_ext_Summer12":   TaskDefMC(njobsIn=90, njobsOut=15),

        "TTToHplusBHminusB_M80_Summer12":        TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M90_Summer12":        TaskDefMC(njobsIn=100, njobsOut=7),
        "TTToHplusBHminusB_M100_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M120_Summer12":       TaskDefMC(njobsIn=20, njobsOut=1),
        "TTToHplusBHminusB_M140_Summer12":       TaskDefMC(njobsIn=20, njobsOut=2),
        "TTToHplusBHminusB_M150_Summer12":       TaskDefMC(njobsIn=20, njobsOut=2),
        "TTToHplusBHminusB_M155_Summer12":       TaskDefMC(njobsIn=20, njobsOut=2),
        "TTToHplusBHminusB_M160_Summer12":       TaskDefMC(njobsIn=20, njobsOut=2),

        "TTToHplusBHminusB_M80_ext_Summer12":    TaskDefMC(njobsIn=100, njobsOut=7),
        "TTToHplusBHminusB_M100_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=7),
        "TTToHplusBHminusB_M120_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=7),
        "TTToHplusBHminusB_M140_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=10),
        "TTToHplusBHminusB_M150_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=10),
        "TTToHplusBHminusB_M155_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=10),
        "TTToHplusBHminusB_M160_ext_Summer12":   TaskDefMC(njobsIn=100, njobsOut=10),

        "Hplus_taunu_t-channel_M80_Summer12":    TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_t-channel_M90_Summer12":    TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_t-channel_M100_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_t-channel_M120_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_t-channel_M140_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_t-channel_M150_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_t-channel_M155_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_t-channel_M160_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),

        "Hplus_taunu_tW-channel_M80_Summer12":    TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_tW-channel_M90_Summer12":    TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_tW-channel_M100_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_tW-channel_M120_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_tW-channel_M140_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_tW-channel_M150_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_tW-channel_M155_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),
        "Hplus_taunu_tW-channel_M160_Summer12":   TaskDefMC(njobsIn=20, njobsOut=1),

        "Hplus_taunu_s-channel_M80_Summer12":       TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M90_Summer12":       TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M100_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M120_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M140_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M150_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M155_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),
        "Hplus_taunu_s-channel_M160_Summer12":      TaskDefMC(njobsIn=10, njobsOut=1),

        "HplusTB_M180_Summer12":       TaskDefMC(njobsIn=40, njobsOut=3),
        "HplusTB_M190_Summer12":       TaskDefMC(njobsIn=40, njobsOut=3),
        "HplusTB_M200_Summer12":       TaskDefMC(njobsIn=40, njobsOut=3),
        "HplusTB_M220_Summer12":       TaskDefMC(njobsIn=40, njobsOut=4),
        "HplusTB_M250_Summer12":       TaskDefMC(njobsIn=40, njobsOut=4),
        "HplusTB_M300_Summer12":       TaskDefMC(njobsIn=40, njobsOut=5),
        "HplusTB_M400_Summer12":       TaskDefMC(njobsIn=250, njobsOut=30),
        "HplusTB_M500_Summer12":       TaskDefMC(njobsIn=250, njobsOut=30),
        "HplusTB_M600_Summer12":       TaskDefMC(njobsIn=250, njobsOut=30),

        "HplusTB_M180_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=15),
        "HplusTB_M190_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=15),
        "HplusTB_M200_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=20),
        "HplusTB_M220_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=20),
        "HplusTB_M250_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=20),
        "HplusTB_M300_ext_Summer12":       TaskDefMC(njobsIn=200, njobsOut=20),

        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDefMC(njobsIn=  5, njobsOut=1),
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDefMC(njobsIn=  5, njobsOut=1),
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDefMC(njobsIn= 15, njobsOut=1),
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 40, njobsOut=1),
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDefMC(njobsIn=130, njobsOut=2),
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDefMC(njobsIn=450, njobsOut=6),
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDefMC(njobsIn=350, njobsOut=6),
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDefMC(njobsIn=200, njobsOut=4),
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDefMC(njobsIn=1100, njobsOut=22),
                                            
        "WW_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut=16),
        "WZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut=13),
        "ZZ_TuneZ2star_Summer12":                 TaskDefMC(njobsIn=150, njobsOut=10),
        "TTJets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=700, njobsOut=50),
        "WJets_TuneZ2star_v1_Summer12":           TaskDefMC(njobsIn= 50, njobsOut= 4, args={"wjetsWeighting": 1, "wjetBin": -1}),
        "WJets_TuneZ2star_v2_Summer12":           TaskDefMC(njobsIn=150, njobsOut=17, args={"wjetsWeighting": 1, "wjetBin": -1}),
        "W1Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=100, njobsOut=10, args={"wjetsWeighting": 1, "wjetBin": 1}),
        "W2Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=400, njobsOut=40, args={"wjetsWeighting": 1, "wjetBin": 2}),
        "W3Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=400, njobsOut=40, args={"wjetsWeighting": 1, "wjetBin": 3}),
        "W4Jets_TuneZ2star_Summer12":             TaskDefMC(njobsIn=550, njobsOut=60, args={"wjetsWeighting": 1, "wjetBin": 4}),
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDefMC(njobsIn=150, njobsOut=12),
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDefMC(njobsIn= 40, njobsOut= 1),
        "T_t-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn=100, njobsOut= 5),
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn= 50, njobsOut= 3),
        "T_tW-channel_TuneZ2star_Summer12":       TaskDefMC(njobsIn= 30, njobsOut= 3),
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDefMC(njobsIn= 30, njobsOut= 3),
        "T_s-channel_TuneZ2star_Summer12":        TaskDefMC(njobsIn= 10, njobsOut= 1),
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDefMC(njobsIn=  5, njobsOut= 1),
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

## Add v44_4 pattuple production workflows
#
# For some reason, some of the signal samples were not triggered in
# pattuple jobs
def addPattuple_v44_4(datasets):
    definitions = {
        "Tau_160431-167913_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_160431_pattuple_v44_4-22fa40c1fbac4684dd3ccb0e713bd4b5/USER", njobsIn=300), # 7694502 evt, min 128 MB, max 907 MB
        "Tau_170722-173198_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_170722_pattuple_v44_4-9ec211af2ee07b45d4ecbc81a3a92e63/USER", njobsIn=70), # 914344 evt, min 62 MB, max 498 MB
        "Tau_173236-173692_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_173236_pattuple_v44_4-525b16261b70f8b500033d7d0afaba83/USER", njobsIn=30), # 470476 evt, min 193 MB. max 641 MB
        "Tau_175832-180252_2011B_Nov19":    TaskDef("/Tau/local-Run2011B_19Nov2011_v1_AOD_175860_pattuple_v44_4-af466d5c64c42a78ca457d4da73a4b82/USER", njobsIn=300), # 6298060 evt, min 142 MB, max 1390 MB

        "TTToHplusBWB_M80_Fall11":          TaskDef("/TTToHplusBWB_M-80_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 7 files, min 37 MB, max 187 MB
        "TTToHplusBWB_M90_Fall11":          TaskDef("/TTToHplusBWB_M-90_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 5 files, min 191 MB, max 197 MB
        "TTToHplusBWB_M100_Fall11":         TaskDef("/TTToHplusBWB_M-100_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 5 files, min 202 MB, max 206 MB
        "TTToHplusBWB_M120_Fall11":         TaskDef("/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 5 files, min 226 MB, max 231 MB
        "TTToHplusBWB_M140_Fall11":         TaskDef("/TTToHplusBWB_M-140_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 6 files, min 61 MB, max 267 MB
        "TTToHplusBWB_M150_Fall11":         TaskDef("/TTToHplusBWB_M-150_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 6 files, min 131 MB, max 287 MB
        "TTToHplusBWB_M155_Fall11":         TaskDef("/TTToHplusBWB_M-155_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[], njobsIn=50), # 2 files, min 1072 MB, max 1260 MB
        "TTToHplusBWB_M160_Fall11":         TaskDef("/TTToHplusBWB_M-160_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 5 files, min 292 MV. max 298 MB

        "TTToHplusBHminusB_M80_Fall11":     TaskDef("/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 6 files, min 60 MB, max 228 MB
        "TTToHplusBHminusB_M90_Fall11":     TaskDef("/TTToHplusBHminusB_M-90_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 5 files, min 230 MB, max 239 MB
        "TTToHplusBHminusB_M100_Fall11":    TaskDef("/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 7 files, min 42 MB, max 253 MB
        "TTToHplusBHminusB_M120_Fall11":    TaskDef("/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 7 files, min 74 MB, max 284 MB
        "TTToHplusBHminusB_M140_Fall11":    TaskDef("/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 7 files, min 94 MB, max 327 MB
        "TTToHplusBHminusB_M150_Fall11":    TaskDef("/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 6 files, min 56 MB, max 354 MB
        "TTToHplusBHminusB_M155_Fall11":    TaskDef("/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[], njobsIn=50), # 4 files, min 378 MB, max 1668 MB
        "TTToHplusBHminusB_M160_Fall11":    TaskDef("/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4fix-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 6 files, min 351 MB, max 373 MB

        "HplusTB_M180_Fall11":              TaskDef("/HplusTB_M-180_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[], njobsIn=50), # 6 files, min 2.5 MB. max 1957 MB
        "HplusTB_M190_Fall11":              TaskDef("/HplusTB_M-190_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[], njobsIn=50), # 5 files, min 1914 MB, max 1943 MB
        "HplusTB_M200_Fall11":              TaskDef("/HplusTB_M-200_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[], njobsIn=50), # 5 files, min 1961 MB, max 1985 MB
        "HplusTB_M220_Fall11":              TaskDef("/HplusTB_M-220_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[], njobsIn=50), # 5 files, min 1881 MB, max 1899 MB
        "HplusTB_M250_Fall11":              TaskDef("/HplusTB_M-250_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[], njobsIn=50), # 5 files, min 1880 MB, max 1897 MB
        "HplusTB_M300_Fall11":              TaskDef("/HplusTB_M-300_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[], njobsIn=50), # 6 files, min 2.5 MB, max 1911 MB

        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDef("/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"), # 11 files, min 1.8 MB, max 6 MB
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDef("/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"), # 11 files, min 1.8 MB, max 9.8 MB
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDef("/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"),# 11 files, min 15 MB, max 40 MB
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDef("/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"), # 21 files, min 4 MB, max 68 MB
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDef("/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER"), # 41 files, min 42 MB, max 105 MB
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDef("/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=40), # 40 files, min 2.4 MB, max 273 MB

        "WW_TuneZ2_Fall11":                 TaskDef("/WW_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 41 files, min 2.4 MB, max 87 MB
        "WZ_TuneZ2_Fall11":                 TaskDef("/WZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 41 files, min 30 MB, max 79 MB
        "ZZ_TuneZ2_Fall11":                 TaskDef("/ZZ_TuneZ2_7TeV_pythia6_tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), #  42 files, min 7 MB, max 67 MB
        "TTJets_TuneZ2_Fall11":             TaskDef("/TTJets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=490), # 495 files, min 57 MB, max 371 MB
        "WJets_TuneZ2_Fall11":              TaskDef("/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=490), # 407 files, min 2.5 MB, max 41 MB
        "W2Jets_TuneZ2_Fall11":             TaskDef("/W2Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=200), # 202 files, min 6.9 MB, max 91 MB
        "W3Jets_TuneZ2_Fall11":             TaskDef("/W3Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=120), # 52 files, min 80 MB, max 165 MB
        "W4Jets_TuneZ2_Fall11":             TaskDef("/W4Jets_TuneZ2_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=200), # 99 files, min 8 MB, max 293 MB
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDef("/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=350), # 302 files, min 5.3 MB, max 18 MB
        "T_t-channel_TuneZ2_Fall11":        TaskDef("/T_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 53 files, min 16 MB, max 66 MB
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDef("/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=50), # 53 files, min 9 MB, max 36 MB
        "T_tW-channel_TuneZ2_Fall11":       TaskDef("/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=20), # 22 files, min 7 MB, max 111 MB
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDef("/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=20),  # 22 files, min 18 MB, max 109 MB
        "T_s-channel_TuneZ2_Fall11":        TaskDef("/T_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=10), # 11 files, min 2.5 MB, max 27 MB
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDef("/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4-f16be938188c46248667b60f0c9e7452/USER", njobsIn=10), # 12 files, min 4 MB, max 14 MB
    }
    addPattuple_44X("v44_4", datasets, definitions)

## Add v44_4_1 pattuple production workflows
#
# These are without trigger
def addPattuple_v44_4_1(datasets):
    definitions = {
        "TTToHplusBWB_M120_Fall11":         TaskDef("/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4_1-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[], njobsIn=50),
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDef("/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4_1-a7cc08c191a8794be9ec81f73dbf125a/USER", triggerOR=[], njobsIn=600),
        }
    addPattuple_44X("v44_4_1", datasets, definitions)


## Add v44_5 pattuple production workflows
def addPattuple_v44_5_test1(datasets):
    definitions = {
        # 470476 events, 131 jobs
        # User mean 4158.8, min 1173.3, max 10329.6
        # Mean 82.7 MB, min 35.0 MB, max 166.1 MB
        "Tau_173236-173692_2011A_Nov08":    TaskDef("/Tau/local-Run2011A_08Nov2011_v1_AOD_173236_173692_pattuple_v44_5_test1-1b3ed6acb33bc8106ac34fb558c6831f/USER"),
        # 23189 events, 30 jobs
        # User mean 1244.2, min 862.8, max 1367.7
        # Mean 64.0 MB, min 59.9 MB, max 68.2 MB
        "TTToHplusBWB_M120_Fall11":         TaskDef("/TTToHplusBWB_M-120_7TeV-pythia6-tauola/local-Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_5_test1-778bc6993dea1b89668515c3036cbe70/USER"),
        }

    addPattuple_44X("v44_5_test1", datasets, definitions)

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
        "Tau_190456-190738_2012A_Jul13":          TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_190456_190738_pattuple_v53_1-00fb6a0648e9082988536b8287ce18fd/USER"),
        # 42028 events, 15 jobs
        # User mean 4284.1, min 1746.4, max 6808.0
        # Mean 85.4 MB, min 37.3 MB, max 120.4 MB
        "Tau_190782-190949_2012A_Aug06":          TaskDef("/Tau/local-Run2012A_recover_06Aug2012_v1_AOD_190782_190949_pattuple_v53_1-1be0c628538f5a4dae541da3c11eb60c/USER"),
        # 368031 events, 208 jobs
        # User mean 2552.0, min 490.3, max 7832.9
        # Mean 55.9 MB, min 20.1 MB, max 114.5 MB
        "Tau_191043-193621_2012A_Jul13":          TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_191043_193621_pattuple_v53_1-39e2e8832bb5d7b032f2b5c9a80e534a/USER"),
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
        "TTToHplusBWB_M80_Summer12":              TaskDef("/TTToHplusBWB_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 2402.1, min 667.7, max 3310.3
        # Mean 85.3 MB, min 35.2 MB, max 93.6 MB
        "TTToHplusBWB_M90_Summer12":              TaskDef("/TTToHplusBWB_M-90_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 1843.8, min 31.9, max 2950.7
        # Mean 74.6 MB, min 1.6 MB, max 81.0 MB
        "TTToHplusBWB_M100_Summer12":             TaskDef("/TTToHplusBWB_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 2112.0, min 69.4, max 3256.6
        # Mean 84.0 MB, min 3.0 MB, max 91.1 MB
        "TTToHplusBWB_M120_Summer12":             TaskDef("/TTToHplusBWB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 1933.6, min 833.5, max 2879.1
        # Mean 86.7 MB, min 42.5 MB, max 93.5 MB
        "TTToHplusBWB_M140_Summer12":             TaskDef("/TTToHplusBWB_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 2191.8, min 1148.9, max 3310.1
        # Mean 86.3 MB, min 46.7 MB, max 96.2 MB
        "TTToHplusBWB_M150_Summer12":             TaskDef("/TTToHplusBWB_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 2310.1, min 566.4, max 3343.5
        # Mean 89.7 MB, min 29.9 MB, max 100.3 MB
        "TTToHplusBWB_M155_Summer12":             TaskDef("/TTToHplusBWB_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"), 
        # User mean 2377.2, min 381.0, max 3628.7
        # Mean 91.1 MB, min 12.2 MB, max 101.4 MB
        "TTToHplusBWB_M160_Summer12":             TaskDef("/TTToHplusBWB_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),

        # 29908-40068 events 40 jobs
        # User mean 1864.4, min 1339.7, max 2824.3
        # Mean 78.1 MB, min 74.8 MB, max 83.1 MB
        "TTToHplusBHminusB_M80_Summer12":         TaskDef("/TTToHplusBHminusB_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 2055.7, min 1398.1, max 2986.4
        # Mean 78.3 MB, min 72.4 MB, max 84.2 MB
        "TTToHplusBHminusB_M100_Summer12":        TaskDef("/TTToHplusBHminusB_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 1849.9, min 261.0, max 2491.6
        # Mean 78.5 MB, min 13.0 MB, max 85.6 MB
        "TTToHplusBHminusB_M120_Summer12":        TaskDef("/TTToHplusBHminusB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 2086.1, min 1435.3, max 3003.0
        # Mean 82.8 MB, min 78.8 MB, max 87.2 M
        "TTToHplusBHminusB_M140_Summer12":        TaskDef("/TTToHplusBHminusB_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 2064.8, min 563.6, max 2974.9
        # Mean 82.8 MB, min 23.4 MB, max 89.4 MB
        "TTToHplusBHminusB_M150_Summer12":        TaskDef("/TTToHplusBHminusB_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 2005.8, min 1434.7, max 3196.9
        # Mean 86.4 MB, min 79.7 MB, max 91.6 MB
        "TTToHplusBHminusB_M155_Summer12":        TaskDef("/TTToHplusBHminusB_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 2016.6, min 1670.6, max 2451.4
        # Mean 88.0 MB, min 83.2 MB, max 93.5 MB        
        "TTToHplusBHminusB_M160_Summer12":        TaskDef("/TTToHplusBHminusB_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),

        # 10275-17098 events 40-41 jobs
        # User mean 709.9, min 33.7, max 973.2
        # Mean 28.6 MB, min 1.6 MB, max 33.9 MB
        "Hplus_taunu_s-channel_M80_Summer12":     TaskDef("/Hplus_taunu_s-channel_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # Mean 28.0 MB, min 1.6 MB, max 31.6 MB
        # User mean 672.5, min 31.9, max 856.0
        "Hplus_taunu_s-channel_M90_Summer12":     TaskDef("/Hplus_taunu_s-channel_M-90_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 782.6, min 69.8, max 1038.3
        # Mean 31.7 MB, min 2.8 MB, max 36.1 MB
        "Hplus_taunu_s-channel_M100_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 752.7, min 87.9, max 950.5
        # Mean 29.7 MB, min 2.8 MB, max 35.7 MB
        "Hplus_taunu_s-channel_M120_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 966.4, min 724.2, max 1137.2
        # Mean 39.9 MB, min 36.1 MB, max 43.4 MB
        "Hplus_taunu_s-channel_M140_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 995.3, min 62.8, max 1188.5
        # Mean 41.5 MB, min 2.6 MB, max 45.4 MB
        "Hplus_taunu_s-channel_M150_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 886.9, min 63.4, max 1216.1
        # Mean 40.5 MB, min 2.8 MB, max 45.6 MB
        "Hplus_taunu_s-channel_M155_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # User mean 1111.6, min 885.4, max 1424.6
        # Mean 46.9 MB, min 42.2 MB, max 50.2 MB
        "Hplus_taunu_s-channel_M160_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),

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
        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDef("/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 2749 events, 22 jobs
        # User mean 1422.9, min 244.0, max 2176.0
        # Mean 19.2 MB, min 4.7 MB, max 22.1 MB
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDef("/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
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
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 797355 events, 305 jobs
        # User mean 6733.4, min 737.7, max 17064.5
        # Mean 258.6 MB, min 27.0 MB, max 276.6 MB
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 616204 events, 251 jobs
        # User mean 5354.8, min 1467.4, max 8339.4
        # Mean 258.3 MB, min 85.4 MB, max 272.3 MB
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1b-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 359260 events, 151 jobs
        # User mean 5180.3, min 948.1, max 7609.2
        # Mean 250.5 MB, min 58.2 MB, max 265.4 MB
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 2045846 events, 854 jobs
        # User mean 5627.8, min 252.5, max 21303.3
        # Mean 252.4 MB, min 19.4 MB, max 269.9 MB
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v3/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),

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
        "WJets_TuneZ2star_v1_Summer12":           TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 285149 events, 257 jobs
        # User mean 3017.1, min 231.8, max 5345.6
        # Mean 99.3 MB, min 6.2 MB, max 110.6 MB
        "WJets_TuneZ2star_v2_Summer12":           TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
        # 203841 events, 154 jobs
        # User mean 2991.6, min 97.7, max 3952.6
        # Mean 107.9 MB, min 5.8 MB, max 117.0 MB
        "W1Jets_TuneZ2star_Summer12":             TaskDef("/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
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
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDef("/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1-cad8d1056ca20d363262a3efa1d97a74/USER"),
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

# Add v53_2_test1 pattuples
def addPattuple_v53_2_test1(datasets):
    definitions = {
        # 258977 events, 123 jobs
        # User mean 2905.2, min 890.5, max 8800.0
        # Mean 63.9 MB, min 32.9 MB, max 137.7 MB
        "Tau_198022-198523_2012C_Aug24":          TaskDef("/Tau/local-Run2012C_24Aug2012_v1_AOD_pattuple_v53_2_198022_198523_test1-63ff13540867be423a0bd89ddcd239a1/USER"),
        # 697510 events, 144 files
        # User mean 8802.5, min 2592.2, max 21963.7
        # Mean 151.7 MB, min 64.1 MB, max 268.8 MB
        "MultiJet_198022-198523_2012C_Aug24":     TaskDef("/MultiJet/local-Run2012C_24Aug2012_v1_AOD_pattuple_v53_2_198022_198523_test1-389fad6151d6b75810dbdb3bf32c8d9d/USER"),
        # 1410641 events, 231 jobs
        # User mean 7468.0, min 495.3, max 25221.8
        # Sys mean 67.8, min 8.4, max 308.3
        "BJetPlusX_193834-194225_2012B_Jul13":    TaskDef("/BJetPlusX/local-Run2012B_13Jul2012_v1_AOD_pattuple_v53_2_193834_194225_test1-7015323d816155eb71c1e8ab78d8837b/USER"),
        "BJetPlusX_198022-198523_2012C_Aug24":    TaskDef(""),
        # 32322 events, 26 jobs
        # User mean 2502.9, min 55.3, max 3725.0
        # Mean 125.7 MB, min 3.1 MB, max 140.0 MB
        "TTToHplusBWB_M120_Summer12":             TaskDef("/TTToHplusBWB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2_test1-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        }

    addPattuple_53X("v53_2_test1", datasets, definitions)

# Add v53_2 pattuples
def addPattuple_v53_2(datasets):
    definitions = {
        # 64775 events, 29 jobs
        # User mean 2880.0, min 985.5, max 6794.1
        # Mean 68.3 MB, min 27.5 MB, max 151.2 MB
        "Tau_190456-190738_2012A_Jul13":          TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_190456_190738_pattuple_v53_2-d6c479cdacadf9e72633682fc77c0fc4/USER"),
        # 42028 events, 8 jobs
        # User mean 8373.0, min 2478.8, max 20373.6
        # Mean 146.2 MB, min 50.0 MB, max 256.8 MB
        "Tau_190782-190949_2012A_Aug06":          TaskDef("/Tau/local-Run2012A_recover_06Aug2012_v1_AOD_190782_190949_pattuple_v53_2-88bdb8e31f6a701f5e5563abbcbd8630/USER"),
        # 368031 events, 107 jobs
        # User mean 4282.8, min 770.2, max 8915.1
        # Mean 96.7 MB, min 29.4 MB, max 180.0 MB
        "Tau_191043-193621_2012A_Jul13":          TaskDef("/Tau/local-Run2012A_13Jul2012_v1_AOD_191043_193621_pattuple_v53_2-e0f8e15ebf177c49a6b3565fa4b6cbb8/USER"),
        # 2825568 events, 1874 jobs
        # User mean 2226.8, min 813.9, max 12132.1
        # Mean 48.5 MB, min 26.9 MB, max 195.3 MB
        "Tau_193834-196531_2012B_Jul13":          TaskDef("/Tau/local-Run2012B_13Jul2012_v1_AOD_193834_196531_pattuple_v53_2-f88f39237c4ee9f8411ea24cf417c4a9/USER"),
        # 258977 events, 123 jobs
        # User mean 3012.3, min 1069.0, max 7764.0
        # Mean 63.9 MB, min 32.9 MB, max 137.7 MB
        "Tau_198022-198523_2012C_Aug24":          TaskDef("/Tau/local-Run2012C_24Aug2012_v1_AOD_198022_198523_pattuple_v53_2-63ff13540867be423a0bd89ddcd239a1/USER"),
        # 3498600 events, 2528 jobs
        # User mean 2067.9, min 32.9, max 9247.3
        # Mean 46.9 MB, min 1.5 MB, max 132.6 MB
        "Tau_198941-202504_2012C_Prompt":         TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_198941_202504_pattuple_v53_2-a079709b0a63f90c6fd5ddd5289cac55/USER"),
        # 78436 events, 59 jobs
        # User mean 1855.6, min 910.6, max 3013.3
        # Mean 46.3 MB, min 26.5 MB, max 61.4 MB
        "Tau_201191-201191_2012C_Dec11":          TaskDef("/Tau/local-Run2012C_EcalRecover_11Dec2012_v1_AOD_201191_201191_pattuple_v53_2-b9a73c53e978690eb378ac4dcef39d09/USER"),
        # 166145 events, 111 jobs
        # User mean 2118.7, min 736.8, max 4259.3
        # Mean 49.7 MB, min 19.6 MB, max 61.2 MB
        "Tau_202972-203742_2012C_Prompt":         TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_202972_203742_pattuple_v53_2-9919151a95171e2529c62b18141b7812/USER"),
        # 5239163 events, 3496 jobs
        # User mean 2532.2, min 28.1, max 15577.7
        # Mean 51.8 MB, min 1.6 MB, max 258.8 MB
        "Tau_203777-208686_2012D_Prompt":         TaskDef("/Tau/local-Run2012D_PromptReco_v1_AOD_203777_208686_pattuple_v53_2-9919151a95171e2529c62b18141b7812/USER"),

        # 466504 events, 303 jobs
        # User mean 3830.4, min 86.0, max 11200.2
        # Mean 49.2 MB, min 2.3 MB, max 128.2 MB
        "MultiJet_190456-190738_2012A_Jul13":     TaskDef("/MultiJet/local-Run2012A_13Jul2012_v1_AOD_190456_190738_pattuple_v53_2-96fa41b5518123a49a7bd0a10242f655/USER"),
        # 313212 events, 87 jobs
        # User mean 9209.7, min 1136.1, max 11791.8
        # Mean 106.2 MB, min 23.0 MB, max 134.5 MB
        "MultiJet_190782-190949_2012A_Aug06":     TaskDef("/MultiJet/local-Run2012A_recover_06Aug2012_v1_AOD_190782_190949_pattuple_v53_2-bb265e7302d9b49716536ffced4d3f49/USER"),
        # 2954598 events, 741 jobs
        # User mean 10021.1, min 101.0, max 16330.2
        # Mean 112.7 MB, min 1.6 MB, max 178.4 MB
        "MultiJet_191043-193621_2012A_Jul13":     TaskDef("/MultiJet/local-Run2012A_13Jul2012_v1_AOD_191043_193621_pattuple_v53_2-64312c92df34a8b6e9825d5a9e1bcc2b/USER"),
        # 798715 events, 355 jobs
        # User mean 5707.0, min 47.1, max 13716.8
        # Mean 72.5 MB, min 1.9 MB, max 170.1 MB
        "MultiJet_193834-194225_2012B_Jul13":     TaskDef("/MultiJet/local-Run2012B_13Jul2012_v1_AOD_193834_194225_pattuple_v53_2-e3b0bb8440b8da4278373fdaf94275dd/USER"),
        # 5623320 events, 1492 jobs
        # User mean 9233.1, min 781.7, max 15737.5
        # Mean 123.1 MB, min 12.0 MB, max 184.0 MB
        "MultiJet_194270-196531_2012B_Jul13":     TaskDef("/MultiJet/local-Run2012B_13Jul2012_v1_AOD_194270_196531_pattuple_v53_2-7c9474a941817679a02e1d102c31cfd3/USER"),
        # 697510 events, 180 jobs
        # User mean 6095.4, min 2322.4, max 25521.5
        # Mean 123.3 MB, min 56.2 MB, max 167.5 MB
        "MultiJet_198022-198523_2012C_Aug24":     TaskDef("/MultiJet/local-Run2012C_24Aug2012_v1_AOD_198022_198523_pattuple_v53_2-389fad6151d6b75810dbdb3bf32c8d9d/USER"),
        # 9269418 events, 2631 jobs
        # User mean 5685.4, min 29.8, max 23573.2
        # Mean 116.1 MB, min 1.5 MB, max 207.0 MB
        "MultiJet_198941-203742_2012C_Prompt":    TaskDef("/MultiJet/local-Run2012C_PromptReco_v2_AOD_198941_203742_pattuple_v53_2-94a08ec1d35323f7ecbc0315d255c89f/USER"),
        # 10483973 events, 3406 jobs
        # User mean 5007.4, min 25.8, max 14880.7
        # Mean 105.9 MB, min 1.6 MB, max 208.5 MB
        "MultiJet_203777-208686_2012D_Prompt":    TaskDef("/MultiJet/local-Run2012D_PromptReco_v1_AOD_203777_208686_pattuple_v53_2-05231082982f84c324e0b5a0459a13ec/USER"),

        # 1410641 events, 322 jobs
        # User mean 5481.3, min 155.8, max 12547.0
        # Mean 113.3 MB, min 5.4 MB, max 161.5 MB
        "BJetPlusX_193834-194225_2012B_Jul13":    TaskDef("/BJetPlusX/local-Run2012B_13Jul2012_v1_AOD_193834_194225_pattuple_v53_2-7015323d816155eb71c1e8ab78d8837b/USER"),
        # 5490992 events, 1987 jobs
        # User mean 3690.8, min 190.4, max 14455.0
        # Mean 78.7 MB, min 7.2 MB, max 128.4 MB
        "BJetPlusX_194270-196531_2012B_Jul13":    TaskDef("/BJetPlusX/local-Run2012B_13Jul2012_v1_AOD_194270_196531_pattuple_v53_2-faed90fb0d556327eb3d97d0f51eda56/USER"),
        # 601483 events, 276 jobs
        # User mean 2706.4, min 1093.7, max 7827.4
        # Mean 63.3 MB, min 13.5 MB, max 104.2 MB
        "BJetPlusX_198022-198523_2012C_Aug24":    TaskDef("/BJetPlusX/local-Run2012C_24Aug2012_v2_AOD_198022_198523_pattuple_v53_2-0151fff8069c712325474b9273eb8f16/USER"),
        # 8162590 events, 3225 jobs
        # User mean 3456.8, min 22.1, max 12126.7
        # Mean 73.4 MB, min 1.5 MB, max 138.1 MB
        "BJetPlusX_198941-203742_2012C_Prompt":   TaskDef("/BJetPlusX/local-Run2012C_PromptReco_v2_AOD_198941_203742_pattuple_v53_2-56d78678cf2082b71cbc845a1eb5b3d8/USER"),
        # 161224 events, 76 jobs
        # User mean 3832.7, min 1380.0, max 10219.6
        # Mean 64.8 MB, min 37.6 MB, max 94.6 MB
        "BJetPlusX_201191-201191_2012C_Dec11":    TaskDef("/BJetPlusX/local-Run2012C_EcalRecover_11Dec2012_v1_AOD_201191_201191_pattuple_v53_2-3a3b7e72eb1ebaba962c79a446e93dc1/USER"),
        # 9122210 events, 4180 jobs
        # User mean 3361.6, min 23.1, max 12128.2
        # Mean 66.7 MB, min 1.6 MB, max 133.7 MB
        "BJetPlusX_203777-208686_2012D_Prompt":   TaskDef("/BJetPlusX/local-Run2012D_PromptReco_v1_AOD_203777_208686_pattuple_v53_2-f6bb0dc7e2833904d68de61382eb29fb/USER"),

        #### Winter13 Reprocessing
        "Tau_190456-193621_2012A_Jan22":       TaskDef(""),
        "TauParked_193834-196531_2012B_Jan22": TaskDef(""),
        "TauParked_198022-202504_2012C_Jan22": TaskDef(""),
        "TauParked_202972-203742_2012C_Jan22": TaskDef(""),
        "TauParked_203777-208686_2012D_Jan22": TaskDef(""),
        
        # 27900-37203 events, 26 jobs
        # User mean 3088.7, min 39.2, max 3945.0
        # Mean 121.2 MB, min 1.8 MB, max 131.3 MB
        "TTToHplusBWB_M80_Summer12":              TaskDef("/TTToHplusBWB_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 2819.1, min 1007.5, max 4537.5
        # Mean 127.6 MB, min 54.1 MB, max 142.3 MB
        "TTToHplusBWB_M90_Summer12":              TaskDef("/TTToHplusBWB_M-90_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 2400.1, min 58.6, max 3971.3
        # Mean 111.0 MB, min 3.3 MB, max 120.2 MB
        "TTToHplusBWB_M100_Summer12":             TaskDef("/TTToHplusBWB_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 3009.3, min 93.4, max 4563.6
        # Mean 125.7 MB, min 3.1 MB, max 140.0 MB
        "TTToHplusBWB_M120_Summer12":             TaskDef("/TTToHplusBWB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 2642.3, min 99.6, max 3547.9
        # Mean 130.0 MB, min 6.6 MB, max 140.4 MB
        "TTToHplusBWB_M140_Summer12":             TaskDef("/TTToHplusBWB_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 3073.6, min 679.5, max 4538.8
        # Mean 129.7 MB, min 48.7 MB, max 144.5 MB
        "TTToHplusBWB_M150_Summer12":             TaskDef("/TTToHplusBWB_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 2492.0, min 479.0, max 4742.4
        # Mean 135.9 MB, min 34.7 MB, max 145.7 MB
        "TTToHplusBWB_M155_Summer12":             TaskDef("/TTToHplusBWB_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 2836.7, min 1109.9, max 4872.8
        # Mean 138.0 MB, min 68.1 MB, max 152.4 MB
        "TTToHplusBWB_M160_Summer12":             TaskDef("/TTToHplusBWB_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),

        # 161556 events, 131 jobs
        # User mean 3276.7, min 1075.1, max 3911.0
        # Mean 126.4 MB, min 44.4 MB, max 134.4 MB
        "TTToHplusBWB_M80_ext_Summer12":          TaskDef("/TTToHplusBWB_M-80_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 161137 events, 131 jobs
        # User mean 3203.0, min 71.1, max 4041.8
        # Mean 125.9 MB, min 3.8 MB, max 134.1 MB
        "TTToHplusBWB_M90_ext_Summer12":          TaskDef("/TTToHplusBWB_M-90_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 1000000 events, 701 jobs
        # User mean 3288.1, min 1926.8, max 4003.2
        # Mean 134.7 MB, min 84.6 MB, max 137.8 MB
        "TTToHplusBWB_M100_ext_Summer12":         TaskDef("/TTToHplusBWB_M-100_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-4aeb6d67b2b548103b549e3eeece455e/USER", args={"triggerMC": 0}, njobsIn=700), # non-triggered because of trigger studies
        # 163630 events, 131 jobs
        # User mean 3144.5, min 99.0, max 3822.9
        # Mean 126.3 MB, min 4.2 MB, max 134.9 MB
        "TTToHplusBWB_M120_ext_Summer12":         TaskDef("/TTToHplusBWB_M-120_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 170489 events, 131 jobs
        # User mean 3185.7, min 99.3, max 4059.5
        # Mean 129.0 MB, min 4.0 MB, max 139.7 MB
        "TTToHplusBWB_M140_ext_Summer12":         TaskDef("/TTToHplusBWB_M-140_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 177525 events, 132 jobs
        # User mean 3211.2, min 599.8, max 3991.2
        # Mean 131.5 MB, min 25.0 MB, max 143.7 MB
        "TTToHplusBWB_M150_ext_Summer12":         TaskDef("/TTToHplusBWB_M-150_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 181562 events, 131 jobs
        # User mean 3391.5, min 1268.5, max 4154.4
        # Mean 134.4 MB, min 47.4 MB, max 143.2 MB
        "TTToHplusBWB_M155_ext_Summer12":         TaskDef("/TTToHplusBWB_M-155_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 1000000 events, 701 jobs
        # User mean 3148.3, min 967.6, max 3922.2
        # Mean 129.2 MB, min 52.4 MB, max 131.2 MB
        "TTToHplusBWB_M160_ext_Summer12":         TaskDef("/TTToHplusBWB_M-160_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-4aeb6d67b2b548103b549e3eeece455e/USER", args={"triggerMC": 0}, njobsIn=700), # non-triggered because of trigger studies

        # 29908 events, 20 jobs
        # User mean 2966.4, min 2333.4, max 3945.0
        # Mean 145.9 MB, min 142.0 MB, max 151.0 MB
        "TTToHplusBHminusB_M80_Summer12":         TaskDef("/TTToHplusBHminusB_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 150959 events, 103 jobs
        # User mean 2908.2, min 332.9, max 5217.2
        # Mean 142.3 MB, min 22.7 MB, max 155.5 MB
        "TTToHplusBHminusB_M90_Summer12":         TaskDef("/TTToHplusBHminusB_M-90_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 30519 events, 20 jobs
        # User mean 3089.0, min 2293.1, max 5207.5
        # Mean 146.7 MB, min 138.7 MB, max 152.0 MB
        "TTToHplusBHminusB_M100_Summer12":        TaskDef("/TTToHplusBHminusB_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 32124 events, 21 jobs
        # User mean 3790.0, min 1929.9, max 4267.6
        # Mean 144.3 MB, min 76.2 MB, max 158.1 MB
        "TTToHplusBHminusB_M120_Summer12":        TaskDef("/TTToHplusBHminusB_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 34757 events, 20 jobs
        # User mean 2751.5, min 2383.8, max 3461.2
        # Mean 156.3 MB, min 152.0 MB, max 160.3 MB
        "TTToHplusBHminusB_M140_Summer12":        TaskDef("/TTToHplusBHminusB_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 36640 events, 21 jobs
        # User mean 3385.1, min 1176.1, max 4137.0
        # Mean 153.0 MB, min 66.4 MB, max 165.4 MB
        "TTToHplusBHminusB_M150_Summer12":        TaskDef("/TTToHplusBHminusB_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 38331 events, 20 jobs
        # User mean 3470.7, min 2979.6, max 4129.5
        # Mean 164.0 MB, min 158.4 MB, max 171.1 MB
        "TTToHplusBHminusB_M155_Summer12":        TaskDef("/TTToHplusBHminusB_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 40068 events, 20 jobs
        # User mean 4207.9, min 3292.0, max 4553.6
        # Mean 167.5 MB, min 160.2 MB, max 172.5 MB
        "TTToHplusBHminusB_M160_Summer12":        TaskDef("/TTToHplusBHminusB_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),

        # 149497-200005 events 100-101 jobs
        # User mean 3598.3, min 2808.1, max 4648.3
        # Mean 145.6 MB, min 135.5 MB, max 152.6 MB
        "TTToHplusBHminusB_M80_ext_Summer12":     TaskDef("/TTToHplusBHminusB_M-80_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 3560.6, min 2881.7, max 4484.7
        # Mean 147.7 MB, min 140.5 MB, max 154.9 MB
        "TTToHplusBHminusB_M100_ext_Summer12":    TaskDef("/TTToHplusBHminusB_M-100_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 3380.5, min 1115.8, max 4625.8
        # Mean 149.3 MB, min 58.6 MB, max 160.1 MB
        "TTToHplusBHminusB_M120_ext_Summer12":    TaskDef("/TTToHplusBHminusB_M-120_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 3445.0, min 886.7, max 4646.1
        # Mean 155.5 MB, min 48.5 MB, max 166.9 MB
        "TTToHplusBHminusB_M140_ext_Summer12":    TaskDef("/TTToHplusBHminusB_M-140_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 3788.5, min 3104.2, max 4775.1
        # Mean 160.8 MB, min 152.3 MB, max 171.8 MB
        "TTToHplusBHminusB_M150_ext_Summer12":    TaskDef("/TTToHplusBHminusB_M-150_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 3934.4, min 3103.4, max 4936.5
        # Mean 163.4 MB, min 156.1 MB, max 172.7 MB
        "TTToHplusBHminusB_M155_ext_Summer12":    TaskDef("/TTToHplusBHminusB_M-155_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 3922.3, min 3215.1, max 5121.4
        # Mean 167.3 MB, min 159.4 MB, max 177.7 MB
        "TTToHplusBHminusB_M160_ext_Summer12":    TaskDef("/TTToHplusBHminusB_M-160_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),

        # 826-927 events, 29 jobs
        # User mean 245.3, min 211.0, max 310.3
        # Mean 7.4 MB, min 6.2 MB, max 8.3 MB
        "Hplus_taunu_t-channel_M80_Summer12":     TaskDef("/Hplus_taunu_t-channel_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 238.4, min 170.1, max 295.2
        # Mean 7.5 MB, min 6.1 MB, max 9.1 MB
        "Hplus_taunu_t-channel_M90_Summer12":     TaskDef("/Hplus_taunu_t-channel_M-90_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 247.9, min 151.8, max 315.6
        # Mean 7.4 MB, min 6.1 MB, max 8.6 MB
        "Hplus_taunu_t-channel_M100_Summer12":    TaskDef("/Hplus_taunu_t-channel_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 224.3, min 174.3, max 310.3
        # Mean 7.4 MB, min 6.3 MB, max 8.4 MB
        "Hplus_taunu_t-channel_M120_Summer12":    TaskDef("/Hplus_taunu_t-channel_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 226.7, min 151.8, max 295.6
        # Mean 7.4 MB, min 6.0 MB, max 8.3 MB
        "Hplus_taunu_t-channel_M140_Summer12":    TaskDef("/Hplus_taunu_t-channel_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 249.2, min 175.2, max 296.5
        # Mean 7.6 MB, min 6.1 MB, max 9.0 MB
        "Hplus_taunu_t-channel_M150_Summer12":    TaskDef("/Hplus_taunu_t-channel_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 236.5, min 151.9, max 295.2
        # Mean 7.2 MB, min 6.1 MB, max 8.7 MB
        "Hplus_taunu_t-channel_M155_Summer12":    TaskDef("/Hplus_taunu_t-channel_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 223.6, min 174.5, max 293.8
        # Mean 7.1 MB, min 5.6 MB, max 8.3 MB
        "Hplus_taunu_t-channel_M160_Summer12":    TaskDef("/Hplus_taunu_t-channel_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),

        # 5359-8604 events, 21 jobs
        # User mean 628.0, min 36.2, max 880.0
        # Mean 27.8 MB, min 1.8 MB, max 32.7 MB
        "Hplus_taunu_tW-channel_M80_Summer12":    TaskDef("/Hplus_taunu_tW-channel_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 633.2, min 33.5, max 850.2
        # Mean 28.0 MB, min 1.8 MB, max 32.7 MB
        "Hplus_taunu_tW-channel_M90_Summer12":    TaskDef("/Hplus_taunu_tW-channel_M-90_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 616.8, min 36.8, max 805.1
        # Mean 28.3 MB, min 1.8 MB, max 31.9 MB
        "Hplus_taunu_tW-channel_M100_Summer12":   TaskDef("/Hplus_taunu_tW-channel_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 674.9, min 29.5, max 888.0
        # Mean 29.9 MB, min 1.8 MB, max 33.1 MB
        "Hplus_taunu_tW-channel_M120_Summer12":   TaskDef("/Hplus_taunu_tW-channel_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 714.8, min 91.4, max 923.6
        # Mean 33.5 MB, min 3.2 MB, max 39.2 MB
        "Hplus_taunu_tW-channel_M140_Summer12":   TaskDef("/Hplus_taunu_tW-channel_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 768.1, min 37.1, max 1032.9
        # Mean 36.0 MB, min 1.8 MB, max 42.5 MB
        "Hplus_taunu_tW-channel_M150_Summer12":   TaskDef("/Hplus_taunu_tW-channel_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 810.1, min 60.4, max 1082.4
        # Mean 38.0 MB, min 3.0 MB, max 44.0 MB
        "Hplus_taunu_tW-channel_M155_Summer12":   TaskDef("/Hplus_taunu_tW-channel_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 817.2, min 79.1, max 1123.2
        # Mean 39.7 MB, min 3.0 MB, max 44.6 MB
        "Hplus_taunu_tW-channel_M160_Summer12":   TaskDef("/Hplus_taunu_tW-channel_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),

        # 10275-19941 events, 10-11 jobs
        # User mean 2374.2, min 36.3, max 3075.3
        # Mean 89.3 MB, min 1.8 MB, max 100.6 MB
        "Hplus_taunu_s-channel_M80_Summer12":     TaskDef("/Hplus_taunu_s-channel_M-80_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 2019.3, min 29.4, max 2733.2
        # Mean 87.6 MB, min 1.8 MB, max 100.9 MB
        "Hplus_taunu_s-channel_M90_Summer12":     TaskDef("/Hplus_taunu_s-channel_M-90_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 2279.0, min 27.6, max 3425.2
        # Mean 99.9 MB, min 1.8 MB, max 113.5 MB
        "Hplus_taunu_s-channel_M100_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-100_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 2139.6, min 62.2, max 2998.0
        # Mean 93.0 MB, min 3.1 MB, max 106.9 MB
        "Hplus_taunu_s-channel_M120_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-120_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 2976.8, min 2783.6, max 3104.8
        # Mean 132.8 MB, min 126.1 MB, max 136.9 MB
        "Hplus_taunu_s-channel_M140_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-140_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 3272.4, min 60.8, max 4251.2
        # Mean 130.6 MB, min 3.1 MB, max 148.3 MB
        "Hplus_taunu_s-channel_M150_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-150_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 3375.9, min 82.4, max 4035.7
        # Mean 126.2 MB, min 3.1 MB, max 144.8 MB
        "Hplus_taunu_s-channel_M155_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-155_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # User mean 3882.1, min 3424.9, max 4833.8
        # Mean 161.3 MB, min 157.3 MB, max 167.2 MB
        "Hplus_taunu_s-channel_M160_Summer12":    TaskDef("/Hplus_taunu_s-channel_M-160_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),

        # 53759 events, 40 jobs
        # User mean 2818.3, min 2013.9, max 4622.8
        # Mean 134.6 MB, min 126.2 MB, max 142.5 MB
        "HplusTB_M180_Summer12":                  TaskDef("/HplusTB_M-180_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 56058 events, 40 jobs
        # User mean 2701.6, min 2153.2, max 4746.6
        # Mean 140.4 MB, min 133.0 MB, max 147.4 MB
        "HplusTB_M190_Summer12":                  TaskDef("/HplusTB_M-190_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 58635 events, 43 jobs
        # User mean 2820.5, min 305.6, max 4863.1
        # Mean 136.8 MB, min 17.6 MB, max 152.2 MB
        "HplusTB_M200_Summer12":                  TaskDef("/HplusTB_M-200_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 63283 events, 40 jobs
        # User mean 2978.8, min 2384.7, max 4266.5
        # Mean 156.7 MB, min 147.2 MB, max 163.8 MB
        "HplusTB_M220_Summer12":                  TaskDef("/HplusTB_M-220_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 69529 events, 40 jobs
        # User mean 3291.4, min 2931.1, max 3533.9
        # Mean 171.5 MB, min 161.9 MB, max 181.4 MB
        "HplusTB_M250_Summer12":                  TaskDef("/HplusTB_M-250_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 78988 events, 40 jobs
        # User mean 3694.7, min 3437.9, max 4124.1
        # Mean 193.3 MB, min 186.6 MB, max 199.1 MB
        "HplusTB_M300_Summer12":                  TaskDef("/HplusTB_M-300_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 998572 events, 701 jobs
        # User mean 3185.2, min 1088.1, max 4080.3
        # Mean 139.7 MB, min 45.5 MB, max 141.8 MB
        "HplusTB_M400_Summer12":                  TaskDef("/HplusTB_M-400_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-4aeb6d67b2b548103b549e3eeece455e/USER", args={"triggerMC": 0}, njobsIn=700), # non-triggered because of trigger studies
        # 509436 events, 250 jobs
        # User mean 4928.8, min 3381.8, max 6023.5
        # Mean 201.5 MB, min 194.3 MB, max 210.5 MB
        "HplusTB_M500_Summer12":                  TaskDef("/HplusTB_M-500_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 539226 events, 252 jobs
        # User mean 4862.5, min 1461.5, max 6403.1
        # Mean 212.8 MB, min 76.4 MB, max 221.9 MB
        "HplusTB_M600_Summer12":                  TaskDef("/HplusTB_M-600_8TeV-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),

        # 269775 events, 202 jobs
        # User mean 2952.3, min 131.2, max 3759.4
        # Mean 133.6 MB, min 8.4 MB, max 145.3 MB
        "HplusTB_M180_ext_Summer12":              TaskDef("/HplusTB_M-180_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 281879 events, 202 jobs
        # User mean 3362.5, min 219.8, max 4410.7
        # Mean 139.9 MB, min 11.9 MB, max 148.4 MB
        "HplusTB_M190_ext_Summer12":              TaskDef("/HplusTB_M-190_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 1000000 events, 701 jobs
        # User mean 3126.0, min 1532.5, max 4009.7
        # Mean 135.4 MB, min 78.8 MB, max 138.5 MB
        "HplusTB_M200_ext_Summer12":              TaskDef("/HplusTB_M-200_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-4aeb6d67b2b548103b549e3eeece455e/USER", args={"triggerMC": 0}, njobsIn=700), # non-triggered because of trigger studies
        # 316737 events, 201 jobs
        # User mean 3660.6, min 2308.1, max 4752.9
        # Mean 156.2 MB, min 83.4 MB, max 167.6 MB
        "HplusTB_M220_ext_Summer12":              TaskDef("/HplusTB_M-220_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 346926 events, 202 jobs
        # User mean 4063.7, min 551.8, max 5114.0
        # Mean 169.4 MB, min 22.5 MB, max 179.5 MB
        "HplusTB_M250_ext_Summer12":              TaskDef("/HplusTB_M-250_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 393867 events, 202 jobs
        # User mean 4511.1, min 1071.5, max 5899.8
        # Mean 191.0 MB, min 48.9 MB, max 202.9 MB
        "HplusTB_M300_ext_Summer12":              TaskDef("/HplusTB_M-300_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),

        # 114 events, 10 jobs
        # User mean 2256.7, min 62.0, max 5285.2
        # Mean 10.6 MB, min 1.8 MB, max 19.5 MB
        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDef("/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 2749 events, 6 jobs
        # User mean 5556.9, min 2573.1, max 6896.6
        # Mean 59.8 MB, min 38.2 MB, max 72.6 MB
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDef("/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 21951 events, 16 jobs
        # User mean 5555.9, min 1738.5, max 10883.7
        # Mean 130.0 MB, min 45.7 MB, max 145.8 MB
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDef("/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 75972 events, 41 jobs
        # User mean 6147.3, min 3727.1, max 7998.0
        # Mean 173.4 MB, min 101.5 MB, max 184.2 MB
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDef("/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v3_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 232796 events, 132 jobs
        # User mean 5356.3, min 472.1, max 6645.2
        # Mean 171.8 MB, min 14.8 MB, max 183.5 MB
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 797355 events, 455 jobs
        # User mean 4847.2, min 221.1, max 7270.5
        # Mean 170.7 MB, min 11.2 MB, max 185.1 MB
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDef("/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 616204 events, 352 jobs
        # User mean 5048.7, min 1212.5, max 6511.6
        # Mean 180.2 MB, min 52.3 MB, max 190.9 MB
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 359260 events, 201 jobs
        # User mean 5247.8, min 1524.5, max 6497.3
        # Mean 183.6 MB, min 56.3 MB, max 195.6 MB
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v2/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 2045846 events, 1103 jobs
        # User mean 4162.6, min 1022.5, max 9087.8
        # Mean 190.0 MB, min 67.4 MB, max 205.6 MB
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDef("/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v3/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),

        # 288671 events, 152 jobs
        # User mean 6255.7, min 183.6, max 7420.5
        # Mean 160.3 MB, min 4.9 MB, max 169.8 MB
        "WW_TuneZ2star_Summer12":                 TaskDef("/WW_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 256016 events, 153 jobs
        # User mean 3963.0, min 331.7, max 4775.4
        # Mean 146.6 MB, min 11.8 MB, max 158.5 MB
        "WZ_TuneZ2star_Summer12":                 TaskDef("/WZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 201924 events, 157 jobs
        # User mean 2545.7, min 107.3, max 5287.7
        # Mean 117.5 MB, min 5.0 MB, max 131.5 MB
        "ZZ_TuneZ2star_Summer12":                 TaskDef("/ZZ_TuneZ2star_8TeV_pythia6_tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 1202301 events, 702 jobs
        # User mean 4630.4, min 194.2, max 8979.0
        # Mean 180.7 MB, min 8.5 MB, max 194.8 MB
        "TTJets_TuneZ2star_Summer12":             TaskDef("/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 94009 events, 54 jobs
        # User mean 4631.8, min 941.0, max 5429.7
        # Mean 146.1 MB, min 31.9 MB, max 161.8 MB
        "WJets_TuneZ2star_v1_Summer12":           TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 293346 events, 159 jobs
        # User mean 4884.2, min 109.2, max 8726.8
        # Mean 154.2 MB, min 3.5 MB, max 173.2 MB
        "WJets_TuneZ2star_v2_Summer12":           TaskDef("/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v2_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 203841 events, 104 jobs
        # User mean 4439.8, min 129.9, max 6353.7
        # Mean 155.1 MB, min 6.2 MB, max 167.9 MB
        "W1Jets_TuneZ2star_Summer12":             TaskDef("/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 752423 events, 407 jobs
        # User mean 3811.3, min 172.1, max 5520.3
        # Mean 153.4 MB, min 7.5 MB, max 167.3 MB
        "W2Jets_TuneZ2star_Summer12":             TaskDef("/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 616480 events, 405 jobs
        # User mean 3544.5, min 224.7, max 5038.7
        # Mean 137.0 MB, min 10.9 MB, max 148.6 MB
        "W3Jets_TuneZ2star_Summer12":             TaskDef("/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 1002056 events, 551 jobs
        # User mean 4149.8, min 1628.0, max 5963.6
        # Mean 175.9 MB, min 75.7 MB, max 190.8 MB
        "W4Jets_TuneZ2star_Summer12":             TaskDef("/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 180247 events, 154 jobs
        # User mean 3078.3, min 164.5, max 5440.6
        # Mean 109.2 MB, min 8.9 MB, max 121.4 MB
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDef("/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 4476 events, 52 jobs
        # User mean 2361.3, min 39.6, max 4732.1
        # Mean 21.5 MB, min 1.8 MB, max 29.5 MB
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDef("/DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 222877 events, 101 jobs
        # User mean 6768.9, min 3945.2, max 9596.4
        # Mean 199.9 MB, min 120.3 MB, max 212.8 MB
        "T_t-channel_TuneZ2star_Summer12":        TaskDef("/T_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 105825 events, 51 jobs
        # User mean 5481.5, min 73.0, max 8899.8
        # Mean 187.8 MB, min 3.2 MB, max 198.8 MB
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDef("/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 61356 events, 31 jobs
        # User mean 4256.4, min 89.2, max 8144.4
        # Mean 192.8 MB, min 3.2 MB, max 207.7 MB
        "T_tW-channel_TuneZ2star_Summer12":       TaskDef("/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 60272 events, 32 jobs
        # User mean 3882.0, min 242.3, max 7997.9
        # Mean 184.1 MB, min 13.0 MB, max 202.6 MB
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDef("/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 11203 events, 11 jobs
        # User mean 3590.6, min 40.1, max 5250.9
        # Mean 100.7 MB, min 1.8 MB, max 114.1 MB
        "T_s-channel_TuneZ2star_Summer12":        TaskDef("/T_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        # 5345 events, 6 jobs
        # User mean 2658.4, min 39.4, max 3610.0
        # Mean 86.9 MB, min 1.8 MB, max 106.2 MB
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDef("/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/local-Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_2-f3f6db3988d554ca655ef290b2e69c3e/USER"),
        }

    addPattuple_53X("v53_2", datasets, definitions)

def addPattuple_v53_3_test1(datasets):
    definitions = {
        # 163630 events, 91 jobs
        # User mean 5026.9, min 28.5, max 6298.7
        # Mean 180.8 MB, min 1.8 MB, max 191.6 MB
        "TTToHplusBWB_M120_ext_Summer12":         TaskDef("/TTToHplusBWB_M-120_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_3_test1-bcf1eb633671b514e9c5d99b6a7d2ccb/USER"),
        # 3498600 events, 1703 jobs
        # User mean 3597.1, min 220.1, max 26645.1
        # Mean 65.6 MB, min 4.1 MB, max 276.5 MB
        "Tau_198941-202504_2012C_Prompt":         TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_pattuple_v53_3_198941_202504_test1-924ba6f2695898f1942a58457f274ada/USER"),
        }

    addPattuple_53X("v53_3_test1", datasets, definitions)


def addPattuple_v53_3_test2(datasets):
    # Same as test1, except START53_V15 GT
    definitions = {
# 163630 events, 91 jobs
        # User mean 4031.2, min 84.8, max 6559.8
        # Mean 180.8 MB, min 3.1 MB, max 191.2 MB
        "TTToHplusBWB_M120_ext_Summer12":         TaskDef("/TTToHplusBWB_M-120_8TeV_ext-pythia6-tauola/local-Summer12_DR53X_PU_S10_START53_V7C_v1_AODSIM_pattuple_v53_3_test2-9cfaf7bc576a6d9f3488935d01684bea/USER"),
        }

    addPattuple_53X("v53_3_test2", datasets, definitions)

def addPattuple_v53_3_test3(datasets):
    # Bugfix for LogErrorEventFilters
    definitions = {
        # 3498600 events, 1703 jobs
        # User mean 3116.1, min 153.4, max 27006.0
        # Mean 65.9 MB, min 4.6 MB, max 276.8 MB
        "Tau_198941-202504_2012C_Prompt":         TaskDef("/Tau/local-Run2012C_PromptReco_v2_AOD_pattuple_v53_3_198941_202504_test3-b1ebb7e21c06710552994e7e8d474dd4/USER"),
        }

    addPattuple_53X("v53_3_test3", datasets, definitions)


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

        #### Winter13 Reprocessing
        "Tau_190456-193621_2012A_Jan22":       TaskDef(""),
        "TauParked_193834-196531_2012B_Jan22": TaskDef(""),
        "TauParked_198022-202504_2012C_Jan22": TaskDef(""),
        "TauParked_202972-203742_2012C_Jan22": TaskDef(""),
        "TauParked_203777-208686_2012D_Jan22": TaskDef(""),

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
