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
- 

Other missing items:
- Common plots
- Configuration for selection



Need to add to data format:
- muon ID variables
vector<bool> Muons_byLooseID
vector<bool> Muons_byTightID
vector<bool> Muons_byVetoID

- electron ID variables
vector<bool> Electrons_byLooseID
vector<bool> Electrons_byTightID
vector<bool> Electrons_byVetoID

- jet ID variables 
vector<bool> Jets_byJetIDLoose
vector<bool> Jets_byJetIDMedium
vector<bool> Jets_byJetIDTight
