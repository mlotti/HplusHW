#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
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
    fTaggedCount(eventCounter.addCounter("b-tagging")),
    fAllSubCount(eventCounter.addSubCounter("b-tagging", "all jets")),
    fTaggedSubCount(eventCounter.addSubCounter("b-tagging", "tagged")),
    fTaggedEtaCutSubCount(eventCounter.addSubCounter("b-tagging", "eta  cut")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    hDiscr = fs->make<TH1F>("jet_bdiscriminator", ("b discriminator "+fDiscriminator).c_str(), 80, -10, 10);
    hPt = fs->make<TH1F>("bjet_pt", "bjet_pt", 100, 0., 200.);
    hPt1 = fs->make<TH1F>("bjet1_pt", "bjet1_pt", 100, 0., 200.);
    hPt2 = fs->make<TH1F>("bjet2_pt", "bjet2_pt", 100, 0., 200.);
    hEta = fs->make<TH1F>("bjet_eta", "bjet_pt", 60, -3., 3.);
    hEta1 = fs->make<TH1F>("bjet1_eta", "bjet1_pt", 60, -3., 3.);
    hEta2 = fs->make<TH1F>("bjet2_eta", "bjet2_pt", 60, -3., 3.);
    hNumberOfBtaggedJets = fs->make<TH1F>("NumberOfBtaggedJets", "NumberOfBtaggedJets", 15, 0., 15.);
  }

  BTagging::~BTagging() {}

  BTagging::Data BTagging::analyze(const edm::PtrVector<pat::Jet>& jets) {
    // Reset variables
    iNBtags = -1;
    bool passEvent = false;

    fSelectedJets.clear();
    fSelectedJets.reserve(jets.size());

    size_t passed = 0;
   
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;

      increment(fAllSubCount);


      float discr = iJet->bDiscriminator(fDiscriminator);
      hDiscr->Fill(discr);
      if(!(discr > fDiscrCut)) continue;
      increment(fTaggedSubCount);
      //      ++passed;

      hPt->Fill(iJet->pt());
      hEta->Fill(iJet->eta());

      if(fabs(iJet->eta()) > fEtaCut ) continue;
      increment(fTaggedEtaCutSubCount);
      ++passed;

      fSelectedJets.push_back(iJet);
    }


    hNumberOfBtaggedJets->Fill(fSelectedJets.size());
    iNBtags = fSelectedJets.size();

    ////////////////////////////////
    if( passed > 0) {
      hPt1->Fill(fSelectedJets[0]->pt());
      hEta1->Fill(fSelectedJets[0]->eta());
    }
    if( passed > 1) {
      hPt2->Fill(fSelectedJets[1]->pt());
      hEta2->Fill(fSelectedJets[1]->eta());
    }
       // plot deltaPhi(bjet,tau jet)
    //      double deltaPhi = -999;    
	//      if ( met->et()>  fMetCut) {
      //	  deltaPhi = DeltaPhi::reconstruct(*(iJet), *(met));
      //	  hDeltaPhiJetMet->Fill(deltaPhi*57.3);
      //      }

    passEvent = true;
    if(passed < fMin) passEvent = false;
    increment(fTaggedCount);

    return Data(this, passEvent);
  }
}
