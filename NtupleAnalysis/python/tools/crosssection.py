## \package crosssection
''' 
Description: 
Background and signal cross sections (in pb)

How to Compute Cross Sections with the GenXSecAnalyzer:
The cross-sections found with this tool are those predicted by the respective generators. 
There may be better estimates, coming from dedicated task forces, theory papers etc. 
In general, you should refer to the GenXsecTaskForce Twiki to find the best estimates.

First find the path of a ROOT file for a given dataset "someFile.root", by searching 
on DAS (for example, dataset=/WW_TuneCUETP8M1*/RunIISpring16MiniAODv2-*/* in https://cmsweb.cern.ch/das/)
Download the dedicated analyzer and run on that single file:
- curl https://raw.githubusercontent.com/syuvivida/generator/master/cross_section/runJob/ana.py  -o ana.py
- cmsRun ana.py inputFiles="someFile.root" maxEvents=-1
The last output line is the final cross section:
"After filter: final cross section = X +- Y pb"

To get the files for a given dataset:
das_client --limit 0 --query "file dataset=<datasetName>"
Example:
das_client.py --query "file dataset=/QCD_bEnriched_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM" --limit 1000
das_client.py --limit 0 --query "file dataset=/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM" --limit 1000

Example:
cmsRun ana.py inputFiles="/store/mc/RunIISpring16MiniAODv2/QCD_bEnriched_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/70000/00DFB564-393F-E611-A97A-02163E012F6E.root" maxEvents=-1

Links:
https://twiki.cern.ch/twiki/bin/view/CMS/GenXsecTaskForce
https://twiki.cern.ch/twiki/bin/view/CMS/HowToGenXSecAnalyzer#Running_the_GenXSecAnalyzer_on_a

'''

DEGUB = False
def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''

    if not DEBUG:
        return
    Print(msg, printHeader)
    return


def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return


class CrossSection:
    '''
    Cross section of a single process (physical dataset)
    
     Constructor
    
     \parma name              Name of the process
     \param energyDictionary  Dictionary of energy -> cross section (energy as string in TeV, cross section as float in pb)
     '''
    def __init__(self, name, energyDictionary):
        self.name = name
        for key, value in energyDictionary.iteritems():
            setattr(self, key, value)

    def get(self, energy):
        '''
        Get cross section
        
        \param energy  Energy as string in TeV
        '''
        try:
            return getattr(self, energy)
        except AttributeError:
            raise Exception("No cross section set for process %s for energy %s" % (self.name, energy))


class CrossSectionList:
    '''
    List of CrossSection objects
    '''
    def __init__(self, *args):
        self.crossSections = args[:]

    def crossSection(self, name, energy):
        for obj in self.crossSections:
            #if name[:len(obj.name)] == obj.name:
            if name == obj.name:
                return obj.get(energy)
        return None

# Cross sections from
# [1] PREP
# [2] https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingSummer2011
# [3] from https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
# [3] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
# [5] https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopMC2011
# [6] https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopSigma
# [7] https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorkingHCP2012#53X_MC_Samples
# [8] https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopSigma8TeV (other useful page https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopMC2012)
# [9] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
# [10] http://arxiv.org/abs/1303.6254
# [11] https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013
# [12] https://twiki.cern.ch/twiki/bin/view/CMS/TmdRecipes
# [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
# [14] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV / GenXSecAnalyzer
# [15] McM
# [16] https://twiki.cern.ch/twiki/bin/view/CMS/HowToGenXSecAnalyzer#Running_the_GenXSecAnalyzer_on_a
# [17] https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#DY_Z and https://arxiv.org/pdf/1105.0020v1.pdf

backgroundCrossSections = CrossSectionList(
    CrossSection("QCD_Pt_15to30", {
            "13": 2237000000., # [12]
            }),
    CrossSection("QCD_Pt_30to50", {
            "7": 5.312e+07, # [2]
            "8": 6.6285328e7, # [1]
            "13": 161500000., # [12]
            }),
    CrossSection("QCD_Pt_50to80", {
            "7": 6.359e+06, # [2]
            "8": 8148778.0, # [1]
            "13": 22110000., # [12]
            }),
    CrossSection("QCD_Pt_80to120", {
            "7": 7.843e+05, # [2]
            "8": 1033680.0, # [1]
            "13": 3000114.3, # [12]
            }),
    CrossSection("QCD_Pt_120to170", {
            "7": 1.151e+05, # [2]
            "8": 156293.3, # [1]
            "13": 493200., # [12] # McM: 471100
            }),
    CrossSection("QCD_Pt_170to300", {
            "7": 2.426e+04, # [2]
            "8": 34138.15, # [1]
            "13": 120300., # [12]
            }),
    CrossSection("QCD_Pt_300to470", {
            "7": 1.168e+03, # [2]
            "8": 1759.549, # [1]
            "13": 7475., # [12]
            }),
    CrossSection("QCD_Pt_470to600", {
            "13": 587.1, # [12]
            }),
    CrossSection("QCD_Pt_600to800", {
            "13": 167., # [12]
            }),
    CrossSection("QCD_Pt_800to1000", {
            "13": 28.25, # [12]
            }),
    CrossSection("QCD_Pt_1000to1400", {
            "13": 8.195, # [12]
            }),
    CrossSection("QCD_Pt_1400to1800", {
            "13": 0.7346, # [12] # McM: 0.84265
            }),
    CrossSection("QCD_Pt_1800to2400", {
            "13": 0.1091, # [12] # McM: 0.114943
            }),
    CrossSection("QCD_Pt_2400to3200", {
            "13": 0.00682981, # [15]
            }),
    CrossSection("QCD_Pt_3200toInf", {
            "13": 0.000165445 , # [15]
            }),
    CrossSection("QCD_Pt20_MuEnriched", {
            "7": 296600000.*0.0002855, # [2]
            "8": 3.64e8*3.7e-4, # [1]
            }),
    CrossSection("QCD_Pt_50to80_MuEnrichedPt5", {
            "13": 4.487e+05, # 4.487e+05 +- 1.977e+02 pb [14]
    }),
    CrossSection("QCD_Pt_80to120_MuEnrichedPt5", {
            "13": 1.052e+05, # 1.052e+05 +- 5.262e+01 [14]
    }),
    CrossSection("QCD_Pt_120to170_MuEnrichedPt5", {
            "13": 2.549e+04, # 2.549e+04 +- 1.244e+01 [14]
    }),
    CrossSection("QCD_Pt_170to300_MuEnrichedPt5", {
            "13": 8.644e+03, # 8.644e+03 +- 4.226e+00 [14]
    }),
    CrossSection("QCD_Pt_300to470_MuEnrichedPt5", {
            "13": 7.967e+02, # 7.967e+02 +- 3.845e-0 [14]
    }),
    CrossSection("QCD_Pt_470to600_MuEnrichedPt5", {
            "13": 7.921e+01, # 7.921e+01 +- 5.425e-02 [14]
    }),
 #   CrossSection("WW", {
 #           "7": 43.0, # [3]
 #           "8": 54.838, # [9], took value for CTEQ PDF since CTEQ6L1 was used in pythia simulation
 #           "13": 118.7, # [13] NNLO QCD
 #           }),
            ######### from Andrea: WW -> lnqq : 52pb + WW -> lnln : 12.46pb
    CrossSection("WW", {
            "7": 43.0, # [3]
            "8": 54.838, # [9], took value for CTEQ PDF since CTEQ6L1 was used in pythia simulation
            "13": 64.46, # [13] NNLO QCD
            }),
    CrossSection("WZ", {
            "7": 18.2, # [3]
            "8": 33.21, # [9], took value for CTEQ PDF since CTEQ6L1 was used in pythia simulation
            #"13": 29.8 + 18.6, # [13] W+ Z/a* + W- Z/a*, MCFM 6.6 m(l+l-) > 40 GeV
            "13": 28.55 + 18.19, # [17]
            }),
    CrossSection("WZ_ext1", {
            "7": 18.2, # [3]
            "8": 33.21, # [9], took value for CTEQ PDF since CTEQ6L1 was used in pythia simulation
            #"13": 29.8 + 18.6, # [13] W+ Z/a* + W- Z/a*, MCFM 6.6 m(l+l-) > 40 GeV
            "13": 28.55 + 18.19, # [17]
            }),
    CrossSection("ZZ", {
            "7": 5.9, # [3]
            "8": 17.654, # [9], took value for CTEQ PDF since CTEQ6L1 was used in pythia simulation, this is slightly questionmark, since the computed value is for m(ll) > 12
            "13": 15.4, # [13]
            }),
    CrossSection("TTJets_FullLept", {
            "8": 245.8* 26.1975/249.50, # [10], BR from [11]
            }),
    CrossSection("TTJets_SemiLept", {
            "8": 245.8* 109.281/249.50, # [10], BR from [11]
            }),
    CrossSection("TTJets_Hadronic", {
            "8": 245.8* 114.0215/249.50, # [10], BR from [11]
            }),
    CrossSection("TTJets", {            
            "7": 172.0, # [10]
            "8": 245.8, # [10]
            "13": 6.639e+02, #6.639e+02 +- 8.237e+00 pb [16] (inputFiles="001AFDCE-C33B-E611-B032-0025905D1C54.root")            
            }),
    CrossSection("TT", {
            "7": 172.0, # [10]
            "8": 245.8, # [10]
            "13": 831.76, # [13] top mass 172.5, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
            }),
    CrossSection("TT_ext", {
            "7": 172.0, # [10]
            "8": 245.8, # [10]
            "13": 831.76, # [13] top mass 172.5, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
            }),
    CrossSection("TTJets_HT600to800", {
            "13": 0.0, 
            }),
    CrossSection("TTJets_HT800to1200", {
            "13": 0.0, 
            }),
    CrossSection("TTJets_HT1200to2500", {
            "13": 0.0, 
            }),
    CrossSection("TTJets_HT2500toInf", {
            "13": 0.0, 
            }),
    #CrossSection("WJets", {
            #"7": 31314.0, # [2], NNLO
            #"8": 36703.2, # [9], NNLO
            #}),
    CrossSection("WJetsToLNu", {
            "13": 20508.9*3, # [13] 20508.9*3, McM for the MLM dataset: 5.069e4
            }),
    CrossSection("WJetsToLNu_HT_100To200", {
            "13": 1.293e+03*1.2138, # McM times NNLO/LO ratio of inclusive sample
            }),
    CrossSection("WJetsToLNu_HT_200To400", {
            "13": 3.86e+02*1.2138, # McM times NNLO/LO ratio of inclusive sample
            }),
    CrossSection("WJetsToLNu_HT_400To600", {
            "13": 47.9*1.2138, # McM times NNLO/LO ratio of inclusive sample
            }),
    CrossSection("WJetsToLNu_HT_600ToInf", {
            "13": 0.0, # Forcing to zero to avoid overlap
            }),
    CrossSection("WJetsToLNu_HT_600To800", {
            "13": 12.8*1.2138, # McM times NNLO/LO ratio of inclusive sample
            }),
    CrossSection("WJetsToLNu_HT_800To1200", {
            "13": 5.26*1.2138, # McM times NNLO/LO ratio of inclusive sample
            }),
    CrossSection("WJetsToLNu_HT_1200To2500", {
            "13": 1.33*1.2138, # McM times NNLO/LO ratio of inclusive sample
            }),
    CrossSection("WJetsToLNu_HT_2500ToInf", {
            "13": 3.089e-02*1.2138, # McM times NNLO/LO ratio of inclusive sample
            }),
    # PREP (LO) cross sections, for W+NJets weighting
    CrossSection("PREP_WJets", {
            "7": 27770.0,
            "8": 30400.0,
            }),
    CrossSection("PREP_W1Jets", {
            "7": 4480.0,
            "8": 5400.0,
            }),
    CrossSection("PREP_W2Jets", {
            "7": 1435.0,
            "8": 1750.0,
            }),
    CrossSection("PREP_W3Jets", {
            "7": 304.2,
            "8": 519.0,
            }),
    CrossSection("PREP_W4Jets", {
            "7": 172.6,
            "8": 214.0,
            }),
    # end W+Njets 
    CrossSection("DYJetsToLL_M_50", {
            "7": 3048.0, # [4], NNLO
            "8": 3531.9, # [9], NNLO
            "13": 2008.4*3.0 # [14]
            }),
    CrossSection("DYJetsToLL_M_50_TauHLT", {
            "7": 3048.0, # [4], NNLO
            "8": 3531.9, # [9], NNLO
            "13": 2008.4*3.0 # [14]
            }),
    CrossSection("DYJetsToLL_M_10to50", {
            "7": 9611.0, # [1]
            "8": 11050.0, # [1]
            "13" :3205.6*3.0, # [14]
            }),
    CrossSection("DYJetsToLL_M_50_HT_100to200", {
            "13": 139.4*1.231, # McM times NNLO/LO ratio of inclusive sample
            }),
    CrossSection("DYJetsToLL_M_50_HT_200to400", {
            "13": 42.75*1.231, # McM times NNLO/LO ratio of inclusive sample
            }),
    CrossSection("DYJetsToLL_M_50_HT_400to600", {
            "13": 5.497*1.231, # McM times NNLO/LO ratio of inclusive sample
            }),
    CrossSection("DYJetsToLL_M_50_HT_600toInf", {
            "13": 2.21*1.231, # McM times NNLO/LO ratio of inclusive sample
            }),
    CrossSection("DYJetsToLL_M_100to200", {
            "13": 0.0, # FIXME
            }),
    CrossSection("DYJetsToLL_M_200to400", {
            "13": 0.0, # FIXME
            }),
    CrossSection("DYJetsToLL_M_400to500", {
            "13": 0.0, # FIXME
            }),
    CrossSection("DYJetsToLL_M_500to700", {
            "13": 0.0, # FIXME
            }),
    CrossSection("DYJetsToLL_M_700to800", {
            "13": 0.0, # FIXME
            }),
    CrossSection("DYJetsToLL_M_800to1000", {
            "13": 0.0, # FIXME
            }),
    CrossSection("DYJetsToLL_M_1000to1500", {
            "13": 0.0, # FIXME
            }),
    CrossSection("DYJetsToLL_M_1500to2000", {
            "13": 0.0, # FIXME
            }),
    CrossSection("DYJetsToLL_M_2000to3000", {
            "13": 0.0, # FIXME
            }),
    CrossSection("DY2JetsToLL_M_50", {
            "13": 3.345e+02, # [14]
            }),
    CrossSection("DY3JetsToLL_M_50", {
            "13": 1.022e+02, # [14]
            }),
    CrossSection("DY4JetsToLL_M_50", {
            "13": 5.446e+01, # [14]
            }),
    CrossSection("DYToTauTau_M_20_", {
            "7": 4998, # [4], NNLO
            "8": 5745.25, # [9], NNLO
            }),
    CrossSection("DYToTauTau_M_100to200", {
            "7": 0, # []
            "8": 34.92, # [1]
	    "13": 2.307e+02, # [14]
            }),
    CrossSection("DYToTauTau_M_200to400", {
            "7": 0, # []      
            "8": 1.181, # [1]
            "13": 7.839e+00, # [14]
            }),
   CrossSection("DYToTauTau_M_400to500", {
            "13": 3.957e-01, # [14]
            }),
   CrossSection("DYToTauTau_M_500to700", {
            "13": 2.352e-01, # [14]
            }),
   CrossSection("DYToTauTau_M_700to800", {
            "13": 3.957e-02, # [14]
            }),
    CrossSection("DYToTauTau_M_400to800", {
            "7": 0, # []      
            "8": 0.08699, # [1]
            }),
    CrossSection("DYToTauTau_M_800", {
            "7": 0, # []      
            "8": 0.004527, # [1]
            }),
    CrossSection("DYJetsToQQ_HT180", {
            "13": 1.209e+03, # 1.209e+03 +- 1.302e+00 pb [16]
            }),
    CrossSection("GluGluHToTauTau_M125", {
            "13": 1, # dummy value, not really needed as this sample is not merged with anything else
            }),
    CrossSection("GluGluHToTauTau_M125_TauHLT", {
            "13": 1, # dummy value, not really needed as this sample is not merged with anything else
            }),
    CrossSection("T_t-channel", {
            "7": 41.92, # [5,6]
            "8": 56.4, # [8]
            }),
    CrossSection("Tbar_t-channel", {
            "7": 22.65, # [5,6]
            "8": 30.7, # [8]
            }),
    CrossSection("T_tW-channel", {
            "7": 7.87, # [5,6]
            "8": 11.1, # [8]
            }),
    CrossSection("Tbar_tW-channel", {
            "7": 7.87, # [5,6]
            "8": 11.1, # [8]
            }),
    CrossSection("T_s-channel", {
            "7": 3.19, # [5,6]
            "8": 3.79, # [8]
            }),
    CrossSection("Tbar_s-channel", {
            "7": 1.44, # [5,6]
            "8": 1.76, # [8]
            }),
    CrossSection("ST_tW_antitop_5f_inclusiveDecays", {
            "13": 30.09, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    CrossSection("ST_tW_antitop_5f_inclusiveDecays_ext1", {
            "13": 30.09, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    CrossSection("ST_tW_antitop_5f_DS_inclusiveDecays", {
            "13": 35.85, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    CrossSection("ST_tW_top_5f_inclusiveDecays", {
            "13": 30.11, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    CrossSection("ST_tW_top_5f_inclusiveDecays_ext1", {
            "13": 30.11, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    CrossSection("ST_tW_top_5f_DS_inclusiveDecays", {
            "13": 35.85, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    CrossSection("ST_t_channel_antitop_4f_leptonDecays", {
            "13": 80.95, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    CrossSection("ST_t_channel_top_4f_leptonDecays", {
            "13": 136.02, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    CrossSection("ST_s_channel_4f_leptonDecays", {
            "13": 10.32, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
            ########################################### test for 743, modified
    CrossSection("ST_t_channel_antitop_4f_inclusiveDecays", {
            "13": 80.95, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
           ########################################### UUSI
    CrossSection("ST_s_channel_4f_InclusiveDecays", {
            "13": 10.32, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    CrossSection("ST_tW_top_4f_inclusiveDecays", {
            "13": 35.85, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    CrossSection("ST_t_channel_top_4f_inclusiveDecays", {
            "13": 136.02, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    CrossSection("ST_s_channel_4f_InclusiveDecays", {
            "13": 10.32, # [13] https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
            }),
    ########################################### Added for H+->tb
    CrossSection("QCD_bEnriched_HT100to200", {
            "13": 1.318e+06, # 1.318e+06 +- 6.249e+03 pb [16] (only 1 input file used)
            }),
    CrossSection("QCD_bEnriched_HT200to300", {
            "13": 8.823e+04, # 8.823e+04 +- 3.818e+01 pb [16]
            }),
    CrossSection("QCD_bEnriched_HT300to500", {
            "13": 8.764e+04, # 8.764e+04 +- 2.824e+02 pb [16] (only 1 input file used)
            }),
    CrossSection("QCD_bEnriched_HT500to700", {
            "13": 1.596e+03, # 1.596e+03 +- 9.784e-01 pb [16]
            }),
    CrossSection("QCD_bEnriched_HT700to1000", {
            "13": 3.213e+02, # 3.213e+02 +- 3.283e-01 pb [16]
            }),
    CrossSection("QCD_bEnriched_HT1000to1500", {
            "13": 5.093e+01, # 5.093e+01 +- 3.080e-01 pb [16]
            }),
    CrossSection("QCD_bEnriched_HT1500to2000", {
            "13": 4.445e+00, # 4.445e+00 +- 1.886e-02 pb [16]
            }),
    CrossSection("QCD_bEnriched_HT2000toInf", {
            "13": 7.847e-01, # 7.847e-01 +- 4.879e-03 pb [16]
            }),
    CrossSection("QCD_HT1500to2000_GenJets5", {
            "13": 6.718e+01, # 6.718e+01 +- 4.535e-02 pb [16]
            }),
    CrossSection("QCD_HT2000toInf_GenJets5", {
            "13": 1.446e+01, # 1.446e+01 +- 1.846e-02 pb [16]
            }),
    CrossSection("QCD_HT1000to1500_BGenFilter", {
            "13": 1.894e+02, # 1.894e+02 +- 1.660e-01 pb [16]
            }),
    CrossSection("QCD_HT1500to2000_BGenFilter", {
            "13": 2.035e+01, # 2.035e+01 +- 3.256e-02 pb [16]
            }),
    CrossSection("QCD_HT50to100", {
            "13": 2.464e+08, # 2.464e+08 +- 1.081e+05 pb [16]
            }),
    CrossSection("QCD_HT100to200", {
            "13": 2.803e+07, # 2.803e+07 +- 1.747e+04 pb [16]
            }),
    CrossSection("QCD_HT200to300", {
            "13": 1.713e+06, # 1.713e+06 +- 8.202e+02 pb [16]
            }),
    CrossSection("QCD_HT300to500", {
            "13": 3.475e+05, # 3.475e+05 +- 1.464e+02 pb [16]
            }),
    CrossSection("QCD_HT500to700", {
            "13": 3.208e+04, # 3.208e+04 +- 1.447e+01 pb [16]
            }),
    CrossSection("QCD_HT700to1000", {
            "13": 6.833e+03, # 6.833e+03 +- 1.668e+00 pb [16]
            }),
    CrossSection("QCD_HT1000to1500", {
            "13": 1.208e+03, # 1.208e+03 +- 5.346e-01 pb [16]
            }),
    CrossSection("QCD_HT1500to2000", {
            "13": 1.201e+02, # 1.201e+02 +- 5.823e-02 pb [16]
            }),
    CrossSection("QCD_HT2000toInf", {
            "13": 2.526e+01, # 2.526e+01 +- 1.728e-02 pb [16]
            }),
    CrossSection("TTTT", {
            "13": 9.103e-03, #9.103e-03 +- 1.401e-05 pb [16]
            }),
    CrossSection("TTWJetsToQQ", {
            "13": 4.034e-01, #4.034e-01 +- 2.493e-03 pb [16] (inputFiles="2211E19A-CC1E-E611-97CC-44A84225C911.root")
            }),
    CrossSection("TTZToQQ", {
            "13": 5.297e-01, #5.297e-01 +- 7.941e-04 pb [16] (inputFiles="204FB864-5D1A-E611-9BA7-001E67A3F49D.root")
            }),
    CrossSection("WJetsToQQ_HT_600ToInf", {
            "13": 9.936e+01, #9.936e+01 +- 4.407e-01 pb [16] (inputFiles="0EA1D6CA-931A-E611-BFCD-BCEE7B2FE01D.root")
            }),
    CrossSection("WWTo4Q", {
            "13": 4.520e+01, #4.520e+01 +- 3.608e-02 pb [16] (inputFiles="0A4AE358-861F-E611-A48C-44A84225C851.root")
            }),
    CrossSection("ZJetsToQQ_HT600toInf", {
            "13": 5.822e+02, #5.822e+02 +- 7.971e-02 pb [16] (inputFiles="0E546A76-E03A-E611-9259-0CC47A4DEDEE.root")
            }),
    CrossSection("ZZTo4Q", {
            "13": 6.883e+00, #6.883e+00 +- 3.718e-02 pb [16] (inputFiles="024C4223-171B-E611-81E5-0025904E4064.root")
            }),
    CrossSection("ttbb_4FS_ckm_amcatnlo_madspin_pythia8", {
            "13": 1.393e+01, #1.393e+01 +- 3.629e-02 pb [16] (inputFiles="0641890F-F72C-E611-9EA8-02163E014B5F.root")
            }),   
    )

## Set background process cross sections
#
# \param datasets            dataset.DatasetManager object
# \param doWNJetsWeighting   Set W+Njets cross sections according to the weighting scheme
def setBackgroundCrossSections(datasets, doWNJetsWeighting=True, quietMode=False):
    for dset in datasets.getMCDatasets():
        setBackgroundCrossSectionForDataset(dset, doWNJetsWeighting, quietMode)

def setBackgroundCrossSectionForDataset(dataset, doWNJetsWeighting=True, quietMode=False):
    value = backgroundCrossSections.crossSection(dataset.getName().replace("_ext",""), dataset.getEnergy())
    value = backgroundCrossSections.crossSection(dataset.getName().replace("_ext3",""), dataset.getEnergy())
    if value is None:
        if "ChargedHiggs" in dataset.getName():
            value = 1.0 # Force signal xsection to 1 pb
        else:
            for wnJets in ["W1Jets", "W2Jets", "W3Jets", "W4Jets"]:
                if wnJets in dataset.getName():
                    inclusiveCrossSection = backgroundCrossSections.crossSection("WJets", dataset.getEnergy())
                    if doWNJetsWeighting:
                        # W+Njets, with the assumption that they are weighted (see
                        # src/WJetsWeight.cc)
                        value = inclusiveCrossSection
                    else:
                        inclusiveLO = backgroundCrossSections.crossSection("PREP_WJets", dataset.getEnergy())
                        wnJetsLO = backgroundCrossSections.crossSection("PREP_"+wnJets, dataset.getEnergy())
                        value = inclusiveCrossSection * wnJetsLO/inclusiveLO
                    break

    if value is not None:
        dataset.setCrossSection(value)
        msg      = ""
        txtAlign = "{0:<10} {1:<40} {2:>15} {3:>20} {4:<5} {5:<50}"
        if value == 0:
            msg = "\n*** Note: to set non-zero xsection; edit NtupleAnalysis/python/tools/crossection.py"
        if "ChargedHiggs" in dataset.getName():
            #msg = "\n*** Note: signal is forced at the moment to 1 pb in NtupleAnalysis/python/tools/crossection.py"
            msg = ""
        if not quietMode:
            msg = txtAlign.format("Setting", dataset.getName(), "cross section to ", "%0.6f" %(value), "pb", msg)
            Print(msg, False)
    else:
        Print("Warning: no cross section for dataset %s with energy %s TeV (see python/tools/crosssection.py)" % (dataset.getName(), dataset.getEnergy()), True)


########################################
# Signal cross section table

import HiggsAnalysis.LimitCalc.BRdataInterface as br

# Default value of MSSM mu parameter
defaultMu = 200

## Generic light H+ MSSM cross section
#
# \param function function to calculate the cross section from BR's
# \param mass     H+ mass
# \param tanbeta  tanbeta parameter
# \param mu       mu parameter
# \param energy   sqrt(s) in TeV as string
def lightCrossSectionMSSM(function, mass, tanbeta, mu, energy):
    br_tH = br.getBR_top2bHp(mass, tanbeta, mu)
    br_Htaunu = br.getBR_Hp2tau(mass, tanbeta, mu)
    return function(br_tH, br_Htaunu, energy)

## Heavy H+ MSSM cross section
#
# \param mass     H+ mass
# \param tanbeta  tanbeta parameter
# \param mu       mu parameter
# \param energy   sqrt(s) in TeV as string
def heavyCrossSectionMSSM(mass, tanbeta, mu, energy):
    raise Exception("No heavy H+ cross sections yet!")

## WH, H->tau nu cross section from BRs
#
# \param br_tH      BR(t -> b H+)
# \param br_Htaunu  BR(H+ -> tau nu)
# \param energy     sqrt(s) in TeV as string
def whTauNuCrossSection(br_tH, br_Htaunu, energy):
    ttCrossSection = backgroundCrossSections.crossSection("TTJets", energy)
    xsec = 2 * ttCrossSection * br_tH * (1-br_tH) * br_Htaunu
    return (xsec, br_tH)

## HH, H->tau nu cross section from BRs
#
# \param br_tH      BR(t -> b H+)
# \param br_Htaunu  BR(H+ -> tau nu)
# \param energy     sqrt(s) in TeV as string
def hhTauNuCrossSection(br_tH, br_Htaunu, energy):
    ttCrossSection = backgroundCrossSections.crossSection("TTJets", energy)
    xsec = ttCrossSection * br_tH*br_tH * br_Htaunu*br_Htaunu
    return (xsec, br_tH)

## Single H, H->tau nu cross section from BRs
#
# \param br_tH      BR(t -> b H+)
# \param br_Htaunu  BR(H+ -> tau nu)
# \param energy     sqrt(s) in TeV as string
# \param channel    channel as string
def hTauNuCrossSection(br_tH, br_Htaunu, energy, channel):
    tCrossSection  = backgroundCrossSections.crossSection("T_"+channel, energy)
    tCrossSection += backgroundCrossSections.crossSection("Tbar_"+channel, energy)
    xsec = tCrossSection * br_tH * br_Htaunu
    return (xsec, br_tH)

## Helper function to set a cross section of one signal dataset
#
# \param name     Name of the dataset
# \param mass     H+ mass
# \param datasets dataset.DatasetManager object
# \param function Function taking the mass and energy, and returning cross section and BR(t->H+)
def _setHplusCrossSectionsHelper(name, mass, datasets, function):
    if not datasets.hasDataset(name):
        return
    d = datasets.getDataset(name)
    (crossSection, BRtH) = function(mass, d.getEnergy())
    d.setCrossSection(crossSection)
    if BRtH is not None:
        d.setProperty("BRtH", BRtH)
    print "Setting %s cross section to %f pb" % (name, crossSection)

## Helper function to set cross sections of all signal datasets
#
# \param datasets     dataset.DatasetManager object
# \param whFunction   Function to calculate tt->WH cross section from
#                     mass and energy, and returning cross section and
#                     BR(t->H+)
# \param hhFunction   Function to calculate tt->HH cross section from
#                     mass and energy, and returning cross section and
#                     BR(t->H+)
# \param hFunction    Function to calculate t->H cross section from mass,
#                     energy, and channel, and returning cross section
#                     and BR(t->H+)
# \param heavyFunction  Function to calculate heavy H+ cross section
#                       from mass and energy, and returning cross
#                       section and BR(t->H+)
def _setHplusCrossSections(datasets, whFunction, hhFunction, hFunction, heavyFunction=None):
    import HiggsAnalysis.NtupleAnalysis.tools.plots as plots

    for mass in plots._lightHplusMasses:
        _setHplusCrossSectionsHelper("TTToHplusBWB_M%d"%mass, mass, datasets, whFunction)
        _setHplusCrossSectionsHelper("TTToHplusBHminusB_M%d"%mass, mass, datasets, hhFunction)

        for channel in ["s-channel", "t-channel", "tW-channel"]:
            _setHplusCrossSectionsHelper("Hplus_taunu_%s_M%d"%(channel, mass), mass, datasets, lambda mass, energy: hFunction(mass, energy, channel))

    if heavyFunction is not None:
        for mass in plots._heavyHplusMasses:
            _setHplusCrossSectionsHelper("HplusTB_M%d"%mass, mass, datasets, heavyFunction)


## Set signal dataset cross sections to ttbar cross section
#
# \param datasets  dataset.DatasetManager object
def setHplusCrossSectionsToTop(datasets):
    function = lambda mass, energy: (backgroundCrossSections.crossSection("TTJets", energy), None)
    _setHplusCrossSections(datasets, function, function)

## Set signal dataset cross sections to MSSM cross section
#
# \param datasets  dataset.DatasetManager object
# \param tanbeta   tanbeta parameter
# \param mu        mu parameter
def setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=defaultMu):
    import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
    histograms.createSignalText.set(tanbeta=tanbeta)
    if mu != defaultMu:
        histograms.createSignalText.set(mu=mu)

    def singleHhelper(mass, energy, channel):
        return lightCrossSectionMSSM(lambda br1, br2, en: hTauNuCrossSection(br1, br2, en, channel), mass, tanbeta, mu, energy)

    _setHplusCrossSections(datasets,
        lambda mass, energy: lightCrossSectionMSSM(whTauNuCrossSection, mass, tanbeta, mu, energy),
        lambda mass, energy: lightCrossSectionMSSM(hhTauNuCrossSection, mass, tanbeta, mu, energy),
        singleHhelper)
#       lambda mass, energy: heavyCrossSectionMSSM(mass, tanbeta, mu, energy)) # FIXME: uncomment when we get heavy H+ cross sections

## Set signal dataset cross sections to cross section via BR
#
# \param datasets   dataset.DatasetManager object
# \param br_tH      BR(t -> b H+)
# \param br_Htaunu  BR(H+ -> tau nu)
def setHplusCrossSectionsToBR(datasets, br_tH, br_Htaunu):
    import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
    histograms.createSignalText.set(br_tH=br_tH)
    _setHplusCrossSections(datasets,
                           lambda mass, energy: whTauNuCrossSection(br_tH, br_Htaunu, energy),
                           lambda mass, energy: hhTauNuCrossSection(br_tH, br_Htaunu, energy),
                           lambda mass, energy, channel: hTauNuCrossSection(br_tH, br_Htaunu, energy, channel))

## Set signal dataset cross sections to cross section (deprecated, only for compatibility)
def setHplusCrossSections(datasets, tanbeta=20, mu=defaultMu, toTop=False):
    if toTop:
        setHplusCrossSectionsToTop(datasets)
    else:
        setHplusCrossSectionsToMSSM(tanbeta, mu)

## Print H+ cross sections for given tanbeta values
#
# \param tanbetas  List of tanbeta values
# \param mu        Mu parameter
# \param energy    sqrt(s) in TeV as string
def printHplusCrossSections(tanbetas=[10, 20, 30, 40], mu=defaultMu, energy="7"):
    ttCrossSection = backgroundCrossSections.crossSection("TTJets", energy)
    tCrossSection  = sum([backgroundCrossSections.crossSection("T_"+channel, energy)    for channel in ["s-channel", "t-channel", "tW-channel"]])
    tCrossSection += sum([backgroundCrossSections.crossSection("Tbar_"+channel, energy) for channel in ["s-channel", "t-channel", "tW-channel"]])
    print "ttbar cross section %.1f pb" % ttCrossSection
    print "single top cross section %.1f pb" % tCrossSection
    print "mu %.1f" % mu
    print
    for tanbeta in [10, 20, 30, 40]:
        print "="*98
        print "tan(beta) = %d" % tanbeta
        print "H+ M (GeV) | BR(t->bH+) | BR(H+->taunu) | sigma(tt->tbH+->tbtaunu) | sigma(tt->bbH+H-->bbtautau) | sigma(t->bH+->btau) |"
        for mass in [90, 100, 120, 140, 150, 155, 160]:
            br_tH = br.getBR_top2bHp(mass, tanbeta, mu)
            br_Htaunu = br.getBR_Hp2tau(mass, tanbeta, mu)

            xsec_wh = lightCrossSectionMSSM(whTauNuCrossSection, mass, tanbeta, mu, energy)[0]
            xsec_hh = lightCrossSectionMSSM(hhTauNuCrossSection, mass, tanbeta, mu, energy)[0]
            xsec_h = sum([lightCrossSectionMSSM(lambda br1, br2, en: hTauNuCrossSection(br1, br2, en, channel), mass, tanbeta, mu, energy)[0] for channel in ["s-channel", "t-channel", "tW-channel"]])

            print "%10d | %10f | %13f | %24f | %27f | %19f |" % (mass, br_tH, br_Htaunu, xsec_wh, xsec_hh, xsec_h)


if __name__ == "__main__":
    printHplusCrossSections(energy="7")
    printHplusCrossSections(energy="8")
    printHplusCrossSections(energy="13")
