## \package multicrabDatasetsPileupNtuple
# Functions for muon tag&probe workflow definitions

from multicrabWorkflowsTools import Dataset, Workflow, Data, Source, updatePublishName, TaskDef, updateTaskDefinitions


def addNtuple_44X(datasets):
    # ~10 s, ~25 kB / 5k events
    # => ~1 Mevents for half an hour job
    definitions = {
        "TTToHplusBWB_M80_Fall11":           TaskDef(njobsIn=1),
        "TTToHplusBWB_M90_Fall11":           TaskDef(njobsIn=1),
        "TTToHplusBWB_M100_Fall11":          TaskDef(njobsIn=1),
        "TTToHplusBWB_M120_Fall11":          TaskDef(njobsIn=1),
        "TTToHplusBWB_M140_Fall11":          TaskDef(njobsIn=1),
        "TTToHplusBWB_M150_Fall11":          TaskDef(njobsIn=1),
        "TTToHplusBWB_M155_Fall11":          TaskDef(njobsIn=1),
        "TTToHplusBWB_M160_Fall11":          TaskDef(njobsIn=1),

        "TTToHplusBHminusB_M80_Fall11":      TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M90_Fall11":      TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M100_Fall11":     TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M120_Fall11":     TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M140_Fall11":     TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M150_Fall11":     TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M155_Fall11":     TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M160_Fall11":     TaskDef(njobsIn=1),

        "HplusTB_M180_Fall11":               TaskDef(njobsIn=1),
        "HplusTB_M190_Fall11":               TaskDef(njobsIn=1),
        "HplusTB_M200_Fall11":               TaskDef(njobsIn=1),
        "HplusTB_M220_Fall11":               TaskDef(njobsIn=1),
        "HplusTB_M250_Fall11":               TaskDef(njobsIn=1),
        "HplusTB_M300_Fall11":               TaskDef(njobsIn=1),

        "QCD_Pt30to50_TuneZ2_Fall11":        TaskDef(njobsIn=7),
        "QCD_Pt50to80_TuneZ2_Fall11":        TaskDef(njobsIn=7),
        "QCD_Pt80to120_TuneZ2_Fall11":       TaskDef(njobsIn=7),
        "QCD_Pt120to170_TuneZ2_Fall11":      TaskDef(njobsIn=6),
        "QCD_Pt170to300_TuneZ2_Fall11":      TaskDef(njobsIn=6),
        "QCD_Pt300to470_TuneZ2_Fall11":      TaskDef(njobsIn=6),
        "QCD_Pt20_MuEnriched_TuneZ2_Fall11": TaskDef(njobsIn=25),
                                            
        "WW_TuneZ2_Fall11":                  TaskDef(njobsIn=4),
        "WZ_TuneZ2_Fall11":                  TaskDef(njobsIn=4),
        "ZZ_TuneZ2_Fall11":                  TaskDef(njobsIn=4),
        "TTJets_TuneZ2_Fall11":              TaskDef(njobsIn=60),
        "WJets_TuneZ2_Fall11":               TaskDef(njobsIn=80),
        "W2Jets_TuneZ2_Fall11":              TaskDef(njobsIn=25),
        "W3Jets_TuneZ2_Fall11":              TaskDef(njobsIn=8),
        "W4Jets_TuneZ2_Fall11":              TaskDef(njobsIn=13),
        "DYJetsToLL_M50_TuneZ2_Fall11":      TaskDef(njobsIn=36),
        "DYJetsToLL_M10to50_TuneZ2_Fall11":  TaskDef(njobsIn=31),
        "T_t-channel_TuneZ2_Fall11":         TaskDef(njobsIn=4),
        "Tbar_t-channel_TuneZ2_Fall11":      TaskDef(njobsIn=2),
        "T_tW-channel_TuneZ2_Fall11":        TaskDef(njobsIn=1),
        "Tbar_tW-channel_TuneZ2_Fall11":     TaskDef(njobsIn=1),
        "T_s-channel_TuneZ2_Fall11":         TaskDef(njobsIn=1),
        "Tbar_s-channel_TuneZ2_Fall11":      TaskDef(njobsIn=1),
        }

    for datasetName, taskDef in definitions.iteritems():
        dataset = datasets.getDataset(datasetName)

        source = Source("AOD", number_of_jobs=taskDef.njobsIn)
        wf = Workflow("pileupNtuple_44X", source=source, output_file="histograms.root")

        # Add the ntuple Workflow to Dataset
        dataset.addWorkflow(wf)

