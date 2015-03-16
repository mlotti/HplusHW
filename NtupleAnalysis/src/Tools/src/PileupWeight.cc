#include "Tools/interface/PileupWeight.h"

PileupWeight::PileupWeight() {
  isdata = true;
  fSet = false;
}
PileupWeight::~PileupWeight() {}

#include "TFile.h"
void PileupWeight::set(std::string path, std::string dataSrc, std::string mcSrc, bool is_data) {
  isdata               = is_data;

  if(!fSet){
  puHistoPath          = path;
  puHistoFileName_data = dataSrc;
  puHistoFileName_mc   = mcSrc;

  TFile* fIN_data = TFile::Open((path+"/PileupHistogramData"+dataSrc+".root").c_str(),"READ");
  TFile* fIN_mc   = TFile::Open((path+"/PileupHistogramMC"+mcSrc+".root").c_str(),"READ");

  TH1F* h_data = (TH1F*)fIN_data->Get("pileup");
  TH1F* h_mc   = (TH1F*)fIN_mc->Get("pileup");

  h_data->Scale(1.0/h_data->Integral());
  h_mc->Scale(1.0/h_mc->Integral());

  h_weight = (TH1F*)h_data->Clone("lumiWeights");
  h_weight->Divide(h_mc);

  fIN_data->Close();
  fIN_mc->Close();

  fSet = true;
  }
}

double PileupWeight::getWeight(Event& fEvent){
  if(!fSet || isdata) return 1;

  int NPU = fEvent.NPU().value();
  int bin = h_weight->GetXaxis()->FindBin( NPU );
  return h_weight->GetBinContent( bin );
}
