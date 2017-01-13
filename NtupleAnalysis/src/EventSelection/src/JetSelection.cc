// -*- c++ -*-
#include "EventSelection/interface/JetSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

JetSelection::Data::Data()
: bPassedSelection(false),
  fJetMatchedToTau(0),
  fHT(-1.0),
  fMHTvalue(-1.0),
  fMinDeltaPhiJetMHT(-1.0),
  fMaxDeltaPhiJetMHT(-1.0),
  fMinDeltaRJetMHT(-1.0),
  fMinDeltaRReversedJetMHT(-1.0)
{ }

JetSelection::Data::~Data() { }

const Jet& JetSelection::Data::getJetMatchedToTau() const { 
  if (!jetMatchedToTauFound())
    throw hplus::Exception("Assert") << "You forgot to check if the jet matched to tau exists (jetMatchedToTauFound()), this message occurs when none exists!";
  return fJetMatchedToTau[0];
}

JetSelection::JetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fJetPtCut(config.getParameter<float>("jetPtCut")),
  fJetEtaCut(config.getParameter<float>("jetEtaCut")),
  fTauMatchingDeltaR(config.getParameter<float>("tauMatchingDeltaR")),
  fNumberOfJetsCut(config, "numberOfJetsCut"),
  fHTCut(config, "HTCut"),
  fJTCut(config, "JTCut"),
  fMHTCut(config, "MHTCut"),
  // Event counter for passing selection
  cPassedJetSelection(fEventCounter.addCounter("passed jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("jet selection ("+postfix+")", "All events")),
  cSubPassedJetID(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed jet ID")),
  cSubPassedJetPUID(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed PU ID")),
  cSubPassedDeltaRMatchWithTau(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed tau matching")),
  cSubPassedEta(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed pt cut")),
  cSubPassedJetCount(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed jet number cut")),
  cSubPassedHT(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed HT cut")),
  cSubPassedJT(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed JT cut")),
  cSubPassedMHT(fEventCounter.addSubCounter("jet selection ("+postfix+")", "Passed MHT cut"))
{ 
  initialize(config);
}

JetSelection::JetSelection(const ParameterSet& config)
: BaseSelection(),
  fJetPtCut(config.getParameter<float>("jetPtCut")),
  fJetEtaCut(config.getParameter<float>("jetEtaCut")),
  fTauMatchingDeltaR(config.getParameter<float>("tauMatchingDeltaR")),
  fNumberOfJetsCut(config, "numberOfJetsCut"),
  fHTCut(config, "HTCut"),
  fJTCut(config, "JTCut"),
  fMHTCut(config, "MHTCut"),
  // Event counter for passing selection
  cPassedJetSelection(fEventCounter.addCounter("passed jet selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("jet selection", "All events")),
  cSubPassedJetID(fEventCounter.addSubCounter("jet selection", "Passed jet ID")),
  cSubPassedJetPUID(fEventCounter.addSubCounter("jet selection", "Passed PU ID")),
  cSubPassedDeltaRMatchWithTau(fEventCounter.addSubCounter("jet selection", "Passed tau matching")),
  cSubPassedEta(fEventCounter.addSubCounter("jet selection", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("jet selection", "Passed pt cut")),
  cSubPassedJetCount(fEventCounter.addSubCounter("jet selection", "Passed jet number cut")),
  cSubPassedHT(fEventCounter.addSubCounter("jet selection", "Passed HT cut")),
  cSubPassedJT(fEventCounter.addSubCounter("jet selection", "Passed JT cut")),
  cSubPassedMHT(fEventCounter.addSubCounter("jet selection", "Passed MHT cut"))
{ 
  initialize(config);
  bookHistograms(new TDirectory());
}

JetSelection::~JetSelection() { 
  delete hJetPtAll;
  delete hJetEtaAll;
  delete hJetPtPassed;
  delete hJetEtaPassed;
  for (auto p: hSelectedJetPt) delete p;
  for (auto p: hSelectedJetEta) delete p;  
  delete hJetMatchingToTauDeltaR;
  delete hJetMatchingToTauPtRatio;
  delete hHTAll;
  delete hJTAll;
  delete hMHTAll;
  delete hHTPassed;
  delete hJTPassed;
  delete hMHTPassed;
}

void JetSelection::initialize(const ParameterSet& config) {
  
}

void JetSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "jetSelection_"+sPostfix);

  // Histograms (1D)
  hJetPtAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "jetPtAll", "Jet pT, all;p_{T} (GeV/c)", 50, 0.0, 500.0);
  hJetEtaAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "jetEtaAll", "Jet #eta, all;#eta", 50, -2.5, 2.5);
  hJetPtPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "jetPtPassed", "Jet pT, passed;p_{T} (GeV/c)", 50, 0.0, 500.0);
  hJetEtaPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "jetEtaPassed", "Jet Eta, passed", 50, -2.5, 2.5);
  hSelectedJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsFirstJetPt" , "First jet pT;p_{T} (GeV/c)" , 50, 0.0, 500.0) );
  hSelectedJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsSecondJetPt", "Second jet pT;p_{T} (GeV/c)", 50, 0.0, 500.0) );
  hSelectedJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsThirdJetPt" , "Third jet pT;p_{T} (GeV/c)" , 50, 0.0, 500.0) );
  hSelectedJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsFourthJetPt", "Fourth jet pT;p_{T} (GeV/c)", 50, 0.0, 500.0) );
  hSelectedJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsFifthJetPt" , "Fifth jet pT;p_{T} (GeV/c)" , 50, 0.0, 500.0) );
  hSelectedJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsSixthJetPt" , "Sixth jet pT;p_{T} (GeV/c)" , 50, 0.0, 500.0) );
  hSelectedJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsFirstJetEta" , "First jet #eta;#eta" , 50, -2.5, +2.5) );
  hSelectedJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsSecondJetEta", "Second jet #eta;#eta", 50, -2.5, +2.5) );
  hSelectedJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsThirdJetEta" , "Third jet #eta;#eta" , 50, -2.5, +2.5) );
  hSelectedJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsFourthJetEta", "Fourth jet #eta;#eta", 50, -2.5, +2.5) );
  hSelectedJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsFifthJetEta" , "Fifth jet #eta;#eta" , 50, -2.5, +2.5) );
  hSelectedJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsSixthJetEta" , "Sixth jet #eta;#eta" , 50, -2.5, +2.5) );
  hJetMatchingToTauDeltaR  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "JetMatchingToTauDeltaR" , "#DeltaR(jet, #tau)", 40, 0, 2);
  hJetMatchingToTauPtRatio = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "JetMatchingToTauPtRatio", "jet pT / #tau pT", 40, 0, 2);
  hHTAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "HTAll"    , ";H_{T}",  30, 0.0, 1500.0); 
  hJTAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "JTAll"    , ";J_{T}",  30, 0.0, 1500.0); 
  hMHTAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MHTAll"   , ";MHT"  ,  30, 0.0,  300.0);
  hHTPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "HTPassed" , ";H_{T}",  30, 0.0, 1500.0); 
  hJTPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "JTPassed" , ";J_{T}",  30, 0.0, 1500.0); 
  hMHTPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MHTPassed", ";MHT"  ,  30, 0.0,  300.0);

  return;
}

JetSelection::Data JetSelection::silentAnalyze(const Event& event, const Tau& tau) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, tau.p4(), tau.pt());
  enableHistogramsAndCounters();
  return myData;
}

JetSelection::Data JetSelection::silentAnalyzeWithoutTau(const Event& event) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  math::LorentzVectorT<double> tauP(0.,0.,9999.,0.);
  Data myData = privateAnalyze(event, tauP, -1.0);
  enableHistogramsAndCounters();
  return myData;
}

JetSelection::Data JetSelection::analyze(const Event& event, const Tau& tau) {
  ensureAnalyzeAllowed(event.eventID());
  JetSelection::Data data = privateAnalyze(event, tau.p4(), tau.pt());
  // Send data to CommonPlots
  if (fCommonPlots != nullptr)
    fCommonPlots->fillControlPlotsAtJetSelection(event, data);
  // Return data
  return data;
}

JetSelection::Data JetSelection::analyzeWithoutTau(const Event& event) {
  ensureAnalyzeAllowed(event.eventID());
  math::LorentzVectorT<double> tauP(0.,0.,9999.,0.);
  JetSelection::Data data = privateAnalyze(event, tauP, -1.);
  // Send data to CommonPlots
  if (fCommonPlots != nullptr)
    fCommonPlots->fillControlPlotsAtJetSelection(event, data);
  // Return data
  return data;
}

JetSelection::Data JetSelection::privateAnalyze(const Event& event, const math::LorentzVectorT<double>& tauP, const double tauPt) {
  Data output;
  cSubAll.increment();
  bool passedJetID = false;
  bool passedJetPUID = false;
  bool passedDeltaRMatchWithTau = false;
  bool passedEta = false;
  bool passedPt  = false;
  
  // Loop over jets
  for(Jet jet: event.jets()) {

    //=== Apply cut on jet ID
    if (!jet.jetIDDiscriminator())
      continue;
    passedJetID = true;

    //=== Apply cut on jet PU ID
    if (!jet.jetPUIDDiscriminator())
      continue;
    passedJetPUID = true;
    output.fAllJets.push_back(jet);   
    hJetPtAll->Fill(jet.pt());
    hJetEtaAll->Fill(jet.eta());

    //=== Apply cut on tau radius
    if (tauPt > 0.0) {
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR(tauP, jet.p4());
      hJetMatchingToTauDeltaR->Fill(myDeltaR);
      if (myDeltaR < fTauMatchingDeltaR)
        continue;
      passedDeltaRMatchWithTau = true;
    }

    //=== Apply cut on eta
    if (std::fabs(jet.eta()) > fJetEtaCut)
      continue;
    passedEta = true;

    //=== Apply cut on pt
    if (jet.pt() < fJetPtCut)
      continue;
    passedPt = true;
    // Jet passed all cuts
    output.fSelectedJets.push_back(jet);
    hJetPtPassed->Fill(jet.pt());
    hJetEtaPassed->Fill(jet.eta());
  }

  // Fill counters so far
  if (passedJetID)
    cSubPassedJetID.increment();
  if (passedJetPUID)
    cSubPassedJetPUID.increment();
  if (passedDeltaRMatchWithTau)
    cSubPassedDeltaRMatchWithTau.increment();
  if (passedEta)
    cSubPassedEta.increment();
  if (passedPt)
    cSubPassedPt.increment();
  
  //=== Apply cut on number of jets
  if (!fNumberOfJetsCut.passedCut(output.fSelectedJets.size()))
    return output;
  cSubPassedJetCount.increment();

  // Sort jets by pT (descending order)
  std::sort(output.fSelectedJets.begin(), output.fSelectedJets.end());

  // Calculate HT
  output.fHT = 0.0;
  for(Jet jet: output.getSelectedJets()) {
    output.fHT += jet.pt();
  }
  if (tauPt > 0.0) output.fHT += tauPt;
  hHTAll->Fill(output.fHT);
  // Calculate JT
  output.fJT = output.fHT - output.fSelectedJets.at(0).pt();
  hJTAll->Fill(output.fJT);
  //=== Apply cut on HT
  if (!fHTCut.passedCut(output.fHT)) return output;
  cSubPassedHT.increment();
  hHTPassed->Fill(output.fHT);
  //=== Apply cut on JT
  if (!fJTCut.passedCut(output.fJT)) return output;
  cSubPassedJT.increment();
  hJTPassed->Fill(output.fJT);

  // Calculate MHT
  calculateMHTInformation(output, tauP, tauPt);
  hMHTAll->Fill(output.fMHTvalue);
  //=== Apply cut on MHT
  if (!fMHTCut.passedCut(output.fMHTvalue)) return output;
  cSubPassedMHT.increment();
  hMHTPassed->Fill(output.fMHTvalue);
  
  //=== Passed all jet selections
  output.bPassedSelection = true;
  cPassedJetSelection.increment();


  // Find jet matched to tau
  if (tauPt > 0.0) {
    findJetMatchingToTau(output.fJetMatchedToTau, event, tauP);
    if (output.jetMatchedToTauFound()) {
      hJetMatchingToTauPtRatio->Fill(tauPt / output.getJetMatchedToTau().pt());
    }
  }

  // Fill pt and eta of jets
  size_t i = 0;
  for (Jet jet: output.fSelectedJets) {
    if (i < 6) {
      hSelectedJetPt[i]->Fill(jet.pt());
      hSelectedJetEta[i]->Fill(jet.eta());
    }
    ++i;
  }  


  // Return data object
  return output;
}

void JetSelection::findJetMatchingToTau(std::vector<Jet>& collection, const Event& event, const math::LorentzVectorT<double>& tauP) {
  double myMinDeltaR = 9999;
  size_t mySelectedIndex = 9999;
  size_t i = 0;
  for(Jet jet: event.jets()) {
    double myDeltaR = ROOT::Math::VectorUtil::DeltaR(tauP, jet.p4());
    if (myDeltaR < myMinDeltaR) {
      myMinDeltaR = myDeltaR;
      mySelectedIndex = i;
    }
    i += 1;
  }
  if (myMinDeltaR < 0.1)
    collection.push_back(event.jets()[mySelectedIndex]);
}

void JetSelection::calculateMHTInformation(JetSelection::Data& output, const math::LorentzVectorT<double>& tauP, const double tauPt) {
  // Construct a list of the jet four momenta for speeding up calculations and for simplifying code
  std::vector<math::LorentzVectorT<double>> fourMomenta;
  for(Jet jet: output.getSelectedJets()) {
    fourMomenta.push_back(jet.p4());
  }
  if (tauPt > 0.0) {
    fourMomenta.push_back(tauP);
  }
  // Calculate MHT (negative vector sum of selected jets and the tau)
  // I.e. not as sensitive as MET to forward calorimetry
  output.fMHT.SetXYZ(0.0, 0.0, 0.0);
  for(auto& p: fourMomenta) {
    output.fMHT.SetXYZ(output.fMHT.x() - p.x(),
                       output.fMHT.y() - p.y(),
                       output.fMHT.z() - p.z());
  }
  output.fMHTvalue = std::sqrt(output.fMHT.Perp2());

  // Calculate the minimum and maximum DeltaPhi and DeltaR of the jet/tau, MHT-jet/tau system
  // I.e. look for events with collinear or back-to-back topologies architypal of QCD multi-jet events
  output.fMinDeltaPhiJetMHT = 9999.0;
  output.fMaxDeltaPhiJetMHT = -1.0;
  output.fMinDeltaRJetMHT = 9999.0;
  output.fMinDeltaRReversedJetMHT = 9999.0;
  for(auto& p: fourMomenta) {
    math::XYZVectorD modifiedMHT = output.MHT();
    modifiedMHT.SetXYZ(output.fMHT.x() + p.x(),
                       output.fMHT.y() + p.y(),
                       output.fMHT.z() + p.z());
    double deltaPhi = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(p, modifiedMHT));
    if (deltaPhi < output.fMinDeltaPhiJetMHT) {
      output.fMinDeltaPhiJetMHT = deltaPhi;
    }
    if (deltaPhi > output.fMaxDeltaPhiJetMHT) {
      output.fMaxDeltaPhiJetMHT = deltaPhi;
    }
    double deltaR = ROOT::Math::VectorUtil::DeltaR(p, modifiedMHT);
    if (deltaR < output.fMinDeltaRJetMHT) {
      output.fMinDeltaRJetMHT = deltaR;
    }
    // Reverse one of the vectors and calculate DeltaR; small DeltaR means the system is back-to-back
    modifiedMHT.SetXYZ(-output.fMHT.x(),
                       -output.fMHT.y(),
                       -output.fMHT.z());
    double reversedSystemDeltaR = ROOT::Math::VectorUtil::DeltaR(p, modifiedMHT);
    if (reversedSystemDeltaR < output.fMinDeltaRReversedJetMHT) {
      output.fMinDeltaRReversedJetMHT = reversedSystemDeltaR;
    }
  }

  return;
}
