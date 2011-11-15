#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {
  BTagging::Data::Data(const BTagging *bTagging, bool passedEvent):
    fBTagging(bTagging), fPassedEvent(passedEvent) {}
  BTagging::Data::~Data() {}

  BTagging::BTaggingScaleFactor::BTaggingScaleFactor() { }
  BTagging::BTaggingScaleFactor::~BTaggingScaleFactor() { }
  
  void BTagging::BTaggingScaleFactor::addBFlavorData(double pT, double scaleFactorB, double scaleFactorUncertaintyB, double epsilonMCB) {
    fPtBinsB.push_back(pT);
    fScaleFactorB.push_back(scaleFactorB);
    fScaleFactorUncertaintyB.push_back(scaleFactorUncertaintyB);
    fEpsilonMCB.push_back(epsilonMCB);
  }
  void BTagging::BTaggingScaleFactor::addNonBFlavorData(double pT, double scaleFactorL, double scaleFactorUncertaintyL, double epsilonMCL) {
    fPtBinsL.push_back(pT);
    fScaleFactorL.push_back(scaleFactorL);
    fScaleFactorUncertaintyL.push_back(scaleFactorUncertaintyL);
    fEpsilonMCL.push_back(epsilonMCL);
  }

  size_t BTagging::BTaggingScaleFactor::obtainIndex(std::vector<double>& table, double pt) {
    size_t myEnd = table.size();
    size_t myPos = 0;
    while (myPos < myEnd) {
      if (pt < table[myPos]) {
        if (myPos == 0)
          return 0; // should never happen
        else
          return myPos-1;
      }
      ++myPos;
    }
    return myEnd-1; // return last bin
  }

  double BTagging::BTaggingScaleFactor::getWeight(int nPassedB, int nPassedL, std::vector<double>& nFailedBpT, std::vector<double>& nFailedLpT) {
    double myValue = 1.0;
    // b-flavor jets that have passed b-tagging
    myValue *= std::pow(fScaleFactorB[0], nPassedB);
    // b-flavor jets that have not passed b-tagging
    for(std::vector<double>::iterator it = nFailedBpT.begin(); it != nFailedBpT.end(); ++it) {
      // obtain index for pT table
      int myIndex = obtainIndex(fPtBinsB, *it);
      myValue *= (1.-fScaleFactorB[myIndex]*fEpsilonMCB[myIndex]) / (1.-fEpsilonMCB[myIndex]);
    }
    // non-b-flavor jets that have passed b-tagging
    myValue *= std::pow(fScaleFactorL[0], nPassedL);
    // non-b-flavor jets that have not passed b-tagging
    for(std::vector<double>::iterator it = nFailedLpT.begin(); it != nFailedLpT.end(); ++it) {
      // obtain index for pT table
      int myIndex = obtainIndex(fPtBinsL, *it);
      myValue *= (1.-fScaleFactorL[myIndex]*fEpsilonMCL[myIndex]) / (1.-fEpsilonMCL[myIndex]);
    }
    // Return calculated value
    return myValue;
  }
  
  double BTagging::BTaggingScaleFactor::getRelativeUncertainty(int nPassedB, int nPassedL, std::vector<double>& nFailedBpT, std::vector<double>& nFailedLpT) {

    // b-flavor jets and non-b-flavor jets are uncorrelated --> error propagation with F=F(scalefactorB, scalefactorL)
    // Notice the nice anti-correlation between the passed and failed components
    // b-flavor jets
    double myBTerm = static_cast<double>(nPassedB)/fScaleFactorB[0];
    for(std::vector<double>::iterator it = nFailedBpT.begin(); it != nFailedBpT.end(); ++it) {
      // obtain index for pT table
      int myIndex = obtainIndex(fPtBinsB, *it);
      myBTerm -= fEpsilonMCB[myIndex]/(1.-fScaleFactorB[myIndex]*fEpsilonMCB[myIndex]);
    }
    myBTerm *= fScaleFactorUncertaintyB[0];
    // l-flavor jets
    double myLTerm = static_cast<double>(nPassedL)/fScaleFactorL[0];
    for(std::vector<double>::iterator it = nFailedLpT.begin(); it != nFailedLpT.end(); ++it) {
      // obtain index for pT table
      int myIndex = obtainIndex(fPtBinsL, *it);
      myLTerm -= fEpsilonMCL[myIndex]/(1.-fScaleFactorL[myIndex]*fEpsilonMCL[myIndex]);
    }
    myLTerm *= fScaleFactorUncertaintyL[0];
    // Return result
    return std::sqrt(std::pow(myBTerm,2) + std::pow(myLTerm,2));
  }

  double BTagging::BTaggingScaleFactor::getAbsoluteUncertainty(int nPassedB, int nPassedL, std::vector<double>& nFailedBpT, std::vector<double>& nFailedLpT) {
    return getWeight(nPassedB, nPassedL, nFailedBpT, nFailedLpT) * getRelativeUncertainty(nPassedB, nPassedL, nFailedBpT, nFailedLpT);
  }

  BTagging::BTagging(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fDiscriminator(iConfig.getUntrackedParameter<std::string>("discriminator")),
    fDiscrCut(iConfig.getUntrackedParameter<double>("discriminatorCut")),
    fMin(iConfig.getUntrackedParameter<uint32_t>("minNumber")),
    fTaggedCount(eventCounter.addSubCounter("b-tagging main","b-tagging")),
    fAllSubCount(eventCounter.addSubCounter("b-tagging", "all jets")),
    fTaggedSubCount(eventCounter.addSubCounter("b-tagging", "tagged")),
    fTaggedEtaCutSubCount(eventCounter.addSubCounter("b-tagging", "eta  cut")),  
    fTaggedAllRealBJetsSubCount(eventCounter.addSubCounter("b-tagging", "All real b jets")),
    fTaggedTaggedRealBJetsSubCount(eventCounter.addSubCounter("b-tagging", "Btagged real b jets")),
    fTaggedNoTaggedJet(eventCounter.addSubCounter("b-tagging", "no b-tagged jet")),
    fTaggedOneTaggedJet(eventCounter.addSubCounter("b-tagging", "one b-tagged jet")),
    fTaggedTwoTaggedJets(eventCounter.addSubCounter("b-tagging", "two b-tagged jets")),
    fEventWeight(eventWeight),
    //    fTaggedEtaCutSubCount(eventCounter.addSubCounter("b-tagging", "eta  cut")),
    //   fEventWeight(eventWeight),
    fMaxDiscriminatorValue(0)
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("Btagging");
    hDiscr = makeTH<TH1F>(myDir, "jet_bdiscriminator", ("b discriminator "+fDiscriminator).c_str(), 100, -10, 10);
    hPt = makeTH<TH1F>(myDir, "bjet_pt", "bjet_pt", 400, 0., 400.);
    hDiscrB = makeTH<TH1F>(myDir, "RealBjet_discrim", ("realm b discrimi. "+fDiscriminator).c_str(), 100, -10, 10);
    hPtB = makeTH<TH1F>(myDir, "relabjet_pt", "realbjet_pt", 400, 0., 400.);
    hEtaB = makeTH<TH1F>(myDir, "realbjet_eta", "realbjet_pt", 400, -5., 5.);
    hPt1 = makeTH<TH1F>(myDir, "bjet1_pt", "bjet1_pt", 100, 0., 400.);
    hPt2 = makeTH<TH1F>(myDir, "bjet2_pt", "bjet2_pt", 100, 0., 400.);
    hEta = makeTH<TH1F>(myDir, "bjet_eta", "bjet_pt", 400, -5., 5.);
    hEta1 = makeTH<TH1F>(myDir, "bjet1_eta", "bjet1_pt", 100, -5., 5.);
    hEta2 = makeTH<TH1F>(myDir, "bjet2_eta", "bjet2_pt", 100, -5., 5.);
    hNumberOfBtaggedJets = makeTH<TH1F>(myDir, "NumberOfBtaggedJets", "NumberOfBtaggedJets", 15, 0., 15.);
    
    hScaleFactor = makeTH<TH1F>(myDir, "scaleFactor", "scaleFactor;b-tag/mistag scale factor;N_{events}/0.05", 100, 0., 5.);
    hMCMatchForPassedJets = makeTH<TH1F>(myDir, "MCMatchForPassedJets", "MCMatchForPassedJets;;N_{jets}", 3, 0., 3.);
    hMCMatchForPassedJets->GetXaxis()->SetBinLabel(1, "b jet");
    hMCMatchForPassedJets->GetXaxis()->SetBinLabel(2, "light jet");
    hMCMatchForPassedJets->GetXaxis()->SetBinLabel(3, "no match");

    hBTagRelativeUncertainty = makeTH<TH1F>(myDir, "BTagRelativeUncertainty", "BTagRelativeUncertainty;Relative Uncertainty;N_{events}", 3000, 0., 3.);
    hBTagAbsoluteUncertainty = makeTH<TH1F>(myDir, "BTagAbsoluteUncertainty", "BTagAbsoluteUncertainty;Absolute Uncertainty;N_{events}", 3000, 0., 3.);

    // BTagging scale factors for b-flavor jets (source: BTV-11-001)
    double fScaleFactorBFlavor = 0.95;
    double fScaleFactorBFlavorUncertainty = 0.05;
    fBTaggingScaleFactor.addBFlavorData(30., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .671);
    fBTaggingScaleFactor.addBFlavorData(40., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .741);
    fBTaggingScaleFactor.addBFlavorData(50., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .779);
    fBTaggingScaleFactor.addBFlavorData(60., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .802);
    fBTaggingScaleFactor.addBFlavorData(70., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .826);
    fBTaggingScaleFactor.addBFlavorData(80., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .840);
    fBTaggingScaleFactor.addBFlavorData(100., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .840);
    fBTaggingScaleFactor.addBFlavorData(120., fScaleFactorBFlavor, fScaleFactorBFlavorUncertainty, .856);
    // BTagging scale factors for non-b-flavor jets (source: BTV-11-001)
    double fScaleFactorLightFlavor = 1.10;
    double fScaleFactorLightFlavorUncertainty = 0.12;
    fBTaggingScaleFactor.addNonBFlavorData(30., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.055);
    fBTaggingScaleFactor.addNonBFlavorData(40., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.076);
    fBTaggingScaleFactor.addNonBFlavorData(50., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.095);
    fBTaggingScaleFactor.addNonBFlavorData(60., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.116);
    fBTaggingScaleFactor.addNonBFlavorData(70., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.128);
    fBTaggingScaleFactor.addNonBFlavorData(80., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.151);
    fBTaggingScaleFactor.addNonBFlavorData(90., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.170);
    fBTaggingScaleFactor.addNonBFlavorData(100., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.186);
    fBTaggingScaleFactor.addNonBFlavorData(110., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.202);
    fBTaggingScaleFactor.addNonBFlavorData(120., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.213);
    fBTaggingScaleFactor.addNonBFlavorData(130., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.226);
    fBTaggingScaleFactor.addNonBFlavorData(140., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.238);
    fBTaggingScaleFactor.addNonBFlavorData(150., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.248);
    fBTaggingScaleFactor.addNonBFlavorData(160., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.260);
    fBTaggingScaleFactor.addNonBFlavorData(170., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.271);
    fBTaggingScaleFactor.addNonBFlavorData(180., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.279);
    fBTaggingScaleFactor.addNonBFlavorData(190., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.286);
    fBTaggingScaleFactor.addNonBFlavorData(200., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.294);
    fBTaggingScaleFactor.addNonBFlavorData(210., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.303);
    fBTaggingScaleFactor.addNonBFlavorData(220., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.311);
    fBTaggingScaleFactor.addNonBFlavorData(230., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.319);
    fBTaggingScaleFactor.addNonBFlavorData(240., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.321);
    fBTaggingScaleFactor.addNonBFlavorData(250., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.329);
    fBTaggingScaleFactor.addNonBFlavorData(260., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.335);
    fBTaggingScaleFactor.addNonBFlavorData(270., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.338);
    fBTaggingScaleFactor.addNonBFlavorData(280., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.347);
    fBTaggingScaleFactor.addNonBFlavorData(290., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.355);
    fBTaggingScaleFactor.addNonBFlavorData(300., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.358);
    fBTaggingScaleFactor.addNonBFlavorData(310., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.361);
    fBTaggingScaleFactor.addNonBFlavorData(320., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.367);
    fBTaggingScaleFactor.addNonBFlavorData(330., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.365);
    fBTaggingScaleFactor.addNonBFlavorData(340., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.371);
    fBTaggingScaleFactor.addNonBFlavorData(350., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.373);
    fBTaggingScaleFactor.addNonBFlavorData(360., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.374);
    fBTaggingScaleFactor.addNonBFlavorData(370., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.377);
    fBTaggingScaleFactor.addNonBFlavorData(380., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.376);
    fBTaggingScaleFactor.addNonBFlavorData(390., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 3.380);
    fBTaggingScaleFactor.addNonBFlavorData(400., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.385);
    fBTaggingScaleFactor.addNonBFlavorData(410., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.387);
    fBTaggingScaleFactor.addNonBFlavorData(420., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.391);
    fBTaggingScaleFactor.addNonBFlavorData(430., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.392);
    fBTaggingScaleFactor.addNonBFlavorData(440., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.389);
    fBTaggingScaleFactor.addNonBFlavorData(450., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.396);
    fBTaggingScaleFactor.addNonBFlavorData(460., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.396);
    fBTaggingScaleFactor.addNonBFlavorData(470., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.402);
    fBTaggingScaleFactor.addNonBFlavorData(480., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.396);
    fBTaggingScaleFactor.addNonBFlavorData(490., fScaleFactorLightFlavor, fScaleFactorLightFlavorUncertainty, 0.402);

  }

  BTagging::~BTagging() {}

  BTagging::Data BTagging::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets) {
    // Reset variables
    iNBtags = -1;
    fMaxDiscriminatorValue = 0.;
    fScaleFactor = 1.0;
    fScaleFactorAbsoluteUncertainty = 0.0;
    fScaleFactorRelativeUncertainty = 0.0;
    bool passEvent = false;

    fSelectedJets.clear();
    fSelectedJets.reserve(jets.size());

    size_t passed = 0;
    bool bmatchedJet = false;
    
    // Calculate 
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;

      increment(fAllSubCount);

      if (!iEvent.isRealData()) {
	edm::Handle <reco::GenParticleCollection> genParticles;
	iEvent.getByLabel("genParticles", genParticles);
	for (size_t i=0; i < genParticles->size(); ++i) {
	  const reco::Candidate & p = (*genParticles)[i];
	  if (p.status() != 2 ) continue;
	  if (std::abs(p.pdgId()) == 5) {	    
	    if (reco::deltaR(p, iJet->p4()) < 0.4) {
	      bmatchedJet = true;
	    }
	  }
	}
      }
      if( bmatchedJet )   increment(fTaggedAllRealBJetsSubCount);

      float discr = iJet->bDiscriminator(fDiscriminator);
      if (bmatchedJet ) {
	if(discr > fDiscrCut ) {
	  hPtB->Fill(iJet->pt(), fEventWeight.getWeight());
	  hEtaB->Fill(iJet->eta(), fEventWeight.getWeight());
	}
	hDiscrB->Fill(discr, fEventWeight.getWeight());
      }

      
      hDiscr->Fill(discr, fEventWeight.getWeight());
      if(!(discr > fDiscrCut)) continue;
      increment(fTaggedSubCount);
      //      ++passed;

      hPt->Fill(iJet->pt(), fEventWeight.getWeight());
      hEta->Fill(iJet->eta(), fEventWeight.getWeight());

      if(fabs(iJet->eta()) > fEtaCut ) continue;
      increment(fTaggedEtaCutSubCount);
      if (discr > fMaxDiscriminatorValue)
        fMaxDiscriminatorValue = discr;

      ++passed;
      if( bmatchedJet )   increment(fTaggedTaggedRealBJetsSubCount);


      fSelectedJets.push_back(iJet);
    } // end of jet loop
    
    // Obtain and apply scale factor for MC events
    if (!iEvent.isRealData())
      applyScaleFactor(jets, fSelectedJets);

    // Fill histograms
    hNumberOfBtaggedJets->Fill(fSelectedJets.size(), fEventWeight.getWeight());
    iNBtags = fSelectedJets.size();

    ////////////////////////////////
    if( passed > 0) {
      hPt1->Fill(fSelectedJets[0]->pt(), fEventWeight.getWeight());
      hEta1->Fill(fSelectedJets[0]->eta(), fEventWeight.getWeight());
    }
    if( passed > 1) {
      hPt2->Fill(fSelectedJets[1]->pt(), fEventWeight.getWeight());
      hEta2->Fill(fSelectedJets[1]->eta(), fEventWeight.getWeight());
    }
       // plot deltaPhi(bjet,tau jet)
    //      double deltaPhi = -999;    
	//      if ( met->et()>  fMetCut) {
      //	  deltaPhi = DeltaPhi::reconstruct(*(iJet), *(met));
      //	  hDeltaPhiJetMet->Fill(deltaPhi*57.3);
      //      }
    if( passed == 0)   increment(fTaggedNoTaggedJet);
    if( passed == 1)   increment(fTaggedOneTaggedJet);
    if( passed == 2)   increment(fTaggedTwoTaggedJets);

    passEvent = true;
    if(passed < fMin) passEvent = false;
    increment(fTaggedCount);

    return Data(this, passEvent);
  }
  
  void BTagging::applyScaleFactor(const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {
    // Count number of b jets and light jets
    int nBJetsPassed = 0;
    std::vector<double> fBJetsFailedPt;
    int nLightJetsPassed = 0;
    std::vector<double> fLightJetsFailedPt;

    // Loop over jets
    for (edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      bool myJetTaggedStatus = false;
      for (edm::PtrVector<pat::Jet>::const_iterator iBjet = bjets.begin(); iBjet != bjets.end(); ++iBjet) {
	if (iJet == *iBjet) myJetTaggedStatus = true;
      }
      if (myJetTaggedStatus) continue; // no double counting

      const reco::GenParticle* myParticle = (*iJet).genParton();
      if (myParticle == 0) { // no MC match; assume its a light flavor jet
	fLightJetsFailedPt.push_back((*iJet).pt());
      } else {
        if (std::abs(myParticle->pdgId()) == 5) {
	  fBJetsFailedPt.push_back((*iJet).pt());
        } else {
	  fLightJetsFailedPt.push_back((*iJet).pt());
        }
      }
    }
    // Loop over b-tagged jets
    for (edm::PtrVector<pat::Jet>::const_iterator iter = bjets.begin(); iter != bjets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      const reco::GenParticle* myParticle = (*iJet).genParton();
      if (myParticle == 0) {
        ++nLightJetsPassed; // no MC match; assume its a light flavor jet
        //std::cout << "zero pointer genParticle" << std::endl;
        hMCMatchForPassedJets->Fill(2);
      } else {
        //std::cout << "pid=" << myParticle->pdgId() << std::endl;
        if (std::abs(myParticle->pdgId()) == 5) {
          ++nBJetsPassed;
          hMCMatchForPassedJets->Fill(0);
        } else {
          ++nLightJetsPassed;
          hMCMatchForPassedJets->Fill(1);
        }
      }
    }
    // Calculate scalefactor
    fScaleFactor = fBTaggingScaleFactor.getWeight(nBJetsPassed, nLightJetsPassed, fBJetsFailedPt, fLightJetsFailedPt);
    fScaleFactorRelativeUncertainty = fBTaggingScaleFactor.getRelativeUncertainty(nBJetsPassed, nLightJetsPassed, fBJetsFailedPt, fLightJetsFailedPt);
    fScaleFactorAbsoluteUncertainty = fBTaggingScaleFactor.getAbsoluteUncertainty(nBJetsPassed, nLightJetsPassed, fBJetsFailedPt, fLightJetsFailedPt);
    /*std::cout << "btagSF debug: jets=" << jets.size() << " bjets=" << bjets.size() << " nb=" << nBJetsPassed << ", nbf pT=";
    for (std::vector<double>::iterator it = fBJetsFailedPt.begin(); it != fBJetsFailedPt.end(); ++it) { std::cout << " " << *it; }
    std::cout << " nl=" << nLightJetsPassed << ", nlf pT=";
    for (std::vector<double>::iterator it = fLightJetsFailedPt.begin(); it != fLightJetsFailedPt.end(); ++it) { std::cout << " " << *it; }
    std::cout << " scalefactor= " << fScaleFactor << ", rel.syst.=" << fBTaggingScaleFactor.getRelativeUncertainty(nBJetsPassed, nLightJetsPassed, fBJetsFailedPt, fLightJetsFailedPt) << std::endl;*/

    //std::cout << "bjets=" << nBJets << ", light jets=" << nLightJets << ", scale factor=" << fScaleFactor << std::endl;
  }
  
  void BTagging::Data::fillScaleFactorHistograms() {
    fBTagging->hScaleFactor->Fill(fBTagging->fScaleFactor, fBTagging->fEventWeight.getWeight());
    fBTagging->hBTagAbsoluteUncertainty->Fill(fBTagging->fScaleFactorAbsoluteUncertainty, fBTagging->fEventWeight.getWeight());
    fBTagging->hBTagRelativeUncertainty->Fill(fBTagging->fScaleFactorRelativeUncertainty, fBTagging->fEventWeight.getWeight());
  }

}
