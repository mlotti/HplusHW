#ifndef MuonAnalyzer_H
#define MuonAnalyzer_H

/** \class MuonAnalyzer
 *
 *
 *  This class is for storing offline muon for Z mass reco
 *
 *  \author Sami Lehti  -  HIP Helsinki
 *
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Math/interface/LorentzVector.h"

namespace reco {
  class Candidate;
}

class TTree;

class MuonAnalyzer {

    public:
	typedef math::XYZTLorentzVector LorentzVector;

        MuonAnalyzer();
        ~MuonAnalyzer();

        void Setup(const edm::ParameterSet&,TTree *l1tree);
        void fill(const edm::Event&, const edm::EventSetup&, const LorentzVector& tau);
        void fill(const edm::Event&, const edm::EventSetup&, const reco::Candidate& tau);

   private:

        // Input parameters
	edm::InputTag MuonSource;
        edm::InputTag muTauPairSource;

        // Output variables
	std::vector<float> muonPt,muonEta,muonPhi;
        std::vector<float> muonIso03SumPt, muonIso03EmEt, muonIso03HadEt;
        std::vector<float> muonPFIsoCharged, muonPFIsoNeutral, muonPFIsoGamma;
	std::vector<bool>  muonIsGlobalMuon;
//        float muTauInvMass;
	int nMuons;
};
#endif
