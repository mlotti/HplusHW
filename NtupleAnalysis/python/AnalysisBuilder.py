'''
Package: AnalysisConfig

Analysis configuration, with ability to create the main analyzer 
and the analyzers for the N systematic uncertainty variations 
and other variations based on the config.
'''

#================================================================================================  
# Imports
#================================================================================================  
from HiggsAnalysis.NtupleAnalysis.main import Analyzer
import HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles

#================================================================================================
# Global Definitions
#================================================================================================
VERBOSE = False

#================================================================================================
# Function Definition
#================================================================================================
def Verbose(msg, printHeader=False):
    '''                                                                                                                                                                       
    Calls Print() only if verbose options is set to true.                                                                                                                     
    '''
    if not VERBOSE:
        return
    Print(msg, printHeader)
    return


def Print(msg, printHeader=True):
    '''                                                                                                                                                                       
    Simple print function. If verbose option is enabled prints, otherwise does nothing.                                                                                       
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return

#================================================================================================
# Class Definition
#================================================================================================
class AnalysisConfig:
    '''
    Container class for analysis configuration
    '''
    def __init__(self, selectorName, moduleName, config, **kwargs):
        Verbose("__init__()", True)
        self._selectorName = selectorName
        self._moduleName = moduleName
        self._config = config.clone()
        #self.__dict__.update(kwargs)
	#print kwargs

        #===== Process all keyword arguments to make changes to the config
        keys = kwargs.keys()
        for key in keys:
	    value = kwargs[key]
	    if key == "systematics":
                self._config.histogramAmbientLevel = "Systematics"

                # Energy scales
		if value.startswith("TauES"):
		    self._config.TauSelection.systematicVariation = "_"+value.replace("Plus","down").replace("Minus","up").replace("TauES","TES")
		elif value.startswith("JES"):
		    self._config.JetSelection.systematicVariation = "_"+value.replace("Plus","down").replace("Minus","up")
		elif value.startswith("JER"):
		    self._config.JetSelection.systematicVariation = "_"+value.replace("Plus","down").replace("Minus","up")
		elif value.startswith("UES"):
		    self._config.METSelection.systematicVariation = "_"+value.replace("Plus_x","down_x").replace("Minus_x","up_x").replace("UES","MET_Type1_UnclusteredEn") #FIXME: should also _y be taken into account?
		    self._config.METSelection.systematicVariation = "_"+value.replace("Plus_y","down_y").replace("Minus_y","up_y").replace("UES","MET_Type1_UnclusteredEn") #FIXME: should also _y be taken into account?

		# Fake tau 
		elif value.startswith("FakeTau"):
                    etaRegion = "full"
                    if "Barrel" in value:
                        etaRegion = "barrel"
                    elif "Endcap" in value:
                        etaRegion = "endcap"
                    partonFakingTau = None
                    if "Electron" in value:
                        partonFakingTau = "eToTau"
                    elif "Muon" in value:
                        partonFakingTau = "muToTau"
                    elif "Jet" in value:
                        partonFakingTau = "jetToTau"
                    scaleFactors.assignTauMisidentificationSF(self._config.TauSelection, 
                                                              partonFakingTau, etaRegion, 
                                                              self._getDirectionString(value))
		# Trigger
		elif value.startswith("TauTrgEff"):
                    variationType = value.replace("TauTrgEff","").replace("Minus","").replace("Plus","")
                    scaleFactors.assignTauTriggerSF(self._config.TauSelection, self._getDirectionString(value), self._config.Trigger.TautriggerEfficiencyJsonName, variationType)
                elif value.startswith("METTrgEff"):
                    variationType = value.replace("METTrgEff","").replace("Minus","").replace("Plus","")
                    scaleFactors.assignMETTriggerSF(self._config.METSelection, self._config.BJetSelection.bjetDiscrWorkingPoint, self._getDirectionString(value), self._config.Trigger.METtriggerEfficiencyJsonName, variationType)
                elif value.startswith("MuonTrgEff"):
                    variationType = value.replace("MuonTrgEff","").replace("Minus","").replace("Plus","")
                    scaleFactors.assignMuonTriggerSF(self._config.MuonSelection, self._getDirectionString(value), self._config.Trigger.MuontriggerEfficiencyJsonName, variationType)

                # tau ID syst
                elif value.startswith("TauIDSyst"):
                    self._config.systematicVariation = "_"+value.replace("Plus","down").replace("Minus","up")

		# muon ID syst
                elif value.startswith("MuonIDSyst"):
                    self._config.systematicVariation = "_"+value.replace("Plus","down").replace("Minus","up")

		# b tag SF
		elif value.startswith("BTagSF") or value.startswith("BMistagSF"):
                    variationType = None
                    if value.startswith("BTagSF"):
                        variationType = "tag"
                    elif value.startswith("BMistagSF"):
                        variationType = "mistag"
                    direction = value.replace("BTagSF","").replace("BMistagSF","").replace("Minus","down").replace("Plus","up")
                    scaleFactors.updateBtagSFInformationForVariations(self._config.BJetSelection, direction=direction, variationInfo=variationType)

		# top quarks
		elif value.startswith("TopPt"):
                    self._config.topPtSystematicVariation = value.replace("TopPt","").replace("Plus","plus").replace("Minus","minus")
#		# PU weights
		elif value.startswith("PUWeight"):
                    self._config.PUWeightSystematicVariation = value.replace("PUWeight","").replace("Plus","plus").replace("Minus","minus")
		else:
		    if value != "nominal":
                        raise Exception("Error: unsupported variation item '%s'!"%value)
	    else:
		# Process optimization options
		# First check that key is found in config
		subkeys = key.split(".")
		subconfig = [self._config]
		suffix = ""
		for i in range(len(subkeys)-1):
		    if not hasattr(subconfig[len(subconfig)-1], subkeys[i]):
			raise Exception("Error: Cannot find key %s.%s in the config!"%(suffix, subkeys[i]))
		    subconfig.append(getattr(subconfig[len(subconfig)-1], subkeys[i]))
		    if suffix == "":
			suffix += "%s"%subkeys[i]
		    else:
			suffix += ".%s"%subkeys[i]
		# Set varied value in configuration (treat AngularCuts in a special way)
		if key.startswith("AngularCuts") and subkeys[len(subkeys)-1] == "workingPoint":
                    from HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import setAngularCutsWorkingPoint
                    setAngularCutsWorkingPoint(subconfig[len(subconfig)-1], value)
                else: # all other settings than AngularCuts
                    if not hasattr(subconfig[len(subconfig)-1], subkeys[len(subkeys)-1]):
                        raise Exception("Error: Cannot find key %s.%s in the config!"%(suffix, subkeys[len(subkeys)-1]))
                    setattr(subconfig[len(subconfig)-1], subkeys[len(subkeys)-1], value)
                # Additionally, set a new tau ID scale factor if needed
                    from HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors import assignTauIdentificationSF
                    scaleFactors.assignTauIdentificationSF(subconfig[len(subconfig)-1])
                # TODO: Define here any other updates for scale factors if needed

    ## Create and register the analysis after the changes have bene done to the config
    def registerAnalysis(self, process):
        Verbose("registerAnalysis()", True)
        process.addAnalyzer(self._moduleName, Analyzer(self._selectorName, config=self._config, silent=True))
        return


    ## Convert value string into direction string
    def _getDirectionString(self, value):
        Verbose("_getDirectionString()", True)
        direction = None
        if value.endswith("Plus"):
            direction = "up"
        elif value.endswith("Minus"):
            direction = "down"
        return direction
    

#================================================================================================
# Class Definition
#================================================================================================
class AnalysisBuilder:
    '''
    Class for building analyses
    '''
    def __init__(self,
                 name,                  # The module name (beware, the downstream python code has assumptions on this)
                 # Required options
                 dataEras=["2016"],        # Data era (see python/tools/dataset.py::_dataEras)
                 searchModes=["m80to160"], # Search mode (see python/parameters/signalAnalysisParameters.py)
                 # Optional options
                 usePUreweighting=True,    # enable/disable vertex reweighting
                 useTopPtReweighting=True, # enable/disable top pt reweighting for ttbar
                 # Systematics options
                 doSystematicVariations=False, # Enable/disable adding modules for systematic uncertainty variation
                 analysisType="HToTauNu",      # Define the analsysi to allow a handle of changing variables accordingly
                ):
        self._name = name
        self._dataEras = []
        if isinstance(dataEras, list):
            self._dataEras = dataEras[:]
        else:
            self._dataEras.append(dataEras)
        self._searchModes = []
        if isinstance(searchModes, list):
            self._searchModes = searchModes[:]
        else:
            self._searchModes.append(searchModes)
        self._usePUreweighting = usePUreweighting
        self._useTopPtReweighting = useTopPtReweighting
        self._variations={}
        self._doSystematics = doSystematicVariations    
        self._analysisType  = self._getAnalysisType(analysisType)
        self._processSystematicsVariations()
        return

    def _getAnalysisType(self, analysis):
        myAnalyses = ["HToTauNu", "HToTB","HToHW","HToHW_background"]
        if analysis not in myAnalyses:
            msg = "Unsupported analysis \"%s\". Please select one of the following: %s" % (analysis, ", ".join(myAnalyses))
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle() )
        else:
            return analysis

    def getListOfSystematics(self):
        if self._analysisType == "HToTauNu":
            return self.getSystematicsForHToTauNu()
        elif  self._analysisType == "HToTB":
            return self.getSystematicsForHToTB()
	elif  self._analysisType == "HToHW":
            return self.getSystematicsForHToHW()
	elif  self._analysisType == "HToHW_background":
            return self.getSystematicsForHToHW_background()
        else:
            raise Exception(ShellStyles.ErrorStyle() + "This should never be reached" + ShellStyles.NormalStyle() )

    def getSystematicsForHToTauNu(self):
        items = []
        # Trigger systematics
        items.extend(["TauTrgEffData", "TauTrgEffMC"])

        #items.extend(["L1ETMDataEff", "L1ETMMCEff"])
        items.extend(["METTrgEffData", "METTrgEffMC"])

        # Tau ID variation systematics
        items.extend(["FakeTauElectron", "FakeTauMuon", "FakeTauJet", "TauIDSyst"])


        # Energy scales and JER systematics
        items.extend(["TauES", "JES", "JER", "UES"])

        # b quark systematics
        items.extend(["BTagSF", "BMistagSF"])

        # top quark systematics
        if self._useTopPtReweighting:
            items.append("TopPt") 

        # PU weight systematics
        items.extend(["PUWeight"])
        return items

    def getSystematicsForHToTB(self):
        items = []
        # Energy scales and JER systematics
        items.extend(["JES", "JER"])

        # b quark systematics
        items.extend(["BTagSF"])

        # top quark systematics
        if self._useTopPtReweighting:
            items.append("TopPt") 

        # PU weight systematics
        items.extend(["PUWeight"])        
        return items


    def getSystematicsForHToHW(self):
        items = []

        # Trigger systematics
        items.extend(["MuonTrgEffData"])

        # Tau ID variation systematics
        items.extend(["FakeTauElectron", "FakeTauMuon", "FakeTauJet", "TauIDSyst"])

        # Muon ID variation systematics
        items.extend(["MuonIDSyst"])

        # Energy scales and JER systematics
        items.extend(["TauES", "JES", "JER", "UES"])

        # b quark systematics
        items.extend(["BTagSF", "BMistagSF"])

        # top quark systematics
        if self._useTopPtReweighting:
            items.append("TopPt")

        # PU weight systematics
        items.extend(["PUWeight"])

        return items

    def getSystematicsForHToHW_background(self):
        items = []

        # Trigger systematics
        items.extend(["MuonTrgEffData"])

        return items

    def _processSystematicsVariations(self):
        if not self._doSystematics:
            return

        # Process systematic uncertainty variations
        items = self.getListOfSystematics()
        # Create configs
        self._variations["systematics"] = []
        for item in items:
            self._variations["systematics"].append("%sPlus" % item)
            self._variations["systematics"].append("%sMinus"% item)
        return

    def addVariation(self, configItemString, listOfValues):
        Verbose("addVariation()", True)
        self._variations[configItemString] = listOfValues
        return


    def build(self, process, config):
        Verbose("build()", True)
        # Add here options to the config
        config.__setattr__("usePileupWeights", self._usePUreweighting)
        config.__setattr__("useTopPtWeights", self._useTopPtReweighting)
        # Add nominal modules
        if len(self._variations.keys()) > 1 and "systematics" in self._variations.keys():
            self._variations["systematics"].insert(0, "nominal")
        # Create list of configs for the modules
        configs = []
        for searchMode in self._searchModes:
            for dataEra in self._dataEras:
                modStr = "%s_%s_Run%s"%(self._name, searchMode, dataEra)
                # Create nominal module without any variation
                configs.append(AnalysisConfig(self._name, modStr, config))
                Print("Created nominal module: %s" % (modStr) )
                # Create modules for optimization and systematics variations
                configs.extend(self._buildVariation(config, modStr))
        # Register the modules
        for module in configs:
            module.registerAnalysis(process)
        Print("Created %d modules" % (len(configs)) )
        #print configs[0]._config
        return
        

    def _buildVariation(self, config, moduleName, optName="", systName="", level=0, **kwargs):
        '''
        Builds iteratively the variations
        Logic: Variation specs are put into kwargs as key,value pairs 
        For systematics key=systematics, value=identifier; only a single systematics variation per module is allowed
        For variations key=config entry, value=value; multiple simultaneous variations per module are allowed
        '''
        Verbose("_buildVariation()", True)
        configs = []
        keys = self._variations.keys()
        if len(keys) == 0:
            return configs

        for item in self._variations[keys[level]]:
            newSystName = systName
            newOptName = optName
            if keys[level] == "systematics":
                if newSystName != "":
                    raise Exception("Error: there can only be one syst. name (asking for %s and already registered %s)"%(item, systName))
                else:
                    newSystName = item
            else:
		split = keys[level].split(".")
		name = split[len(split)-1]
                newOptName += "%s%s"%(name[0].upper()+name[1:], str(item).replace("-","m").replace(".","p"))
            # Move to next level or build variation
            if level < len(keys)-1:
                kwargs[keys[level]] = item
                configs.extend(self._buildVariation(config, moduleName, newOptName, newSystName, level+1, **kwargs))
                del kwargs[keys[level]]
            else:
                modStr = moduleName
                if newOptName != "":
                    modStr += "_Opt%s"%newOptName
                if newSystName != "" and newSystName != "nominal":
                    modStr += "_SystVar%s"%newSystName
		kwargs[keys[level]]=item
                configs.append(AnalysisConfig(self._name, modStr, config, **kwargs))
                del kwargs[keys[level]]
                print "Created variation module %s"%modStr
        return configs

# TODO:
# need to figure out how to set scale factors
