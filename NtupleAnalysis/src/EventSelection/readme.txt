Event selection done for:
- electrons (ID missing)
- muons (ID missing)

Event selection missing for:
- taus
- jets
- b jets
- MET
- angular cuts
- transverse mass
- delta phi
- MET filters
https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2
https://github.com/cms-sw/cmssw/blob/CMSSW_7_4_X/PhysicsTools/PatAlgos/python/slimming/metFilterPaths_cff.py

Other missing items:
- Common plots
- Configuration for selection



Need to add to data format:
- muon ID variables
(https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId)
pat::Muon::isLooseMuon vector<bool> Muons_byLooseID  
pat::Muon::isTightMuon vector<bool> Muons_byTightID
pat::Muon::isSoftMuon vector<bool> Muons_bySoftID
Isolation, see http://cmslxr.fnal.gov/source/DataFormats/MuonReco/interface/MuonPFIsolation.h
reco::Muon::pfIsolationR03() struct -> vector<float> Muons_isolationR03
reco::Muon::pfIsolationR04() struct -> vector<float> Muons_isolationR04

- electron ID variables
https://twiki.cern.ch/twiki/bin/view/CMS/EgammaIDRecipesRun2
https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariateElectronIdentificationRun2

- jet ID variables 
vector<bool> Jets_byJetIDLoose
vector<bool> Jets_byJetIDMedium
vector<bool> Jets_byJetIDTight

- MET with Puppi

collection in miniAOD (7.4 ->): slimmedMETsPuppi