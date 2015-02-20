#include "test_createTree.h"

#include <vector>
#include <algorithm>

std::unique_ptr<TTree> createSimpleTree() {
  auto tree = std::unique_ptr<TTree>(new TTree("Events", "Events"));

  int b_event;
  unsigned int b_lumi;
  unsigned long long b_run;
  std::vector<int> b_num1;
  std::vector<float> b_num2;
  tree->Branch("event", &b_event);
  tree->Branch("lumi", &b_lumi);
  tree->Branch("run", &b_run);
  tree->Branch("num1", &b_num1);
  tree->Branch("num2", &b_num2);

  b_event = 1;
  b_lumi = 2;
  b_run = 3;
  b_num1 = std::vector<int>{1,2,3};
  b_num2 = std::vector<float>{0.1f, 0.2f, 0.3f};
  tree->Fill();

  b_event = 2;
  b_num1 = std::vector<int>{4};
  b_num2 = std::vector<float>{10.f, 20.f, 30.f, 40.f, 50.f};
  tree->Fill();

  b_event = 3;
  b_num1 = std::vector<int>{-10, 0, 10, 100, 1000};
  b_num2 = std::vector<float>{-1e10f, -5e5f, 1.f};
  tree->Fill();

  return tree;
}

namespace {
  template <typename T>
  auto esScale(const std::vector<T>& input, T scale) -> std::vector<T> {
    std::vector<T> ret;
    ret.reserve(input.size());
    std::transform(input.begin(), input.end(), std::back_inserter(ret), [=](T value) {
        return value*scale;
      });
    return ret;
  }
}

std::unique_ptr<TTree> createRealisticTree(const std::string& tauPrefix) {
  auto tree = std::unique_ptr<TTree>(new TTree("Events", "Events"));

  unsigned int run;           tree->Branch("run",   &run);
  unsigned int lumi;          tree->Branch("lumi",  &lumi);
  unsigned long long event;   tree->Branch("event", &event);
  std::vector<float> tau_pt;  tree->Branch((tauPrefix+"_pt").c_str(),  &tau_pt);
  std::vector<float> tau_eta; tree->Branch((tauPrefix+"_eta").c_str(), &tau_eta);
  std::vector<float> tau_phi; tree->Branch((tauPrefix+"_phi").c_str(), &tau_phi);
  std::vector<float> tau_e;   tree->Branch((tauPrefix+"_e").c_str(),   &tau_e);
  std::vector<bool> tau_decayModeFinding;
  tree->Branch((tauPrefix+"_decayModeFinding").c_str(), &tau_decayModeFinding);

  std::vector<float> tau_pt_esup; tree->Branch((tauPrefix+"_pt_systVarTESUp").c_str(),  &tau_pt_esup);
  std::vector<float> tau_e_esup;  tree->Branch((tauPrefix+"_e_systVarTESUp").c_str(),   &tau_e_esup);


  double MET_et;  tree->Branch("MET_Type1_et", &MET_et);
  double MET_phi; tree->Branch("MET_Type1_phi", &MET_phi);

  double MET_et_tesup;  tree->Branch("MET_Type1_et_systVarTESUp", &MET_et_tesup);
  double MET_phi_tesup; tree->Branch("MET_Type1_phi_systVarTESUp", &MET_phi_tesup);

  constexpr float TAU_ESUP = 1.03f;

  run = 1;
  lumi = 1;
  event = 1;
  tau_pt = std::vector<float>{50.f, 20.f, 10.f, 25.f};
  tau_eta = std::vector<float>{0.1f, -2.3f, 1.7f, 0.3f};
  tau_phi = std::vector<float>{-2.9f, -0.5f, 1.f, 0.3f};
  tau_e = std::vector<float>{60.f, 25.f, 40.f, 30.f};
  tau_pt_esup = esScale(tau_pt, TAU_ESUP);
  tau_e_esup = esScale(tau_e, TAU_ESUP);
  tau_decayModeFinding = std::vector<bool>{true, false, true, false};
  MET_et = 50;
  MET_phi = 0.1;
  MET_et_tesup = 60.0;
  MET_phi_tesup = 0.7;
  tree->Fill();

  event = 2;
  tau_pt = std::vector<float>{20.f};
  tau_eta = std::vector<float>{0.9f,};
  tau_phi = std::vector<float>{3.1f};
  tau_e = std::vector<float>{25.f};
  tau_pt_esup = esScale(tau_pt, TAU_ESUP);
  tau_e_esup = esScale(tau_e, TAU_ESUP);
  tau_decayModeFinding = std::vector<bool>{true};
  MET_et = 45.0;
  MET_phi = 3.1;
  MET_et_tesup = 30.0;
  MET_phi_tesup = -2.6;
  tree->Fill();

  lumi = 2;
  event = 3;
  tau_pt = std::vector<float>{15.f, 17.f};
  tau_eta = std::vector<float>{-2.0f, 1.5f};
  tau_phi = std::vector<float>{1.3f, -1.2f};
  tau_e = std::vector<float>{17.f, 20.f};
  tau_pt_esup = esScale(tau_pt, TAU_ESUP);
  tau_e_esup = esScale(tau_e, TAU_ESUP);
  tau_decayModeFinding = std::vector<bool>{false, false};
  MET_et = 200.0;
  MET_phi = -2.4;
  MET_et_tesup = 150.0;
  MET_phi_tesup = 1.5;
  tree->Fill();

  return tree;
}
