#include "HiggsAnalysis/MiniAOD2TTree/interface/MiniAOD2TTreeFilter.h"

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

MiniAOD2TTreeFilter::MiniAOD2TTreeFilter(const edm::ParameterSet& iConfig) :
    outputFileName(iConfig.getParameter<std::string>("OutputFileName")),
    codeVersion(iConfig.getParameter<std::string>("CodeVersion")),
    eventInfoCollections(iConfig.getParameter<edm::ParameterSet>("EventInfo"))
//    trigger(iConfig.getParameter<edm::ParameterSet>("Trigger")),
//    tauCollections(iConfig.getParameter<std::vector<edm::ParameterSet>>("Taus")),
//    electronCollections(iConfig.getParameter<std::vector<edm::ParameterSet>>("Electrons")),
//    muonCollections(iConfig.getParameter<std::vector<edm::ParameterSet>>("Muons")),
//    jetCollections(iConfig.getParameter<std::vector<edm::ParameterSet>>("Jets")),
//    metCollections(iConfig.getParameter<std::vector<edm::ParameterSet>>("METs"))
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

    genParticleDumper = 0;
    if (iConfig.exists("GenParticles")) {
        genParticleCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("GenParticles");
        genParticleDumper = new GenParticleDumper(genParticleCollections);
        genParticleDumper->book(Events);
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
    if (genParticleDumper) accept = accept && genParticleDumper->fill(iEvent,iSetup);
    if(accept) Events->Fill();

    return accept;
}

void MiniAOD2TTreeFilter::reset(){
    if (tauDumper) tauDumper->reset();
    if (electronDumper) electronDumper->reset();
    if (muonDumper) muonDumper->reset();
    if (jetDumper) jetDumper->reset();
    if (metDumper) metDumper->reset();
    if (genParticleDumper) genParticleDumper->reset();
}

#include <time.h>
void MiniAOD2TTreeFilter::endJob(){

// write date
    time_t rawtime;
    time (&rawtime);
    TString dateName = "Generated "+TString(ctime(&rawtime));
    TNamed* dateString = new TNamed("","");
    dateString->Write(dateName);

// write commit string
    TString versionName = codeVersion;
    TNamed* versionString = new TNamed("","");
    versionString->Write(versionName);

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
