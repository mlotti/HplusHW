#include "Framework/interface/TreeWriter.h"
#include "Framework/interface/Exception.h"

#include "EventSelection/interface/TransverseMass.h"

#include <iomanip>
#include <sstream>


TreeWriter::TreeWriter() {

}


TreeWriter::~TreeWriter() {

}


void TreeWriter::book(TDirectory *dir) {

  //create files and book branches

  // get the file dataset name and clean it
  name = dir->GetMotherDir()->GetName();

  name = std::string(name).substr(0,std::string(name).find_last_of("\\/"));

  name = std::string(name).substr(0,std::string(name).find_last_of("\\/"));

  name = std::string(name).substr(std::string(name).find_last_of("/\\")+1);

  b = name.c_str();


  f = new TFile("AnalysisToTree.root","UPDATE");
  t = new TTree(b,b);

  //taus

  Float_t leading_tau_pt;
  Float_t leading_tau_eta;
  Float_t leading_tau_phi;

  Float_t sub_leading_tau_pt;
  Float_t sub_leading_tau_eta;
  Float_t sub_leading_tau_phi;

  //muons

  Float_t leading_muon_pt;
  Float_t leading_muon_eta;
  Float_t leading_muon_phi;

  // electrons

  // jets
//  Float_t leading_tau_pt;
//  Float_t leading_tau_eta;
//  Float_t leading_tau_phi;

  // b-jets
//  Float_t leading_tau_pt;
//  Float_t leading_tau_eta;
//  Float_t leading_tau_phi;

  // MET
  Float_t MET_pt;
  Float_t MET_phi;


  //Transverse mass
  Float_t transverse_mass;


  // branches
  t->Branch("leading_tau_pt",&leading_tau_pt,"leading_tau_pt/F");
  t->Branch("leading_tau_eta",&leading_tau_eta,"leading_tau_eta/F");
  t->Branch("leading_tau_phi",&leading_tau_phi,"leading_tau_phi/F");

  t->Branch("sub_leading_tau_pt",&sub_leading_tau_pt,"sub_leading_tau_pt/F");
  t->Branch("sub_leading_tau_eta",&sub_leading_tau_eta,"sub_leading_tau_eta/F");
  t->Branch("sub_leading_tau_phi",&sub_leading_tau_phi,"sub_leading_tau_phi/F");

  t->Branch("leading_muon_pt",&leading_muon_pt,"leading_muon_pt/F");
  t->Branch("leading_muon_eta",&leading_muon_eta,"leading_muon_eta/F");
  t->Branch("leading_muon_phi",&leading_muon_phi,"leading_muon_phi/F");

  t->Branch("MET_pt",&MET_pt,"MET_pt/F");
  t->Branch("MET_phi",&MET_phi,"MET_phi/F");

  t->Branch("transverse_mass",&transverse_mass,"transverse_mass/F");



//  t->Fill();
  t->Write();

  f->Close();

}


void TreeWriter::initialize() {

  // initialize() used to open already booked file

}

void TreeWriter::write(const Event& event,
                TauSelection::Data tauData,
                ElectronSelection::Data electronData,
                MuonSelection::Data muonData,
                JetSelection::Data jetData,
                BJetSelection::Data bJetData,
                METSelection::Data METData
                ) {

  f = new TFile("AnalysisToTree.root","UPDATE");

  // write information to the root file

  Float_t leading_tau_pt;
  Float_t leading_tau_eta;
  Float_t leading_tau_phi;

  Float_t sub_leading_tau_pt;
  Float_t sub_leading_tau_eta;
  Float_t sub_leading_tau_phi;

  Float_t leading_muon_pt;
  Float_t leading_muon_eta;
  Float_t leading_muon_phi;

  Float_t MET_pt;
  Float_t MET_phi;

  Float_t transverse_mass;


  t = (TTree*)f->Get(b);


  t->SetBranchAddress("leading_tau_pt",&leading_tau_pt);
  t->SetBranchAddress("leading_tau_eta",&leading_tau_eta);
  t->SetBranchAddress("leading_tau_phi",&leading_tau_phi);

  t->SetBranchAddress("sub_leading_tau_pt",&sub_leading_tau_pt);
  t->SetBranchAddress("sub_leading_tau_eta",&sub_leading_tau_eta);
  t->SetBranchAddress("sub_leading_tau_phi",&sub_leading_tau_phi);

  t->SetBranchAddress("leading_muon_pt",&leading_muon_pt);
  t->SetBranchAddress("leading_muon_eta",&leading_muon_eta);
  t->SetBranchAddress("leading_muon_phi",&leading_muon_phi);

  t->SetBranchAddress("MET_pt",&MET_pt);
  t->SetBranchAddress("MET_phi",&MET_phi);

  t->SetBranchAddress("transverse_mass",&transverse_mass);




  leading_tau_pt = tauData.getSelectedTaus()[0].pt();
  leading_tau_eta = tauData.getSelectedTaus()[0].eta();
  leading_tau_phi = tauData.getSelectedTaus()[0].phi();

  sub_leading_tau_pt = tauData.getSelectedTaus()[1].pt();
  sub_leading_tau_eta = tauData.getSelectedTaus()[1].eta();
  sub_leading_tau_phi = tauData.getSelectedTaus()[1].phi();

  leading_muon_pt = muonData.getSelectedMuons()[0].pt();
  leading_muon_eta = muonData.getSelectedMuons()[0].eta();
  leading_muon_phi = muonData.getSelectedMuons()[0].phi();

  MET_pt = METData.getMET().R();
  MET_phi = METData.getMET().Phi();

  transverse_mass = TransverseMass::reconstruct(tauData.getSelectedTaus()[0],tauData.getSelectedTaus()[1],muonData.getSelectedMuons()[0], METData.getMET());




  t->Fill();
  t->Write("",TObject::kOverwrite); //use override to delete previous trees from the file

  f->Close();

}


void TreeWriter::terminate() {
  f->Close();
}
