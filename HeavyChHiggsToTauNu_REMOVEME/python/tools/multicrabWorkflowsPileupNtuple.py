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
        "W1Jets_TuneZ2_Fall11":              TaskDef(njobsIn=75),
        "W2Jets_TuneZ2_Fall11":              TaskDef(njobsIn=25),
        "W3Jets_TuneZ2_Fall11":              TaskDef(njobsIn=8),
        "W3Jets_TuneZ2_v2_Fall11":           TaskDef(njobsIn=8),
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


def addNtuple_53X(datasets):
    # ~30 s, ~37 kB / 6k events
    # => ~1 Mevents for 1 hour 20 minutes job
    definitions = {
        "TTToHplusBWB_M80_Summer12":              TaskDef(njobsIn=1),
        "TTToHplusBWB_M90_Summer12":              TaskDef(njobsIn=1),
        "TTToHplusBWB_M100_Summer12":             TaskDef(njobsIn=1),
        "TTToHplusBWB_M120_Summer12":             TaskDef(njobsIn=1),
        "TTToHplusBWB_M140_Summer12":             TaskDef(njobsIn=1),
        "TTToHplusBWB_M150_Summer12":             TaskDef(njobsIn=1),
        "TTToHplusBWB_M155_Summer12":             TaskDef(njobsIn=1),
        "TTToHplusBWB_M160_Summer12":             TaskDef(njobsIn=1),

        "TTToHplusBWB_M80_ext_Summer12":          TaskDef(njobsIn=1),
        "TTToHplusBWB_M90_ext_Summer12":          TaskDef(njobsIn=1),
        "TTToHplusBWB_M100_ext_Summer12":          TaskDef(njobsIn=1),
        "TTToHplusBWB_M120_ext_Summer12":         TaskDef(njobsIn=1),
        "TTToHplusBWB_M140_ext_Summer12":         TaskDef(njobsIn=1),
        "TTToHplusBWB_M150_ext_Summer12":         TaskDef(njobsIn=1),
        "TTToHplusBWB_M155_ext_Summer12":         TaskDef(njobsIn=1),
        "TTToHplusBWB_M160_ext_Summer12":         TaskDef(njobsIn=1),

        "TTToHplusBHminusB_M80_Summer12":         TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M90_Summer12":         TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M100_Summer12":        TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M120_Summer12":        TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M140_Summer12":        TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M150_Summer12":        TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M155_Summer12":        TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M160_Summer12":        TaskDef(njobsIn=1),

        "TTToHplusBHminusB_M80_ext_Summer12":     TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M100_ext_Summer12":    TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M120_ext_Summer12":    TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M140_ext_Summer12":    TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M150_ext_Summer12":    TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M155_ext_Summer12":    TaskDef(njobsIn=1),
        "TTToHplusBHminusB_M160_ext_Summer12":    TaskDef(njobsIn=1),

        "Hplus_taunu_t-channel_M80_Summer12":     TaskDef(njobsIn=1),
        "Hplus_taunu_t-channel_M90_Summer12":     TaskDef(njobsIn=1),
        "Hplus_taunu_t-channel_M100_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_t-channel_M120_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_t-channel_M140_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_t-channel_M150_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_t-channel_M155_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_t-channel_M160_Summer12":    TaskDef(njobsIn=1),

        "Hplus_taunu_tW-channel_M80_Summer12":     TaskDef(njobsIn=1),
        "Hplus_taunu_tW-channel_M90_Summer12":     TaskDef(njobsIn=1),
        "Hplus_taunu_tW-channel_M100_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_tW-channel_M120_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_tW-channel_M140_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_tW-channel_M150_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_tW-channel_M155_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_tW-channel_M160_Summer12":    TaskDef(njobsIn=1),

        "Hplus_taunu_s-channel_M80_Summer12":     TaskDef(njobsIn=1),
        "Hplus_taunu_s-channel_M90_Summer12":     TaskDef(njobsIn=1),
        "Hplus_taunu_s-channel_M100_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_s-channel_M120_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_s-channel_M140_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_s-channel_M150_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_s-channel_M155_Summer12":    TaskDef(njobsIn=1),
        "Hplus_taunu_s-channel_M160_Summer12":    TaskDef(njobsIn=1),

        "HplusTB_M180_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M190_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M200_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M220_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M250_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M300_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M400_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M500_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M600_Summer12":                  TaskDef(njobsIn=1),

        "HplusTB_M180_ext_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M190_ext_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M200_ext_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M220_ext_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M250_ext_Summer12":                  TaskDef(njobsIn=1),
        "HplusTB_M300_ext_Summer12":                  TaskDef(njobsIn=1),

        "HplusToTBbar_M180_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M200_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M220_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M240_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M250_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M260_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M280_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M300_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M350_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M400_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M500_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M600_Summer12":       TaskDef(njobsIn=1),
        "HplusToTBbar_M700_Summer12":       TaskDef(njobsIn=1),

        "QCD_Pt30to50_TuneZ2star_Summer12":       TaskDef(njobsIn=6),
        "QCD_Pt50to80_TuneZ2star_Summer12":       TaskDef(njobsIn=6),
        "QCD_Pt80to120_TuneZ2star_Summer12":      TaskDef(njobsIn=6),
        "QCD_Pt120to170_TuneZ2star_Summer12":     TaskDef(njobsIn=6),
        "QCD_Pt170to300_TuneZ2star_Summer12":     TaskDef(njobsIn=6),
        "QCD_Pt170to300_TuneZ2star_v2_Summer12":  TaskDef(njobsIn=20),
        "QCD_Pt300to470_TuneZ2star_Summer12":     TaskDef(njobsIn=6),
        "QCD_Pt300to470_TuneZ2star_v2_Summer12":  TaskDef(njobsIn=4),
        "QCD_Pt300to470_TuneZ2star_v3_Summer12":  TaskDef(njobsIn=20),
        "QCD_Pt20_MuEnriched_TuneZ2star_Summer12":TaskDef(njobsIn=22),
        
        "WW_TuneZ2star_Summer12":                 TaskDef(njobsIn=10),
        "WZ_TuneZ2star_Summer12":                 TaskDef(njobsIn=10),
        "ZZ_TuneZ2star_Summer12":                 TaskDef(njobsIn=10),
        "TTJets_TuneZ2star_Summer12":             TaskDef(njobsIn=7),
        "TTJets_FullLept_TuneZ2star_Summer12":    TaskDef(njobsIn=20),
        "TTJets_SemiLept_TuneZ2star_Summer12":    TaskDef(njobsIn=30),
        "TTJets_Hadronic_TuneZ2star_ext_Summer12":TaskDef(njobsIn=50),
        "WJets_TuneZ2star_v1_Summer12":           TaskDef(njobsIn=20),
        "WJets_TuneZ2star_v2_Summer12":           TaskDef(njobsIn=60),
        "W1Jets_TuneZ2star_Summer12":             TaskDef(njobsIn=25),
        "W2Jets_TuneZ2star_Summer12":             TaskDef(njobsIn=35),
        "W3Jets_TuneZ2star_Summer12":             TaskDef(njobsIn=16),
        "W4Jets_TuneZ2star_Summer12":             TaskDef(njobsIn=15),
        "DYJetsToLL_M50_TuneZ2star_Summer12":     TaskDef(njobsIn=30),
        "DYJetsToLL_M10to50_TuneZ2star_Summer12": TaskDef(njobsIn=38),
        "T_t-channel_TuneZ2star_Summer12":        TaskDef(njobsIn=4),
        "Tbar_t-channel_TuneZ2star_Summer12":     TaskDef(njobsIn=2),
        "T_tW-channel_TuneZ2star_Summer12":       TaskDef(njobsIn=1),
        "Tbar_tW-channel_TuneZ2star_Summer12":    TaskDef(njobsIn=1),
        "T_s-channel_TuneZ2star_Summer12":        TaskDef(njobsIn=1),
        "Tbar_s-channel_TuneZ2star_Summer12":     TaskDef(njobsIn=1),
        }

    for datasetName, taskDef in definitions.iteritems():
        dataset = datasets.getDataset(datasetName)

        source = Source("AOD", number_of_jobs=taskDef.njobsIn)
        wf = Workflow("pileupNtuple_53X", source=source, output_file="histograms.root")

        # Add the ntuple Workflow to Dataset
        dataset.addWorkflow(wf)

