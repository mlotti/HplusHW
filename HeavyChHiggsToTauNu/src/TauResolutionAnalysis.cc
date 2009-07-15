#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauResolutionAnalysis.h"

#include "DataFormats/Common/interface/Handle.h"
using namespace edm;

#include "SimDataFormats/HepMCProduct/interface/HepMCProduct.h"
#include "HepMC/GenEvent.h"
using namespace HepMC;

#include "DataFormats/TauReco/interface/CaloTau.h"
#include "DataFormats/TauReco/interface/PFTau.h"

#include "RecoTauTag/TauTagTools/interface/CaloTauElementsOperators.h"
#include "RecoTauTag/TauTagTools/interface/PFTauElementsOperators.h"


#include "TLorentzVector.h"

#include <iostream>
using namespace std;

//double phiDis(double,double);
vector<TLorentzVector> visibleTaus(const edm::Event&,int);

TauResolutionAnalysis::TauResolutionAnalysis(){

	resoRootFile = new TFile("resolution.root","RECREATE");

        h_tauEnergyResolution   = new TH1F("h_tauEnergyResolution","",100,-1.2,1.2);
        h_pftauEnergyResolution = (TH1F*)h_tauEnergyResolution->Clone("h_pftauEnergyResolution");
        h_pfcandEnergyResolution = (TH1F*)h_tauEnergyResolution->Clone("h_pfcandEnergyResolution");

	h_tauDR = new TH1F("h_tauDR","",100,0,0.5);
        h_pftauDR = (TH1F*)h_tauDR->Clone("h_pftauDR");

	h_tauDeta = new TH1F("h_tauDeta","",100,-1.,1.);
	h_pftauDeta = (TH1F*)h_tauDeta->Clone("h_pftauDeta");

	h_tauDphi = new TH1F("h_tauDphi","",100,-3,3);
        h_pftauDphi = (TH1F*)h_tauDphi->Clone("h_pftauDphi");

	h_mcRtau = new TH1F("h_mcRtau","",100,0,1);

        h_ntracksPfTau = new TH1F("h_ntracksPfTau","",20,-0.5,19.5);
        h_ntracksCaloTau = (TH1F*)h_ntracksPfTau->Clone("h_ntracksCaloTau");
        h_ntracksPfInCaloTauCone = (TH1F*)h_ntracksPfTau->Clone("h_ntracksPfInCaloTauCone");
        h_ntracksPfTauMinusCaloTau = new TH1F("h_ntracksPfTauMinusCaloTau","",21,-10.5,10.5);


	eventCounter         		= 0;
        mcTauCounter	            	= 0;
	mcHadronicTauCounter 		= 0;
	mcVisibleTauCounter  		= 0;
	mcTauPtCutCounter    		= 0;
	caloTauCounter	     		= 0;
	pfTauCounter	    		= 0;
	caloTauWithLeadingTrackCounter  = 0;
	isolatedCaloTauCounter		= 0;
        pfTauWithLeadingTrackCounter  	= 0;
        isolatedPfTauCounter          	= 0;
}

TauResolutionAnalysis::~TauResolutionAnalysis(){

	if(eventCounter > 0){

	  resoRootFile->cd();
	  resoRootFile->Write();
	  resoRootFile->Close();

	  cout << "TauResolutionAnalysis: "
               << eventCounter << " events analysed " << endl;
          cout << " mc taus               " << mcTauCounter << endl;
	  cout << " mc hadronic taus      " << mcHadronicTauCounter << endl;
	  cout << " mc visible taus       " << mcVisibleTauCounter << endl;
          cout << " mc visible tau pt cut " << mcTauPtCutCounter << endl;
	  cout << endl;
	  cout << " calotaus in cone      " << caloTauCounter << endl;
	  cout << " calotaus with ltrack  " << caloTauWithLeadingTrackCounter << endl;
          cout << " isolated calotaus     " << isolatedCaloTauCounter << endl;
	  cout << endl;
          cout << " pftaus in cone        " << pfTauCounter << endl;
          cout << " pftaus with ltrack    " << pfTauWithLeadingTrackCounter << endl;
          cout << " isolated pftaus       " << isolatedPfTauCounter << endl;
          cout << endl;
	}
}

bool TauResolutionAnalysis::analyse(const edm::Event& iEvent){

	bool select = false;

        eventCounter++;
//        resoRootFile->cd();

        Handle<CaloTauCollection> theCaloTauHandle;
        try{
          iEvent.getByLabel("caloRecoTauProducer",theCaloTauHandle);
        }catch(...) {;}

        Handle<PFTauCollection> thePFTauHandle;
        try{
          iEvent.getByLabel("pfRecoTauProducer",thePFTauHandle);
        }catch(...) {;}


        bool lepton = false;
	bool tau    = false;

        TLorentzVector visibleTau(0,0,0,0);
	TLorentzVector leadingTrack(0,0,0,0);

        Handle<HepMCProduct> mcEventHandle;
        try{
          iEvent.getByLabel("source",mcEventHandle);
        }catch(...) {;}

        if(mcEventHandle.isValid()){
                const HepMC::GenEvent* mcEvent = mcEventHandle->GetEvent() ;

                HepMC::GenEvent::particle_const_iterator i;
                for(i = mcEvent->particles_begin(); i!= mcEvent->particles_end(); i++){
                     int id = (*i)->pdg_id();

                     if(abs(id) != 15) continue;

		     tau = true;

                     int motherId  = 0;
                     if( (*i)->production_vertex() ) {
                                HepMC::GenVertex::particle_iterator iMother;
                                for(iMother = (*i)->production_vertex()->particles_begin(HepMC::parents);
                                    iMother!= (*i)->production_vertex()->particles_end(HepMC::parents); iMother++){
                                     motherId = (*iMother)->pdg_id();
                                     //cout << " tau mother " <<  motherId   <<  endl;
                                }
                     }

                     if( abs(motherId) != 37 ) continue;

		     FourVector p4 = (*i)->momentum();
                     visibleTau = TLorentzVector(p4.px(),p4.py(),p4.pz(),p4.e());

                     if( (*i)->production_vertex() ) {
                        HepMC::GenVertex::particle_iterator iChild;
                        for(iChild = (*i)->production_vertex()->particles_begin(HepMC::descendants);
                            iChild!= (*i)->production_vertex()->particles_end(HepMC::descendants);iChild++){
                                int childId = (*iChild)->pdg_id();
                                //cout << "tau child id " << childId << endl;
                                FourVector fv = (*iChild)->momentum();
                                TLorentzVector p(fv.px(),fv.py(),fv.pz(),fv.e());

                                if( abs(childId) == 12 || abs(childId) == 14 || abs(childId) == 16){
                                   if((*iChild)->status() == 1 && childId*id > 0) {
                                        visibleTau -= p;
                                   }
                                }

                                if( abs(childId) == 11 || abs(childId) == 13 ){
                                        lepton = true;
                                }

				if( abs(childId) == 211 ){ // pi+,rho+
					if(p.P() > leadingTrack.P()) leadingTrack = p;
				}

                        }
                     }


                }


        }

	if(!tau) return select; 
        mcTauCounter++;

        if(lepton) return select;
        mcHadronicTauCounter++;

	if(visibleTau.Pt() == 0) return select;
	mcVisibleTauCounter++;
//cout << "vis tau px,py,pz " << visibleTau.Px() << " " << visibleTau.Py() << " " << visibleTau.Pz() << endl;
//cout << "        eta,phi  " << visibleTau.Eta() << " " << visibleTau.Phi() << endl;


        if(visibleTau.Pt() < 100) return select;
	mcTauPtCutCounter++;

        //cout << "visible tau pt " << visibleTau.Pt() << endl;

        double Rtau = leadingTrack.P()/visibleTau.E();
        h_mcRtau->Fill(Rtau);
//cout << "check Rtau " << Rtau << " " << leadingTrack.P() << " " << visibleTau.E() << endl;


////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        double matchingConeSize  	= 0.1,
               signalConeSize 		= 0.07,
               isolationConeSize    	= 0.4,
               ptLeadingTrackMin   	= 20,
               ptOtherTracksMin  	= 1;
	string metric = "DR"; // can be DR,angle,area
	unsigned int isolationAnnulus_Tracksmaxn = 0;


        if(theCaloTauHandle.isValid()){
          const CaloTauCollection & caloTaus = *(theCaloTauHandle.product());

	  //cout << "calotau collection size " << caloTaus.size() << endl;

          CaloTauCollection::const_iterator iTau;
          for(iTau = caloTaus.begin(); iTau != caloTaus.end(); iTau++){
			TLorentzVector p4(iTau->px(),iTau->py(),iTau->pz(),iTau->energy());
                        double DR = p4.DeltaR(visibleTau);
                        if(DR > 0.4) continue;
			caloTauCounter++;

	                if(!iTau->leadTrack()) continue;
			caloTauWithLeadingTrackCounter++;

			CaloTau theCaloTau = *iTau;
			CaloTauElementsOperators theCaloTauElementsOperators(theCaloTau);

//			double d_trackIsolation = theCaloTauElementsOperators.discriminatorByIsolTracksN(0);
			double d_trackIsolation = theCaloTauElementsOperators.discriminatorByIsolTracksN(
				metric, 
				matchingConeSize, 
				ptLeadingTrackMin, 
				ptOtherTracksMin, 
				metric, 
				signalConeSize, 
				metric, 
				isolationConeSize, 
				isolationAnnulus_Tracksmaxn);

			if(d_trackIsolation == 0) continue;
			isolatedCaloTauCounter++;

                        double dEt = (iTau->et() - visibleTau.Et())/visibleTau.Et();
                        h_tauEnergyResolution->Fill(dEt);
			h_tauDR->Fill(DR);
			h_tauDeta->Fill(iTau->eta()-visibleTau.Eta());
			h_tauDphi->Fill(p4.DeltaPhi(visibleTau));

          }

        }

/*
        Handle<IsolatedTauTagInfoCollection> isolatedTauHandle;
        try{
          iEvent.getByLabel("coneIsolation",isolatedTauHandle);
        }catch(...) {;}

        if(isolatedTauHandle.isValid()){
          const IsolatedTauTagInfoCollection & isolatedTaus =
                                                *(isolatedTauHandle.product());

                IsolatedTauTagInfoCollection::const_iterator iTau;
                for(iTau = isolatedTaus.begin(); iTau != isolatedTaus.end(); iTau++){

                        Jet tauJet = *(iTau->jet().get());
                        //if( tauJet.et() < 100 ) continue;

                        if(iTau->discriminator(Rmatch,Rsignal,Riso,pT_LT,pT_min) == 0) continue;

			TLorentzVector p4(iTau->px(),iTau->py(),iTau->pz(),iTau->e());
                        double DR = p4.DeltaR(visibleTau);

                        if(DR > 0.4) continue;

                        double dEt = (tauJet.et() - visibleTau.Et())/visibleTau.Et();
                        h_tauEnergyResolution->Fill(dEt);
                }
        }
*/
////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        if(thePFTauHandle.isValid()){
          const PFTauCollection & pfTaus = *(thePFTauHandle.product());

		//cout << "pftau collection size " << pfTaus.size() << endl;

          	PFTauCollection::const_iterator iTau;
          	for(iTau = pfTaus.begin(); iTau != pfTaus.end(); iTau++){

			TLorentzVector p4(iTau->px(),iTau->py(),iTau->pz(),iTau->energy());
                        double DR = p4.DeltaR(visibleTau);

                        if(DR > 0.4) continue;
			pfTauCounter++;

                        if(!iTau->leadTrack()) continue;
////          		if(!iTau->leadPFChargedHadrCand()) continue;
			pfTauWithLeadingTrackCounter++;


			PFTau thePFTau = *iTau;
			PFTauElementsOperators thePFTauElementsOperators(thePFTau);

	        	//double d_trackIsolation = thePFTauElementsOperators.discriminatorByIsolTracksN(0);
                	double d_trackIsolation = thePFTauElementsOperators.discriminatorByIsolTracksN(
                                metric,
                                matchingConeSize,
                                ptLeadingTrackMin,
                                ptOtherTracksMin,
                                metric,
                                signalConeSize,
                                metric,
                                isolationConeSize,
                                isolationAnnulus_Tracksmaxn);
                	if(d_trackIsolation == 0) continue;
			isolatedPfTauCounter++;			

                	double dEt = (iTau->et() - visibleTau.Et())/visibleTau.Et();
			h_pftauEnergyResolution->Fill(dEt);
                        h_pftauDR->Fill(DR);
                        h_pftauDeta->Fill(iTau->eta()-visibleTau.Eta());
                        h_pftauDphi->Fill(p4.DeltaPhi(visibleTau));

                        // pfjet energy from candidates in 0.4 around the jet axis

			TLorentzVector newPFTau(0,0,0,0);
		        const PFCandidateRefVector pfCandidates = iTau->signalPFCands();

		        RefVector<PFCandidateCollection>::const_iterator iTrack;
        		for(iTrack = pfCandidates.begin(); iTrack!= pfCandidates.end(); iTrack++){

		                PFCandidate pfCand = **iTrack;
				TLorentzVector p4(pfCand.px(),pfCand.py(),pfCand.pz(),pfCand.p());
				newPFTau += p4;
			}
			double dEtCand = (newPFTau.Pt() - visibleTau.Et())/visibleTau.Et();			
                        h_pfcandEnergyResolution->Fill(dEtCand);

			select = true;
          }
        }


/*
        Handle<PFIsolatedTauTagInfoCollection> pfIsolatedTauHandle;
        try{
          iEvent.getByLabel("pfConeIsolation",pfIsolatedTauHandle);
        }catch(...) {;}

        if(pfIsolatedTauHandle.isValid()){
          const PFIsolatedTauTagInfoCollection & isolatedTaus =
                                                *(pfIsolatedTauHandle.product());

                PFIsolatedTauTagInfoCollection::const_iterator iTau;
                for(iTau = isolatedTaus.begin(); iTau != isolatedTaus.end(); iTau++){

                        const PFJet tauJet = *(iTau->pfjetRef().get());
                        //if( tauJet.et() < 100 ) continue;

                        if(iTau->discriminatorByIsolPFChargedHadrCandsN(Rmatch,Rsignal,Riso,true,pT_LT,pT_min) == 0) continue;

			TLorentzVector p4(tauJet.px(),tauJet.py(),tauJet.pz(),tauJet.e());
                        double DR = p4.DeltaR(visibleTau);

                        if(DR > 0.4) continue;

                        double dEt = (tauJet.et() - visibleTau.Et())/visibleTau.Et();
                        h_pftauEnergyResolution->Fill(dEt);
                }
        }
*/

	return select;
}

void TauResolutionAnalysis::chargedTrackCounter(const edm::Event& iEvent){

	eventCounter++;

        int nPfTrack        = 0;
        int nPfTrackCaloTau = 0;
        int nCaloTauTrack   = 0;

	vector<TLorentzVector> visibleTaus = ::visibleTaus(iEvent,0);
	vector<TLorentzVector>::const_iterator visibleTausEnd = visibleTaus.end();

	Handle<CaloTauCollection> theCaloTauHandle;
        iEvent.getByLabel("caloRecoTauProducer",theCaloTauHandle);

        Handle<PFTauCollection> thePFTauHandle;
        iEvent.getByLabel("pfRecoTauProducer",thePFTauHandle);

	if(!(theCaloTauHandle.isValid() && thePFTauHandle.isValid())) return;

        const CaloTauCollection & caloTaus = *(theCaloTauHandle.product());
	const PFTauCollection& pfTaus = *(thePFTauHandle.product());

	vector<TLorentzVector>::const_iterator i;
        for(i = visibleTaus.begin(); i!= visibleTausEnd; ++i){
		double DR_mcTau = 999;
		PFTauCollection::const_iterator iPfTau = pfTaus.begin();
		PFTauCollection::const_iterator pfTauEnd = pfTaus.end();

		while(DR_mcTau > 0.4 && iPfTau != pfTauEnd){
		  TLorentzVector p4(iPfTau->px(),iPfTau->py(),iPfTau->pz(),iPfTau->energy());
                  DR_mcTau = i->DeltaR(p4);

		  if(DR_mcTau < 0.4){
			double DR = 999;
			CaloTauCollection::const_iterator iCaloTau = caloTaus.begin();	
                        CaloTauCollection::const_iterator caloTauEnd = caloTaus.end();

			while(DR > 0.4 && iCaloTau != caloTauEnd){
			  
                          double DR = ROOT::Math::VectorUtil::DeltaR(iPfTau->p4(),iCaloTau->p4());
			  if(DR < 0.4){
                                const PFCandidateRefVector pfCandidates = iPfTau->signalPFCands();
        			for(RefVector<PFCandidateCollection>::const_iterator iTrack = pfCandidates.begin(); 
                                    iTrack!= pfCandidates.end(); iTrack++){
					if((*iTrack)->particleId() != 1) continue;					
					double DRPfTrackPfTau = ROOT::Math::VectorUtil::DeltaR(iPfTau->p4(),(*iTrack)->p4());
                                        if(DRPfTrackPfTau < 0.45) nPfTrack++;
                                        double DRPfTrackCaloTau = ROOT::Math::VectorUtil::DeltaR(iCaloTau->p4(),(*iTrack)->p4());
                                        if(DRPfTrackCaloTau < 0.45) nPfTrackCaloTau++;
				}

				const TrackRefVector tracksInCone = iCaloTau->caloTauTagInfoRef()->Tracks();
        			for(RefVector<TrackCollection>::const_iterator iTrack = tracksInCone.begin(); 
                                    iTrack!= tracksInCone.end(); iTrack++){
                                        double DRCaloTrackCaloTau = ROOT::Math::VectorUtil::DeltaR(iCaloTau->p4(),(*iTrack)->momentum());
                                        if(DRCaloTrackCaloTau < 0.45) nCaloTauTrack++;
				}
			  }
			  ++iCaloTau;
			}
		  }
		  ++iPfTau;
		}		
	}

        if(nPfTrack == 0 && nCaloTauTrack == 0) return;

        h_ntracksPfTau->Fill(nPfTrack);
        h_ntracksCaloTau->Fill(nCaloTauTrack);
        h_ntracksPfInCaloTauCone->Fill(nPfTrackCaloTau);
        h_ntracksPfTauMinusCaloTau->Fill(nPfTrack-nCaloTauTrack);
}

