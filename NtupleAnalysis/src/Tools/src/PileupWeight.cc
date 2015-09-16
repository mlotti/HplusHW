#include "Tools/interface/PileupWeight.h"

#include "TFile.h"
#include "TH1.h"

namespace {
  TH1 *calculateWeights(const std::string& data, const std::string& mc) {
    TFile* fIN_data = TFile::Open(data.c_str(), "READ");
    TFile* fIN_mc   = TFile::Open(mc.c_str(), "READ");

    TH1* h_data = dynamic_cast<TH1 *>(fIN_data->Get("pileup"));
    TH1* h_mc   = dynamic_cast<TH1 *>(fIN_mc->Get("pileup"));

    if(!h_data)
      throw std::runtime_error("Did not find TH1 'pileup' from "+data);
    if(!h_mc)
      throw std::runtime_error("Did not find TH1 'pileup' from "+mc);

    h_data->Scale(1.0/h_data->Integral());
    h_mc->Scale(1.0/h_mc->Integral());

    TH1 *weight = dynamic_cast<TH1 *>(h_data->Clone("lumiWeights"));
    weight->Divide(h_mc);

    fIN_data->Close();
    fIN_mc->Close();

    return weight;
  }
}

PileupWeight::PileupWeight(const ParameterSet& pset):
  fEnabled(pset.getParameter<bool>("PileupWeight.enabled")),
  h_weight(fEnabled ?
           calculateWeights(
                            pset.getParameter<std::string>("PileupWeight.data"),
                            pset.getParameter<std::string>("PileupWeight.mc")) :
           nullptr)
{}
PileupWeight::~PileupWeight() {}

double PileupWeight::getWeight(const Event& fEvent){
  if(!fEnabled || fEvent.isData()) return 1;

  int NPU = fEvent.vertexInfo().value();
  int bin = h_weight->GetXaxis()->FindBin( NPU );
  return h_weight->GetBinContent( bin );
}
