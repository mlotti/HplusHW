## Package: AnalysisConfig
# Analysis configuration, with ability to create the main analyzer 
# and the analyzers for the N systematic uncertainty variations and other variations based on the config

from HiggsAnalysis.NtupleAnalysis.main import Analyzer

## Container class for analysis configuration
class AnalysisConfig:
    def __init__(self, selectorName, moduleName, config, **kwargs):
        self._selectorName = selectorName
        self._moduleName = moduleName
        self._config = config.clone()
        #self.__dict__.update(kwargs)
        # Process all keyword arguments to make changes to thte config
        
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
              items.extend(["GenuineTau", "FakeTauBarrelElectron", "FakeTauEndcapElectron", "FakeTauMuon", "FakeTauJet"])
              # Energy scales and JER systematics
              #items.extend(["tauES", "JES", "JER", "UES"])
              # b and top quarks systematics
              #items.extend("TopPt", "BTagSF", "BMistagSF")
              # PU weight systematics
              #items.extend(["PUWeight"])
              # Create configs
              self._variations["systematics"] = []
              for item in items:
                  self._variations["systematics"].append("%sPlus"%item)
                  self._variations["systematics"].append("%sMinus"%item)
    
    def addVariation(self, configItemString, listOfValues):
        self._variations[configItemString] = listOfValues
    
    def build(self, process, config):
        # Add here options to the config
        config.__setattr__("usePileupWeights", self._usePUreweighting)
        # Create list of configs for the modules
        configs = []
        for searchMode in self._searchModes:
            for dataEra in self._dataEras:
                modStr = "%s_%s_Run%s"%(self._name, searchMode, dataEra)
                # Create nominal module
                configs.append(AnalysisConfig(self._name, modStr, config))
                print "Created module: %s"%modStr
                # Create modules for optimization and systematics variations
                configs.extend(self._buildVariation(config, modStr))
        # Register the modules
        for module in configs:
            module.registerAnalysis(process)
        print "\nAnalysisBuilder created %d modules\n"%len(configs)
        
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
                newOptName += item # FIXME this does not work
            # Move to next level or build variation
            if level < len(keys)-1:
                kwargs[keys[level]] = item
                self._buildVariation(config, moduleName, newOptName, newSystName, level+1, **kwargs)
            else:
                modStr = moduleName
                if newOptName != "":
                    modStr += "_Opt%s"%newOptName
                if newSystName != "":
                    modStr += "_SystVar%s"%newSystName
                configs.append(AnalysisConfig(self._name, modStr, config, **kwargs))
                print "Created variation module %s"%modStr
        return configs

