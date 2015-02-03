#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithWSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"
#include "TLorentzVector.h"
#include "TVector3.h"

#include <limits>

namespace HPlus {

  //constructor
  TopWithWSelection::TopWithWSelection(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper) : TopSelectionBase::TopSelectionBase(iConfig, eventCounter, histoWrapper),
    //BaseSelection(eventCounter, histoWrapper),
    fTopMassLow(iConfig.getUntrackedParameter<double>("TopMassLow")),
    fTopMassHigh(iConfig.getUntrackedParameter<double>("TopMassHigh")),
    fChi2Cut(iConfig.getUntrackedParameter<double>("Chi2Cut")),
    //fTopWithWMassCount(eventCounter.addSubCounter("Top with W mass cut","Top with W Mass cut")),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src"))
  {
    edm::Service<TFileService> fs;

    TFileDirectory myDir = fs->mkdir("TopSelection");
    
    //top histograms
    htopPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopPt", "TopPt;top p_{T} (GeV)", 80, 0., 400.);
    htopMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass", "TopMass; m_{t} (GeV)", 80, 0., 400.);
    htopEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopEta", "TopEta; #eta_{t}", 100, -5., 5.);
    
    htopPtAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopPtAfterCut", "TopPtAfterCut; top p_{T} (GeV)", 80, 0., 400.);
    htopMassAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMassAfterCut", "TopMassAfterCut; m_{t}", 80, 0., 400.);
    htopEtaAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopEtaAfterCut", "TopEtaAfterCut; #eta_{t}", 100, -5., 5.);
    htopMassRejected = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMassRejected", "TopMassRejected; m_{t} (GeV)", 80, 0., 400.);

    //W histograms
    hWPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WPt", "WPt; W p_{T} (GeV)", 80, 0., 400.);
    hWMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass", "WMass; m_{W} (GeV)", 100, 0., 200.);
    hWEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WEta", "WEta; #eta_{W}", 80, 0., 400.);

    hWPtAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WPtAfterCut", "WPtAfterCut; W p_{T} (GeV)", 80, 0., 400.);
    hWMassAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMassAfterCut", "WMassAfterCut; m_{W} (GeV)", 100, 0., 200.);
    hWEtaAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WEtaAfterCut", "WEtaAfterCut; #eta_{W}", 80, 0., 400.);

    //angular hisrograms:
    hdeltaPhi_Wb = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "DeltaPhi_Wb","DeltaPhi_Wb;#Delta#phi(W,b) (^{o}); N_{events} / 5^{o}", 36, 0., 180.);
    hdeltaR_Wb = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "DeltaR_Wb", "hDeltaR_Wb;#Delta R(W,b) (^{o});N_{events} / 5^{o}", 52, 0.0, 260.);
    hdeltaPhi_jets = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "DeltaPhi_jets","DeltaPhi_jets;#Delta#phi(jet_{1},jet_{2}) (^{o}); N_{events} / 5^{o}", 36, 0., 180.);
    hdeltaR_jets = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "DeltaR_jets", "hDeltaR_jets;#Delta R(jet_{1},jet_{2}) (^{o});N_{events} / 5^{o}", 52, 0.0, 260.);
    
    //MC matching histograms
    htopMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass_fullMatch", "TopMass_fullMatch; m_{t} (GeV)", 80, 0., 400.);
    htopMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass_bMatch", "TopMass_bMatch; m_{t} (GeV)", 80, 0., 400.);
    htopMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass_qMatch", "TopMass_qMatch; m_{t} (GeV)", 80, 0., 400.);
    htopMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass_MatchWrongB", "TopMass_MatchWrongB; m_{t} (GeV)", 80, 0., 400.);
    hWMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass_fullMatch", "WMass_fullMatchMatch; m_{W} (GeV)", 100, 0., 200.);
    hWMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass_bMatch", "WMass_bMatch; m_{W} (GeV)", 100, 0., 200.);
    hWMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass_qMatch", "WMass_qMatch; m_{W} (GeV)", 100, 0., 200.);
    hWMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass_MatchWrongB", "WMass_MatchWrongB; m_{W} (GeV)", 100, 0., 200.);
    htopPt_match = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopPt_fullMatch", "TopPt_fullMatch;top p_{T} (GeV)", 80, 0., 400.);
    hWPt_match = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WPt_fullMatch", "WPt_fullMatch; W p_{T} (GeV)", 80, 0., 400.);
    hdeltaPhi_Wb_match = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "DeltaPhi_Wb_fullMatch","DeltaPhi_Wb_fullMatch;#Delta#phi(W,b) (^{o}); N_{events} / 5^{o}", 36, 0., 180.);
    hdeltaR_Wb_match = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "DeltaR_Wb_fullMatch", "hDeltaR_Wb_fullMatch;#Delta R(W,b) (^{o});N_{events} / 5^{o}", 52, 0.0, 260.);
    hdeltaPhi_jets_match = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "DeltaPhi_jets_fullMatch","DeltaPhi_jets_fullMatch;#Delta#phi(jet_{1},jet_{2}) (^{o}); N_{events} / 5^{o}", 36, 0., 180.);
    hdeltaR_jets_match = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "DeltaR_jets_fullMatch", "hDeltaR_jets_fullMatch;#Delta R(jet_{1},jet_{2}) (^{o});N_{events} / 5^{o}", 52, 0.0, 260.);

    //other histograms    
    hjjMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "jjMass", "jjMass;m_{jj} (GeV)", 80, 0., 400.);
    hChi2Min = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "Chi2Min", "Chi2Min; {#chi^2}_{min}", 200, 0., 40.);
  }

  //destructor
  TopWithWSelection::~TopWithWSelection() {}

//---------------------------------------------------------------------------------------------

  //privateAnalyze
  TopWithWSelection::Data TopWithWSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<pat::Jet> iJetb) { 
    Data output;

    // Suppress warnings about unused variables
    (void)bjets;
   
    // Reset variables
    double chi2Min = 999999;
    double nominalW = 80.4; //value used in simulation (unchanged)
    double sigmaW = 14.4; //RMS of Gaussian fit to 2012 TTJets_SemiLept (used to be 11.0)
    bool wmassfound = false;
    bool topmassfound = false;
  
    edm::Ptr<pat::Jet> Jet1;
    edm::Ptr<pat::Jet> Jet2;
    edm::Ptr<pat::Jet> Jetb;
    double dR_jets;
    double dPhi_jets;
    double dR_Wb;
    double dPhi_Wb;
    
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet1 = *iter;

    //for all combos of 3 jets...
      for(edm::PtrVector<pat::Jet>::const_iterator iter2 = jets.begin(); iter2 != jets.end(); ++iter2) {
	edm::Ptr<pat::Jet> iJet2 = *iter2;

    //same jet must not be used twice
	if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJet2->p4()) < 0.4) continue;
	if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJetb->p4()) < 0.4) continue;
	if (ROOT::Math::VectorUtil::DeltaR(iJet2->p4(), iJetb->p4()) < 0.4) continue;	  

    //...find W candidate with minimum chi2	
	XYZTLorentzVector candW = iJet1->p4() + iJet2->p4();
	
	hjjMass->Fill(candW.M());
	double chi2 = ((candW.M() - nominalW)/sigmaW)*((candW.M() - nominalW)/sigmaW); 

    dR_jets = (180.0/TMath::Pi())*ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJet2->p4());
    dPhi_jets = (180.0/TMath::Pi())*ROOT::Math::VectorUtil::DeltaPhi(iJet1->p4(), iJet2->p4());
    dR_Wb = (180.0/TMath::Pi())*ROOT::Math::VectorUtil::DeltaR(candW, iJetb->p4());
    dPhi_Wb = (180.0/TMath::Pi())*ROOT::Math::VectorUtil::DeltaPhi(candW, iJetb->p4());
	
	if (chi2 < chi2Min ) {
	  chi2Min = chi2;
	  Jet1 = iJet1;
	  Jet2 = iJet2;
	  Jetb = iJetb;        
	  wmassfound = true;  
	  output.W = candW;          
	  }
    }
  }
  
  if ( wmassfound ) {
      hChi2Min->Fill(sqrt(chi2Min));
      output.top = Jet1->p4() + Jet2->p4() + iJetb->p4(); 
      htopMass->Fill(output.getTopMass());
      htopPt->Fill(output.top.Pt());
      htopEta->Fill(output.getTopEta());      
      hWMass->Fill(output.getWMass());
      hWPt->Fill(output.W.Pt());
      hWEta->Fill(output.getWEta());
      //angular hisrograms:
      hdeltaPhi_Wb->Fill(dPhi_Wb);
      hdeltaR_Wb->Fill(dR_Wb);
      hdeltaPhi_jets->Fill(dPhi_jets);
      hdeltaR_jets->Fill(dR_jets);
   }
          
    //Event selection based on top reconstruction
    if( output.getTopMass() < fTopMassLow || output.getTopMass() > fTopMassHigh ) {
      output.fPassedEvent = false;
      htopMassRejected->Fill(output.getTopMass());      
      } else {
      output.fPassedEvent = true;
      topmassfound = true;
      htopPtAfterCut->Fill(output.top.Pt());
      htopMassAfterCut->Fill(output.getTopMass());
      htopEtaAfterCut->Fill(output.getTopEta());
      hWPtAfterCut->Fill(output.W.Pt());
      hWMassAfterCut->Fill(output.getWMass());
      hWEtaAfterCut->Fill(output.getWEta());
      }
      
    //MC matching for events that passed the top secletion
    //if (!iEvent.isRealData() && output.fPassedEvent == true ) {
    
    //alternative: MC matching for all events with a reconstructed top quark  
    if (!iEvent.isRealData() && topmassfound ) {

      edm::Handle <reco::GenParticleCollection> genParticles;
      iEvent.getByLabel(fSrc, genParticles);

      bool bMatchHiggsSide = false;
      bool bMatchWSide = false;
      bool Jet1Match = false;
      bool Jet2Match = false;

    //Determine HiggSide variable: 6 if top, -6 if antitop, 0 if top not found
      int idHiggsSide = 0;
      for (size_t i=0; i < genParticles->size(); ++i){
        const reco::Candidate & p = (*genParticles)[i];
        int id = p.pdgId();
        //if top and has immediate Higgs daughter:
        if(abs(id) == 6 && (hasImmediateDaughter(p,37) || hasImmediateDaughter(p,-37))) {
          idHiggsSide = id;
          }
        //NEW, FOR HEAVY H+: if b quark and has immediate Higgs daughter:
        if(idHiggsSide == 0){
          if(abs(id) == 37) {
            idHiggsSide = id;
          }
        }
      }
             
    //Test if b-jet is W-side or Higgs-side
      for (size_t i=0; i < genParticles->size(); ++i){
        const reco::Candidate & p = (*genParticles)[i];
        int id = p.pdgId();
        // select only b-jet particles
        if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
        //if immediate top mother
        if(hasImmediateMother(p,6) || hasImmediateMother(p,-6)) {
          if ( id * idHiggsSide > 0 ) {
            // test with b jet to Higgs side
            double deltaR = ROOT::Math::VectorUtil::DeltaR(Jetb->p4(),p.p4() );
            if ( deltaR < 0.4) bMatchHiggsSide = true;
            }
          if ( id * idHiggsSide < 0 ) {
            // test with b jet to W side
            double deltaR = ROOT::Math::VectorUtil::DeltaR(Jetb->p4(),p.p4() );
            if ( deltaR < 0.4) bMatchWSide = true;
          }
        }
      } 

      //Check light quark jets      
      for (size_t i=0; i < genParticles->size(); ++i){
          const reco::Candidate & p = (*genParticles)[i];
          int id = p.pdgId();
          //if not light quark but from light quark
          if ( abs(id) > 4  )continue;
          if ( hasImmediateMother(p,1) || hasImmediateMother(p,-1) )continue;
          if ( hasImmediateMother(p,2) || hasImmediateMother(p,-2) )continue;
          if ( hasImmediateMother(p,3) || hasImmediateMother(p,-3) )continue;
          if ( hasImmediateMother(p,4) || hasImmediateMother(p,-4) )continue;
          //if from W
          if(hasImmediateMother(p,24) || hasImmediateMother(p,-24)) {
              double deltaR1 = ROOT::Math::VectorUtil::DeltaR(Jet1->p4(),p.p4() );
              if ( deltaR1 < 0.4) Jet1Match = true;
              double deltaR2 = ROOT::Math::VectorUtil::DeltaR(Jet2->p4(),p.p4() );
              if ( deltaR2 < 0.4) Jet2Match = true;
              }
          }    

    //Fill histograms
     //everything matches
     if ( bMatchWSide && Jet1Match && Jet2Match) {
       htopMassMatch->Fill(output.getTopMass());
       hWMassMatch->Fill(output.getWMass()); 
       htopPt_match->Fill(output.top.Pt());
       hWPt_match->Fill(output.W.Pt());
       hdeltaPhi_Wb_match->Fill(dPhi_Wb);
       hdeltaR_Wb_match->Fill(dR_Wb);
       hdeltaPhi_jets_match->Fill(dPhi_jets);
       hdeltaR_jets_match->Fill(dR_jets);
       }
     //everything matches but b
     if ( bMatchHiggsSide && Jet1Match && Jet2Match) {
       htopMassMatchWrongB->Fill(output.getTopMass());
       hWMassMatchWrongB->Fill(output.getWMass()); 
       }
     //b matches
     if ( bMatchWSide ) {
       htopMassBMatch->Fill(output.getTopMass());
       hWMassBMatch->Fill(output.getWMass()); 
       }
     //quark jets match
     if ( Jet1Match && Jet2Match ) {
       htopMassQMatch->Fill(output.getTopMass());
       hWMassQMatch->Fill(output.getWMass()); 
       }

    }

    return output;
  }
     
}
