#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauMETTriggerAnalysis.h"

#include "DataFormats/Common/interface/Handle.h"
using namespace edm;
using namespace reco;
//using namespace l1extra;

#include "DataFormats/L1Trigger/interface/L1ParticleMapFwd.h"

/*
#include "SimDataFormats/HepMCProduct/interface/HepMCProduct.h"
#include "HepMC/GenEvent.h"
using namespace HepMC;

#include "DataFormats/TauReco/interface/CaloTau.h"
#include "DataFormats/TauReco/interface/PFTau.h"

#include "RecoTauTag/TauTagTools/interface/CaloTauElementsOperators.h"
#include "RecoTauTag/TauTagTools/interface/PFTauElementsOperators.h"
*/

#include "DataFormats/L1Trigger/interface/L1JetParticle.h"

#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/BTauReco/interface/EMIsolatedTauTagInfo.h"
#include "DataFormats/BTauReco/interface/IsolatedTauTagInfo.h"

//#include "DataFormats/TauReco/interface/L2TauInfoAssociation.h"
//#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"

#include "TLorentzVector.h"

#include <iostream>
//using namespace std;

//double myDeltaR(double,double,double,double);
//double phiDis(double,double);

vector<TLorentzVector> visibleTaus(const edm::Event&,int);

TauMETTriggerAnalysis::TauMETTriggerAnalysis(){
        init();
}

TauMETTriggerAnalysis::TauMETTriggerAnalysis(MyRootTree* myRootTree){
        init();
        userRootTree = myRootTree;
}

void TauMETTriggerAnalysis::init(){

        taumetRootFile = new TFile("trigger.root","RECREATE");

        h_L1TauEt 	= new TH1F("h_L1TauEt","",100,0,200);
        h_L3TauEt 	= (TH1F*)h_L1TauEt->Clone("h_L3TauEt");
	h_MET		= new TH1F("h_MET","",100,0,200);

	allEvents 	     = 0;
	l1Events	     = 0;
	l1EventsTrue	     = 0;
	l1EventsFalse	     = 0;
	metEvents	     = 0;
	metEventsTrue        = 0;
        l2EventsReco         = 0;
        l2EventsRecoTrue     = 0;
        l2EventsRecoFalse    = 0;
        l2EventsEcalIso      = 0;
        l2EventsEcalIsoTrue  = 0;
        l2EventsEcalIsoFalse = 0;
        l25Events            = 0;
        l25EventsTrue        = 0;
        l25EventsFalse       = 0;
        l3Events             = 0;
        l3EventsTrue         = 0;
        l3EventsFalse        = 0;

	l1truetau = false;
}

TauMETTriggerAnalysis::~TauMETTriggerAnalysis(){

	if(allEvents > 0){

          	taumetRootFile->cd();
          	taumetRootFile->Write();
          	taumetRootFile->Close();


		cout << "            Passed true fakes" << endl;
		cout << "all events    " << allEvents << endl;
		cout << "Level 1       " << l1Events << "   " << l1EventsTrue << "   " << l1EventsFalse << endl;
                cout << "L2 MET        " << metEvents << "   " << metEventsTrue << endl;
                cout << "L2 Reco       " << l2EventsReco << "   " << l2EventsRecoTrue << "   " << l2EventsRecoFalse << endl;
                cout << "L2 EcalIso    " << l2EventsEcalIso << "   " << l2EventsEcalIsoTrue << "   " << l2EventsEcalIsoFalse << endl;
                cout << "L25 Isolation " << l25Events << "   " << l25EventsTrue << "   " << l25EventsFalse << endl;
                cout << "L3 Isolation  " << l3Events << "   " << l3EventsTrue << "   " << l3EventsFalse << endl;
                cout << "HLT total     " << l3Events << "   " << l3EventsTrue << "   " << l3EventsFalse << endl;

		cout << "            Efficiencies " << endl;
		cout << "Level 1       " << double(l1Events)/allEvents << "  " << double(l1EventsTrue)/allEvents << endl;
                cout << "L2 MET        " << double(metEvents)/l1Events << "  " << double(metEventsTrue)/l1EventsTrue << endl;
                cout << "L2 Reco       " << double(l2EventsReco)/metEvents << "  " << double(l2EventsRecoTrue)/metEventsTrue << endl;
                cout << "L2 EcalIso    " << double(l2EventsEcalIso)/l2EventsReco << "  " << double(l2EventsEcalIsoTrue)/l2EventsRecoTrue << endl;
                cout << "L25 Isolation " << double(l25Events)/l2EventsEcalIso << "  " << double(l25EventsTrue)/l2EventsEcalIsoTrue << endl;
                cout << "L3 Isolation  " << double(l3Events)/l25Events << "  " << double(l3EventsTrue)/l25EventsTrue << endl;
                cout << "HLT total     " << double(l3Events)/l1Events << "  " << double(l3EventsTrue)/l1EventsTrue << endl;
		cout << endl;

                if(userRootTree != NULL){
                        userRootTree->setAcceptance("trigger:all",allEvents);
                        userRootTree->setAcceptance("trigger:L1",l1Events);
                        userRootTree->setAcceptance("trigger:L2MET",metEvents);
                        userRootTree->setAcceptance("trigger:L2Reco",l2EventsReco);
                        userRootTree->setAcceptance("trigger:L2Ecal",l2EventsEcalIso);
                        userRootTree->setAcceptance("trigger:L25",l25Events);
                        userRootTree->setAcceptance("trigger:L3",l3Events);

                        userRootTree->setAcceptance("trigger:L1TrueTau",l1EventsTrue);
                        userRootTree->setAcceptance("trigger:L2METTrue",metEventsTrue);
                        userRootTree->setAcceptance("trigger:L2RecoTrueTau",l2EventsRecoTrue);
                        userRootTree->setAcceptance("trigger:L2EcalTrueTau",l2EventsEcalIsoTrue);
                        userRootTree->setAcceptance("trigger:L25TrueTau",l25EventsTrue);
                        userRootTree->setAcceptance("trigger:L3TrueTau",l3EventsTrue);
                }
	}
}

bool TauMETTriggerAnalysis::analyse(const edm::Event& iEvent){

	mcAnalysis(iEvent);

	allEvents++;
        if(! L1(iEvent) ) return false;
	if(! L2MET(iEvent) ) return false;
	if(! L2reco(iEvent) ) return false;
        if(! L2ecalIso(iEvent) ) return false;
        if(! L25(iEvent) ) return false;
        if(! L3(iEvent) ) return false;
        return true;
}

bool TauMETTriggerAnalysis::L1(const edm::Event& iEvent){

	Handle< L1JetParticleCollection > l1TriggeredTaus;
	iEvent.getByLabel(edm::InputTag("l1extraParticles:Tau"),l1TriggeredTaus);

        bool singleTauFired = false;
	bool trueTau = false;
	l1truetau = false;
        if(l1TriggeredTaus.isValid()){
		const L1JetParticleCollection & L1jets  = *(l1TriggeredTaus.product());

                cout << "L1  tau collection size " << L1jets.size() << endl;

		L1JetParticleCollection::const_iterator i;
                for(i = L1jets.begin(); i!= L1jets.end(); i++){
		  	double et = i->et();
			h_L1TauEt->Fill(et);
//                        if(singleTauMap.triggerDecision() && et > 80){
                        if(et > 80){
                                singleTauFired = true;
				if(!trueTau) trueTau = genuineTau(i->p4());
                        }
                }
        }
	if(singleTauFired){
		l1Events++;
		if(trueTau){
                	l1EventsTrue++;
			l1truetau = true;
                }else{
                        l1EventsFalse++;
                }
	}

        return singleTauFired;
}

bool TauMETTriggerAnalysis::L2MET(const edm::Event& iEvent){

        Handle<CaloMETCollection> caloMET;
        try{
            iEvent.getByLabel("met",caloMET);
        }catch(...) {;}

	double met = 0;
        if(caloMET.isValid()){

          CaloMETCollection::const_iterator imet = caloMET->begin();
          double metX = imet->px();
          double metY = imet->py();

          met = sqrt(metX*metX + metY*metY);
	  h_MET->Fill(met);
          cout << "calo MET  : " << met
               << "  METx : "  << metX
               << "  METy : "  << metY << endl;
        }

	if(met < 65) return false;

	metEvents++;

	if(l1truetau) metEventsTrue++;
	return true;
}

bool TauMETTriggerAnalysis::L2reco(const edm::Event& iEvent){

        Handle<CaloJetCollection> l2TauJetHandle;
//        iEvent.getByLabel(InputTag("l2SingleTauJets"),l2TauJetHandle);
        iEvent.getByLabel(InputTag("l2TauJetsProvider:SingleTau"),l2TauJetHandle);

        bool singleTauFired = false;
        bool trueTau = false;

        if(l2TauJetHandle.isValid()){
                const CaloJetCollection & l2Jets = *(l2TauJetHandle.product());
                cout << "L2 tau collection size " << l2Jets.size() << endl;
                CaloJetCollection::const_iterator i;
                for(i = l2Jets.begin(); i != l2Jets.end(); i++) {
                        singleTauFired = true;
                        if(!trueTau) trueTau = genuineTau(i->p4());
                }
	}

        if(singleTauFired){
                l2EventsReco++;
                if(trueTau){
                        l2EventsRecoTrue++;
                }else{
                        l2EventsRecoFalse++;
                }
        }
        return singleTauFired;
}

bool TauMETTriggerAnalysis::L2ecalIso(const edm::Event& iEvent){


	Handle<CaloJetCollection> ecalIsolatedJetHandle;
	iEvent.getByLabel(InputTag("ecalSingleTauIsolated:Isolated"),ecalIsolatedJetHandle);

        bool singleTauFired = false;
	bool trueTau = false;

        if(ecalIsolatedJetHandle.isValid()){
		const CaloJetCollection & ecalIsolatedJets = *(ecalIsolatedJetHandle.product());
		cout << "L2 ecal isol tau collection size " << ecalIsolatedJets.size() << endl;
		CaloJetCollection::const_iterator i;
		for(i = ecalIsolatedJets.begin(); i != ecalIsolatedJets.end(); i++) {
			singleTauFired = true;
			if(!trueTau) trueTau = genuineTau(i->p4());
		}
        }

        if(singleTauFired){
                l2EventsEcalIso++;
                if(trueTau){
                        l2EventsEcalIsoTrue++;
                }else{
                        l2EventsEcalIsoFalse++;
                }
        }
        return singleTauFired;
}

bool TauMETTriggerAnalysis::L25(const edm::Event& iEvent){

        Handle<IsolatedTauTagInfoCollection> tauTagInfoHandle;
        try{
                iEvent.getByLabel("coneIsolationL25SingleTau", tauTagInfoHandle);
        }catch(...) {;}

        bool singleTauFired = false;
        bool trueTau = false;

        if(tauTagInfoHandle.isValid()){
               	const IsolatedTauTagInfoCollection & tauTagInfo = *(tauTagInfoHandle.product());
               	cout << "L25 tau collection size " << tauTagInfo.size() << endl;

               	IsolatedTauTagInfoCollection::const_iterator i;

               	for(i = tauTagInfo.begin(); i != tauTagInfo.end(); ++i) {
			if(i->discriminator(0.1,0.065,0.4,20.,1.)){
				Jet thejet = *(i->jet().get());
				singleTauFired = true;
	                        if(!trueTau) trueTau = genuineTau(thejet.p4());
			}
		}
	}
        if(singleTauFired){
                l25Events++;
                if(trueTau){
                        l25EventsTrue++;
                }else{
                        l25EventsFalse++;
                }
        }
        return singleTauFired;	
}

bool TauMETTriggerAnalysis::L3(const edm::Event& iEvent){

        Handle<IsolatedTauTagInfoCollection> tauTagL3Handle;
        try{
                iEvent.getByLabel("coneIsolationL3SingleTau", tauTagL3Handle);
        }catch(...) {;}

        bool singleTauFired = false;
        bool trueTau = false;

        if(tauTagL3Handle.isValid()){
                const IsolatedTauTagInfoCollection & L3Taus = *(tauTagL3Handle.product());
                cout << "L3 tau collection size " << L3Taus.size() << endl;

                IsolatedTauTagInfoCollection::const_iterator i;
                for(i = L3Taus.begin(); i != L3Taus.end(); i++){
			if(i->discriminator(0.1,0.065,0.4,20.,1.)){
                                Jet thejet = *(i->jet().get());
				singleTauFired = true;
                                if(!trueTau) trueTau = genuineTau(thejet.p4());
				h_L3TauEt->Fill(thejet.et());
			}
		}
	}
        if(singleTauFired){
                l3Events++;
                if(trueTau){
                        l3EventsTrue++;
                }else{
                        l3EventsFalse++;
                }
        }
        return singleTauFired;
}

bool TauMETTriggerAnalysis::genuineTau(math::XYZTLorentzVector p4){

	bool trueTau = false;

	TLorentzVector p4TLor(p4.X(),p4.Y(),p4.Z(),p4.T());

	vector<TLorentzVector>::const_iterator i;
	for(i = visible_taus.begin(); i!= visible_taus.end(); i++){
		double DR = i->DeltaR(p4TLor);
		if(DR < 0.5) trueTau = true;
	}
	return trueTau;
}

void TauMETTriggerAnalysis::mcAnalysis(const edm::Event& iEvent){
	visible_taus = ::visibleTaus(iEvent,37);
}
