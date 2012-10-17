## \package multicrabDatasetsTriggerEff
# Functions for trigger efficiency workflow definitions

from multicrabDatasetsTools import Dataset, Workflow, Data, Source, updatePublishName, TaskDef, updateTaskDefinitions
from multicrabDatasetsPattuple import constructProcessingWorkflow_44X

def addMetLegSkim_44X(version, datasets, updateDefinitions):
    mcTrigger = "HLT_MediumIsoPFTau35_Trk20_v1"
    def TaskDefMC(njobsIn, njobsOut):
        return TaskDef(njobsIn=njobsIn, njobsOut=njobsOut, triggerOR=[mcTrigger])

    # The numbers of jobs are from multicrabDatasetsPattuple, they may have to be adjusted
    defaultDefinitions = {
        "Tau_165970-167913_2011A_Nov08": TaskDef(njobsIn=300, njobsOut=15, triggerOR=[
                                                    "HLT_IsoPFTau35_Trk20_v2", # 165970-166164, 166374-167043
                                                    "HLT_IsoPFTau35_Trk20_v3", # 166346-166346
                                                    "HLT_IsoPFTau35_Trk20_v4", # 167078-167913
                                                ], triggerThrow=False),
        "Tau_170722-173198_2011A_Nov08": TaskDef(njobsIn=70, njobsOut=3, triggerOR=["HLT_IsoPFTau35_Trk20_v6"]),
        "Tau_173236-173692_2011A_Nov08": TaskDef(njobsIn=30, njobsOut=2, triggerOR=["HLT_MediumIsoPFTau35_Trk20_v1"]),
        "Tau_175832-180252_2011B_Nov19": TaskDef(njobsIn=300, njobsOut=30, triggerOR=[
                                                    "HLT_MediumIsoPFTau35_Trk20_v1", #175832-178380
                                                    "HLT_MediumIsoPFTau35_Trk20_v5", #178420-179889
                                                    "HLT_MediumIsoPFTau35_Trk20_v6", #179959-180252
                                              ], triggerThrow=False),

        # MC, triggered with mcTrigger
        "QCD_Pt30to50_TuneZ2_Fall11":       TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt50to80_TuneZ2_Fall11":       TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt80to120_TuneZ2_Fall11":      TaskDefMC(njobsIn=10, njobsOut=1),
        "QCD_Pt120to170_TuneZ2_Fall11":     TaskDefMC(njobsIn=20, njobsOut=1),
        "QCD_Pt170to300_TuneZ2_Fall11":     TaskDefMC(njobsIn=40, njobsOut=4),
        "QCD_Pt300to470_TuneZ2_Fall11":     TaskDefMC(njobsIn=40, njobsOut=10),
                                            
        "WW_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),
        "WZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),
        "ZZ_TuneZ2_Fall11":                 TaskDefMC(njobsIn=50, njobsOut=3),
        "TTJets_TuneZ2_Fall11":             TaskDefMC(njobsIn=490, njobsOut=50),
        "WJets_TuneZ2_Fall11":              TaskDefMC(njobsIn=490, njobsOut=10),
        "W2Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=300, njobsOut=20),
        "W3Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=120, njobsOut=10),
        "W4Jets_TuneZ2_Fall11":             TaskDefMC(njobsIn=200, njobsOut=12),
        "DYJetsToLL_M50_TuneZ2_Fall11":     TaskDefMC(njobsIn=350, njobsOut=2),
        "DYJetsToLL_M10to50_TuneZ2_Fall11": TaskDefMC(njobsIn=300, njobsOut=1),
        "T_t-channel_TuneZ2_Fall11":        TaskDefMC(njobsIn=50, njobsOut=2),
        "Tbar_t-channel_TuneZ2_Fall11":     TaskDefMC(njobsIn=50, njobsOut=1),
        "T_tW-channel_TuneZ2_Fall11":       TaskDefMC(njobsIn=20, njobsOut=1),
        "Tbar_tW-channel_TuneZ2_Fall11":    TaskDefMC(njobsIn=20, njobsOut=1),
        "T_s-channel_TuneZ2_Fall11":        TaskDefMC(njobsIn=10, njobsOut=1),
        "Tbar_s-channel_TuneZ2_Fall11":     TaskDefMC(njobsIn=10, njobsOut=1),
        }

    # Update the default definitions from the argument
    updateTaskDefinitions(defaultDefinitions, updateDefinitions)

    # Add Workflow for each dataset
    for datasetName, taskDef in defaultDefinitions.iteritems():
        dataset = datasets.getDataset(datasetName)

        # Construct processing workflow
        wf = constructProcessingWorkflow_44X(dataset, taskDef, sourceWorkflow="AOD", workflowName="triggerMetLeg_skim_"+version)

        # Example of how to set user_remote_dir for this workflow only
        # For dataset-specific setting one can e.g.
        # - modify TaskDef class, or
        # - create new TaskDef class for the purpose of this workflow, or
        # - create a dictionary from dataset name to user_remote_dir,
        #   and pick the one for this dataset from there
        #wf.addCrabLine("USER.user_remote_dir = /whatever")

        dataset.addWorkflow(wf)

        # If have skim output, define the workflows which depend on it
        if wf.output != None:
            dataset.addWorkflow(Workflow("triggerMetLeg_analysis_"+version, source=Source("triggerMetLeg_skim_"+version),
                                         triggerOR=taskDef.triggerOR, args=wf.args, output_file="histograms.root"))


def addMetLegSkim_vXXX(datasets):
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

    addMetLegSkim_44X("vXXX", datasets, definitions)
