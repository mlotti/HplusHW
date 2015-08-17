#ifndef TauDumper_h
#define TauDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include <string>
#include <vector>

#include "TTree.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/BaseDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/FourVectorDumper.h"

class TauDumper : public BaseDumper {
    public:
	TauDumper(std::vector<edm::ParameterSet>);
	~TauDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
	bool filter();
        
        edm::Handle<edm::View<pat::Tau> > *handle;

        std::vector<double> *lChTrackPt;
        std::vector<double> *lChTrackEta;
        std::vector<double> *lNeutrTrackPt;
        std::vector<double> *lNeutrTrackEta;

	std::vector<short> *nProngs;
        std::vector<short> *pdgTauOrigin;
        
        // Systematics settings (do not reset)
        std::vector<double> TESvariation;
        std::vector<double> TESvariationExtreme;
        // Systematics variations for tau 4-vector
        FourVectorDumper *systTESup;
        FourVectorDumper *systTESdown;
        FourVectorDumper *systExtremeTESup;
        FourVectorDumper *systExtremeTESdown;
        
};
#endif
