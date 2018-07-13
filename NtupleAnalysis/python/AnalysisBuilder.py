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
sh_Error   = ShellStyles.ErrorStyle()
sh_Success = ShellStyles.SuccessStyle()
sh_Note    = ShellStyles.HighlightAltStyle()
sh_Normal  = ShellStyles.NormalStyle()

#================================================================================================
# Class Definition
#================================================================================================
class AnalysisConfig:
    '''
    Container class for analysis configuration
    '''
    def __init__(self, selectorName, moduleName, config, verbose, **kwargs):
        self._selectorName = selectorName
        self._moduleName = moduleName
        self._config  = config.clone()
        self._verbose = verbose

        # Process all keyword arguments to make changes to the config
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
                    # FIXME: should also _y be taken into account?
		    self._config.METSelection.systematicVariation = "_"+value.replace("Plus_x","down_x").replace("Minus_x","up_x").replace("UES","MET_Type1_UnclusteredEn") 
		    self._config.METSelection.systematicVariation = "_"+value.replace("Plus_y","down_y").replace("Minus_y","up_y").replace("UES","MET_Type1_UnclusteredEn")
		# Fake tau 
		elif value.startswith("FakeTau"):
                    partonFakingTau = None
                    if "Electron" in value:
                        partonFakingTau = "eToTau"
                    elif "Muon" in value:
                        partonFakingTau = "muToTau"
                    elif "Jet" in value:
                        partonFakingTau = "jetToTau"
                    scaleFactors.assignTauMisidentificationSF(self._config.TauSelection, 
                                                              partonFakingTau, 
                                                              self._getDirectionString(value))
		# Trigger
		elif value.startswith("TauTrgEff"):
                    variationType = value.replace("TauTrgEff","").replace("Minus","").replace("Plus","")
                    scaleFactors.assignTauTriggerSF(self._config.TauSelection, self._getDirectionString(value), self._config.Trigger.TautriggerEfficiencyJsonName, variationType)
                elif value.startswith("METTrgEff"):
                    variationType = value.replace("METTrgEff","").replace("Minus","").replace("Plus","")
                    scaleFactors.assignMETTriggerSF(self._config.METSelection, self._config.BJetSelection.bjetDiscrWorkingPoint, self._getDirectionString(value), self._config.Trigger.METtriggerEfficiencyJsonName, variationType)

                # tau ID syst
                elif value.startswith("TauIDSyst"):
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

		# top-tag SF
		elif value.startswith("TopTagSF") or value.startswith("TopMistagSF"):
                    variationType = None
                    if value.startswith("TopTagSF"):
                        variationType = "tag"
                    elif value.startswith("TopMistagSF"):
                        variationType = "mistag"
                    direction = value.replace("TopTagSF","").replace("TopMistagSF","").replace("Minus","down").replace("Plus","up")
                    scaleFactors.updateTopTagSFInformationForVariations(self._config.TopSelectionBDT, direction=direction, variationInfo=variationType)

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

    def Verbose(self, msg, printHeader=False):
        '''                                                                                                                                                                       
        Calls Print() only if verbose options is set to true.                                                                                                                     
        '''
        if not opts._verbose:
            return
        self.Print(msg, printHeader)
        return

    def Print(self, msg, printHeader=True):
        '''                                                                                                                                                                       
        Simple print function. If verbose option is enabled prints, otherwise does nothing.                                                                                       
        '''
        fName = __file__.split("/")[-1]
        if printHeader:
            print "=== ", fName
        print "\t", msg
        return

    def registerAnalysis(self, process):
        '''
        Create and register the analysis after the changes have bene done to the config
        '''
        process.addAnalyzer(self._moduleName, Analyzer(self._selectorName, config=self._config, silent=True))
        return
    
    def _getDirectionString(self, value):
        '''
        Convert value string into direction string
        '''
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
                 name, # The module name (beware, the downstream python code has assumptions on this)
                 dataEras=["2016"], # Data era (see python/tools/dataset.py::_dataEras)
                 searchModes=["m80to160"], # Search mode (see python/parameters/signalAnalysisParameters.py)
                 # Optional options
                 usePUreweighting=True,    # enable/disable vertex reweighting
                 useTopPtReweighting=True, # enable/disable top pt reweighting for ttbar
                 # Systematics options
                 doSystematicVariations=False, # Enable/disable adding modules for systematic uncertainty variation
                 analysisType="HToTauNu", # Define the analysis type (e.g. "HToTauNu", "HToTB")
                 verbose=False,
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
        self._verbose = verbose
        self._processSystematicsVariations()
        return

    def Verbose(self, msg, printHeader=False):
        '''                                                                                                                                                                       
        Calls Print() only if verbose options is set to true.                                                                                                                     
        '''
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return

    def Print(self, msg, printHeader=True):
        '''                                                                                                                                                                       
        Simple print function. If verbose option is enabled prints, otherwise does nothing.                                                                                       
        '''
        fName = __file__.split("/")[-1].replace(".pyc", ".py")
        if printHeader:
            print "=== ", fName
        print "\t", msg
        return

    def _getAnalysisType(self, analysis):
        myAnalyses = ["HToTauNu", "HToTB"]
        if analysis not in myAnalyses:
            msg = "Unsupported analysis \"%s\". Please select one of the following: %s" % (analysis, ", ".join(myAnalyses))
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle() )
        else:
            self.Print("Analysis type set to %s" % (sh_Note + analysis + sh_Normal), True)
            return analysis

    def getListOfSystematics(self):
        systList = None
        if self._analysisType == "HToTauNu":
            systList =  self.getSystematicsForHToTauNu()
        elif  self._analysisType == "HToTB":
            systList = self.getSystematicsForHToTB()
        else:
            raise Exception(ShellStyles.ErrorStyle() + "This should never be reached" + ShellStyles.NormalStyle() )
        if len(systList) < 1:
            self.Print("Disabled systematics", False)
        else:
            self.Print("Enabled %d systematics (%s)" % (len(systList), sh_Note + ", ".join(systList) + sh_Normal), False)
        return systList

    def getSystematicsForHToTauNu(self):
        items = []
        # Trigger systematics
        items.extend(["TauTrgEffData", "TauTrgEffMC"]) 

        #items.extend(["L1ETMDataEff", "L1ETMMCEff"])
        items.extend(["METTrgEffData", "METTrgEffMC"])

        # Tau ID variation systematics
        items.extend(["TauIDSyst"])

        # Tau mis-ID systematics
        items.extend(["FakeTauElectron", "FakeTauMuon"])

        # Energy scales and JER systematics
#        items.extend(["TauES", "JES", "UES"]) # use in case of problems with JER
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
        
        # TopTagSF weight systematics
        self.Print("Disabled top-tag SF systematic variations (temporary", True)
        # items.extend(["TopTagSF"])
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
        self._variations[configItemString] = listOfValues
        return

    def build(self, process, config):
        # Add here options to the config
        config.__setattr__("usePileupWeights", self._usePUreweighting)
        config.__setattr__("useTopPtWeights" , self._useTopPtReweighting)

        # Add nominal modules
        if len(self._variations.keys()) > 1 and "systematics" in self._variations.keys():
            self._variations["systematics"].insert(0, "nominal")

        # Create list of configs for the modules
        configs = []        
        for searchMode in self._searchModes:
            for dataEra in self._dataEras:
                modStr = "%s_%s_Run%s"%(self._name, searchMode, dataEra)
                # Create nominal module without any variation
                configs.append(AnalysisConfig(self._name, modStr, config, self._verbose))
                self.Print("Created nominal module %s" % (sh_Note + modStr + sh_Normal) )
                # Create modules for optimization and systematics variations
                configs.extend(self._buildVariation(config, modStr))

        # Register the modules
        for module in configs:
            module.registerAnalysis(process)
        self.Verbose("Created %d modules in total" % (len(configs)) )
        return        

    def _buildVariation(self, config, moduleName, optName="", systName="", level=0, **kwargs):
        '''
        Builds iteratively the variations
        Logic: Variation specs are put into kwargs as key,value pairs 
        For systematics key=systematics, value=identifier; only a single systematics variation per module is allowed
        For variations key=config entry, value=value; multiple simultaneous variations per module are allowed
        '''
        configs = []
        keys = self._variations.keys()
        if len(keys) == 0:
            return configs

        variationsList = self._variations[keys[level]]
        # For-loop: All variations
        for i, item in enumerate(variationsList, 1):
            newSystName = systName
            newOptName  = optName
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
                configs.append(AnalysisConfig(self._name, modStr, config, self._verbose, **kwargs))
                del kwargs[keys[level]]
                self.Print("Created variation module %s" % (sh_Note + modStr + sh_Normal), i==0)
        return configs
