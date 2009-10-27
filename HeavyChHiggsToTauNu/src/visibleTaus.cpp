#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

#include "TLorentzVector.h"
#include <vector>

using namespace edm;
using namespace std;
using namespace HepMC;

vector<TLorentzVector> visibleTaus(const edm::Event& iEvent,int motherId){

	vector<TLorentzVector> theVisibleTaus;

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


		     bool motherSelection = false;
                     if( (*i)->production_vertex() ) {
                                HepMC::GenVertex::particle_iterator iMother;
                                for(iMother = (*i)->production_vertex()->particles_begin(HepMC::parents);
                                    iMother!= (*i)->production_vertex()->particles_end(HepMC::parents); iMother++){
					if(abs((*iMother)->pdg_id()) == abs(motherId)) motherSelection = true;
                                }
                     }

                     if(!motherSelection && motherId != 0 ) continue;

                     FourVector p4 = (*i)->momentum();
                     TLorentzVector visibleTau(p4.px(),p4.py(),p4.pz(),p4.e());

		     bool lepton = false;
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
/*
                                if( abs(childId) == 211 ){ // pi+,rho+
                                        if(p.P() > leadingTrack.P()) leadingTrack = p;
                                }
*/
                        }
                     }
		     if(!lepton) theVisibleTaus.push_back(visibleTau);
                }
        }

	return theVisibleTaus;
}
