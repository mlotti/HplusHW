#include "Tools/interface/TopPtWeight.h"
#include "Framework/interface/Exception.h"

#include "TFile.h"
#include "TH1.h"
#include "TMath.h"

TopPtWeight::TopPtWeight(const ParameterSet& pset):
  fParA(pset.getParameter<double>("parameterA")),
  fParB(pset.getParameter<double>("parameterB"))
{ }

TopPtWeight::~TopPtWeight() {}

double TopPtWeight::getWeight(const Event& fEvent){
  if(fEvent.isData()) return 1.0;

  // Obtain top pt from gen particles
  double weight = 1.0;
  int n = 0;
  for (auto p: fEvent.genparticles().getGenTopCollection()) {
    // Formula is of form exp(A-Bx), see https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
    weight *= TMath::Exp(fParA - fParB*p.pt());
    ++n;
  }
  if (n != 2)
    throw hplus::Exception("runtime") << "TopPtWeight found " << n << " generator top quarks instead of 2!";

  return weight;
}
