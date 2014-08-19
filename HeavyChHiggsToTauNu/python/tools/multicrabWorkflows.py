## \package multicrabWorkflows
# Root of dataset definitions for multicrab operations
#
# Note that you can obtain a list of all defined datasets by running
# this file through the python interpreter.
#
# \see multicrab

import crosssection as xsect

from multicrabWorkflowsTools import DatasetSet, Dataset, Workflow, Data, Source
import multicrabWorkflowsPattuple
import multicrabWorkflowsTauEmbedding
import multicrabWorkflowsMuonTagProbe
import multicrabWorkflowsTriggerEff
import multicrabWorkflowsPileupNtuple

## Helper to specify data dataset
#
# Holds the energy and dataVersion, so that they can be easily changed
# for 7 and 8 TeV data
class DataDatasetHelper:
    def __init__(self):
        self.energy = "7"
        self.dataVersion = "44Xdata"

    ## Function call syntax
    # \param name  Name of the dataset (should contain '%s' in place of the run region)
    # \param runs  Two-tuple for the run region
    # \param aod   String for the DBS-dataset path of AOD
    # \param reco  Reco era to append to the otherwise common dataVersion (needed for 53X)
    def __call__(self, name, runs, aod, reco=""):
        rr = "%d-%d" % runs
        return Dataset(name % rr , dataVersion=self.dataVersion+reco, energy=self.energy, runs=runs, workflows=[Workflow("AOD", output=Data(datasetpath=aod))])
DataDataset = DataDatasetHelper()

## Helper to specify MC dataset
#
# Holds the energy and dataVersion, so that they can be easily changed
# for 7 and 8 TeV data
class MCDatasetHelper:
    def __init__(self):
        self.energy = "7"
        self.dataVersion = "44XmcS6"

        self.argSamples = ["WJets", "W1Jets", "W2Jets", "W3Jets", "W4Jets", "TTJets"]

    ## Function call syntax
    #
    # \param name          Name of the dataset
    # \param aod           String for the DBS-dataset path of AOD
    def __call__(self, name, aod, setCrossSection=True):
        crossSection = None
        if setCrossSection:
            if "TTToHplusBWB" in name or "TTToHplusBHminusB" in name:
                # For BR limit LandS expectes WH and HH samples to have ttbar cross section
                crossSection = xsect.backgroundCrossSections.crossSection("TTJets", self.energy)
            elif "HplusTB" in name or "HplusToTBbar" in name:
                # For sigma*BR limit LandS expects heavy H+ samples to have cross section of 1 pb
                crossSection = 1
            elif "Hplus_taunu" in name:
                if "t-channel" in name:
                    crossSection = sum([xsect.backgroundCrossSections.crossSection(st, self.energy) for st in ["T_t-channel", "Tbar_t-channel"]])
                elif "tW-channel" in name:
                    crossSection = sum([xsect.backgroundCrossSections.crossSection(st, self.energy) for st in ["T_tW-channel", "Tbar_tW-channel"]])
                elif "s-channel" in name:
                    crossSection = sum([xsect.backgroundCrossSections.crossSection(st, self.energy) for st in ["T_s-channel", "Tbar_s-channel"]])
                else:
                    raise Exception("Unrecognized single top -> H+ sample: %s" % name)
            else:
                # W+Njets, with the assumption that they are weighted (see
                # src/WJetsWeight.cc) And if they are not, the cross section can
                # always be set in the plot scripts by the user.
                nameTmp = name
                for wNjets in ["W1Jets", "W2Jets", "W3Jets", "W4Jets"]:
                    if wNjets in name:
                        nameTmp = name.replace(wNjets, "WJets")
                        break
                
                crossSection = xsect.backgroundCrossSections.crossSection(nameTmp, self.energy)
                if crossSection is None:
                    print "Warning: unable to find cross section for dataset %s with energy %s (check python/tools/crosssection.py)" % (name, self.energy)

        args = {}
        for sname in self.argSamples:
            if sname in name:
                args["sample"] = sname
                break

        return Dataset(name, dataVersion=self.dataVersion, energy=self.energy, crossSection=crossSection, workflows=[Workflow("AOD", output=Data(datasetpath=aod), args=args)])
MCDataset = MCDatasetHelper()

## List of datasets
#
# Here only the AOD datasets are specified. The results of our
# workflows (pattuples etc) are added more below.

#################### 7 TeV data and MC ####################
datasets = DatasetSet([
    # Tau, Run2011A
    # Need two definitions, first is for pattuples, second is for
    # trigger MET-leg (first run of single tau trigger is 165970)
    DataDataset("Tau_%s_2011A_Nov08",      runs=(160431, 167913), aod="/Tau/Run2011A-08Nov2011-v1/AOD"), # 20819377 events, 772 files
    DataDataset("Tau_%s_2011A_Nov08",      runs=(165970, 167913), aod="/Tau/Run2011A-08Nov2011-v1/AOD"),
    # break of range because of trigger eff. boundary
    DataDataset("Tau_%s_2011A_Nov08",      runs=(170722, 173198), aod="/Tau/Run2011A-08Nov2011-v1/AOD"), # 11790094 events, 476 files
    DataDataset("Tau_%s_2011A_Nov08",      runs=(173236, 173692), aod="/Tau/Run2011A-08Nov2011-v1/AOD"), # 5402857 events, 241 files
    # Tau, Run2011B
    DataDataset("Tau_%s_2011B_Nov19",      runs=(175832, 180252), aod="/Tau/Run2011B-19Nov2011-v1/AOD"), # 11511371 evetns, 640 files
])
datasets.extend([
    # SingleMu, Run2011A
    DataDataset("SingleMu_%s_2011A_Nov08", runs=(160431, 173692), aod="/SingleMu/Run2011A-08Nov2011-v1/AOD"),
    # SingleMu, Run2011B
    DataDataset("SingleMu_%s_2011B_Nov19", runs=(173693, 180371), aod="/SingleMu/Run2011B-19Nov2011-v1/AOD"), # for backward compatibility only
    DataDataset("SingleMu_%s_2011B_Nov19", runs=(175832, 180252), aod="/SingleMu/Run2011B-19Nov2011-v1/AOD"), # 50367238 events, 3431 files
])

# 2011 Tau leg trigger efficiency with RAW samples                                                                                                                                                                        
datasets.extend([                                                                                                                                                                                                         
    # SingleMu, Run2011A RAW-RECO                                                                                                                                                                                         
    DataDataset("SingleMu_%s_2011A_Nov08_RAWRECO", runs=(165970, 167913), aod="/SingleMu/Run2011A-Tau-08Nov2011-v1/RAW-RECO"),                                                                                            
    DataDataset("SingleMu_%s_2011A_Nov08_RAWRECO", runs=(170722, 173198), aod="/SingleMu/Run2011A-Tau-08Nov2011-v1/RAW-RECO"),                                                                                            
    DataDataset("SingleMu_%s_2011A_Nov08_RAWRECO", runs=(173236, 173692), aod="/SingleMu/Run2011A-Tau-08Nov2011-v1/RAW-RECO"),                                                                                            
                                                                                                                                                                                                                          
    # SingleMu, Run2011B RAW-RECO                                                                                                                                                                                         
    DataDataset("SingleMu_%s_2011B_Nov19_RAWRECO", runs=(175832, 180252), aod="/SingleMu/Run2011B-Tau-19Nov2011-v1/RAW-RECO"),                                                                                            
                                                                                                                                                                                                                          
    MCDataset("DYJetsToLL_TuneZ2_MPIoff_M50_7TeV_madgraph_tauola_GENRAW", aod="/DYJetsToLL_TuneZ2_MPIoff_M-50_7TeV-madgraph-tauola/Fall11-PU_S6_START42_V14B-v1/GEN-RAW"),                                                
    MCDataset("DYToTauTau_M20_CT10_TuneZ2_7TeV_powheg_pythia_tauola_TTEffSkim_v447_v1", aod="/DYToTauTau_M-20_CT10_TuneZ2_7TeV-powheg-pythia-tauola/Fall11-PU_S6_START42_V14B-v1/GEN-RAW", setCrossSection=False), # disable cross section setting to silence a harmless warning
])

# Split for backward compatibility, also for Mu-trigger thresholds
datasets.splitDataByRuns("SingleMu_160431-173692_2011A_Nov08", [
        (160431, 163261), # 38372194 events, 1415 files
        (163270, 163869), # 27672323 events, 1062 files
        (165088, 166150), # 30978754 events, 1202 files
        (166161, 166164),       
        (166346, 166346),
        (166374, 167043),
        (167078, 167913),
        (170722, 172619),
        (172620, 173198),
        (173236, 173692), # 14714495 events, 660 files
        ])
datasets.splitDataByRuns("SingleMu_173693-180371_2011B_Nov19", [
        (173693, 177452),
        (177453, 178380),
        (178411, 179889),
        (179942, 180371),
        ])
# Split for Mu-trigger thresholds
datasets.splitDataByRuns("SingleMu_160431-173692_2011A_Nov08", [
        (166161, 173198), # 76283557 events, 3067 files
        ])
datasets.splitDataByRuns("SingleMu_165088-166150_2011A_Nov08", [
        (165088, 165633), # Split this run range into two (and keep original),
        (165970, 166150), # because IsoMu trigger changes between them
        ])
# Split for hltMet not including and including HF
datasets.splitDataByRuns("SingleMu_160431-173692_2011A_Nov08", [
        (166161, 167913),
        (170722, 173198),
        ])

datasets.extend([
    ## Fall11 MC
    # Signal, tt -> H+W
    MCDataset("TTToHplusBWB_M80_Fall11",   aod="/TTToHplusBWB_M-80_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M90_Fall11",   aod="/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M100_Fall11",  aod="/TTToHplusBWB_M-100_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M120_Fall11",  aod="/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M140_Fall11",  aod="/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M150_Fall11",  aod="/TTToHplusBWB_M-150_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M155_Fall11",  aod="/TTToHplusBWB_M-155_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M160_Fall11",  aod="/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    # Signal, tt -> H+H-
    MCDataset("TTToHplusBHminusB_M80_Fall11",   aod="/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M90_Fall11",   aod="/TTToHplusBHminusB_M-90_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M100_Fall11",  aod="/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M120_Fall11",  aod="/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M140_Fall11",  aod="/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M150_Fall11",  aod="/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M155_Fall11",  aod="/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M160_Fall11",  aod="/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    # Signal, heavy, FIXME cross sections
    MCDataset("HplusTB_M180_Fall11",   aod="/HplusTB_M-180_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("HplusTB_M190_Fall11",   aod="/HplusTB_M-190_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("HplusTB_M200_Fall11",   aod="/HplusTB_M-200_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("HplusTB_M220_Fall11",   aod="/HplusTB_M-220_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("HplusTB_M250_Fall11",   aod="/HplusTB_M-250_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("HplusTB_M300_Fall11",   aod="/HplusTB_M-300_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    # QCD backgrounds
    MCDataset("QCD_Pt30to50_TuneZ2_Fall11",        aod="/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt50to80_TuneZ2_Fall11",        aod="/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt80to120_TuneZ2_Fall11",       aod="/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt120to170_TuneZ2_Fall11",      aod="/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt170to300_TuneZ2_Fall11",      aod="/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt300to470_TuneZ2_Fall11",      aod="/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt20_MuEnriched_TuneZ2_Fall11", aod="/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    # EWK pythia
    MCDataset("WW_TuneZ2_Fall11", aod="/WW_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("WZ_TuneZ2_Fall11", aod="/WZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("ZZ_TuneZ2_Fall11", aod="/ZZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    # EWK madgraph
    MCDataset("TTJets_TuneZ2_Fall11",             aod="/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("WJets_TuneZ2_Fall11",              aod="/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"), # 81345381 events
    MCDataset("W1Jets_TuneZ2_Fall11",             aod="/W1Jet_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"), # 76051609 events
    MCDataset("W2Jets_TuneZ2_Fall11",             aod="/W2Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("W3Jets_TuneZ2_Fall11",             aod="/W3Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("W3Jets_TuneZ2_v2_Fall11",          aod="/W3Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v2/AODSIM"), # has replaced v1
    MCDataset("W4Jets_TuneZ2_Fall11",             aod="/W4Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("DYJetsToLL_M50_TuneZ2_Fall11",     aod="/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"), # 36264432 events
    MCDataset("DYJetsToLL_M10to50_TuneZ2_Fall11", aod="/DYJetsToLL_M-10To50_TuneZ2_7TeV-madgraph/Fall11-PU_S6_START44_V9B-v1/AODSIM"), # 31480628 events
    # SingleTop Powheg
    MCDataset("T_t-channel_TuneZ2_Fall11",     aod="/T_TuneZ2_t-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("Tbar_t-channel_TuneZ2_Fall11",  aod="/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("T_tW-channel_TuneZ2_Fall11",    aod="/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("Tbar_tW-channel_TuneZ2_Fall11", aod="/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("T_s-channel_TuneZ2_Fall11",     aod="/T_TuneZ2_s-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("Tbar_s-channel_TuneZ2_Fall11",  aod="/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
])

#################### 8 TeV data and MC ####################
DataDataset.energy = "8"
DataDataset.dataVersion = "53Xdata"
MCDataset.energy = "8"
MCDataset.dataVersion = "53XmcS10"
# Tau PD, tau+MET trigger for signal, tau trigger for MET trigger efficiency measurement
datasets.extend([
    # Run2012A
    DataDataset("Tau_%s_2012A_Jul13",     reco="13Jul2012", runs=(190456, 190738), aod="/Tau/Run2012A-13Jul2012-v1/AOD"), # 1487727 events, 110 files
    DataDataset("Tau_%s_2012A_Aug06",     reco="06Aug2012", runs=(190782, 190949), aod="/Tau/Run2012A-recover-06Aug2012-v1/AOD"), # 329106 events, 30 files
    DataDataset("Tau_%s_2012A_Jul13",     reco="13Jul2012", runs=(191043, 193621), aod="/Tau/Run2012A-13Jul2012-v1/AOD"), # 3818840 events, 261 files
    # Run212B
    DataDataset("Tau_%s_2012B_Jul13",     reco="13Jul2012", runs=(193834, 196531), aod="/Tau/Run2012B-13Jul2012-v1/AOD"), # 25035330 events, 1874 files
    # Run212C
    DataDataset("Tau_%s_2012C_Aug24",     reco="24Aug2012", runs=(198022, 198523), aod="/Tau/Run2012C-24Aug2012-v1/AOD"), # 2212448 events, 190 files
    DataDataset("Tau_%s_2012C_Prompt",    reco="PromptCv2", runs=(198941, 203742), aod="/Tau/Run2012C-PromptReco-v2/AOD"), # 29597169 events, 2865 files
    DataDataset("Tau_%s_2012C_Dec11",     reco="11Dec2012", runs=(201191, 201191), aod="/Tau/Run2012C-EcalRecover_11Dec2012-v1/AOD"), # 579104 events, 59 files
    # Run2012D
    DataDataset("Tau_%s_2012D_Prompt",    reco="PromptDv1", runs=(203777, 208686), aod="/Tau/Run2012D-PromptReco-v1/AOD"), # 34164175 events, 3593 files
])
# Splitting here because when Matti first processed these for v53_1
# pattuples, he hought that the 200961-202504 would be completely
# invalid because of 0T field (but he later learned that this is not
# the case, there are valid runs with 3.8T field, which are marked OK
# in the golden JSON).
datasets.splitDataByRuns("Tau_198941-203742_2012C_Prompt", [
        (198941, 200601), # 14040901 events, 1327 files
        (200961, 202504), # 14232091 events, 1381 files  <--- This one has periods with 0T field
        (202792, 203742), # 1324177 events, 149 files
        ])
# Splitting here because the last part of Run2012C has the fix for
# high-pt taus
datasets.splitDataByRuns("Tau_198941-203742_2012C_Prompt", [
        (198941, 202504), # 28272992 events, 2716 files
        (202972, 203742), # 1271834 events, 136 files
])
# MultiJet PD, QuadJet trigger for signal
datasets.extend([
    # Run2012A
    DataDataset("MultiJet_%s_2012A_Jul13",     reco="13Jul2012", runs=(190456, 190738), aod="/MultiJet/Run2012A-13Jul2012-v1/AOD"), # 3947403 events,  308 files
    DataDataset("MultiJet_%s_2012A_Aug06",     reco="06Aug2012", runs=(190782, 190949), aod="/MultiJet/Run2012A-recover-06Aug2012-v1/AOD"), # 980342 events,  87 files
    DataDataset("MultiJet_%s_2012A_Jul13",     reco="13Jul2012", runs=(191043, 193621), aod="/MultiJet/Run2012A-13Jul2012-v1/AOD"), # 9518018 events, 742 files
    # Run212B
    DataDataset("MultiJet_%s_2012B_Jul13",     reco="13Jul2012", runs=(193834, 196531), aod="/MultiJet/Run2012B-13Jul2012-v1/AOD"), # 18675566 events, 1574 files
    # Run212C
    DataDataset("MultiJet_%s_2012C_Aug24",     reco="24Aug2012", runs=(198022, 198523), aod="/MultiJet/Run2012C-24Aug2012-v1/AOD"), # 2004842 events, 180 files
    DataDataset("MultiJet_%s_2012C_Prompt",    reco="PromptCv2", runs=(198941, 203742), aod="/MultiJet/Run2012C-PromptReco-v2/AOD"), # 27743543 events, 2833 files
    # Run2012D
    DataDataset("MultiJet_%s_2012D_Prompt",    reco="PromptDv1", runs=(203777, 208686), aod="/MultiJet/Run2012D-PromptReco-v1/AOD"), # 31810929 events, 3481 files
])
datasets.splitDataByRuns("MultiJet_193834-196531_2012B_Jul13", [
        (193834, 194225), # This has both BTagCSV and BTagIP triggers, 4765979 events, 363 files
        (194270, 196531), # This has only BTagIP trigger, 17488560 events, 1492 files
        ])
# Splitting here because when Matti first processed these for v53_1
# pattuples, he hought that the 200961-202504 would be completely
# invalid because of 0T field (but he later learned that this is not
# the case, there are valid runs with 3.8T field, which are marked OK
# in the golden JSON).
datasets.splitDataByRuns("MultiJet_198941-203742_2012C_Prompt", [
        (198941, 200601), # 13458312 events, 1339 files
        (200961, 202504), # 12966632 events, 1334 files  <--- This one has periods with 0T field
        (202792, 203742), # 1317502 events, 152 files
        ])

# BJetPlusX PD, QuadJet trigger for signal
datasets.extend([
    # Run212B
    DataDataset("BJetPlusX_%s_2012B_Jul13",     reco="13Jul2012", runs=(193834, 196531), aod="/BJetPlusX/Run2012B-13Jul2012-v1/AOD"), # 27868808 events, 2215 files
    # Run212C
    DataDataset("BJetPlusX_%s_2012C_Aug24",     reco="24Aug2012", runs=(198022, 198523), aod="/BJetPlusX/Run2012C-24Aug2012-v2/AOD"), # 2650602 events, 276 files
    DataDataset("BJetPlusX_%s_2012C_Prompt",    reco="PromptCv2", runs=(198941, 203742), aod="/BJetPlusX/Run2012C-PromptReco-v2/AOD"), # 33847953 events, 3420 files
    DataDataset("BJetPlusX_%s_2012C_Dec11",     reco="11Dec2012", runs=(201191, 201191), aod="/BJetPlusX/Run2012C-EcalRecover_11Dec2012-v1/AOD"), # 668183 eventsm, 76 files
    # Run2012D
    DataDataset("BJetPlusX_%s_2012D_Prompt",    reco="PromptDv1", runs=(203777, 208686), aod="/BJetPlusX/Run2012D-PromptReco-v1/AOD"), # 40966073 events, 4467 files
])
datasets.splitDataByRuns("BJetPlusX_193834-196531_2012B_Jul13", [
        (193834, 194225), # This has both BTagCSV and BTagIP triggers, 4540690 events, 322 files
        (194270, 196531), # This has only BTagIP trigger, 24497173 events, 1987 files
        ])

# TauPlusX PD, IsoMu+MET, IsoMu+MET+Tau triggers for tau trigger efficiency measurement
datasets.extend([
    # Run2012A
    DataDataset("TauPlusX_%s_2012A_Jul13",     reco="13Jul2012", runs=(190456, 190738), aod="/TauPlusX/Run2012A-13Jul2012-v1/AOD"), # 3010186 events, 214 files
    DataDataset("TauPlusX_%s_2012A_Aug06",     reco="06Aug2012", runs=(190782, 190949), aod="/TauPlusX/Run2012A-recover-06Aug2012-v1/AOD"), # 702399 events, 56 files
    DataDataset("TauPlusX_%s_2012A_Jul13",     reco="13Jul2012", runs=(191043, 193621), aod="/TauPlusX/Run2012A-13Jul2012-v1/AOD"), # 6247183 events, 443 files
    # Run212B
    DataDataset("TauPlusX_%s_2012B_Jul13",     reco="13Jul2012", runs=(193834, 196531), aod="/TauPlusX/Run2012B-13Jul2012-v1/AOD"), # 39410283 events, 3013 files
    # Run212C
    DataDataset("TauPlusX_%s_2012C_Aug24",     reco="24Aug2012", runs=(198022, 198523), aod="/TauPlusX/Run2012C-24Aug2012-v1/AOD"), # 4067828 events, 313 files
#    DataDataset("TauPlusX_%s_2012C_Prompt",    reco="PromptCv2", runs=(198941, 203742), aod="/TauPlusX/Run2012C-PromptReco-v2/AOD"), #
    DataDataset("TauPlusX_%s_2012C_Prompt",    reco="PromptCv2", runs=(198941, 199608), aod="/TauPlusX/Run2012C-PromptReco-v2/AOD"), #                                   
    DataDataset("TauPlusX_%s_2012C_Prompt",    reco="PromptCv2", runs=(199698, 203742), aod="/TauPlusX/Run2012C-PromptReco-v2/AOD"), #
    DataDataset("TauPlusX_%s_2012C_Dec11",     reco="11Dec2012", runs=(201191, 201191), aod="/TauPlusX/Run2012C-EcalRecover_11Dec2012-v1/AOD"), # 962881 events, 94 files
    # Run2012D
    DataDataset("TauPlusX_%s_2012D_Prompt",    reco="PromptDv1", runs=(203777, 208686), aod="/TauPlusX/Run2012D-PromptReco-v1/AOD"), # 59840242 events, 6068 files
])
# SingleMu PD, Mu trigger for embedding, IsoMu trigger for muon efficiency measurement
datasets.extend([  
    # SingleMu, Run2012A
    DataDataset("SingleMu_%s_2012A_Jul13",     reco="13Jul2012", runs=(190456, 190738), aod="/SingleMu/Run2012A-13Jul2012-v1/AOD"), # 5326430 events,  165 files
    DataDataset("SingleMu_%s_2012A_Aug06",     reco="06Aug2012", runs=(190782, 190949), aod="/SingleMu/Run2012A-recover-06Aug2012-v1/AOD"), # 2845333 events, 99 files
    DataDataset("SingleMu_%s_2012A_Jul13",     reco="13Jul2012", runs=(191043, 193621), aod="/SingleMu/Run2012A-13Jul2012-v1/AOD"), # 13952991 events, 570 files
    # SingleMu, Run212B
    DataDataset("SingleMu_%s_2012B_Jul13",     reco="13Jul2012", runs=(193834, 196531), aod="/SingleMu/Run2012B-13Jul2012-v1/AOD"), # 59538958 events, 4294 files
    # SingleMu, Run212C
    DataDataset("SingleMu_%s_2012C_Aug24",     reco="24Aug2012", runs=(198022, 198523), aod="/SingleMu/Run2012C-24Aug2012-v1/AOD"), # 6076746 events, 460 files
    DataDataset("SingleMu_%s_2012C_Prompt",    reco="PromptCv2", runs=(198941, 203742), aod="/SingleMu/Run2012C-PromptReco-v2/AOD"), # 81770645 events, 7450 files
    DataDataset("SingleMu_%s_2012C_Dec11",     reco="11Dec2012", runs=(201191, 201191), aod="/SingleMu/Run2012C-EcalRecover_11Dec2012-v1/AOD"), # 1619573 events, 145 files
    # SingleMu, Run2012D
    DataDataset("SingleMu_%s_2012D_Prompt",    reco="PromptDv1", runs=(203777, 208686), aod="/SingleMu/Run2012D-PromptReco-v1/AOD"), # 90255013 events, 8886 files
])
# Split to cope with number of jobs(?)
datasets.splitDataByRuns("SingleMu_198941-203742_2012C_Prompt", [
        (198941, 199608),
        (199698, 202504),
        (202970, 203742),
])

########
# MultiJet1Parked ReReco, QuadJet trigger for signal
datasets.extend([
    DataDataset("MultiJet1Parked_%s_2012B_Nov05", reco="05Nov2012B",   runs=(193834, 196531), aod="/MultiJet1Parked/Run2012B-05Nov2012-v2/AOD"), # 78067581 events,  7084 files
    DataDataset("MultiJet1Parked_%s_2012C_Nov05", reco="05Nov2012Cv1", runs=(198022, 198523), aod="/MultiJet1Parked/Run2012C-part1_05Nov2012-v2/AOD"), # 9209168 events, 626 files
    DataDataset("MultiJet1Parked_%s_2012C_Nov05", reco="05Nov2012Cv2", runs=(198941, 203742), aod="/MultiJet1Parked/Run2012C-part2_05Nov2012-v2/AOD"), # 130268374 events, 10136 files
    DataDataset("MultiJet1Parked_%s_2012D_Dec10", reco="10Dec2012",    runs=(203777, 207779), aod="/MultiJet1Parked/Run2012D-part1_10Dec2012-v1/AOD"), # 218620252 events, 22176 files
    DataDataset("MultiJet1Parked_%s_2012D_Jan17", reco="17Jan2013",    runs=(207875, 208686), aod="/MultiJet1Parked/Run2012D-part2_17Jan2013-v1/AOD"), # 28985011 events, 3051 files
    DataDataset("MultiJet1Parked_%s_2012D_Jan17", reco="17Jan2013",    runs=(207883, 208307), aod="/MultiJet1Parked/Run2012D-part2_PixelRecover_17Jan2013-v1/AOD"), # 20015244 events, 1878 files
])
datasets.splitDataByRuns("MultiJet1Parked_193834-196531_2012B_Nov05", [
        (193834, 194225), # HLT_QuadJet50 is prescaled, use HLT_QuadJet80, 78059999 events, 6484 files
        (194270, 196531), # HLT_QuadJet50 is unprescaled, 76705110 events, 6356 files
])
# Split to have separate pieces of this around PixelRecover
datasets.splitDataByRuns("MultiJet1Parked_207875-208686_2012D_Jan17", [
        (207875, 207882), # 395625 events, 35 files
        (208339, 208686), # 28902576 events, 3043 files
])


########
# ReRecos (Jan22)

# Tau(Parked) PD, tau+MET trigger for signal, tau trigger for MET trigger efficiency measurement
datasets.extend([
    DataDataset("Tau_%s_2012A_Jan22",       reco="22Jan2013", runs=(190456, 193621), aod="/Tau/Run2012A-22Jan2013-v1/AOD"), # 4316637 events, 317 files
    DataDataset("TauParked_%s_2012B_Jan22", reco="22Jan2013", runs=(193834, 196531), aod="/TauParked/Run2012B-22Jan2013-v1/AOD"), # 46187183 events, 3416 files
    DataDataset("TauParked_%s_2012C_Jan22", reco="22Jan2013", runs=(198022, 203742), aod="/TauParked/Run2012C-22Jan2013-v1/AOD"), # 58152493 events, 4385 files
    DataDataset("TauParked_%s_2012D_Jan22", reco="22Jan2013", runs=(203777, 208686), aod="/TauParked/Run2012D-22Jan2013-v1/AOD"), # 63220920 events, 5127 files
])
# Splitting here because the last part of Run2012C has the fix for
# high-pt taus
datasets.splitDataByRuns("TauParked_198022-203742_2012C_Jan22", [
        (198022, 202504), # 56890206 events, 4301 files
        (202972, 203742), # 4122415 events, 307 files
])

# TauPlusX PD, IsoMu+MET, IsoMu+MET+Tau triggers for tau trigger efficiency measurement
datasets.extend([
    DataDataset("TauPlusX_%s_2012A_Jan22", reco="22Jan2013", runs=(190456, 193621), aod="/TauPlusX/Run2012A-22Jan2013-v1/AOD"), # 7350406 events, 487 files
    DataDataset("TauPlusX_%s_2012B_Jan22", reco="22Jan2013", runs=(193834, 196531), aod="/TauPlusX/Run2012B-22Jan2013-v1/AOD"), # 39411579 events, 3006 files
    DataDataset("TauPlusX_%s_2012C_Jan22", reco="22Jan2013", runs=(198022, 203742), aod="/TauPlusX/Run2012C-22Jan2013-v1/AOD"), # 53083103 events, 7862 files
    DataDataset("TauPlusX_%s_2012D_Jan22", reco="22Jan2013", runs=(203777, 208686), aod="/TauPlusX/Run2012D-22Jan2013-v1/AOD"), # 63421453 events, 5395 files
])

# MultiJet PD, QuadJet trigger for signal
datasets.extend([
    DataDataset("MultiJet_%s_2012A_Jan22",        reco="22Jan2013",    runs=(190456, 193621), aod="/MultiJet/Run2012A-22Jan2013-v1/AOD"), # 11068071 events, 879 files
])

# BJetPlusX PD, QuadJet trigger for signal
datasets.extend([
    DataDataset("BJetPlusX_%s_2012B_Jan22", reco="22Jan2013", runs=(193834, 196531), aod="/BJetPlusX/Run2012B-22Jan2013-v1/AOD"), # 27868808 events, 2289 files
    DataDataset("BJetPlusX_%s_2012C_Jan22", reco="22Jan2013", runs=(198022, 203742), aod="/BJetPlusX/Run2012C-22Jan2013-v1/AOD"), # 36498856 events, 3091 files
    DataDataset("BJetPlusX_%s_2012D_Jan22", reco="22Jan2013", runs=(203777, 208686), aod="/BJetPlusX/Run2012D-22Jan2013-v1/AOD"), # 40926332 events, 3943 files
])
datasets.splitDataByRuns("BJetPlusX_193834-196531_2012B_Jan22", [
        (193834, 194225), # This has both BTagCSV and BTagIP triggers, 6146763 events, 462 files
        (194270, 196531), # This has only BTagIP trigger, 25513309 events, 2125 files
        ])

# SingleMu PD, Mu trigger for embedding, IsoMu trigger for muon efficiency measurement
datasets.extend([
    DataDataset("SingleMu_%s_2012A_Jan22", reco="22Jan2013", runs=(190456, 193621), aod="/SingleMu/Run2012A-22Jan2013-v1/AOD"), # 19785316 events, 817 files
    DataDataset("SingleMu_%s_2012B_Jan22", reco="22Jan2013", runs=(193834, 196531), aod="/SingleMu/Run2012B-22Jan2013-v1/AOD"), # 59516381 events, 4204 files
    DataDataset("SingleMu_%s_2012C_Jan22", reco="22Jan2013", runs=(198022, 203742), aod="/SingleMu/Run2012C-22Jan2013-v1/AOD"), # 87683348 events, 6171 files
    DataDataset("SingleMu_%s_2012D_Jan22", reco="22Jan2013", runs=(203777, 208686), aod="/SingleMu/Run2012D-22Jan2013-v1/AOD"), # 95089646 events, 7567 files
])
# Split by HLT menu boundaries to have < 5k jobs for embedding skims
datasets.splitDataByRuns("SingleMu_198022-203742_2012C_Jan22", [
        (198022, 200381), # 51586584 events, 3482 files
        (200466, 203742), # 58207084 events, 4285 files
])
datasets.splitDataByRuns("SingleMu_203777-208686_2012D_Jan22", [
        (203777, 205834), # 45358726 events, 3601 files
        (205908, 207100), # 44923291 events, 3643 files
        (207214, 208686), # 47041659 events, 3908 files
])



datasets.extend([
    ## Summer12 MC (DR53X)
    #
    # Signal, tt -> H+W, 200 kevt/sample
    MCDataset("TTToHplusBWB_M80_Summer12",  aod="/TTToHplusBWB_M-80_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M90_Summer12",  aod="/TTToHplusBWB_M-90_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M100_Summer12", aod="/TTToHplusBWB_M-100_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M120_Summer12", aod="/TTToHplusBWB_M-120_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M140_Summer12", aod="/TTToHplusBWB_M-140_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M150_Summer12", aod="/TTToHplusBWB_M-150_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M155_Summer12", aod="/TTToHplusBWB_M-155_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M160_Summer12", aod="/TTToHplusBWB_M-160_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    # (Probably) extension, 1 Mevt/sample
    MCDataset("TTToHplusBWB_M80_ext_Summer12",  aod="/TTToHplusBWB_M-80_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M90_ext_Summer12",  aod="/TTToHplusBWB_M-90_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M100_ext_Summer12", aod="/TTToHplusBWB_M-100_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M120_ext_Summer12", aod="/TTToHplusBWB_M-120_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M140_ext_Summer12", aod="/TTToHplusBWB_M-140_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M150_ext_Summer12", aod="/TTToHplusBWB_M-150_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M155_ext_Summer12", aod="/TTToHplusBWB_M-155_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M160_ext_Summer12", aod="/TTToHplusBWB_M-160_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    # Signal, tt -> H+H-, 200 kevt/sample
    MCDataset("TTToHplusBHminusB_M80_Summer12",  aod="/TTToHplusBHminusB_M-80_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M90_Summer12",  aod="/TTToHplusBHminusB_M-90_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"), # 1 Mevt
    MCDataset("TTToHplusBHminusB_M100_Summer12", aod="/TTToHplusBHminusB_M-100_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M120_Summer12", aod="/TTToHplusBHminusB_M-120_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M140_Summer12", aod="/TTToHplusBHminusB_M-140_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M150_Summer12", aod="/TTToHplusBHminusB_M-150_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M155_Summer12", aod="/TTToHplusBHminusB_M-155_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M160_Summer12", aod="/TTToHplusBHminusB_M-160_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    # (Probably) extension, 1 Mevt/sample
    MCDataset("TTToHplusBHminusB_M80_ext_Summer12",  aod="/TTToHplusBHminusB_M-80_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M100_ext_Summer12", aod="/TTToHplusBHminusB_M-100_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M120_ext_Summer12", aod="/TTToHplusBHminusB_M-120_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M140_ext_Summer12", aod="/TTToHplusBHminusB_M-140_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M150_ext_Summer12", aod="/TTToHplusBHminusB_M-150_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M155_ext_Summer12", aod="/TTToHplusBHminusB_M-155_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M160_ext_Summer12", aod="/TTToHplusBHminusB_M-160_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    # Signal t -> H+, t-channel, 300 kevt/sample
    MCDataset("Hplus_taunu_t-channel_M80_Summer12",  aod="/Hplus_taunu_t-channel_M-80_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_t-channel_M90_Summer12",  aod="/Hplus_taunu_t-channel_M-90_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_t-channel_M100_Summer12", aod="/Hplus_taunu_t-channel_M-100_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_t-channel_M120_Summer12", aod="/Hplus_taunu_t-channel_M-120_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_t-channel_M140_Summer12", aod="/Hplus_taunu_t-channel_M-140_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_t-channel_M150_Summer12", aod="/Hplus_taunu_t-channel_M-150_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_t-channel_M155_Summer12", aod="/Hplus_taunu_t-channel_M-155_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_t-channel_M160_Summer12", aod="/Hplus_taunu_t-channel_M-160_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    # Signal t -> H+, tW-channel, 131 kevt/sample
    MCDataset("Hplus_taunu_tW-channel_M80_Summer12",  aod="/Hplus_taunu_tW-channel_M-80_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_tW-channel_M90_Summer12",  aod="/Hplus_taunu_tW-channel_M-90_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_tW-channel_M100_Summer12", aod="/Hplus_taunu_tW-channel_M-100_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_tW-channel_M120_Summer12", aod="/Hplus_taunu_tW-channel_M-120_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_tW-channel_M140_Summer12", aod="/Hplus_taunu_tW-channel_M-140_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_tW-channel_M150_Summer12", aod="/Hplus_taunu_tW-channel_M-150_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_tW-channel_M155_Summer12", aod="/Hplus_taunu_tW-channel_M-155_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("Hplus_taunu_tW-channel_M160_Summer12", aod="/Hplus_taunu_tW-channel_M-160_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    # Signal t -> H+, s-channel, 250-300 kevt/sample
    MCDataset("Hplus_taunu_s-channel_M80_Summer12",  aod="/Hplus_taunu_s-channel_M-80_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("Hplus_taunu_s-channel_M90_Summer12",  aod="/Hplus_taunu_s-channel_M-90_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("Hplus_taunu_s-channel_M100_Summer12", aod="/Hplus_taunu_s-channel_M-100_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("Hplus_taunu_s-channel_M120_Summer12", aod="/Hplus_taunu_s-channel_M-120_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("Hplus_taunu_s-channel_M140_Summer12", aod="/Hplus_taunu_s-channel_M-140_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("Hplus_taunu_s-channel_M150_Summer12", aod="/Hplus_taunu_s-channel_M-150_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("Hplus_taunu_s-channel_M155_Summer12", aod="/Hplus_taunu_s-channel_M-155_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("Hplus_taunu_s-channel_M160_Summer12", aod="/Hplus_taunu_s-channel_M-160_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    # Signal, heavy, 200 kevt/sample
    MCDataset("HplusTB_M180_Summer12", aod="/HplusTB_M-180_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("HplusTB_M190_Summer12", aod="/HplusTB_M-190_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("HplusTB_M200_Summer12", aod="/HplusTB_M-200_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("HplusTB_M220_Summer12", aod="/HplusTB_M-220_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("HplusTB_M250_Summer12", aod="/HplusTB_M-250_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    MCDataset("HplusTB_M300_Summer12", aod="/HplusTB_M-300_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"),
    # 1 Mevt/sample
    MCDataset("HplusTB_M400_Summer12", aod="/HplusTB_M-400_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("HplusTB_M500_Summer12", aod="/HplusTB_M-500_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("HplusTB_M600_Summer12", aod="/HplusTB_M-600_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    # (Probably) extension, 1 Mevt/sample
    MCDataset("HplusTB_M180_ext_Summer12", aod="/HplusTB_M-180_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("HplusTB_M190_ext_Summer12", aod="/HplusTB_M-190_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("HplusTB_M200_ext_Summer12", aod="/HplusTB_M-200_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("HplusTB_M220_ext_Summer12", aod="/HplusTB_M-220_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("HplusTB_M250_ext_Summer12", aod="/HplusTB_M-250_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    MCDataset("HplusTB_M300_ext_Summer12", aod="/HplusTB_M-300_8TeV_ext-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"),
    # Signal H+ -> tb, heavy, 300 kevt/sample
    MCDataset("HplusToTBbar_M180_Summer12", aod="/HplusToTBbar_M-180_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M200_Summer12", aod="/HplusToTBbar_M-200_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M220_Summer12", aod="/HplusToTBbar_M-220_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M240_Summer12", aod="/HplusToTBbar_M-240_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M250_Summer12", aod="/HplusToTBbar_M-250_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M260_Summer12", aod="/HplusToTBbar_M-260_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M280_Summer12", aod="/HplusToTBbar_M-280_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M300_Summer12", aod="/HplusToTBbar_M-300_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M350_Summer12", aod="/HplusToTBbar_M-350_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M400_Summer12", aod="/HplusToTBbar_M-400_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M500_Summer12", aod="/HplusToTBbar_M-500_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M600_Summer12", aod="/HplusToTBbar_M-600_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    MCDataset("HplusToTBbar_M700_Summer12", aod="/HplusToTBbar_M-700_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM"),
    # QCD backgrounds, 6 Mevt/sample
    MCDataset("QCD_Pt30to50_TuneZ2star_Summer12",        aod="/QCD_Pt-30to50_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM"),
    MCDataset("QCD_Pt50to80_TuneZ2star_Summer12",        aod="/QCD_Pt-50to80_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM"),
    MCDataset("QCD_Pt80to120_TuneZ2star_Summer12",       aod="/QCD_Pt-80to120_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v3/AODSIM"),
    MCDataset("QCD_Pt120to170_TuneZ2star_Summer12",      aod="/QCD_Pt-120to170_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v3/AODSIM"),
    MCDataset("QCD_Pt170to300_TuneZ2star_Summer12",      aod="/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM"),
    MCDataset("QCD_Pt170to300_TuneZ2star_v2_Summer12",   aod="/QCD_Pt-170to300_TuneZ2star_8TeV_pythia6_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 20 Mevt, extension
    MCDataset("QCD_Pt300to470_TuneZ2star_Summer12",      aod="/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM"),
    MCDataset("QCD_Pt300to470_TuneZ2star_v2_Summer12",   aod="/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 3.5 Mevt, extension
    MCDataset("QCD_Pt300to470_TuneZ2star_v3_Summer12",   aod="/QCD_Pt-300to470_TuneZ2star_8TeV_pythia6_v3/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 20 Mevt, extension
    MCDataset("QCD_Pt20_MuEnriched_TuneZ2star_Summer12", aod="/QCD_Pt_20_MuEnrichedPt_15_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v3/AODSIM"), # 21.5 Mevt
    # EWK pythia, 10 Mevt/sample
    # Cross sections from [3], took values for CTEQ PDF since CTEQ6L1 was used in pythia simulation
    # ZZ cross section is slightly questionmark, since the computed value is for m(ll) > 12
    MCDataset("WW_TuneZ2star_Summer12", aod="/WW_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 10 Mevt
    MCDataset("WZ_TuneZ2star_Summer12", aod="/WZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 10 Mevt
    MCDataset("ZZ_TuneZ2star_Summer12", aod="/ZZ_TuneZ2star_8TeV_pythia6_tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 10 Mevt
    # EWK madgraph
    #
    # The original 8 TeV madgraph samples had massless b-quark. This
    # has been fixed in Massive B in DECAY samples
    MCDataset("TTJets_TuneZ2star_Summer12",             aod="/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 6.9 Mevt; v2 has currently ~1 Mevt
    MCDataset("TTJets_FullLept_TuneZ2star_Summer12",    aod="/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v2/AODSIM"), # 12 Mevt
    MCDataset("TTJets_SemiLept_TuneZ2star_Summer12",    aod="/TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM"), # 25 Mevt
    MCDataset("TTJets_Hadronic_TuneZ2star_ext_Summer12",aod="/TTJets_HadronicMGDecays_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A_ext-v1/AODSIM"), # 31 Mevt
    MCDataset("WJets_TuneZ2star_v1_Summer12",           aod="/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 18.4 Mevt
    MCDataset("WJets_TuneZ2star_v2_Summer12",           aod="/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM"), # 57.7
    MCDataset("W1Jets_TuneZ2star_Summer12",             aod="/W1JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 23 Mevt
    MCDataset("W2Jets_TuneZ2star_Summer12",             aod="/W2JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 34 Mevt
    MCDataset("W3Jets_TuneZ2star_Summer12",             aod="/W3JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 15.5 Mevt
    MCDataset("W4Jets_TuneZ2star_Summer12",             aod="/W4JetsToLNu_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 13.4 Mevt
    MCDataset("DYJetsToLL_M50_TuneZ2star_Summer12",     aod="/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 30 Mevt
    MCDataset("DYJetsToLL_M10to50_TuneZ2star_Summer12", aod="/DYJetsToLL_M-10To50_TuneZ2Star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 38 Mevt
    # DY for trigger tau efficiency measurement
    MCDataset("DYToTauTau_M_20_CT10_TuneZ2star_powheg_tauola_Summer12", aod="/DYToTauTau_M-20_CT10_TuneZ2star_8TeV-powheg-tauola-pythia6/Summer12_DR53X-PU_S8_START53_V7A-v1/AODSIM"), # 3.3 Mevt
    MCDataset("DYToTauTau_M_20_CT10_TuneZ2star_v2_powheg_tauola_Summer12", aod="/DYToTauTau_M-20_CT10_TuneZ2star_v2_8TeV-powheg-tauola-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM"), # 48.8 Mevt
    MCDataset("DYToTauTau_M_100to200_TuneZ2Star_pythia6_tauola_Summer12", aod="/DYToTauTau_M-100to200_TuneZ2Star_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 200kevt
    MCDataset("DYToTauTau_M_200to400_TuneZ2Star_pythia6_tauola_Summer12", aod="/DYToTauTau_M-200to400_TuneZ2Star_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 100kevt
    MCDataset("DYToTauTau_M_400to800_TuneZ2Star_pythia6_tauola_Summer12", aod="/DYToTauTau_M-400to800_TuneZ2Star_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 100kevt
    MCDataset("DYToTauTau_M_800_TuneZ2Star_pythia6_tauola_Summer12", aod="/DYToTauTau_M-800_TuneZ2Star_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 100kevt
    # SingleTop Powheg
    MCDataset("T_t-channel_TuneZ2star_Summer12",     aod="/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 3.8 Mevt
    MCDataset("Tbar_t-channel_TuneZ2star_Summer12",  aod="/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 1.9 Mevt
    MCDataset("T_tW-channel_TuneZ2star_Summer12",    aod="/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 500 kevt
    MCDataset("Tbar_tW-channel_TuneZ2star_Summer12", aod="/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 500 kevt
    MCDataset("T_s-channel_TuneZ2star_Summer12",     aod="/T_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 260 kevt
    MCDataset("Tbar_s-channel_TuneZ2star_Summer12",  aod="/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM"), # 140 kevt
])


# /QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/local-Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_QCD_Pt20_MuEnriched_TuneZ2_Fall11-f102f48f945c7d8b633b6cfb2ce7b4c8/USER
# /DYJetsToLL_M-10To50_TuneZ2_7TeV-madgraph/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_DYJetsToLL_M10to50_TuneZ2_Fall11-a776c511e9ef937d92535c43d40d7d9b/USER
# /Tau/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_Tau_Single_165970-167913_2011A_Nov08-e9140fd17e7e1e1046a08ea867b6ea3b/USER
# /Tau/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_Tau_Single_170722-173198_2011A_Nov08-a6c05c7e9a3d44262e26ce7c36099a5c/USER
# /Tau/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_Tau_Single_173236-173692_2011A_Nov08-0b4b37a70df41aa83f6b277cd6180eda/USER
# /Tau/local-Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_Tau_Single_175832-180252_2011B_Nov19-24097e1b77cf020b884a6b4c31bedd64/USER

# Add definition
multicrabWorkflowsPileupNtuple.addNtuple_44X(datasets)
multicrabWorkflowsPileupNtuple.addNtuple_53X(datasets)

# Add pattuple definitions
multicrabWorkflowsPattuple.addPattuple_v44_5(datasets)

multicrabWorkflowsPattuple.addPattuple_v53_2(datasets)
multicrabWorkflowsPattuple.addPattuple_v53_3_test6_quadjet(datasets)
multicrabWorkflowsPattuple.addPattuple_v53_3_taumet(datasets)
multicrabWorkflowsPattuple.addPattuple_v53_3_quadjet(datasets)

# Add embedding definitions
multicrabWorkflowsTauEmbedding.addEmbeddingAodAnalysis_44X(datasets)
multicrabWorkflowsTauEmbedding.addEmbeddingGenTauSkim_v44_5(datasets)
multicrabWorkflowsTauEmbedding.addEmbeddingSkim_v44_5(datasets)
multicrabWorkflowsTauEmbedding.addEmbeddingSkim_v44_5_1(datasets)
multicrabWorkflowsTauEmbedding.addEmbeddingEmbedding_v44_5_2(datasets)
multicrabWorkflowsTauEmbedding.addEmbeddingGenTauSkim_v53_3(datasets)
multicrabWorkflowsTauEmbedding.addEmbeddingSkim_v53_3(datasets)
multicrabWorkflowsTauEmbedding.addEmbeddingEmbedding_v53_3(datasets)

# Add muon tag&probe definitions
multicrabWorkflowsMuonTagProbe.addMuonTagProbe_44X(datasets)

# Add trigger efficiency definitions
multicrabWorkflowsTriggerEff.addTauLegSkim_53X_v3(datasets)
multicrabWorkflowsTriggerEff.addMetLegSkim_53X_v3(datasets)
multicrabWorkflowsTriggerEff.addQuadJetSkim_53X_v3(datasets)

def printAllDatasets():
    for d in datasets.getDatasetList():
        print str(d)+","

if __name__ == "__main__":
    printAllDatasets()
