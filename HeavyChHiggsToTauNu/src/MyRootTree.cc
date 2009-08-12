#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyRootTree.h"
#include <iostream>

using namespace std;

MyRootTree::MyRootTree(const char *fileName){
  if(fileName)
    rootFile = TFile::Open(fileName, "RECREATE");
  else
    rootFile = TFile::Open("analysis.root", "RECREATE");
  rootFile->SetCompressionLevel(1);

  rootTree = new TTree("rootTree","events");
  rootTree->SetAutoSave(1000000000);
  myEvent  = new MyEvent(); 
  int bufsize = 256000;
  int split   = 1;
  rootTree->Branch("MyEvent","MyEvent",&myEvent,bufsize,split);

}

MyRootTree::~MyRootTree(){

  char* ENV_IBG = getenv("IBG");
  if( ENV_IBG != NULL){
    cout << " IBG set to " << ENV_IBG 
         << ", storing to root file " << endl;
    IBG = atoi(ENV_IBG);
  }else{
//    cout << " IBG not used, set IBG using environmental variable IBG if needed " << endl;
    IBG = 0;
  }

  char* ENV_RUN = getenv("RUN");
  if( ENV_RUN != NULL){
    cout << " RUN set to " << ENV_RUN
         << ", storing to root file " << endl;
    RUN = atoi(ENV_RUN);
  }else{
//    cout << " RUN not used, set RUN using environmental variable RUN if needed " << endl;
    RUN = 1;
  }

  char* ENV_CNOR = getenv("CNOR");
  if( ENV_CNOR != NULL){
    cout << " CNOR set to " << ENV_CNOR
         << ", storing to root file " << endl;
    CNOR = atof(ENV_CNOR);
  }else{
//    cout << " CNOR not used, set CNOR using environmental variable CNOR if needed " << endl;
    CNOR = 1;
  }


  char* ENV_cross_section = getenv("CROSS_SECTION");
  if( ENV_cross_section != NULL){
    cout << " cross_section set to " << ENV_cross_section 
         << ", storing to root file " << endl;
    cross_section = atof(ENV_cross_section);
  }else{
//    cout << " cross_section not used, set cross_section" 
//         << " using environmental variable CROSS_SECTION if needed " << endl;
    cross_section = 0;
  }

  // storing event info into a histogram
  int binSize = 4 + acceptances.size();
  eventInfo = new TH1F("eventInfo","eventInfo",binSize,0,binSize);
	  eventInfo->SetBinContent(1,IBG);
	  eventInfo->GetXaxis()->SetBinLabel(1,"label");

	  eventInfo->SetBinContent(2,RUN);
	  eventInfo->GetXaxis()->SetBinLabel(2,"run");

	  eventInfo->SetBinContent(3,CNOR);
	  eventInfo->GetXaxis()->SetBinLabel(3,"preSeleEff");

	  eventInfo->SetBinContent(4,cross_section);
	  eventInfo->GetXaxis()->SetBinLabel(4,"cross_section");

  int i = 5;
  for(vector<string>::const_iterator iName = names.begin();
                                     iName!= names.end(); iName++){
    eventInfo->SetBinContent(i,acceptances[*iName]);
    eventInfo->GetXaxis()->SetBinLabel(i,(*iName).c_str());
    i++;
  }

  rootFile->cd();
  eventInfo->Write();
  rootTree->Write();
  rootFile->ls();
  rootFile->Close();
  delete rootFile;
}

void MyRootTree::fillTree(MyEvent* event){

  myEvent = event;

  rootFile->cd();

////  rootTree->Fill();
}

void MyRootTree::setAcceptance(string name,double value){
  names.push_back(name);
  acceptances[name] = value;
}

