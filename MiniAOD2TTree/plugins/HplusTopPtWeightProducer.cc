// -*- C++ -*-
// Description: An event counter that stores the sum of positive and negative events counts into the lumi block
// Modified from CommonTools/​UtilAlgos/​plugins/​EventCountProducer.cc

#include <memory>
#include <vector>
#include <algorithm>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/Common/interface/Handle.h"

#include "HiggsAnalysis/MiniAOD2TTree/interface/GenParticleTools.h"

#include "TFile.h"
#include "TMath.h"
#include "TH1F.h"


class HplusTopPtWeightProducer : public edm::one::EDProducer<edm::one::SharedResources> {
public:
  explicit HplusTopPtWeightProducer(const edm::ParameterSet&);
  ~HplusTopPtWeightProducer();

private:
  virtual void produce(edm::Event &, const edm::EventSetup&) override;
  virtual void beginJob();
  virtual void endJob();
  
  //virtual void beginLuminosityBlock(const edm::LuminosityBlock &, const edm::EventSetup&) override;
  //virtual void endLuminosityBlock(edm::LuminosityBlock const&, const edm::EventSetup&) override;
  //virtual void endLuminosityBlockProduce(edm::LuminosityBlock &, const edm::EventSetup&) override;
  
  // ----------member data ---------------------------
  edm::EDGetTokenT<GenEventInfoProduct> eventInfoToken;
  edm::EDGetTokenT<reco::GenParticleCollection> genParticleToken;
  const std::string sFilename;
  const double fParA;
  const double fParB;
  
  TH1F* hTopPtWeightAllEvents;
};

using namespace edm;
using namespace std;

HplusTopPtWeightProducer::HplusTopPtWeightProducer(const edm::ParameterSet& iConfig):
  eventInfoToken(consumes<GenEventInfoProduct>(edm::InputTag("generator"))),
  genParticleToken(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticleSrc"))),
  sFilename(iConfig.getParameter<std::string>("OutputFileName")),
  fParA(iConfig.getParameter<double>("parameterA")),
  fParB(iConfig.getParameter<double>("parameterB"))
{
  produces<double>();
  hTopPtWeightAllEvents = new TH1F("topPtWeightAllEvents","topPtWeightAllEvents",3,0,3);
  hTopPtWeightAllEvents->GetXaxis()->SetBinLabel(1, "control");
  hTopPtWeightAllEvents->GetXaxis()->SetBinLabel(2, "NAllEventsTopPtReweighted");
  hTopPtWeightAllEvents->GetXaxis()->SetBinLabel(3, "NAllEventsTopPtReweightedPlus");
}

HplusTopPtWeightProducer::~HplusTopPtWeightProducer(){ }

void HplusTopPtWeightProducer::beginJob() {
  hTopPtWeightAllEvents->Fill(0.5, 1);
}

void HplusTopPtWeightProducer::endJob() {
  if(hTopPtWeightAllEvents->GetEntries() > 0){
    TFile* fOUT = TFile::Open(sFilename.c_str(),"RECREATE");
    fOUT->cd();
    hTopPtWeightAllEvents->Write();
    fOUT->Close();
  }  
}

void HplusTopPtWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (iEvent.isRealData()) {
    return;
  }
  
  // For MC, read gen particles list
  edm::Handle<reco::GenParticleCollection> handle;
  iEvent.getByToken(genParticleToken, handle);
  if (handle.isValid()) {
    // For MC, read gen weight
    edm::Handle<GenEventInfoProduct> weightHandle;
    iEvent.getByToken(eventInfoToken, weightHandle);
    if (weightHandle.isValid()) {
      double sign = 1.0;
      if (weightHandle->weight() < 0.0) {
        sign = -1.0;
      }
      double weight = 1.0;
      std::vector<const reco::Candidate*> tops = GenParticleTools::findParticles(handle, 6);
      for (auto& p: tops) {
        double pt = p->pt();
        // Top pt weight is valid only up to 400 GeV
        if (pt > 400.0) {
          pt = 400.0;
        }
        weight *= TMath::Exp(fParA - fParB*pt);
      }
      hTopPtWeightAllEvents->SetBinContent(2, hTopPtWeightAllEvents->GetBinContent(2) + sign*weight);
      hTopPtWeightAllEvents->SetBinContent(2, hTopPtWeightAllEvents->GetBinContent(3) + sign*weight*weight);
      std::auto_ptr<double> w(new double);
      *w = weight*sign;
      iEvent.put(w);
    }
  }
}

//define this as a plug-in
DEFINE_FWK_MODULE(HplusTopPtWeightProducer);
