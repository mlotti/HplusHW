## \package multicrabDatasetsTriggerEff
# Functions for trigger efficiency workflow definitions

from multicrabWorkflowsTools import Dataset, Workflow, Data, Source, updatePublishName, TaskDef, updateTaskDefinitions
from multicrabWorkflowsPattuple import constructProcessingWorkflow_44X

import multicrabDatasetsCommon as common

def addTauLegSkim_44X(version, datasets, updateDefinitions):
    mcTrigger = "HLT_IsoMu30_eta2p1_v3"
    def TaskDefMC(**kwargs):
        return TaskDef(triggerOR=[mcTrigger], **kwargs)

    # The numbers of jobs are from multicrabDatasetsPattuple, they may have to be adjusted
    defaultDefinitions = {

        # 2011A HLT_IsoPFTau35_Trk20_MET45_v{1,2,4,6}, 2011A HLT_IsoPFTau35_Trk20_MET60_v{2,3,4}
        "SingleMu_165970-167913_2011A_Nov08_RAWRECO": TaskDef(njobsIn=300, njobsOut=30, triggerOR=[
                                                    "HLT_IsoMu17_v9",
                                                    "HLT_IsoMu17_v11",
                                                    ], triggerThrow=False),
        # 2011A HLT_IsoPFTau35_Trk20_MET60_v6
        "SingleMu_170722-173198_2011A_Nov08_RAWRECO": TaskDef(njobsIn=300, njobsOut=30, triggerOR=[
                                                    " HLT_IsoMu20_v8 ",
                                                    ], triggerThrow=False),
        # 2011A HLT_MediumIsoPFTau35_Trk20_MET60_v1
        "SingleMu_173236-173692_2011A_Nov08_RAWRECO": TaskDef(njobsIn=300, njobsOut=30, triggerOR=[
                                                    "HLT_IsoMu30_eta2p1_v3"
                                                    ], triggerThrow=False),
        # 2011B HLT_MediumIsoPFTau35_Trk20_MET60_v{1,5,6}
        "SingleMu_175832-180252_2011B_Nov19_RAWRECO": TaskDef(njobsIn=300, njobsOut=30, triggerOR=[
                                                    "HLT_IsoMu30_eta2p1_v3","HLT_IsoMu30_eta2p1_v6","HLT_IsoMu30_eta2p1_v7",
                                                    ], triggerThrow=False),
        
        "DYJetsToLL_TuneZ2_MPIoff_M50_7TeV_madgraph_tauola_GENRAW":       TaskDefMC(njobsIn=4000, njobsOut=2000),
        }

    workflowName = "triggerTauLeg_skim_"+version      
                                                      
    # Update the default definitions from the argument
    updateTaskDefinitions(defaultDefinitions, updateDefinitions, workflowName)
                                                                              
    # Add Workflow for each dataset                                           
    for datasetName, taskDef in defaultDefinitions.iteritems():               
        dataset = datasets.getDataset(datasetName)

        # Construct processing workflow
        wf = constructProcessingWorkflow_44X(dataset, taskDef, sourceWorkflow="AOD", workflowName=workflowName, inputLumiMaskData="Nov08ReReco", outputLumiMaskData=None)

        # Set tau-leg specific customizations on job configuration
        wf.addArg("customizeConfig", "TauLegZMuTauFilter")

        # Example of how to set user_remote_dir for this workflow only (but for all datasets)
        #wf.addCrabLine("USER.user_remote_dir = /whatever")                                  
                                                                                             
        dataset.addWorkflow(wf)                                                              
                                                                                             
        # If have skim output, define the workflows which depend on it                       
        if wf.output != None:                                                                
            wf.output.dbs_url = common.tteff_dbs                                             
            dataset.addWorkflow(Workflow("triggerTauLeg_analysis_"+version, source=Source(workflowName),
                                         triggerOR=taskDef.triggerOR, args=wf.args, output_file="tteffAnalysis-tauleg.root"))

def addTauLegSkim_v44_v5(datasets):
#def addTauLegSkim_cmssw44X_v1(datasets):
    definitions = {

        "SingleMu_165970-167913_2011A_Nov08_RAWRECO":    TaskDef(""),
        "SingleMu_170722-173198_2011A_Nov08_RAWRECO":    TaskDef(""),
        "SingleMu_173236-173692_2011A_Nov08_RAWRECO":    TaskDef(""),
        "SingleMu_175832-180252_2011B_Nov19_RAWRECO":    TaskDef(""),

        "DYJetsToLL_TuneZ2_MPIoff_M50_7TeV_madgraph_tauola_GENRAW":    TaskDef("")
        }

    addTauLegSkim_44X("v44_v5", datasets, definitions)

def addMetLegSkim_44X(version, datasets, updateDefinitions):
    mcTrigger = "HLT_MediumIsoPFTau35_Trk20_v1"
    def TaskDefMC(**kwargs):
        return TaskDef(triggerOR=[mcTrigger], **kwargs)

    # The numbers of jobs are from multicrabDatasetsPattuple, they may have to be adjusted
    defaultDefinitions = {
        "Tau_165970-167913_2011A_Nov08": TaskDef(njobsIn=300, njobsOut=30, triggerOR=[
                                                    "HLT_IsoPFTau35_Trk20_v2", # 165970-166164, 166374-167043
                                                    "HLT_IsoPFTau35_Trk20_v3", # 166346-166346
                                                    "HLT_IsoPFTau35_Trk20_v4", # 167078-167913
                                                ], triggerThrow=False),
        "Tau_170722-173198_2011A_Nov08": TaskDef(njobsIn=70, njobsOut=30, triggerOR=["HLT_IsoPFTau35_Trk20_v6"]),
        "Tau_173236-173692_2011A_Nov08": TaskDef(njobsIn=30, njobsOut=30, triggerOR=["HLT_MediumIsoPFTau35_Trk20_v1"]),
        "Tau_175832-180252_2011B_Nov19": TaskDef(njobsIn=300, njobsOut=30, triggerOR=[
                                                    "HLT_MediumIsoPFTau35_Trk20_v1", #175832-178380
                                                    "HLT_MediumIsoPFTau35_Trk20_v5", #178420-179889
                                                    "HLT_MediumIsoPFTau35_Trk20_v6", #179959-180252
                                              ], triggerThrow=False),

        # MC, triggered with mcTrigger
        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDefMC(njobsIn=10, njobsOut=10),
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDefMC(njobsIn=20, njobsOut=20),
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDefMC(njobsIn=40, njobsOut=4),
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDefMC(njobsIn=40, njobsOut=10),
                                            
        "WW_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),
        "WZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),
        "ZZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),
        "TTJets_TuneZ2_Fall11":             TaskDefMC(njobsIn=490, njobsOut=250),
        "WJets_TuneZ2_Fall11":              TaskDefMC(njobsIn=490, njobsOut=10),
        "W2Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=300, njobsOut=20),
        "W3Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=120, njobsOut=10),
        "W3Jets_TuneZ2_v2_Fall11":          TaskDefMC(njobsIn=120, njobsOut=10),
        "W4Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=200, njobsOut=12),
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDefMC(njobsIn=350, njobsOut=35),
        "DYJetsToLL_M10to50_TuneZ2_Fall11": TaskDefMC(njobsIn=300, njobsOut=10),
        "T_t-channel_TuneZ2_Fall11":        TaskDefMC(njobsIn=50, njobsOut=2),
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDefMC(njobsIn=50, njobsOut=1),
        "T_tW-channel_TuneZ2_Fall11":       TaskDefMC(njobsIn=20, njobsOut=1),
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDefMC(njobsIn=20, njobsOut=1),
        "T_s-channel_TuneZ2_Fall11":        TaskDefMC(njobsIn=10, njobsOut=1),
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDefMC(njobsIn=10, njobsOut=1),

        # Here is an example how to specity number of events/job
        # instead of number of jobs, and how to give dataset-specific
        # arbitrary crab configuration lines
        #"Tbar_s-channel_TuneZ2_Fall11":     TaskDefMC(neventsPerJobIn=10000, neventsPerJobOut=1000000, crabLines=["USER.user_remote_dir=/foo"]),
        }

    workflowName = "triggerMetLeg_skim_"+version

    # Update the default definitions from the argument
    updateTaskDefinitions(defaultDefinitions, updateDefinitions, workflowName)

    # Add Workflow for each dataset
    for datasetName, taskDef in defaultDefinitions.iteritems():
        dataset = datasets.getDataset(datasetName)

        # Construct processing workflow
        wf = constructProcessingWorkflow_44X(dataset, taskDef, sourceWorkflow="AOD", workflowName=workflowName, inputLumiMaskData="Nov08ReReco", outputLumiMaskData=None)

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
                "source": Source(workflowName),
                "args": wf.args,
                "skimConfig": skim
                }
            commonArgs["args"]["trgAnalysis"] = "MetLeg"

            if dataset.isData():
                # For data, construct one analysis workflow per trigger type
                pd = datasetName.split("_")[0]                              
                if pd == "Tau" or pd == "TauPlusX":                         
                    dataset.addWorkflow(Workflow("triggerMetLeg_analysis_"+version, triggerOR=wf.triggerOR, **commonArgs))
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
                dataset.addWorkflow(Workflow("triggerMetLeg_analysis_"+version, triggerOR=[mcTriggerTauLeg], **commonArgs))






        # If have skim output, define the workflows which depend on it
        if wf.output != None:
	    wf.output.dbs_url = common.tteff_dbs
            dataset.addWorkflow(Workflow("triggerMetLeg_analysis_"+version, source=Source(workflowName),
                                         triggerOR=taskDef.triggerOR, args=wf.args, output_file="tteffAnalysis-metleg.root"))


def addMetLegSkim_v44_v5(datasets):
    definitions = {

        "Tau_165970-167913_2011A_Nov08":    TaskDef(""),
        "Tau_170722-173198_2011A_Nov08":    TaskDef(""),
        "Tau_173236-173692_2011A_Nov08":    TaskDef(""),
        "Tau_175832-180252_2011B_Nov19":    TaskDef(""),

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
        "W3Jets_TuneZ2_v2_Fall11":          TaskDef(""),
        "W4Jets_TuneZ2_Fall11":             TaskDef(""),
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDef(""),
        "DYJetsToLL_M10to50_TuneZ2_Fall11": TaskDef(""),
        "T_t-channel_TuneZ2_Fall11":        TaskDef(""),
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDef(""),
        "T_tW-channel_TuneZ2_Fall11":       TaskDef(""),
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDef(""),
        "T_s-channel_TuneZ2_Fall11":        TaskDef(""),
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDef(""),
        }

    addMetLegSkim_44X("v44_v5", datasets, definitions)
