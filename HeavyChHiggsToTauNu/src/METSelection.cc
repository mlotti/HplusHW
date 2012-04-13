#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {
  METSelection::Data::Data(const METSelection *metSelection, bool passedEvent):
    fMETSelection(metSelection), fPassedEvent(passedEvent) {}
  METSelection::Data::~Data() {}
  
  METSelection::METSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, std::string label):
    fRawSrc(iConfig.getUntrackedParameter<edm::InputTag>("rawSrc")),
    fType1Src(iConfig.getUntrackedParameter<edm::InputTag>("type1Src")),
    fType2Src(iConfig.getUntrackedParameter<edm::InputTag>("type2Src")),
    fCaloSrc(iConfig.getUntrackedParameter<edm::InputTag>("caloSrc")),
    fTcSrc(iConfig.getUntrackedParameter<edm::InputTag>("tcSrc")),
    fMetCut(iConfig.getUntrackedParameter<double>("METCut")),
    fTauJetMatchingCone(iConfig.getUntrackedParameter<double>("tauJetMatchingCone")),
    fJetType1Threshold(iConfig.getUntrackedParameter<double>("jetType1Threshold")),
    fJetOffsetCorrLabel(iConfig.getUntrackedParameter<std::string>("jetOffsetCorrLabel")),
    //fType2ScaleFactor(iConfig.getUntrackedParameter<double>("type2ScaleFactor")),
    fMetCutCount(eventCounter.addSubCounter(label+"_MET","MET cut")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(label);

    std::string select = iConfig.getUntrackedParameter<std::string>("select");
    if(select == "raw")
      fSelect = kRaw;
    else if(select == "type1")
      fSelect = kType1;
    else if(select == "type2") {
      fSelect = kType2;
      throw cms::Exception("Configuration") << "Type II MET is not supported at the moment" << std::endl;
    }
    else
      throw cms::Exception("Configuration") << "Invalid value for select '" << select << "', valid values are raw, type1, type2" << std::endl;
    
    hMet = makeTH<TH1F>(myDir, "met", "met", 400, 0., 400.);
    hMetSignif = makeTH<TH1F>(myDir, "metSignif", "metSignif", 100, 0., 50.);
    hMetSumEt  = makeTH<TH1F>(myDir, "metSumEt", "metSumEt", 50, 0., 1500.);
    hMetDivSumEt = makeTH<TH1F>(myDir, "hMetDivSumEt", "hMetDivSumEt", 50, 0., 1.);
    hMetDivSqrSumEt = makeTH<TH1F>(myDir, "hMetDivSqrSumEt", "hMetDivSqrSumEt", 50, 0., 1.);
  }

  METSelection::~METSelection() {}

  METSelection::Data METSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau>& selectedTau, const edm::PtrVector<pat::Jet>& allJets) {
    bool passEvent = false;
    edm::Handle<edm::View<reco::MET> > hrawmet;
    iEvent.getByLabel(fRawSrc, hrawmet);

    edm::Handle<edm::View<reco::MET> > htype1met;
    iEvent.getByLabel(fType1Src, htype1met);

    /*
    edm::Handle<edm::View<reco::MET> > htype2met;
    iEvent.getByLabel(fType2Src, htype2met);
    */

    edm::Handle<edm::View<reco::MET> > hcalomet;
    iEvent.getByLabel(fCaloSrc, hcalomet);

    edm::Handle<edm::View<reco::MET> > htcmet;
    iEvent.getByLabel(fTcSrc, htcmet);

    // Reset then handles
    fRawMET = edm::Ptr<reco::MET>();
    fType1MET = edm::Ptr<reco::MET>();
    fType2MET = edm::Ptr<reco::MET>();
    fCaloMET = edm::Ptr<reco::MET>();
    fTcMET = edm::Ptr<reco::MET>();

    // Set the handles, if object available
    if(hrawmet.isValid())
      fRawMET = hrawmet->ptrAt(0);
    if(htype1met.isValid()) {
      fType1METCorrected.clear();
      fType1MET = htype1met->ptrAt(0);
      fType1METCorrected.push_back(undoJetCorrectionForSelectedTau(fType1MET, selectedTau, allJets, kType1));
      fType1MET = edm::Ptr<reco::MET>(&fType1METCorrected, 0);
    }
    /*
    if(htype2met.isValid()) {
      fType2METCorrected.clear();
      fType2MET = htype2met->ptrAt(0);
      fType2METCorrected.push_back(undoJetCorrectionForSelectedTau(fType2MET, selectedTau, allJets, kType2));
      fType2MET = edm::Ptr<reco::MET>(&fType2METCorrected, 0);
    }
    */
    if(hcalomet.isValid())
      fCaloMET = hcalomet->ptrAt(0);
    if(htcmet.isValid())
      fTcMET = htcmet->ptrAt(0);

    // Do the selection
    edm::Ptr<reco::MET> met;
    if(fSelect == kRaw)
      met = hrawmet->ptrAt(0);
    else if(fSelect == kType1)
      met = htype1met->ptrAt(0);
    else if(fSelect == kType2)
      //met = htype2met->ptrAt(0);
      throw cms::Exception("Configuration") << "Type II MET is not supported at the moment at " << __FILE__ << ":" << __LINE__ << std::endl;
    else
      throw cms::Exception("LogicError") << "This should never happen at " << __FILE__ << ":" << __LINE__ << std::endl;

    hMet->Fill(met->et(), fEventWeight.getWeight());
    hMetSignif->Fill(met->significance(), fEventWeight.getWeight());
    hMetSumEt->Fill(met->sumEt(), fEventWeight.getWeight());
    double sumEt = met->sumEt();
    if(sumEt != 0){
        hMetDivSumEt->Fill(met->et()/sumEt, fEventWeight.getWeight());
        hMetDivSqrSumEt->Fill(met->et()/sumEt, fEventWeight.getWeight());
    }

    if(met->et() > fMetCut) {
      passEvent = true;
      increment(fMetCutCount);
    }
    fSelectedMET = met;
    
    return Data(this, passEvent);
  }

  reco::MET METSelection::undoJetCorrectionForSelectedTau(const edm::Ptr<reco::MET>& met, const edm::Ptr<pat::Tau>& selectedTau, const edm::PtrVector<pat::Jet>& allJets, Select type) {
    /**
     * When the type I/II corrections are done, it is assumed (for
     * simplicity at that point) that the type I correction should be
     * done with all jets (with pt>10 etc). However, this is not
     * really the case, as we have a tau jet in the event. The JES
     * from a jet corresponding to the selected tau should not be
     * propagated to type I correction. In this method we undo that
     * correction for that particula jet.
     */

    if(type == kRaw)
      throw cms::Exception("Assert") << "METSelection::undoJetCorrectionForSelectedTau should not be called for raw MET" << std::endl;

    // Find the hadronic jet corresponding to the selected tau
    double minDR = fTauJetMatchingCone;
    edm::Ptr<pat::Jet> selectedJet;
    for(size_t i=0; i<allJets.size(); ++i) {
      double dr = reco::deltaR(*selectedTau, *(allJets[i]));
      if(dr < minDR) {
        minDR = dr;
        selectedJet = allJets[i];
      }
    }
    if(selectedJet.isNull())
      throw cms::Exception("Assert") << "METSelection: Did not find the hadronic jet corresponding to the selected tau jet" << std::endl;

    // The code doing the correction is at
    // JetMETCorrections/Type1MET/interface/PFJetMETcorrInputProducerT.h
    // (Here we try to undo the corrections for one jet)

    double mex = 0;
    double mey = 0;
    /*
    double unclusteredX = 0;
    double unclusteredY = 0;
    */
    //double sumet = 0;

    reco::Candidate::LorentzVector rawJetP4 = selectedJet->correctedP4("Uncorrected");
    reco::Candidate::LorentzVector rawJetP4offset = selectedJet->correctedP4(fJetOffsetCorrLabel);
    if(selectedJet->pt() > fJetType1Threshold) {
      mex += (selectedJet->px() - rawJetP4offset.px());
      mey += (selectedJet->py() - rawJetP4offset.py());
      //sumet -= (selectedJet->Et() - rawJetP4offset.Et());

      // For type II MET, we should undo also the portion of L1FastJet
      // correction for unclustered energy due to pile-up
      /*
      if(type == kType2) {
        unclusteredX -= (rawJetP4offset.px() - rawJetP4.px());
        unclusteredY -= (rawJetP4offset.py() - rawJetP4.py());
      }
      */
    }
    /*
    else {
      // If the corresponding jet was not above type I threshold, we
      // should subtract the contribution from raw jet from the unclustered energy
      if(type == kType2) {
        unclusteredX -= rawJetP4.px();
        unclusteredY -= rawJetP4.py();
      }
    }
    */

    // JetMETCorrections/Type1MET/interface/CorrectedMETProducerT.h
    double correctedEx = met->px() + mex;
    double correctedEy = met->py() + mey;
    /*
    if(type == kType2) {
      correctedEx += (fType2ScaleFactor-1.) * unclusteredX;
      correctedEy += (fType2ScaleFactor-1.) * unclusteredY;
    }
    */
    reco::Candidate::LorentzVector correctedP4(correctedEx, correctedEy, 0,
                                               std::sqrt(correctedEx*correctedEx + correctedEy+correctedEy));
    // sumet is not set for pat::MET in the corrections anyway
    //double correctedSumEt = met->sumEt() + sumet;

    reco::MET correctedMet = *met;
    correctedMet.setP4(correctedP4);
    return correctedMet;
  }
}
