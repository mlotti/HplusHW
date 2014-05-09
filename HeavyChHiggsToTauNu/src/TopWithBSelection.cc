#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithBSelection.h"
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
  TopWithBSelection::TopWithBSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper) : TopSelectionBase::TopSelectionBase(iConfig, eventCounter, histoWrapper),
    //BaseSelection(eventCounter, histoWrapper),
    fTopMassLow(iConfig.getUntrackedParameter<double>("TopMassLow")),
    fTopMassHigh(iConfig.getUntrackedParameter<double>("TopMassHigh")),
    fChi2Cut(iConfig.getUntrackedParameter<double>("Chi2Cut")),
    //fTopWithBMassCount(eventCounter.addSubCounter("Top with B mass cut","Top with B Mass cut")),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src"))
  {
    edm::Service<TFileService> fs;

    TFileDirectory myDir = fs->mkdir("TopWithBSelection");

    //top histograms
    htopPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopPt", "TopPt;top p_{T} (GeV)", 80, 0., 400.);
    htopMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass", "TopMass; m_{t} (GeV)", 80, 0., 400.);
    htopEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopEta", "TopEta; #eta_{t}", 100, -5., 5.);
    
    htopPtAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopPtAfterCut", "TopPtAfterCut; top p_{T} (GeV)", 80, 0., 400.);
    htopMassAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMassAfterCut", "TopMassAfterCut; m_{t}", 80, 0., 400.);
    htopEtaAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopEtaAfterCut", "TopEtaAfterCut; #eta_{t}", 100, -5., 5.);
    htopMassRejected = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMassRejected", "TopMassRejected; m_{t} (GeV)", 80, 0., 400.);
    
    //W histograms
    hWPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WPt", "WPt; W p_{T} (GeV)", 80, 0., 400.);
    hWMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMass", "WMass; m_{W} (GeV)", 100, 0., 200.);
    hWEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WEta", "WEta; #eta_{W}", 80, 0., 400.);

    hWPtAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WPtAfterCut", "WPtAfterCut; W p_{T} (GeV)", 80, 0., 400.);
    hWMassAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMassAfterCut", "WMassAfterCut; m_{W} (GeV)", 100, 0., 200.);
    hWEtaAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WEtaAfterCut", "WEtaAfterCut; #eta_{W}", 80, 0., 400.);
    
    //MC matching histograms
    htopMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass_fullMatch", "TopMass_fullMatch; m_{t} (GeV)", 80, 0., 400.);
    htopMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass_bMatch", "TopMass_bMatch; m_{t} (GeV)", 80, 0., 400.);
    htopMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass_qMatch", "TopMass_qMatch; m_{t} (GeV)", 80, 0., 400.);
    htopMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass_MatchWrongB", "TopMass_MatchWrongB; m_{t} (GeV)", 80, 0., 400.);
    hWMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMass_fullMatch", "WMass_fullMatchMatch; m_{W} (GeV)", 100, 0., 200.);
    hWMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMass_bMatch", "WMass_bMatch; m_{W} (GeV)", 100, 0., 200.);
    hWMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMass_qMatch", "WMass_qMatch; m_{W} (GeV)", 100, 0., 200.);
    hWMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMass_MatchWrongB", "WMass_MatchWrongB; m_{W} (GeV)", 100, 0., 200.);

    //other histograms    
    hjjbMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jjbMass", "jjbMass;m_{jjb} (GeV)", 80, 0., 400.);
    hChi2Min = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Chi2Min", "Chi2Min; {#chi^2}_{min}", 200, 0., 40.);
  }

  //destructor
  TopWithBSelection::~TopWithBSelection() {}

  //privateAnalyze
  TopWithBSelection::Data TopWithBSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> iJetb) {
    Data output;

    // Reset variables
    double chi2Min = 999999;
    double nominalTop = 172.9;
    double nominalW = 80.4;
    double sigmaTop = 18.;
    double sigmaW = 11.;
    bool topmassfound = false;
      
    edm::Ptr<pat::Jet> Jet1;
    edm::Ptr<pat::Jet> Jet2;
    edm::Ptr<pat::Jet> Jetb;

    //for all combos of 3 jets close enough to each other...
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet1 = *iter;

      for(edm::PtrVector<pat::Jet>::const_iterator iter2 = jets.begin(); iter2 != jets.end(); ++iter2) {
	edm::Ptr<pat::Jet> iJet2 = *iter2;

	if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJet2->p4()) < 0.4) continue;
	
	if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJetb->p4()) < 0.4) continue;
	if (ROOT::Math::VectorUtil::DeltaR(iJet2->p4(), iJetb->p4()) < 0.4) continue;	  
	
    //...find top and W candidates with minimum chi2
	XYZTLorentzVector candTop = iJet1->p4() + iJet2->p4() + iJetb->p4();
	XYZTLorentzVector candW = iJet1->p4() + iJet2->p4();
	
	hjjbMass->Fill(candTop.M());
	double chi2 = ((candTop.M() - nominalTop)/sigmaTop)*((candTop.M() - nominalTop)/sigmaTop) + ((candW.M() - nominalW)/sigmaW)*((candW.M() - nominalW)/sigmaW); 
	
	if (chi2 < chi2Min ) {
	  chi2Min = chi2;
	  Jet1 = iJet1;
	  Jet2 = iJet2;
	  Jetb = iJetb;            
	  output.top = candTop;
	  output.W = candW;
	  topmassfound = true;
	  }
    }
  }

    hChi2Min->Fill(sqrt(chi2Min));

    htopPt->Fill(output.top.Pt());
    htopMass->Fill(output.getTopMass());
    htopEta->Fill(output.getTopEta());
    hWPt->Fill(output.W.Pt());
    hWMass->Fill(output.getWMass());
    hWEta->Fill(output.getWEta());
    
    if( output.getTopMass() >= fTopMassLow && output.getTopMass() <= fTopMassHigh ) {    
//    if (sqrt(chi2Min) < fChi2Cut) { //TODO: the cut criterion should be changed to this or something more sophisticated later
        htopPtAfterCut->Fill(output.top.Pt());
        htopMassAfterCut->Fill(output.getTopMass());
        htopEtaAfterCut->Fill(output.getTopEta());
        hWPtAfterCut->Fill(output.W.Pt());
        hWMassAfterCut->Fill(output.getWMass());
        hWEtaAfterCut->Fill(output.getWEta());
      }

//---------------------------------------------------------------------------------------------
    //Search correct combinations

    //if (!iEvent.isRealData() && chi2Min < fChi2Cut ) {
    if (!iEvent.isRealData() && topmassfound ) {
      edm::Handle <reco::GenParticleCollection> genParticles;
      iEvent.getByLabel(fSrc, genParticles);

      bool bMatchHiggsSide = false;
      bool bMatchTauSide = false;
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
        }
             
    //Test if b-jet is tau-side or Higgs-side
      for (size_t i=0; i < genParticles->size(); ++i){
        const reco::Candidate & p = (*genParticles)[i];
        int id = p.pdgId();
        // select only b-jet particles
        if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
        //if immediate top mother
        if(hasImmediateMother(p,6) || hasImmediateMother(p,-6)) {
          if ( id * idHiggsSide > 0 ) {
            // test with b jet to tau side
            double deltaR = ROOT::Math::VectorUtil::DeltaR(Jetb->p4(),p.p4() );
            if ( deltaR < 0.4) bMatchHiggsSide = true;
            }
          if ( id * idHiggsSide < 0 ) {
            // test with b jet to top side
            double deltaR = ROOT::Math::VectorUtil::DeltaR(Jetb->p4(),p.p4() );
            if ( deltaR < 0.4) bMatchTauSide = true;
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
     if ( bMatchTauSide && Jet1Match && Jet2Match) {
       htopMassMatch->Fill(output.getTopMass());
       hWMassMatch->Fill(output.getWMass()); 
       }
     //everything matches but b
     if ( bMatchHiggsSide && Jet1Match && Jet2Match) {
       htopMassMatchWrongB->Fill(output.getTopMass());
       hWMassMatchWrongB->Fill(output.getWMass()); 
       }
     //b matches
     if ( bMatchTauSide ) {
       htopMassBMatch->Fill(output.getTopMass());
       hWMassBMatch->Fill(output.getWMass()); 
       }
     //quark jets match
     if ( Jet1Match && Jet2Match ) {
       htopMassQMatch->Fill(output.getTopMass());
       hWMassQMatch->Fill(output.getWMass()); 
       }
      }

    //Event selection based on top reconstruction
    if( output.getTopMass() < fTopMassLow || output.getTopMass() > fTopMassHigh ) {
      output.fPassedEvent = false;
      htopMassRejected->Fill(output.getTopMass());      
      } else {
      output.fPassedEvent = true;
      //increment(fTopChiMassCount); //TODO
      } 
    return output;
  }
     
}
