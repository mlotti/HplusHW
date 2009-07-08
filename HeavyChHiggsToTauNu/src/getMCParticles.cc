#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyMCParticle> MyEventConverter::getMCParticles(const edm::Event& iEvent){

	vector<MyMCParticle> mcParticles = getMCJets(iEvent);

        Handle<HepMCProduct> mcEventHandle;
        try{
          iEvent.getByLabel("source",mcEventHandle);
        }catch(...) {;}

        if(mcEventHandle.isValid()){

                const HepMC::GenEvent* mcEvent = mcEventHandle->GetEvent() ;
                cout << "MC particles size " << mcEvent->particles_size() << endl;

		double mcMetX = 0;
		double mcMetY = 0;
                HepMC::GenEvent::particle_const_iterator i;
                for(i = mcEvent->particles_begin(); i!= mcEvent->particles_end(); i++){
/*
                        cout << "  particle " << (*i)->barcode()
                             << " " << (*i)->pdg_id()
                             << " " << (*i)->status()
                             << " " << (*i)->momentum().perp()
                             << " " << (*i)->momentum().eta()
                             << " " << (*i)->momentum().phi()
                             << endl;
*/

			int id = (*i)->pdg_id();

                        if((*i)->status() == 1 && (abs(id) == 12 || abs(id) == 14 || abs(id) == 16)){
                                mcMetX += (*i)->momentum().x();
                                mcMetY += (*i)->momentum().y();
                        }

//                        if( ( (*i)->status() == 1 && (*i)->momentum().perp() > 1) ||
                        if( ( (*i)->status() == 1 ) ||
			    ( abs(id) == 12 || abs(id) == 14 || abs(id) == 16 ) ||
                            ( (*i)->status() == 3) ) {

                                // searching parents

                                vector<int> motherList;
                                vector<int> motherBarcodes;
                                if( (*i)->production_vertex() ) {
                                        HepMC::GenVertex::particle_iterator iMother =
                                                (*i)->production_vertex()->particles_begin(HepMC::parents);
					  if(*iMother != 0) {
                                            while( (*iMother)->production_vertex() ) {
                                                int motherId = (*iMother)->pdg_id();
						int motherBarCode = (*iMother)->barcode();
                                                //cout << "          mother ids,barcode " << motherId 
                                                //     << " " << (*iMother)->barcode() << endl;
                                                iMother = (*iMother)->production_vertex()->particles_begin(HepMC::parents);
						if((*iMother)->pdg_id() != motherId) {
							motherList.push_back(motherId);
							motherBarcodes.push_back(motherBarCode);
						}
                                            }
					  }
                                }

				if(motherList.size() > 0){
				  if(motherList[0] != id){
					MyMCParticle mcParticle;
					mcParticle.pid    = id;
					mcParticle.status = (*i)->status();
					mcParticle.barcode = (*i)->barcode();
                                	mcParticle.SetE((*i)->momentum().e());
                                	mcParticle.SetPx((*i)->momentum().px());
                                	mcParticle.SetPy((*i)->momentum().py());
                                	mcParticle.SetPz((*i)->momentum().pz());

                                        //mcParticle.motherLine = myMCMotherIterator;
	                                mcParticle.mother = motherList;
					mcParticle.motherBarcodes = motherBarcodes;
					//cout << "SAVING particle " << mcParticle.barcode << " " << mcParticle.pid << endl;
					mcParticles.push_back(mcParticle);
				  }
				}
			}
		}
		mcMET.x = mcMetX;
		mcMET.y = mcMetY;
	}


	// newSource from muon->tau conversion, saving the MC tau and its decay products
        Handle<HepMCProduct> mcEventHandle2;
        try{
          iEvent.getByLabel("newSource",mcEventHandle2);
        }catch(...) {;}

        if(mcEventHandle2.isValid()){

                const HepMC::GenEvent* mcEvent = mcEventHandle2->GetEvent() ;
                cout << "MC particles size " << mcEvent->particles_size() << endl;

                HepMC::GenEvent::particle_const_iterator i;
                for(i = mcEvent->particles_begin(); i!= mcEvent->particles_end(); i++){
/*
                        cout << "  particle " << (*i)->barcode()
                             << " " << (*i)->pdg_id()
                             << " " << (*i)->status()
                             << " " << (*i)->momentum().perp()
                             << " " << (*i)->momentum().eta()
                             << " " << (*i)->momentum().phi()
                             << endl;
*/

                        int id = (*i)->pdg_id();

                        // searching parents
                        // searching parents

                        vector<int> motherList;
                        vector<int> motherBarcodes;
                        if( (*i)->production_vertex() ) {
                                HepMC::GenVertex::particle_iterator iMother =
                                        (*i)->production_vertex()->particles_begin(HepMC::parents);
                                if(*iMother != 0) {
                                    while( (*iMother)->production_vertex() ) {
                                        int motherId = (*iMother)->pdg_id();
                                        int motherBarCode = (*iMother)->barcode();
                                        //cout << "          mother ids,barcode " << motherId
                                        //     << " " << (*iMother)->barcode() << endl;
                                        iMother = (*iMother)->production_vertex()->particles_begin(HepMC::parents);
                                        if(! *iMother)
                                          break;
                                        if((*iMother)->pdg_id() != motherId) {
                                                motherList.push_back(motherId);
                                                motherBarcodes.push_back(motherBarCode);
                                        }
                                    }
                                }
                        }

                        if(motherList.size() > 0){
                          if(motherList[0] != id){
                                MyMCParticle mcParticle;
                                mcParticle.pid    = id;
                                mcParticle.status = (*i)->status();
                                mcParticle.barcode = (*i)->barcode();
                                mcParticle.SetE((*i)->momentum().e());
                                mcParticle.SetPx((*i)->momentum().px());
                                mcParticle.SetPy((*i)->momentum().py());
                                mcParticle.SetPz((*i)->momentum().pz());

                                //mcParticle.motherLine = myMCMotherIterator;
                                mcParticle.mother = motherList;
                                mcParticle.motherBarcodes = motherBarcodes;
                                //cout << "SAVING particle " << mcParticle.barcode << " " << mcParticle.pid << endl;
                                mcParticles.push_back(mcParticle);
                          }
                        }
                }
	}
	return mcParticles;
}

