#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Math/interface/deltaR.h"

//Standard C++ classes
#include <string>
#include <vector>
#include <iostream>
#include <map>
#include <utility>
#include <ostream>
#include <fstream>
#include <algorithm>
#include <cmath>
#include <memory>
#include <iomanip>

//Root Classes
#include "TH1F.h"
#include "TH2F.h"
#include "TH1I.h"
#include "TFile.h"
#include "TDirectory.h"
#include "TTree.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TString.h"
#include "TMath.h"
#include "TLorentzVector.h"
#include "TLegend.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/BaseDumper.h"

#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"

#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"

double getMiniIsolation_DeltaBeta(edm::Handle<edm::View<pat::PackedCandidate> > pfcands,
				  const reco::Candidate* ptcl,
				  double r_iso_min, double r_iso_max, double kt_scale,
				  bool charged_only);

double getMiniIsolation_EffectiveArea(edm::Handle<edm::View<pat::PackedCandidate> > pfcands,
				      const reco::Candidate* ptcl,
				      double r_iso_min, double r_iso_max, double kt_scale,
				      bool use_pfweight, bool charged_only, double rho);

