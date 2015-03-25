#include "HiggsAnalysis/MiniAOD2TTree/interface/MiniAOD2TTreeFilter.h"

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

MiniAOD2TTreeFilter::MiniAOD2TTreeFilter(const edm::ParameterSet& iConfig) :
    outputFileName(iConfig.getParameter<std::string>("OutputFileName")),
    codeVersion(iConfig.getParameter<std::string>("CodeVersion")),
    dataVersion(iConfig.getParameter<std::string>("DataVersion")),
    cmEnergy(iConfig.getParameter<int>("CMEnergy")),
    eventInfoCollections(iConfig.getParameter<edm::ParameterSet>("EventInfo"))
{
    fOUT = TFile::Open(outputFileName.c_str(),"RECREATE");	
    Events = new TTree("Events","");

    eventInfo = new EventInfoDumper(eventInfoCollections);
    eventInfo->book(Events);

    trgDumper = 0;
    if (iConfig.exists("Trigger")) {
	trigger = iConfig.getParameter<edm::ParameterSet>("Trigger");
        trgDumper = new TriggerDumper(trigger);
        trgDumper->book(Events);
    }

    tauDumper = 0;
    if (iConfig.exists("Taus")) {
	tauCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("Taus");
        tauDumper = new TauDumper(tauCollections);
        tauDumper->book(Events);
    }

    electronDumper = 0;
    if (iConfig.exists("Electrons")) {
	electronCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("Electrons");
        electronDumper = new ElectronDumper(electronCollections);
        electronDumper->book(Events);
    }

    muonDumper = 0;
    if (iConfig.exists("Muons")) {
	muonCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("Muons");
        muonDumper = new MuonDumper(muonCollections);
        muonDumper->book(Events);
    }

    jetDumper = 0;
    if (iConfig.exists("Jets")) {
	jetCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("Jets");
        jetDumper = new JetDumper(jetCollections);
        jetDumper->book(Events);
    }

    metDumper = 0;
    if (iConfig.exists("METs")) {
	metCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("METs");
        metDumper = new METDumper(metCollections);
        metDumper->book(Events);
    }

    trackDumper = 0;
    if (iConfig.exists("Tracks")) {
        trackCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("Tracks");
        trackDumper = new TrackDumper(trackCollections);
        trackDumper->book(Events);
    }

    genParticleDumper = 0;
    if (iConfig.exists("GenParticles")) {
        genParticleCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("GenParticles");
        genParticleDumper = new GenParticleDumper(genParticleCollections);
        genParticleDumper->book(Events);
    }
    genJetDumper = 0;
    if (iConfig.exists("GenJets")) {
        genJetCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("GenJets");
        genJetDumper = new GenJetDumper(genJetCollections);
        genJetDumper->book(Events);
    }
}

MiniAOD2TTreeFilter::~MiniAOD2TTreeFilter() {
}

void MiniAOD2TTreeFilter::beginJob(){
}   

bool MiniAOD2TTreeFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup){
    reset();

    eventInfo->fill(iEvent,iSetup);

    bool accept = true;
    if (trgDumper) accept = accept && trgDumper->fill(iEvent,iSetup);
    if (tauDumper) accept = accept && tauDumper->fill(iEvent,iSetup);
    if (electronDumper) accept = accept && electronDumper->fill(iEvent,iSetup);
    if (muonDumper) accept = accept && muonDumper->fill(iEvent,iSetup);
    if (jetDumper) accept = accept && jetDumper->fill(iEvent,iSetup);
    if (metDumper) accept = accept && metDumper->fill(iEvent,iSetup);
    if (trackDumper) accept = accept && trackDumper->fill(iEvent,iSetup);
    if (genParticleDumper) accept = accept && genParticleDumper->fill(iEvent,iSetup);
    if (genJetDumper) accept = accept && genJetDumper->fill(iEvent,iSetup);
    if(accept) Events->Fill();

    return accept;
}

void MiniAOD2TTreeFilter::reset(){
    if (trgDumper) trgDumper->reset();
    if (tauDumper) tauDumper->reset();
    if (electronDumper) electronDumper->reset();
    if (muonDumper) muonDumper->reset();
    if (jetDumper) jetDumper->reset();
    if (metDumper) metDumper->reset();
    if (trackDumper) trackDumper->reset();
    if (genParticleDumper) genParticleDumper->reset();
    if (genJetDumper) genJetDumper->reset();
}

#include <time.h>
#include "TH1F.h"
void MiniAOD2TTreeFilter::endJob(){

// write date
    time_t rawtime;
    time (&rawtime);
    TString dateName = "Generated "+TString(ctime(&rawtime));
    TNamed* dateString = new TNamed("","");
    dateString->Write(dateName);

// write commit string
    TString versionName = "Commit "+codeVersion;
    TNamed* versionString = new TNamed("","");
    versionString->Write(versionName);

// write config info
    TDirectory* infodir = fOUT->mkdir("configInfo");
    infodir->cd();

    TNamed* dv = new TNamed("dataVersion",dataVersion);
    dv->Write();

    int nbins = 2;
    TH1F* cfgInfo = new TH1F("configinfo","",nbins,0,nbins);
    cfgInfo->SetBinContent(1,1.0);
    cfgInfo->GetXaxis()->SetBinLabel(1,"control");
    cfgInfo->SetBinContent(2,cmEnergy);
    cfgInfo->GetXaxis()->SetBinLabel(2,"energy");
    cfgInfo->Write();

    fOUT->cd();

// write TTree
    Events->Write();

    std::cout << std::endl << "List of branches:" << std::endl;
    TObjArray* branches = Events->GetListOfBranches();
    for(int i = 0; i < branches->GetEntries(); ++i){
	std::cout << "    " << branches->At(i)->GetName() << std::endl;
    }
    std::cout << "Number of events saved " << Events->GetEntries() << std::endl << std::endl;


    fOUT->Close();
}
          
DEFINE_FWK_MODULE(MiniAOD2TTreeFilter);
