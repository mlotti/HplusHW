## \package multicrabDatasetsMuonTagProbe
# Functions for muon tag&probe workflow definitions

from multicrabWorkflowsTools import Dataset, Workflow, Data, Source, updatePublishName, TaskDef, updateTaskDefinitions


def addMuonTagProbe_44X(datasets):
    mcTrigger = "HLT_IsoMu30_eta2p1_v3"

    definitions = {
        "SingleMu_160431-163261_2011A_Nov08": TaskDef(njobsIn=1000, triggerOR=["HLT_IsoMu12_v1"]), # HLT_Mu20_v1 (~430 in reality)
        "SingleMu_163270-163869_2011A_Nov08": TaskDef(njobsIn=1000, triggerOR=["HLT_IsoMu17_v6"]), # HLT_Mu24_v2 (~390 in reality)
        "SingleMu_165088-165633_2011A_Nov08": TaskDef(njobsIn= 490, triggerOR=["HLT_IsoMu17_v8"]), # HLT_Mu30_v3 (~200 in reality)
        "SingleMu_165970-166150_2011A_Nov08": TaskDef(njobsIn= 490, triggerOR=["HLT_IsoMu24_v5"]), # HLT_Mu30_v3 (~160 in reality)
        "SingleMu_166161-166164_2011A_Nov08": TaskDef(njobsIn=  20, triggerOR=["HLT_IsoMu24_v5"]), # HLT_Mu40_v1 (~10 in reality)
        "SingleMu_166346-166346_2011A_Nov08": TaskDef(njobsIn=  20, triggerOR=["HLT_IsoMu24_v6"]), # HLT_Mu40_v2 (~10 in reality)
        "SingleMu_166374-167043_2011A_Nov08": TaskDef(njobsIn=1000, triggerOR=["HLT_IsoMu24_v5"]), # HLT_Mu40_v1 (~400 in reality)
        "SingleMu_167078-167913_2011A_Nov08": TaskDef(njobsIn=1000, triggerOR=["HLT_IsoMu24_v7"]), # HLT_Mu40_v3 (~330 in reality)
        "SingleMu_170722-172619_2011A_Nov08": TaskDef(njobsIn= 490, triggerOR=["HLT_IsoMu24_v8"]), # HLT_Mu40_v5
        "SingleMu_172620-173198_2011A_Nov08": TaskDef(njobsIn=1000, triggerOR=["HLT_IsoMu24_v8"]), # HLT_Mu40_v5 (~330 in reality)
        "SingleMu_173236-173692_2011A_Nov08": TaskDef(njobsIn=1000, triggerOR=["HLT_IsoMu30_eta2p1_v3"]), # HLT_Mu40_eta2p1_v1 (~330 in reality)
        "SingleMu_173693-177452_2011B_Nov19": TaskDef(njobsIn=1000, triggerOR=["HLT_IsoMu30_eta2p1_v3"]), # HLT_Mu40_eta2p1_v1 FIXME: do we need to split this one?
        "SingleMu_177453-178380_2011B_Nov19": TaskDef(njobsIn= 490, triggerOR=["HLT_IsoMu30_eta2p1_v3"]), # HLT_Mu40_eta2p1_v1

        "SingleMu_178411-179889_2011B_Nov19": TaskDef(njobsIn=1000, triggerOR=["HLT_IsoMu30_eta2p1_v6"]), # HLT_Mu40_eta2p1_v4
        "SingleMu_179942-180371_2011B_Nov19": TaskDef(njobsIn= 300, triggerOR=["HLT_IsoMu30_eta2p1_v7"]), # HLT_Mu40_eta2p1_v5

        # MC, triggered with mcTrigger
        "DYJetsToLL_M50_TuneZ2_Fall11":      TaskDef(njobsIn= 350, triggerOR=[mcTrigger]),
        }

    for datasetName, taskDef in definitions.iteritems():
        dataset = datasets.getDataset(datasetName)

        inputLumiMask=None
        if dataset.isData():
            inputLumiMask = "Nov08ReReco"

        source = Source("AOD", number_of_jobs=taskDef.njobsIn, lumiMask=inputLumiMask)
        args = {
            "doPat": "1"
            }
        wf = Workflow("muonTagProbe", source=source, triggerOR=taskDef.triggerOR, args=args, output_file="histograms.root")

        # Add the skim Workflow to Dataset
        dataset.addWorkflow(wf)

