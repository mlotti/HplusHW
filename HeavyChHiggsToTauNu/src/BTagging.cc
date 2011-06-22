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

  BTagging::BTagging(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fDiscriminator(iConfig.getUntrackedParameter<std::string>("discriminator")),
    fDiscrCut(iConfig.getUntrackedParameter<double>("discriminatorCut")),
    fMin(iConfig.getUntrackedParameter<uint32_t>("minNumber")),
    fScaleFactorBFlavor(iConfig.getUntrackedParameter<double>("scaleFactorBFlavorValue")),
    fScaleFactorLightFlavor(iConfig.getUntrackedParameter<double>("scaleFactorLightFlavorValue")),
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
    
    // Obtain scale factor variation information
    std::string myVariationModeName = iConfig.getUntrackedParameter<std::string>("variationMode");
    if (myVariationModeName == "normal")
      fVariationMode = kBTagVariationNormal;
    else if (myVariationModeName == "plus")
      fVariationMode = kBTagVariationPlus;
    else if (myVariationModeName == "minus")
      fVariationMode = kBTagVariationMinus;
    else throw cms::Exception("Configuration") << "BTagging: Error: Unknown variationMode! options are 'normal', 'plus', 'minus', you had '" << myVariationModeName << "'.";
    double fScaleFactorBFlavorUncertainty = iConfig.getUntrackedParameter<double>("scaleFactorBFlavorUncertainty");
    double fScaleFactorLightFlavorUncertainty = iConfig.getUntrackedParameter<double>("scaleFactorLightFlavorUncertainty");
    if (fVariationMode == kBTagVariationPlus) {
      fScaleFactorBFlavor += fScaleFactorBFlavorUncertainty;
      fScaleFactorLightFlavor += fScaleFactorLightFlavorUncertainty;
    } else if (fVariationMode == kBTagVariationMinus) {
      fScaleFactorBFlavor -= fScaleFactorBFlavorUncertainty;
      fScaleFactorLightFlavor -= fScaleFactorLightFlavorUncertainty;      
      // Protection against negative values
      if (fScaleFactorBFlavor < 0) fScaleFactorBFlavor = 0;
      if (fScaleFactorLightFlavor < 0) fScaleFactorLightFlavor = 0;
    }
    hScaleFactor = makeTH<TH1F>(myDir, "scaleFactor", "scaleFactor;b-tag/mistag scale factor;N_{events}/0.05", 100, 0., 5.);
    hControlBTagUncertaintyMode = makeTH<TH1F>(myDir, "scaleUncertaintyMode", "scaleUncertaintyMode;;N_{events}", 3, 0., 3.);
    hControlBTagUncertaintyMode->GetXaxis()->SetBinLabel(kBTagVariationNormal+1, "Normal");
    hControlBTagUncertaintyMode->GetXaxis()->SetBinLabel(kBTagVariationMinus+1, "Minus");
    hControlBTagUncertaintyMode->GetXaxis()->SetBinLabel(kBTagVariationPlus+1, "Plus");
    hMCMatchForPassedJets = makeTH<TH1F>(myDir, "MCMatchForPassedJets", "MCMatchForPassedJets;;N_{jets}", 3, 0., 3.);
    hMCMatchForPassedJets->GetXaxis()->SetBinLabel(1, "b jet");
    hMCMatchForPassedJets->GetXaxis()->SetBinLabel(2, "light jet");
    hMCMatchForPassedJets->GetXaxis()->SetBinLabel(3, "no match");
  }

  BTagging::~BTagging() {}

  BTagging::Data BTagging::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets) {
    // Reset variables
    iNBtags = -1;
    fMaxDiscriminatorValue = 0;
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
      applyScaleFactor(fSelectedJets);

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
  
  void BTagging::applyScaleFactor(const edm::PtrVector<pat::Jet>& jets) {
    // Control
    hControlBTagUncertaintyMode->Fill(fVariationMode, fEventWeight.getWeight());
    // Count number of b jets and light jets
    
    int nBJets = 0;
    int nLightJets = 0;
    for (edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      const reco::GenParticle* myParticle = (*iJet).genParton();
      if (myParticle == 0) {
        ++nLightJets; // no MC match; assume its a light flavor jet
        //std::cout << "zero pointer genParticle" << std::endl;
        hMCMatchForPassedJets->Fill(2);
      } else {
        //std::cout << "pid=" << myParticle->pdgId() << std::endl;
        if (std::abs(myParticle->pdgId()) == 5) {
          ++nBJets;
          hMCMatchForPassedJets->Fill(0);
        } else {
          ++nLightJets;
          hMCMatchForPassedJets->Fill(1);
        }
      }
    }
    fScaleFactor = std::pow(fScaleFactorBFlavor, nBJets) * std::pow(fScaleFactorLightFlavor, nLightJets);
    hScaleFactor->Fill(fScaleFactor, fEventWeight.getWeight());
    // Apply scale factor as weight to event
    fEventWeight.multiplyWeight(fScaleFactor);
    //std::cout << "bjets=" << nBJets << ", light jets=" << nLightJets << ", scale factor=" << fScaleFactor << std::endl;
  }
}
