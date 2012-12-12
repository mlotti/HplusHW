## \package multicrabWorkflows
# Root of dataset definitions for multicrab operations
#
# Note that you can obtain a list of all defined datasets by running
# this file through the python interpreter.
#
# \see multicrab

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
        self.energy = 7
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
        self.energy = 7
        self.dataVersion = "44XmcS6"

    ## Function call syntax
    #
    # \param name          Name of the dataset
    # \param crossSection  Cross section in pb
    # \param aod           String for the DBS-dataset path of AOD
    def __call__(self, name, crossSection, aod):
        return Dataset(name, dataVersion=self.dataVersion, energy=self.energy, crossSection=crossSection, workflows=[Workflow("AOD", output=Data(datasetpath=aod))])
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
    DataDataset("Tau_%s_2011A_Nov08",      runs=(160431, 167913), aod="/Tau/Run2011A-08Nov2011-v1/AOD"),
    DataDataset("Tau_%s_2011A_Nov08",      runs=(165970, 167913), aod="/Tau/Run2011A-08Nov2011-v1/AOD"),
    #
    DataDataset("Tau_%s_2011A_Nov08",      runs=(170722, 173198), aod="/Tau/Run2011A-08Nov2011-v1/AOD"), # break of range because of trigger eff. boundary
    DataDataset("Tau_%s_2011A_Nov08",      runs=(173236, 173692), aod="/Tau/Run2011A-08Nov2011-v1/AOD"), # break of range because of trigger eff. boundary
    # Tau, Run2011B
    DataDataset("Tau_%s_2011B_Nov19",      runs=(175832, 180252), aod="/Tau/Run2011B-19Nov2011-v1/AOD"),
])
datasets.extend([
    # SingleMu, Run2011A
    DataDataset("SingleMu_%s_2011A_Nov08", runs=(160431, 163261), aod="/SingleMu/Run2011A-08Nov2011-v1/AOD"),
    DataDataset("SingleMu_%s_2011A_Nov08", runs=(163270, 163869), aod="/SingleMu/Run2011A-08Nov2011-v1/AOD"),
    DataDataset("SingleMu_%s_2011A_Nov08", runs=(165088, 166150), aod="/SingleMu/Run2011A-08Nov2011-v1/AOD"),
    #
    DataDataset("SingleMu_%s_2011A_Nov08", runs=(166161, 166164), aod="/SingleMu/Run2011A-08Nov2011-v1/AOD"),
    DataDataset("SingleMu_%s_2011A_Nov08", runs=(166346, 166346), aod="/SingleMu/Run2011A-08Nov2011-v1/AOD"),
    DataDataset("SingleMu_%s_2011A_Nov08", runs=(166374, 167043), aod="/SingleMu/Run2011A-08Nov2011-v1/AOD"),
    DataDataset("SingleMu_%s_2011A_Nov08", runs=(167078, 167913), aod="/SingleMu/Run2011A-08Nov2011-v1/AOD"),
    DataDataset("SingleMu_%s_2011A_Nov08", runs=(170722, 172619), aod="/SingleMu/Run2011A-08Nov2011-v1/AOD"),
    DataDataset("SingleMu_%s_2011A_Nov08", runs=(172620, 173198), aod="/SingleMu/Run2011A-08Nov2011-v1/AOD"),
    DataDataset("SingleMu_%s_2011A_Nov08", runs=(173236, 173692), aod="/SingleMu/Run2011A-08Nov2011-v1/AOD"),
    # SingleMu, Run2011B
    DataDataset("SingleMu_%s_2011B_Nov19", runs=(173693, 177452), aod="/SingleMu/Run2011B-19Nov2011-v1/AOD"),
    DataDataset("SingleMu_%s_2011B_Nov19", runs=(177453, 178380), aod="/SingleMu/Run2011B-19Nov2011-v1/AOD"),
    DataDataset("SingleMu_%s_2011B_Nov19", runs=(178411, 179889), aod="/SingleMu/Run2011B-19Nov2011-v1/AOD"),
    DataDataset("SingleMu_%s_2011B_Nov19", runs=(179942, 180371), aod="/SingleMu/Run2011B-19Nov2011-v1/AOD"),
])
datasets.splitDataByRuns("SingleMu_165088-166150_2011A_Nov08", [
        (165088, 165633), # Split this run range into two (and keep original),
        (165970, 166150), # because IsoMu trigger changes between them
        ])

datasets.extend([
    ## Fall11 MC
    # Signal, tt -> H+W
    MCDataset("TTToHplusBWB_M80_Fall11",   crossSection=165, aod="/TTToHplusBWB_M-80_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M90_Fall11",   crossSection=165, aod="/TTToHplusBWB_M-90_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M100_Fall11",  crossSection=165, aod="/TTToHplusBWB_M-100_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M120_Fall11",  crossSection=165, aod="/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M140_Fall11",  crossSection=165, aod="/TTToHplusBWB_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M150_Fall11",  crossSection=165, aod="/TTToHplusBWB_M-150_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M155_Fall11",  crossSection=165, aod="/TTToHplusBWB_M-155_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBWB_M160_Fall11",  crossSection=165, aod="/TTToHplusBWB_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    # Signal, tt -> H+H-
    MCDataset("TTToHplusBHminusB_M80_Fall11",   crossSection=165, aod="/TTToHplusBHminusB_M-80_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M90_Fall11",   crossSection=165, aod="/TTToHplusBHminusB_M-90_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M100_Fall11",  crossSection=165, aod="/TTToHplusBHminusB_M-100_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M120_Fall11",  crossSection=165, aod="/TTToHplusBHminusB_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M140_Fall11",  crossSection=165, aod="/TTToHplusBHminusB_M-140_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M150_Fall11",  crossSection=165, aod="/TTToHplusBHminusB_M-150_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M155_Fall11",  crossSection=165, aod="/TTToHplusBHminusB_M-155_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("TTToHplusBHminusB_M160_Fall11",  crossSection=165, aod="/TTToHplusBHminusB_M-160_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    # Signal, heavy, FIXME cross sections
    MCDataset("HplusTB_M180_Fall11",   crossSection=165, aod="/HplusTB_M-180_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("HplusTB_M190_Fall11",   crossSection=165, aod="/HplusTB_M-190_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("HplusTB_M200_Fall11",   crossSection=165, aod="/HplusTB_M-200_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("HplusTB_M220_Fall11",   crossSection=165, aod="/HplusTB_M-220_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("HplusTB_M250_Fall11",   crossSection=165, aod="/HplusTB_M-250_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("HplusTB_M300_Fall11",   crossSection=165, aod="/HplusTB_M-300_7TeV-pythia6-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    # QCD backgrounds, cross sections from https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingSummer2011
    MCDataset("QCD_Pt30to50_TuneZ2_Fall11",   crossSection=5.312e+07, aod="/QCD_Pt-30to50_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt50to80_TuneZ2_Fall11",   crossSection=6.359e+06, aod="/QCD_Pt-50to80_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt80to120_TuneZ2_Fall11",  crossSection=7.843e+05, aod="/QCD_Pt-80to120_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt120to170_TuneZ2_Fall11", crossSection=1.151e+05, aod="/QCD_Pt-120to170_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt170to300_TuneZ2_Fall11", crossSection=2.426e+04, aod="/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt300to470_TuneZ2_Fall11", crossSection=1.168e+03, aod="/QCD_Pt-300to470_TuneZ2_7TeV_pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("QCD_Pt20_MuEnriched_TuneZ2_Fall11", crossSection=296600000.*0.0002855, aod="/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    # EWK pythia, cross sections from https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    MCDataset("WW_TuneZ2_Fall11", crossSection=43, aod="/WW_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("WZ_TuneZ2_Fall11", crossSection=18.2, aod="/WZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("ZZ_TuneZ2_Fall11", crossSection=5.9, aod="/ZZ_TuneZ2_7TeV_pythia6_tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    # EWK madgraph
    # Cross sections from
    # [1] https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
    # [2] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
    MCDataset("TTJets_TuneZ2_Fall11",             crossSection=165, aod="/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"), # [1,2], approx. NNLO
    # Cross section [2], NNLO
    # W+Njets, with the assumption that they are weighted (see
    # src/WJetsWeight.cc) And if they are not, the cross section can
    # always be set in the plot scripts by the user.
    MCDataset("WJets_TuneZ2_Fall11",              crossSection=31314, aod="/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("W2Jets_TuneZ2_Fall11",             crossSection=31314, aod="/W2Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("W3Jets_TuneZ2_Fall11",             crossSection=31314, aod="/W3Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("W4Jets_TuneZ2_Fall11",             crossSection=31314, aod="/W4Jets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("DYJetsToLL_M50_TuneZ2_Fall11",     crossSection=3048, aod="/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"), # [2], NNLO
    MCDataset("DYJetsToLL_M10to50_TuneZ2_Fall11", crossSection=9611, aod="/DYJetsToLL_M-10To50_TuneZ2_7TeV-madgraph/Fall11-PU_S6_START44_V9B-v1/AODSIM"), # taken from PREP
    # SingleTop Powheg
    # Cross sections from
    # https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopMC2011
    # https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopSigma
    MCDataset("T_t-channel_TuneZ2_Fall11",     crossSection=41.92, aod="/T_TuneZ2_t-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("Tbar_t-channel_TuneZ2_Fall11",  crossSection=22.65, aod="/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("T_tW-channel_TuneZ2_Fall11",    crossSection=7.87, aod="/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("Tbar_tW-channel_TuneZ2_Fall11", crossSection=7.87, aod="/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("T_s-channel_TuneZ2_Fall11",     crossSection=3.19, aod="/T_TuneZ2_s-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
    MCDataset("Tbar_s-channel_TuneZ2_Fall11",  crossSection=1.44, aod="/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM"),
])

# Add definition
multicrabWorkflowsPileupNtuple.addNtuple_44X(datasets)

# Add pattuple definitions
multicrabWorkflowsPattuple.addPattuple_v44_4(datasets)

# Add embedding definitions
multicrabWorkflowsTauEmbedding.addEmbeddingSkim_v44_4_2(datasets)
multicrabWorkflowsTauEmbedding.addEmbeddingEmbedding_v44_4_2(datasets)

# Add muon tag&probe definitions
multicrabWorkflowsMuonTagProbe.addMuonTagProbe_44X(datasets)

# Add trigger efficiency definitions
#multicrabWorkflowsTriggerEff.addMetLegSkim_vXXX(datasets)

def printAllDatasets():
    for d in datasets.getDatasetList():
        print str(d)+","

if __name__ == "__main__":
    printAllDatasets()
