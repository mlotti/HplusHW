// -*- c++ -*-
#include "EventSelection/interface/JetCorrelations.h"
#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
#include "Math/GenVector/VectorUtil.h"
#include "EventSelection/interface/TransverseMass.h"
//#include "Framework/interface/makeTH.h"
#include "TLorentzVector.h"

JetCorrelations::Data::Data()
: bPassedSelection(false)
{ }

JetCorrelations::Data::~Data() { }

JetCorrelations::JetCorrelations(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
  : BaseSelection(eventCounter, histoWrapper, commonPlots, postfix)
    //  nMaxJets(4),
    //    nConsideredJets(static_cast<size_t>(config.getParameter<int>("nConsideredJets"))),
    //bEnableOptimizationPlots(config.getParameter<bool>("enableOptimizationPlots")),
    //   sPrefix(prefix),
    //fType(type)
    //  cPassedAngularCuts(eventCounter.addCounter("passed angular cuts / "+prefix+" ("+postfix+")")),
    //    cSubAllEvents(eventCounter.addSubCounter("jet correlations", "All events"))

{
  // Obtain algorithm and working point

}

JetCorrelations::~JetCorrelations() { }

void JetCorrelations::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "JetCorrelations");
  /*
  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFirstJetPt", "First b-jet pT", 40, 0, 400));
  hSelectedBJetPt.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsSecondJetPt", "Second b-jet pT", 40, 0, 400));
  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsFirstJetEta", "First b-jet #eta", 50, -2.5, 2.5));
  hSelectedBJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedBJetsSecondJetEta", "Second b-jet #eta", 50, -2.5, 2.5));
  */  
  //  hPt3Jets  =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "pT_3jets", "pT_3jets", 100, 0, 600);
  //  hM3Jets  =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "M_3jets", "M_3jets", 100, 0, 500);
  //  hDrTau3Jets =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "DrTau3Jets", "DrTau3Jets", 100, 0, 5);
  hmaxDr3Jets =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "maxDr3Jets", "maxDr3Jets", 100, 0, 5);
  hgenJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "genjetPt", "genJet pT", 200, 0, 1000);
  hgenJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "genjetEta", "genJet eta", 100, -5, 5);
  hgenJetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "genjetPhi", "genJet phi", 90, 0, 180);
  hgenBJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "genBjetEta", "genBJet Eta", 100, -5, 5);
  hdrTauMaxBjet_gen =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "hdrTauMaxBjet_gen",  "drTauMaxBjet_gen", 100, 0, 5);
  hdrTauMinBjet_gen =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "hdrTauMinBjet_gen",  "drTauMinBjet_gen", 100, 0, 5);

  hPt3Jets =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "pt3Jets",  "pt3Jets", 200, 0, 600);
  hM3Jets =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "M3Jets",  "M3Jets", 200, 0, 600);
  h3jetPtcut =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "3JetsPtCut",  "3JetsPtCut", 200, 0, 600);
  hDrTau3Jets =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "DrTau3Jets",  "DrTau3Jets", 200, 0, 5);
  hDPhiTauMetVsPt3jets =  fHistoWrapper.makeTH<TH2F>(HistoLevel::kInformative, subdir, "DPhiTauMetVsPt3jets",  "DPhiTauMetVsPt3jets", 180, 0, 180,200,0,600);
  htransverseMassNoCut =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "transverseMassNoCut",  "transverseMassNoCut", 200, 0, 600);
  htransverseMass3JetCut =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "transverseMass3JetCut",  "transverseMass3JetCut", 200, 0, 600);
  htransverseMassTriangleCut =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, subdir, "transverseMassTriangleCut",  "transverseMassTriangleCut", 200, 0, 600);
  htransverseMassTriangleCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "transverseMassTriangleCut", "transverseMassTriangleCut", 200, 0., 800);  
  htransverseMassDeltaR3JetsTauCut =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "transverseMassDeltaR3JetsTauCut", "transverseMassDeltaR3JetsTauCut", 200, 0., 800);
  htransverseMassDeltaRCorrCut =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "transverseMassDeltaRCorrCut", "transverseMassDeltaRCorrCut", 200, 0., 800);
}  


JetCorrelations::Data JetCorrelations::silentAnalyze(const Event& event, const JetSelection::Data& jetData, const TauSelection::Data& tauData, const METSelection::Data& metData) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, jetData, tauData, metData);
  enableHistogramsAndCounters();
  return myData;
}

JetCorrelations::Data JetCorrelations::analyze(const Event& event, const JetSelection::Data& jetData, const TauSelection::Data& tauData, const METSelection::Data& metData) {
  ensureAnalyzeAllowed(event.eventID());
  return privateAnalyze(event, jetData, tauData, metData);
}

JetCorrelations::Data JetCorrelations::privateAnalyze(const Event& iEvent, const JetSelection::Data& jetData, const TauSelection::Data& tauData, const METSelection::Data& metData) {
  Data output;
  //  cSubAll.increment();


  
  math::XYZTLorentzVector threeJets;

  for(Jet jet: jetData.getSelectedJets()) {                                                                                    
    threeJets += jet.p4();
  }

   
  /*

  std::vector<GenJet> genJets;
  //  GenJet genBjetMax;
  //  GenJet genBjetMin;
  double ptmax = 0;
  double ptmin = 10000;
  //  math::XYZTLorentzVector genBjetMax;
  //  math::XYZTLorentzVector genBjetMin;
  math::LorentzVectorT<double>  genBjetMax(0.,0.,999.,0.);
  math::LorentzVectorT<double>  genBjetMin(0.,0.,999.,0.);
  
  for(GenJet genjet: iEvent.genjets()) {
    genJets.push_back(genjet);
  }
  
 
  for(GenJet genjet: iEvent.genjets()) {
    hgenJetPt->Fill(genjet.pt());
    hgenJetEta->Fill(genjet.eta());
    hgenJetPhi->Fill(genjet.phi()* 180/3.14159265);
    
    if (genjet.pdgId() == 5) {
      hgenBJetPt->Fill(genjet.pt());
      hgenBJetEta->Fill(genjet.eta());
      if (genjet.pt() > ptmax) {
	ptmax = genjet.pt();
	//	genBjetMax= genjet;
	genBjetMax= genjet.p4();
      }
    }
    
    //    if(genjet.pt() > 30 && std::abs(genjet.eta()) < 2.4) {
    //   genJets.push_back(genjet);
  }
 
  
  
  size_t bjets = 0;
  for(GenJet genjet: iEvent.genjets()) {
    if (genjet.pdgId() == 5 && bjets < 2) {
      if (genjet.pt() < ptmin) {
	ptmin = genjet.pt();
	genBjetMin= genjet.p4();
      }
    }
  }
   
  math::LorentzVectorT<double> tauP(0.,0.,999.,0.);
  if (tauData.hasIdentifiedTaus())
    tauP = tauData.getSelectedTau().p4();


  double drTauMaxBjet_gen = -999;
  double drTauMinBjet_gen = -999;  if ( bjets == 2) {
    double drTauMaxBjet_gen = ROOT::Math::VectorUtil::DeltaR(tauP,genBjetMax);
    double drTauMinBjet_gen = ROOT::Math::VectorUtil::DeltaR(tauP,genBjetMin);
  }
  

  double drTau3Jets = ROOT::Math::VectorUtil::DeltaR(tauP,threeJets);
  hdrTauMaxBjet_gen->Fill(drTauMaxBjet_gen);
  hdrTauMinBjet_gen->Fill(drTauMinBjet_gen);
  */ 
  hPt3Jets->Fill(threeJets.pt());
  hM3Jets->Fill(threeJets.mass());                                                                                                                                                                                                
  //  std::cout << "   threeJets.pt()"<<   threeJets.pt()   << std::endl;                                                                                                                                                          
   
  double transverseMass = TransverseMass::reconstruct(tauData.getSelectedTau(),metData.getMET() );
  double DeltaPhiTauMET = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(tauData.getSelectedTau().p4(), metData.getMET())*57.29578);
  hDPhiTauMetVsPt3jets->Fill(std::abs(DeltaPhiTauMET),threeJets.pt());

  double ptcut = 400.0 * (1.0 - DeltaPhiTauMET/180.0);
  double ptConstant =  threeJets.pt() /(1.0 - DeltaPhiTauMET/180.0);
  h3jetPtcut->Fill(ptConstant);

  double drTau3Jets = ROOT::Math::VectorUtil::DeltaR(tauData.getSelectedTau().p4(),threeJets);
  hDrTau3Jets->Fill(drTau3Jets);
  

 // mt with 3jet and  triangle cut                                                                                                                                                                                               
  htransverseMassNoCut->Fill(transverseMass);

  if (threeJets.pt()  > ptcut )    htransverseMass3JetCut->Fill(transverseMass);
  if (!(threeJets.pt()  < ptcut && DeltaPhiTauMET  > 60)) { 
    htransverseMassTriangleCut->Fill(transverseMass);
  }

  if ( drTau3Jets < 3 ) {
    htransverseMassDeltaR3JetsTauCut->Fill(transverseMass);
    if (DeltaPhiTauMET  > 90) {
      htransverseMassDeltaRCorrCut->Fill(transverseMass);
    }
  }


  /*
  if (!(threeJets.pt()  < ptcut && DeltaPhiTauMET  > 60)) {
    htransverseMassTriangleCut->Fill(transverseMass);
  }
 

  double DeltaPhi3jetsMet = std::abs(ROOT::Math::VectorUtil::DeltaPhi(threeJets, fEvent.met_Type1())) * 57.3;
  hDPhi3JetsMet->Fill(DeltaPhi3jetsMet);
  double JetEtSum = jet1.pt() + jet2.pt() + jet3.pt();
  double JetTauEtSum = jet1.pt() + jet2.pt() + jet3.pt()+ tau.pt();
  double JetTauMetEtSum = jet1.pt() + jet2.pt() + jet3.pt()+ tau.pt() + myMet;
  double TauMetEtSum = tau.pt() + myMet;
  // assume known slope                                                                                                                                                                                                          
  double constantEtSum = JetTauMetEtSum - 1.4 *  JetEtSum;
  // assume known constant term                                                                                                                                                                                                  
  double slopeEtSum = (JetTauMetEtSum - 100)/JetEtSum;
  hconstantEtSum->Fill(constantEtSum);
  hslopeEtSum->Fill(slopeEtSum);
  hJetEtSum->Fill(JetEtSum);
  hJetTauEtSum->Fill(JetTauEtSum);
  hJetTauMetEtSum->Fill(JetTauMetEtSum);
  hJetEtSumVsJetTauMetEtSum->Fill(JetEtSum,JetTauMetEtSum);

   
  // Fill pt and eta of jets
  size_t i = 0;
  for (Jet jet: output.fSelectedBJets) {
    if (i < 2) {
      hSelectedBJetPt[i]->Fill(jet.pt());
      hSelectedBJetEta[i]->Fill(jet.eta());
    }
    ++i;
  }
  */
  // Calculate and store b-jet weight and it's uncertainty
  // FIXME to be implemented
  
  // Return data object
  return output;
}
