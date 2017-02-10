#include "HiggsAnalysis/MiniAOD2TTree/interface/MiniAOD2TTreeFilter.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include <regex>

MiniAOD2TTreeFilter::MiniAOD2TTreeFilter(const edm::ParameterSet& iConfig) :
    //prescaleWeight(iConfig.getParameter<edm::ParameterSet>("PrescaleProvider"), consumesCollector(), this),
    outputFileName(iConfig.getParameter<std::string>("OutputFileName")),
    PUInfoInputFileName(iConfig.getParameter<std::string>("PUInfoInputFileName")),
//    TopPtInputFileName(iConfig.getParameter<std::string>("TopPtInputFileName")),
    codeVersion(iConfig.getParameter<std::string>("CodeVersion")),
    dataVersion(iConfig.getParameter<std::string>("DataVersion")),
    cmEnergy(iConfig.getParameter<int>("CMEnergy")),
    eventInfoCollections(iConfig.getParameter<edm::ParameterSet>("EventInfo"))
{
  
  fOUT = TFile::Open(outputFileName.c_str(),"RECREATE");	
    Events = new TTree("Events","");

    eventInfo = new EventInfoDumper(consumesCollector(), eventInfoCollections);
    eventInfo->book(Events);

    skimDumper = 0;
    if (iConfig.exists("Skim")) {
	skim = iConfig.getParameter<edm::ParameterSet>("Skim");
        skimDumper = new SkimDumper(consumesCollector(), skim);
        skimDumper->book();
    } else {
      std::cout << "Config: SkimDumper ignored, because 'Skim' is missing from config" << std::endl;
    }

    trgDumper = 0;
    if (iConfig.exists("Trigger")) {
        trigger = iConfig.getParameter<edm::ParameterSet>("Trigger");
        trgDumper = new TriggerDumper(consumesCollector(), trigger);
        trgDumper->book(Events);
        hltProcessName = trigger.getParameter<edm::InputTag>("TriggerResults").process();
    } else {
      std::cout << "Config: TriggerDumper ignored, because 'Trigger' is missing from config" << std::endl;
    }
    
    metNoiseFilterDumper = 0;
    if (iConfig.exists("METNoiseFilter")) {
        metNoiseFilter = iConfig.getParameter<edm::ParameterSet>("METNoiseFilter");
        metNoiseFilterDumper = new METNoiseFilterDumper(consumesCollector(), metNoiseFilter);
        metNoiseFilterDumper->book(Events);
    } else {
      std::cout << "Config: METNoiseFilter ignored, because 'METNoiseFilter' is missing from config" << std::endl;
    }

    TopPtInputFileName = "";
    if (iConfig.exists("TopPtInputFileName")) {
       TopPtInputFileName = iConfig.getParameter<std::string>("TopPtInputFileName");
    }

    tauDumper = 0;
    if (iConfig.exists("Taus")) {
	tauCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("Taus");
        tauDumper = new TauDumper(consumesCollector(), tauCollections);
        tauDumper->book(Events);
    } else {
      std::cout << "Config: TauDumper ignored, because 'Skim' is missing from config" << std::endl;
    }

    electronDumper = 0;
    if (iConfig.exists("Electrons")) {
	electronCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("Electrons");
        electronDumper = new ElectronDumper(consumesCollector(), electronCollections);
        electronDumper->book(Events);
    } else {
      std::cout << "Config: ElectronDumper ignored, because 'Electrons' is missing from config" << std::endl;
    }

    muonDumper = 0;
    if (iConfig.exists("Muons")) {
	muonCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("Muons");
        muonDumper = new MuonDumper(consumesCollector(), muonCollections, eventInfoCollections.getParameter<edm::InputTag>("OfflinePrimaryVertexSrc"));
        muonDumper->book(Events);
    }

    jetDumper = 0;
    if (iConfig.exists("Jets")) {
	jetCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("Jets");
        jetDumper = new JetDumper(consumesCollector(), jetCollections);
        jetDumper->book(Events);
    } else {
      std::cout << "Config: JetDumper ignored, because 'Jets' is missing from config" << std::endl;
    }

    topDumper = 0;
    if (iConfig.exists("Top")) {
        topCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("Top");
        topDumper = new TopDumper(consumesCollector(), topCollections);
        topDumper->book(Events);
    } else {
      std::cout << "Config: TopDumper ignored, because 'Top' is missing from config" << std::endl;
    }

    metDumper = 0;
    if (iConfig.exists("METs")) {
	metCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("METs");
        metDumper = new METDumper(consumesCollector(), metCollections, this->isMC());
        metDumper->book(Events);
    } else {
      std::cout << "Config: METDumper ignored, because 'METs' is missing from config" << std::endl;
    }

    trackDumper = 0;
    if (iConfig.exists("Tracks")) {
        trackCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("Tracks");
        trackDumper = new TrackDumper(consumesCollector(), trackCollections);
        trackDumper->book(Events);
    } else {
      std::cout << "Config: TrackDumper ignored, because 'Tracks' is missing from config" << std::endl;       
    }

    genMetDumper = 0;
    genWeightDumper = 0;
    genParticleDumper = 0;
    genJetDumper = 0;

    if(this->isMC()){
      if (iConfig.exists("GenMETs")) {
	genMetCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("GenMETs");
        genMetDumper = new GenMETDumper(consumesCollector(), genMetCollections);
        genMetDumper->book(Events);
      } else {
        std::cout << "Config: GenMETDumper ignored, because 'GenMETs' is missing from config" << std::endl;
      }

      if (iConfig.exists("GenWeights")) {
	genWeightCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("GenWeights");
        genWeightDumper = new GenWeightDumper(consumesCollector(), genWeightCollections);
        genWeightDumper->book(Events);
      } else {
        std::cout << "Config: GenWeightDumper ignored, because 'GenWeights' is missing from config" << std::endl;
      }

      if (iConfig.exists("GenParticles")) {
        genParticleCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("GenParticles");
        genParticleDumper = new GenParticleDumper(consumesCollector(), genParticleCollections);
        genParticleDumper->book(Events);
      } else {
        std::cout << "Config: GenParticleDumper ignored, because 'GenParticles' is missing from config" << std::endl;
      }

      if (iConfig.exists("GenJets")) {
        genJetCollections = iConfig.getParameter<std::vector<edm::ParameterSet>>("GenJets");
        genJetDumper = new GenJetDumper(consumesCollector(), genJetCollections);
        genJetDumper->book(Events);
      } else {
        std::cout << "Config: GenJetDumper ignored, because 'GenJets' is missing from config" << std::endl;
      }
    }
}

MiniAOD2TTreeFilter::~MiniAOD2TTreeFilter() {
    system("ls -lt");
}

void MiniAOD2TTreeFilter::beginRun(edm::Run const & iRun, edm::EventSetup const& iSetup) {
    bool changed = true;
    hltConfig.init(iRun,iSetup,hltProcessName,changed);
    if(trgDumper != 0) trgDumper->book(iRun,hltConfig);
}

void MiniAOD2TTreeFilter::beginJob(){
}   

bool MiniAOD2TTreeFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup){
    reset();

    eventInfo->fill(iEvent,iSetup);

    bool accept = true;

    if (trgDumper) accept = accept && trgDumper->fill(iEvent,iSetup);
    if (metNoiseFilterDumper) accept = accept && metNoiseFilterDumper->fill(iEvent,iSetup);
    if (tauDumper) {
	accept = accept && tauDumper->fill(iEvent,iSetup);
        if (trgDumper) trgDumper->triggerMatch(trigger::TriggerTau,tauDumper->selected());
    }
    if (electronDumper) accept = accept && electronDumper->fill(iEvent,iSetup);
    if (muonDumper) {
	accept = accept && muonDumper->fill(iEvent,iSetup);
	if (trgDumper) trgDumper->triggerMatch(trigger::TriggerMuon,muonDumper->selected());
    }
    if (jetDumper) accept = accept && jetDumper->fill(iEvent,iSetup);
    if (topDumper) accept = accept && topDumper->fill(iEvent,iSetup);
    if (metDumper) accept = accept && metDumper->fill(iEvent,iSetup);
    if (genMetDumper) accept = accept && genMetDumper->fill(iEvent,iSetup);
    if (genWeightDumper) accept = accept && genWeightDumper->fill(iEvent,iSetup);
    if (trackDumper) accept = accept && trackDumper->fill(iEvent,iSetup);
    if (genParticleDumper) accept = accept && genParticleDumper->fill(iEvent,iSetup);
    if (genJetDumper) accept = accept && genJetDumper->fill(iEvent,iSetup);
    if(accept) Events->Fill();

    return accept;
}

void MiniAOD2TTreeFilter::reset(){
    if (skimDumper) skimDumper->reset();
    if (trgDumper) trgDumper->reset();
    if (metNoiseFilterDumper) metNoiseFilterDumper->reset();
    if (tauDumper) tauDumper->reset();
    if (electronDumper) electronDumper->reset();
    if (muonDumper) muonDumper->reset();
    if (jetDumper) jetDumper->reset();
    if (topDumper) topDumper->reset();
    if (metDumper) metDumper->reset();
    if (genMetDumper) genMetDumper->reset();
    if (genWeightDumper) genWeightDumper->reset();
    if (trackDumper) trackDumper->reset();
    if (genParticleDumper) genParticleDumper->reset();
    if (genJetDumper) genJetDumper->reset();
}

#include <time.h>
#include "TH1F.h"
void MiniAOD2TTreeFilter::endJob(){

    fOUT->cd();

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

    if(skimDumper){
      TH1F* skimCounter = skimDumper->getCounter();
      skimCounter->Write();
    }

    fOUT->cd();

// write TTree
    Events->Write();

    std::cout << std::endl << "List of branches:" << std::endl;
    TObjArray* branches = Events->GetListOfBranches();
    for(int i = 0; i < branches->GetEntries(); ++i){
      int hltCounterAll    = 0;
      int hltCounterPassed = 0;
      if (trgDumper) {
	std::pair<int,int> hltCounters = trgDumper->counters(branches->At(i)->GetName());
	if(hltCounters.first > 0) {
	  hltCounterAll    = hltCounters.first;
	  hltCounterPassed = hltCounters.second;
	}
      }
      if(hltCounterAll > 0){
	std::string name(branches->At(i)->GetName());
	while(name.length() < 70) name += " ";
	
	std::cout << "    " << name << " " << hltCounterAll << " " << hltCounterPassed << std::endl;
      }else{
	std::cout << "    " << branches->At(i)->GetName() << std::endl;
      }
    }
    std::cout << "Number of events saved " << Events->GetEntries() << std::endl << std::endl;

// copy PU histogram from separate file (makes merging of root files so much easier)
    if (PUInfoInputFileName.size()) {
      TFile* fPU = TFile::Open(PUInfoInputFileName.c_str());
      if (fPU) {
        // File open is successful
        TH1F* hPU = dynamic_cast<TH1F*>(fPU->Get("pileup"));
        if (hPU) {
          // Histogram exists
          TH1F* hPUclone = dynamic_cast<TH1F*>(hPU->Clone());
          hPUclone->SetDirectory(fOUT);
	  infodir->cd();
          hPUclone->Write();
        }
      }
      fPU->Close();
    }

// copy top pt weight histogram from separate file (makes merging of root files so much easier)
    if (TopPtInputFileName.size()) {
      TFile* fTopPt = TFile::Open(TopPtInputFileName.c_str());
      if (fTopPt) {
        // File open is successful
        TH1F* hTopPt = dynamic_cast<TH1F*>(fTopPt->Get("topPtWeightAllEvents"));
        if (hTopPt) {
          // Histogram exists
          TH1F* hTopPtClone = dynamic_cast<TH1F*>(hTopPt->Clone());
          hTopPtClone->SetDirectory(fOUT);
          infodir->cd();
          hTopPtClone->Write();
        }
      }
      fTopPt->Close();
    }    
    
// close output file
    fOUT->Close();
}

void MiniAOD2TTreeFilter::endLuminosityBlock(const edm::LuminosityBlock & iLumi, const edm::EventSetup & iSetup) {
    if(skimDumper) skimDumper->fill(iLumi,iSetup);
}

bool MiniAOD2TTreeFilter::isMC(){
    std::regex data_re("data");
    if(std::regex_search(dataVersion, data_re)) return false;
    return true;
}          
DEFINE_FWK_MODULE(MiniAOD2TTreeFilter);
