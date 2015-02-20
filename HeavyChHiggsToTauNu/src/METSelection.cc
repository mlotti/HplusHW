#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  METSelection::Data::Data():
    fPassedEvent(false) {}
  METSelection::Data::~Data() {}

  const edm::Ptr<reco::MET> METSelection::Data::getSelectedMET() const {
    if (fMETMode == METSelection::kRaw)
      return fRawMET;
    if (fMETMode == METSelection::kType1)
      return getPhiUncorrectedSelectedMET();
    if (fMETMode == METSelection::kType1PhiCorrected)
      return getPhiCorrectedSelectedMET();
    if (fMETMode == METSelection::kType2)
      throw cms::Exception("Configuration") << "Type II MET is not supported at the moment at " << __FILE__ << ":" << __LINE__ << std::endl;
    else
      throw cms::Exception("Logic") << "This should not happen" << __FILE__ << ":" << __LINE__ << std::endl;
  }

   const edm::Ptr<reco::MET> METSelection::Data::getPhiUncorrectedSelectedMET() const {
     if (fMETMode == METSelection::kRaw)
       return fRawMET;
     if (fMETMode == METSelection::kType1 || fMETMode == METSelection::kType1PhiCorrected)
       return getType1MET();
     else if (fMETMode == METSelection::kType2)
       throw cms::Exception("Configuration") << "Type II MET is not supported at the moment at " << __FILE__ << ":" << __LINE__ << std::endl;
     // Fallback
     edm::Ptr<reco::MET> myNullPointer;
     return myNullPointer;
   }

   const edm::Ptr<reco::MET> METSelection::Data::getPhiCorrectedSelectedMET() const {
     if (fPhiOscillationCorrectedType1MET.size() == 0) {
       throw cms::Exception("Configuration") << "fPhiOscillationCorrectedType1MET not calculated! " << __FILE__ << ":" << __LINE__ << std::endl;
     }
     if (fMETMode == METSelection::kType1 || fMETMode == METSelection::kType1PhiCorrected)
       if (fPhiOscillationCorrectedType1MET.size() > 0) {
         return edm::Ptr<reco::MET>(&fPhiOscillationCorrectedType1MET, 0);
       } else {
         edm::Ptr<reco::MET> myNullPointer;
         return myNullPointer;
       }
     else if (fMETMode == METSelection::kType2)
       throw cms::Exception("Configuration") << "Type II MET is not supported at the moment at " << __FILE__ << ":" << __LINE__ << std::endl;
     else
       throw cms::Exception("Configuration") << "METSelection::Data::getPhiCorrectedSelectedMET is supported only for type I MET! " << __FILE__ << ":" << __LINE__ << std::endl;
   }

   const edm::Ptr<reco::MET> METSelection::Data::getType1MET() const { 
     if (fType1METCorrected.size() > 0) {
       // Need to construct edm::Ptr here or otherwise copy operation will destroy the pointer and cause seg fault
       return edm::Ptr<reco::MET>(&fType1METCorrected, 0);
     }
     edm::Ptr<reco::MET> myNullPointer;
     return myNullPointer;
   }

  METSelection::METSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, const std::string& label, const std::string& tauIsolationDiscriminator):
    BaseSelection(eventCounter, histoWrapper),
    fRawSrc(iConfig.getUntrackedParameter<edm::InputTag>("rawSrc")),
    fType1Src(iConfig.getUntrackedParameter<edm::InputTag>("type1Src")),
    fType2Src(iConfig.getUntrackedParameter<edm::InputTag>("type2Src")),
    fCaloSrc(iConfig.getUntrackedParameter<edm::InputTag>("caloSrc")),
    fTcSrc(iConfig.getUntrackedParameter<edm::InputTag>("tcSrc")),
    fMetCut(iConfig.getUntrackedParameter<double>("METCut")),
    fPreMetCut(iConfig.getUntrackedParameter<double>("preMETCut")),
    // For type I/II correction
    fTauJetMatchingCone(iConfig.getUntrackedParameter<double>("tauJetMatchingCone")),
    fJetType1Threshold(iConfig.getUntrackedParameter<double>("jetType1Threshold")),
    fJetOffsetCorrLabel(iConfig.getUntrackedParameter<std::string>("jetOffsetCorrLabel")),
    //fType2ScaleFactor(iConfig.getUntrackedParameter<double>("type2ScaleFactor")),
    fTauIsolationDiscriminator(tauIsolationDiscriminator),
    // For phi oscillation correction
    fPhiCorrectionSlopeXForData(iConfig.getUntrackedParameter<double>("phiCorrectionSlopeXForData")),
    fPhiCorrectionOffsetXForData(iConfig.getUntrackedParameter<double>("phiCorrectionOffsetXForData")),
    fPhiCorrectionSlopeYForData(iConfig.getUntrackedParameter<double>("phiCorrectionSlopeYForData")),
    fPhiCorrectionOffsetYForData(iConfig.getUntrackedParameter<double>("phiCorrectionOffsetYForData")),
    fPhiCorrectionSlopeXForMC(iConfig.getUntrackedParameter<double>("phiCorrectionSlopeXForMC")),
    fPhiCorrectionOffsetXForMC(iConfig.getUntrackedParameter<double>("phiCorrectionOffsetXForMC")),
    fPhiCorrectionSlopeYForMC(iConfig.getUntrackedParameter<double>("phiCorrectionSlopeYForMC")),
    fPhiCorrectionOffsetYForMC(iConfig.getUntrackedParameter<double>("phiCorrectionOffsetYForMC")),
    bDisablingOfPhiCorrectionNotifiedStatus(true),
    // Counters
    fTypeIAllEvents(eventCounter.addSubCounter(label+"_MET", "MET TypeI correction all events")),
    fTypeITauRefJetFound(eventCounter.addSubCounter(label+"_MET", "MET TypeI correction tau reference jet found")),
    fTypeITauIsolated(eventCounter.addSubCounter(label+"_MET", "MET TypeI correction tau treated as isolated")),
    fMetCutCount(eventCounter.addSubCounter(label+"_MET","MET cut"))
  {
    if (fPreMetCut > fMetCut) {
      throw cms::Exception("Configuration") << "Pre-MET cut value " << fPreMetCut << " is larger than MET cut value " << fMetCut << "! Check your counfig!" << std::endl;
    }

    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(label);

    std::string select = iConfig.getUntrackedParameter<std::string>("select");
    if(select == "raw")
      fSelect = kRaw;
    else if(select == "type1")
      fSelect = kType1;
    else if(select == "type1phicorrected")
      fSelect = kType1PhiCorrected;
    else if(select == "type2") {
      fSelect = kType2;
      throw cms::Exception("Configuration") << "Type II MET is not supported at the moment" << std::endl;
    }
    else
      throw cms::Exception("Configuration") << "Invalid value for select '" << select << "', valid values are raw, type1, type1phicorrected, type2" << std::endl;

    std::string possiblyMode = iConfig.getUntrackedParameter<std::string>("doTypeICorrectionForPossiblyIsolatedTaus");
    if(possiblyMode == "disabled")
      fDoTypeICorrectionForPossiblyIsolatedTaus = kDisabled;
    else if(possiblyMode == "never")
      fDoTypeICorrectionForPossiblyIsolatedTaus = kNever;
    else if(possiblyMode == "always")
      fDoTypeICorrectionForPossiblyIsolatedTaus = kAlways;
    else if(possiblyMode == "forIsolatedOnly")
      fDoTypeICorrectionForPossiblyIsolatedTaus = kForIsolatedOnly;
    else
      throw cms::Exception("Configuration") << "METSelection: invalid value '" << possiblyMode << "' for parameter doTypeICorrectionForPossiblyIsolatedTaus, valid values are disabled, never, always, forIsolatedOnly";

    hMet = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "met", "met", 80, 0., 400.);
    hMetPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "metPhi", "met #phi", 72, -3.14159265, 3.14159265);
    hMetSignif = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "metSignif", "metSignif", 100, 0., 50.);
    hMetSumEt  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "metSumEt", "metSumEt", 30, 0., 1500.);
    hMetDivSumEt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "hMetDivSumEt", "hMetDivSumEt", 50, 0., 1.);
    hMetDivSqrSumEt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "hMetDivSqrSumEt", "hMetDivSqrSumEt", 50, 0., 1.);
  }

  METSelection::~METSelection() {}

  METSelection::Data METSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, nVertices, selectedTau, allJets, false);
  }

  METSelection::Data METSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, nVertices, selectedTau, allJets, false);
  }


  METSelection::Data METSelection::silentAnalyzeWithPossiblyIsolatedTaus(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, nVertices, selectedTau, allJets, true);
  }

  METSelection::Data METSelection::analyzeWithPossiblyIsolatedTaus(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, nVertices, selectedTau, allJets, true);
  }

  METSelection::Data METSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets, bool possiblyIsolatedTaus) {
    Data output;
    output.fMETMode = fSelect;

    edm::Handle<edm::View<reco::MET> > hrawmet;
    iEvent.getByLabel(fRawSrc, hrawmet);

    edm::Handle<edm::View<reco::MET> > htype1met;
    if (fType1Src.label() != "")
      iEvent.getByLabel(fType1Src, htype1met);

    /*
    edm::Handle<edm::View<reco::MET> > htype2met;
    iEvent.getByLabel(fType2Src, htype2met);
    */

    edm::Handle<edm::View<reco::MET> > hcalomet;
    iEvent.getByLabel(fCaloSrc, hcalomet);

    edm::Handle<edm::View<reco::MET> > htcmet;
    iEvent.getByLabel(fTcSrc, htcmet);

    // Set the handles, if object available
    if(hrawmet.isValid())
      output.fRawMET = hrawmet->ptrAt(0);
    if(htype1met.isValid() && fType1Src.label() != "") {
      output.fType1METCorrected.clear();
      output.fType1MET = htype1met->ptrAt(0);
      output.fType1METCorrected.push_back(undoJetCorrectionForSelectedTau(output.fType1MET, selectedTau, allJets, kType1, possiblyIsolatedTaus));
      output.fType1MET = edm::Ptr<reco::MET>(&output.fType1METCorrected, 0);
      // MET phi correction
      output.fPhiOscillationCorrectedType1MET.clear();
      output.fPhiOscillationCorrectedType1MET.push_back(getPhiOscillationCorrectedMET(output.fType1MET, iEvent.isRealData(), nVertices));
    } else {
      throw cms::Exception("LogicError") << "This should never happen at " << __FILE__ << ":" << __LINE__ << std::endl;
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
      output.fCaloMET = hcalomet->ptrAt(0);
    if(htcmet.isValid())
      output.fTcMET = htcmet->ptrAt(0);

    // Do the selection
    edm::Ptr<reco::MET> met;
    if(fSelect == kRaw)
      met = output.fRawMET;
    else if(fSelect == kType1)
      met = output.getType1MET();
    else if(fSelect == kType1PhiCorrected)
      met = output.getPhiCorrectedSelectedMET();
    else if(fSelect == kType2)
      //met = htype2met->ptrAt(0);
      throw cms::Exception("Configuration") << "Type II MET is not supported at the moment at " << __FILE__ << ":" << __LINE__ << std::endl;
    else
      throw cms::Exception("LogicError") << "This should never happen at " << __FILE__ << ":" << __LINE__ << std::endl;
    if (met.isNull()) {
      output.fPassedEvent = false;
      return output;
    }

    hMet->Fill(met->et());
    hMetPhi->Fill(met->phi());
    hMetSignif->Fill(met->significance());
    hMetSumEt->Fill(met->sumEt());
    double sumEt = met->sumEt();
    if(sumEt != 0){
        hMetDivSumEt->Fill(met->et()/sumEt);
        hMetDivSqrSumEt->Fill(met->et()/sumEt);
    }

    // Pre-met cut status
    if (met->et() > fPreMetCut) {
      output.fPassedPreMetCut = true;
    } else {
      output.fPassedPreMetCut = false;
    }
    // Met cut status
    if(met->et() > fMetCut) {
      output.fPassedEvent = true;
      increment(fMetCutCount);
    } else {
      output.fPassedEvent = false;
    }

    return output;
  }

  METSelection::Data METSelection::silentAnalyzeNoIsolatedTaus(const edm::Event& iEvent, const edm::EventSetup& iSetup, int nVertices) {
    Data output;
    output.fMETMode = fSelect;

    edm::Handle<edm::View<reco::MET> > hrawmet;
    iEvent.getByLabel(fRawSrc, hrawmet);

    edm::Handle<edm::View<reco::MET> > htype1met;
    if (fType1Src.label() != "")
      iEvent.getByLabel(fType1Src, htype1met);

    /*
    edm::Handle<edm::View<reco::MET> > htype2met;
    iEvent.getByLabel(fType2Src, htype2met);
    */

    edm::Handle<edm::View<reco::MET> > hcalomet;
    iEvent.getByLabel(fCaloSrc, hcalomet);

    edm::Handle<edm::View<reco::MET> > htcmet;
    iEvent.getByLabel(fTcSrc, htcmet);

    if(hrawmet.isValid())
      output.fRawMET = hrawmet->ptrAt(0);
    if(htype1met.isValid()) {
      output.fType1METCorrected.clear();
      output.fType1MET = htype1met->ptrAt(0);
      output.fType1METCorrected.push_back(*output.fType1MET);
      // MET phi correction
      output.fPhiOscillationCorrectedType1MET.clear();
      output.fPhiOscillationCorrectedType1MET.push_back(getPhiOscillationCorrectedMET(output.fType1MET, iEvent.isRealData(), nVertices));
    }
    if(hcalomet.isValid())
      output.fCaloMET = hcalomet->ptrAt(0);
    if(htcmet.isValid())
      output.fTcMET = htcmet->ptrAt(0);

    // Do the selection
    edm::Ptr<reco::MET> met;
    if(fSelect == kRaw)
      met = output.fRawMET;
    else if(fSelect == kType1)
      met = output.getType1MET();
    else if(fSelect == kType1PhiCorrected)
      met = output.getPhiCorrectedSelectedMET();
    if(met->et() > fMetCut) {
      output.fPassedEvent = true;
    } else {
      output.fPassedEvent = false;
    }
    //std::cout << "type1MET valid = " << htype1met.isValid() << std::endl;
    //std::cout << "type1MET = " << htype1met->ptrAt(0)->et() << std::endl;

    return output;
  }

  reco::MET METSelection::undoJetCorrectionForSelectedTau(const edm::Ptr<reco::MET>& met, const edm::Ptr<reco::Candidate>& selectedTau, const edm::PtrVector<pat::Jet>& allJets, Select type, bool possiblyIsolatedTaus) {
    /**
     * When the type I/II corrections are done, it is assumed (for
     * simplicity at that point) that the type I correction should be
     * done with all jets (with pt>10 etc). However, this is not
     * really the case, as we have a tau jet in the event. The JES
     * from a jet corresponding to the selected tau should not be
     * propagated to type I correction. In this method we undo that
     * correction for that particula jet.
     */

    increment(fTypeIAllEvents);
    if(type == kRaw)
      throw cms::Exception("Assert") << "METSelection::undoJetCorrectionForSelectedTau should not be called for raw MET" << std::endl;

    const pat::Tau *tau = dynamic_cast<const pat::Tau *>(selectedTau.get());

    if(possiblyIsolatedTaus) {
      if(fDoTypeICorrectionForPossiblyIsolatedTaus == kNever)
        return *met;
      if(fDoTypeICorrectionForPossiblyIsolatedTaus == kForIsolatedOnly) {
        if(!tau)
          throw cms::Exception("Assert") << "METSelection::undoJetCorrectionForSelectedTau(): nonIsolatedTausAsJets=true, but selectedTau is not of type pat::Tau!";

        if(tau->tauID(fTauIsolationDiscriminator) < 0.5)
          return *met;
      }
    }
    increment(fTypeITauIsolated);

    // Find the hadronic jet corresponding to the selected tau
    double minDR = fTauJetMatchingCone;
    edm::Ptr<pat::Jet> selectedJet;
    //std::cout << std::endl;
    for(size_t i=0; i<allJets.size(); ++i) {
      double dr = reco::deltaR(*selectedTau, *(allJets[i]));

      /*
      std::cout << "Jet         pt " << allJets[i]->pt()  << " eta " << allJets[i]->eta()  << " phi " << allJets[i]->phi() << std::endl
                << "   tau      pt " << selectedTau->pt() << " eta " << selectedTau->eta() << " phi " << selectedTau->phi() << " DR " << dr << std::endl
                << "   tau rjet pt " << tau->p4Jet().pt() << " eta " << tau->p4Jet().eta() << " phi " << tau->p4Jet().phi() << " DR " << reco::deltaR(tau->p4Jet(), *(allJets[i])) << std::endl;
      */

      if(dr < minDR) {
        minDR = dr;
        selectedJet = allJets[i];
      }
    }
    // It can happen that the JER smearing causes the tau reference
    // jet to have pt < 10, which is not stored in our pattuples. Here
    // it is assumed that this is what happens if the reference jet is
    // not found. The frequency of this must be monitored with the
    // counters.
    if(selectedJet.isNull()) {
      //throw cms::Exception("Assert") << "METSelection: Did not find the hadronic jet corresponding to the selected tau jet" << std::endl;
      return *met;
    }

    increment(fTypeITauRefJetFound);

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
                                               std::sqrt(correctedEx*correctedEx + correctedEy*correctedEy));
    // sumet is not set for pat::MET in the corrections anyway
    //double correctedSumEt = met->sumEt() + sumet;

    reco::MET correctedMet(correctedP4, met->vertex());
    //correctedMet.setP4(correctedP4);
    //std::cout << "corrected type I MET: " << correctedMet.et() << std::endl;
    return correctedMet;
  }

  reco::MET METSelection::getPhiOscillationCorrectedMET(const edm::Ptr<reco::MET>& met, const bool isRealData, const int nVertices) {
    if (nVertices < 0) {
      if (!bDisablingOfPhiCorrectionNotifiedStatus) {
        bDisablingOfPhiCorrectionNotifiedStatus = true;
        std::cout << "Warning: MET phi oscillation correction disabled!" << std::endl;
      }
      return *met;
    }
    double myCorrectionX = 0.0;
    double myCorrectionY = 0.0;
    if (isRealData) {
      myCorrectionX = met->px() - (static_cast<double>(nVertices)*fPhiCorrectionSlopeXForData + fPhiCorrectionOffsetXForData);
      myCorrectionY = met->py() - (static_cast<double>(nVertices)*fPhiCorrectionSlopeYForData + fPhiCorrectionOffsetYForData);
    } else {
      myCorrectionX = met->px() - (static_cast<double>(nVertices)*fPhiCorrectionSlopeXForMC + fPhiCorrectionOffsetXForMC);
      myCorrectionY = met->py() - (static_cast<double>(nVertices)*fPhiCorrectionSlopeYForMC + fPhiCorrectionOffsetYForMC);
    }
    reco::Candidate::LorentzVector myCorrectedP4(myCorrectionX, myCorrectionY, 0., std::sqrt(myCorrectionX*myCorrectionX + myCorrectionY*myCorrectionY));
    reco::MET correctedMet(myCorrectedP4, met->vertex());
    //std::cout << "phi corrected MET: " << correctedMet.et() << std::endl;
    //correctedMet.setP4(myCorrectedP4);
    return correctedMet;
  }

}
