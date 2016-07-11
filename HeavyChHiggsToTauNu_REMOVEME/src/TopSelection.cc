#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"

#include <limits>

namespace HPlus {

  //constructor
  TopSelection::TopSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper) : TopSelectionBase::TopSelectionBase(iConfig, eventCounter, histoWrapper),
    //BaseSelection(eventCounter, histoWrapper),
    fTopMassLow(iConfig.getUntrackedParameter<double>("TopMassLow")),
    fTopMassHigh(iConfig.getUntrackedParameter<double>("TopMassHigh")),
    //fTopMassCount(eventCounter.addSubCounter("Top mass","Top Mass cut")),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src"))
    {
      edm::Service<TFileService> fs;

      TFileDirectory myDir = fs->mkdir("TopSelection");

    //top histograms
    htopPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopPt", "TopPt;top p_{T} (GeV)", 80, 0., 400.);
    htopMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass", "TopMass; m_{t} (GeV)", 80, 0., 400.);
    htopEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopEta", "TopEta; #eta_{t}", 100, -5., 5.);
    htopMassAfterCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMassAfterCut", "TopMassAfterCut; m_{t}", 80, 0., 400.);
    htopMassRejected = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMassRejected", "TopMassRejected; m_{t} (GeV)", 80, 0., 400.);
        
    //W histograms
    hWPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WPt", "WPt; W p_{T} (GeV)", 80, 0., 400.);
    hWMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass", "WMass; m_{W} (GeV)", 100, 0., 200.);
    hWEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WEta", "WEta; #eta_{W}", 80, 0., 400.);

    //other histograms
      hPtjjb = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "Pt_jjb", "Pt_jjb", 160, 0., 800.);
      hPtmax = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "Ptmax", "Ptmax", 160, 0., 800.);
      hPtmaxMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "PtmaxMatch", "PtmaxMatch", 160, 0., 800.);
      hPtmaxBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "PtmaxBMatch", "PtmaxBMatch", 160, 0., 800.);
      hPtmaxQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "PtmaxQMatch", "PtmaxQMatch", 160, 0., 800.);
      hPtmaxMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "PtmaxMatchWrongB", "PtmaxMatchWrongB", 160, 0., 800.);

      hjjbMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "jjbMass", "jjbMass", 80, 0., 400.);
      htopMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass_fullMatch", "TopMass_fullMatch", 80, 0., 400.);
      hWMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass_fullMatch", "WMass_fullMatchMatch", 100, 0., 200.);
      htopMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass_bMatch", "TopMass_bMatch", 80, 0., 400.);
      hWMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass_bMatch", "WMass_bMatch", 100, 0., 200.);
      htopMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass_qMatch", "TopMass_qMatch", 80, 0., 400.);
      hWMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass_qMatch", "WMass_qMatch", 100, 0., 200.);
      htopMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass_MatchWrongB", "TopMass_MatchWrongB", 80, 0., 400.);
      hWMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass_MatchWrongB", "WMass_MatchWrongB", 100, 0., 200.);
    }

  //destructor
  TopSelection::~TopSelection() {}

//---------------------------------------------------------------------------------------------

  //privateAnalyze
  TopSelection::Data TopSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<pat::Jet> bjet) {

    Data output;

    // Suppress warning about unused variable
    (void)bjet;

    // Reset variables
    double ptmax = 0;

    edm::Ptr<pat::Jet> Jet1;
    edm::Ptr<pat::Jet> Jet2;
    edm::Ptr<pat::Jet> Jetb;
    
    //for all combos of 3 jets close enough to each other...
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet1 = *iter;

      for(edm::PtrVector<pat::Jet>::const_iterator iter2 = jets.begin(); iter2 != jets.end(); ++iter2) {
        edm::Ptr<pat::Jet> iJet2 = *iter2;

        //same jet must not be used twice
        if (iter==iter2) continue;

        for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjets.begin(); iterb != bjets.end(); ++iterb) {
          edm::Ptr<pat::Jet> iJetb = *iterb;
          if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJetb->p4()) < 0.4) continue;
          if (ROOT::Math::VectorUtil::DeltaR(iJet2->p4(), iJetb->p4()) < 0.4) continue;      

          //...find top and W candidates with highest Pt
          XYZTLorentzVector candTop = iJet1->p4() + iJet2->p4() + iJetb->p4();
          XYZTLorentzVector candW = iJet1->p4() + iJet2->p4();
    
          hPtjjb->Fill(candTop.Pt());
          hjjbMass->Fill(candTop.M());

          if (candTop.Pt() > ptmax ) {
            ptmax = candTop.Pt();
            Jet1 = iJet1;
            Jet2 = iJet2;
            Jetb = iJetb;
            output.top = candTop;
            output.W = candW;
            }
          }
        }
      }
      
    hPtmax->Fill(ptmax);
    
    htopPt->Fill(output.top.Pt());
    htopMass->Fill(output.getTopMass());
    htopEta->Fill(output.getTopEta());
    hWPt->Fill(output.W.Pt());
    hWMass->Fill(output.getWMass());
    hWEta->Fill(output.getWEta());

    //Event selection based on top reconstruction
    if( output.getTopMass() < fTopMassLow || output.getTopMass() > fTopMassHigh ) {
      output.fPassedEvent = false;
      htopMassRejected->Fill(output.getTopMass());
      } else {
      output.fPassedEvent = true;
      htopMassAfterCut->Fill(output.getTopMass());      
      } 

    //MC matching for events that passed the top secletion
    if (!iEvent.isRealData() && output.fPassedEvent == true ) {
    
    //alternative: MC matching for all events with a reconstructed top quark  
    //if (!iEvent.isRealData() && && ptmax > 0  ) {

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
        //NEW, FOR HEAVY H+: if b quark and has immediate Higgs daughter:
        if(idHiggsSide == 0){
          if(abs(id) == 37) {
            idHiggsSide = id;
          }
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

    return output;
  }
  
}
