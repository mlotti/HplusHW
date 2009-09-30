#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MCConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMET.h"

#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/JetReco/interface/GenJet.h"
#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

using std::vector;
using edm::Handle;
using edm::SimVertexContainer;
using edm::HepMCProduct;

MyMCParticle MCConverter::convert(const reco::GenJet& genJet){
	MyMCParticle mcJet(genJet.px(),genJet.py(),genJet.pz(),genJet.energy());
	mcJet.pid = 0; //= genJet.pdgId();
	mcJet.status = 4;
	return mcJet;
}

void MCConverter::addMCJets(const edm::Event& iEvent, vector<MyMCParticle>& mcParticles){
	Handle<reco::GenJetCollection> genJetHandle;
        iEvent.getByLabel("iterativeCone5GenJets",genJetHandle);

        const reco::GenJetCollection & genJetCollection = *(genJetHandle.product());
        //cout << "MC GenJets " << genJetCollection.size();

        reco::GenJetCollection::const_iterator iJet;
        for(iJet = genJetCollection.begin(); iJet!= genJetCollection.end(); ++iJet){

          if(iJet->et() < 20 || fabs(iJet->eta()) > 2.5) continue;
          //cout << "     GenJet Et,eta " << iJet->et() << " " << iJet->eta() << endl;
          MyMCParticle mcJet = convert(*iJet);
          mcParticles.push_back(mcJet);
        }
        //cout << ", saved " << mcParticles.size() << endl;
}


MyGlobalPoint MCConverter::getMCPrimaryVertex(const edm::Event& iEvent){
	Handle<SimVertexContainer> simVertices;
	iEvent.getByLabel("g4SimHits",simVertices);

	MyGlobalPoint mcPV;
	if(simVertices->size() > 0){
		mcPV.SetX((*simVertices)[0].position().x());
		mcPV.SetY((*simVertices)[0].position().y());
		mcPV.SetZ((*simVertices)[0].position().z());
	}else{
                mcPV.SetX(-999);
                mcPV.SetY(-999);
                mcPV.SetZ(-999);
	}
	return mcPV;
}

void MCConverter::addMCParticles(const edm::Event& iEvent, vector<MyMCParticle>& mcParticles, MyMET& mcMET){
        addMCJets(iEvent, mcParticles);

        Handle<HepMCProduct> mcEventHandle;
//      iEvent.getByLabel("source",mcEventHandle);
        iEvent.getByLabel("generator",mcEventHandle);

        const HepMC::GenEvent* mcEvent = mcEventHandle->GetEvent() ;
        //cout << "MC particles size " << mcEvent->particles_size() << endl;

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
                    ( abs(id) == 12 || abs(id) == 14 || abs(id) == 16 || abs(id) <= 21) ||
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
	mcMET.Set(mcMetX,mcMetY);

	// newSource from muon->tau conversion, saving the MC tau and its decay products
        Handle<HepMCProduct> mcEventHandle2;
        iEvent.getByLabel("newSource",mcEventHandle2);

        if(mcEventHandle2.isValid()){

                const HepMC::GenEvent* mcEvent = mcEventHandle2->GetEvent() ;
                //cout << "MC particles size " << mcEvent->particles_size() << endl;

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
                                while( *iMother && (*iMother)->production_vertex() ) {
                                        int motherId = (*iMother)->pdg_id();
                                        int motherBarCode = (*iMother)->barcode();
                                        //cout << "          mother ids,barcode " << motherId
                                        //     << " " << (*iMother)->barcode() << endl;
                                        iMother = (*iMother)->production_vertex()->particles_begin(HepMC::parents);
                                        // If the mother doesn't have mother, add to the motherList
                                        if(!*iMother || (*iMother)->pdg_id() != motherId) {
                                                motherList.push_back(motherId);
                                                motherBarcodes.push_back(motherBarCode);
                                        }
                                }
                        }

                        if(motherList.size() == 0 || motherList[0] != id){
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

