## Package: AnalysisConfig
# Analysis configuration, with ability to create the main analyzer 
# and the analyzers for the N systematic uncertainty variations and other variations based on the config

from HiggsAnalysis.NtupleAnalysis.main import Analyzer
import HiggsAnalysis.NtupleAnalysis.parameters.scaleFactors as scaleFactors

## Container class for analysis configuration
class AnalysisConfig:
    def __init__(self, selectorName, moduleName, config, **kwargs):
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
		if value.startswith("tauES"):
		    self._config.TauSelection.systematicVariation = value.replace("Plus","plus").replace("Minus","minus")
		elif value.startswith("JES"):
		    self._config.JetSelection.systematicVariation = value.replace("Plus","plus").replace("Minus","minus")
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
                    direction = None
                    if value.endswith("Plus"):
                        direction = "up"
                    elif value.endswith("Minus"):
                        direction = "down"
                    scaleFactors.assignTauMisidentificationSF(self._config.TauSelection, partonFakingTau, etaRegion, direction)
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
		# Set value
		if not hasattr(subconfig[len(subconfig)-1], subkeys[len(subkeys)-1]):
		    raise Exception("Error: Cannot find key %s.%s in the config!"%(suffix, subkeys[len(subkeys)-1]))
		setattr(subconfig[len(subconfig)-1], subkeys[len(subkeys)-1], value)
        
    ## Create and register the analysis after the changes have bene done to the config
    def registerAnalysis(self, process):
        process.addAnalyzer(self._moduleName, Analyzer(self._selectorName, config=self._config, silent=True))
    
## Class for building analyses
class AnalysisBuilder:
    def __init__(self,
                 name,                  # The module name (beware, the downstream python code has assumptions on this)
                 # Required options
                 dataEras=["2015"],        # Data era (see python/tools/dataset.py::_dataEras)
                 searchModes=["m80to160"], # Search mode (see python/parameters/signalAnalysisParameters.py)
                 # Optional options
                 usePUreweighting=False, # enable/disable vertex reweighting
                 # Systematics options
                 doSystematicVariations=False, # Enable/disable adding modules for systematic uncertainty variation
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
          
          self._variations={}
          # Process systematic uncertainty variations
          if doSystematicVariations:
              items = []
              # Trigger systematics
              #items.extend(["TauTrgDataEff", "TauTrgMCEff"])
              #items.extend(["L1ETMDataEff", "L1ETMMCEff"])
              #items.extend(["METTrgDataEff", "METTrgMCEff"])
              # Tau ID variation systematics
              items.extend(["FakeTauElectron", "FakeTauMuon", "FakeTauJet"])
              # Energy scales and JER systematics
              items.extend(["tauES", "JES"]), # "JER", "UES"])
              # b and top quarks systematics
              #items.extend("TopPt", "BTagSF", "BMistagSF")
              # PU weight systematics
              #items.extend(["PUWeight"])
              # Create configs
              self._variations["systematics"] = []
              for item in items:
                  self._variations["systematics"].append("%sPlus"%item)
                  self._variations["systematics"].append("%sMinus"%item)
	  #self.addVariation("TauSelection.tauPtCut", [50,60])
	  #self.addVariation("TauSelection.tauEtaCut", [0.5,1.5])
    
    def addVariation(self, configItemString, listOfValues):
        self._variations[configItemString] = listOfValues
    
    def build(self, process, config):
        # Add here options to the config
        config.__setattr__("usePileupWeights", self._usePUreweighting)
        # Add nominal modules
        if len(self._variations.keys()) > 1 and "systematics" in self._variations.keys():
            self._variations["systematics"].insert(0, "nominal")
        # Create list of configs for the modules
        configs = []
        for searchMode in self._searchModes:
            for dataEra in self._dataEras:
                modStr = "%s_%s_Run%s"%(self._name, searchMode, dataEra)
                # Create nominal module without any variation
                if "systematics" in self._variations.keys():
                    if len(self._variations.keys()) == 1:
                        configs.append(AnalysisConfig(self._name, modStr, config))
                        print "Created nominal module: %s"%modStr
                else:
                    if len(self._variations.keys()) == 0:
                        configs.append(AnalysisConfig(self._name, modStr, config))
                        print "Created nominal module: %s"%modStr
                # Create modules for optimization and systematics variations
                configs.extend(self._buildVariation(config, modStr))
        # Register the modules
        for module in configs:
            module.registerAnalysis(process)
        print "\nAnalysisBuilder created %d modules\n"%len(configs)
    
    ## Builds iteratively the variations
    # Logic: Variation specs are put into kwargs as key,value pairs 
    #        For systematics key=systematics, value=identifier; only a single systematics variation per module is allowed
    #        For variations key=config entry, value=value; multiple simultaneous variations per module are allowed
    def _buildVariation(self, config, moduleName, optName="", systName="", level=0, **kwargs):
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
