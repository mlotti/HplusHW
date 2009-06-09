#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEvent.h"

ClassImp(MyEvent)

MyEvent::MyEvent(){;}

MyEvent::~MyEvent(){;}

MyGlobalPoint MyEvent::getPrimaryVertex(){ return primaryVertex; }
MyGlobalPoint MyEvent::getMCPrimaryVertex(){ return mcPrimaryVertex; }

bool MyEvent::trigger(string name){
	return triggerResults[name];
}

void MyEvent::print(){
    cout << " Run "    << setw(8) << runNumber;
    cout << ", event "  << setw(8) << eventNumber;
    cout << ", HLT: "  << setw(2) << HLTobjects.size();
    cout << ", e: "    << setw(2) << electrons.size();
    cout << ", mu: "   << setw(2) << muons.size();
    cout << ", tau: "  << setw(2) << taujets.size();
    cout << ", pftau: "<< setw(2) << pftaus.size();
    cout << ", jet: "  << setw(2) << jets.size();
    cout << ", gamma: "<< setw(2) << photons.size();
    cout << ", MC: "   << setw(2) << mcParticles.size();
    cout << endl;
}

vector<MyJet> MyEvent::getL1objects(){return L1objects;}
vector<MyJet> MyEvent::getHLTobjects(){return HLTobjects;}
vector<MyJet> MyEvent::getElectrons(){return electrons;}
vector<MyJet> MyEvent::getPhotons(){return photons;}
vector<MyJet> MyEvent::getMuons(){return muons;}
vector<MyJet> MyEvent::getTaujets(){return taujets;}
vector<MyJet> MyEvent::getPFTaus(){return pftaus;}
vector<MyJet> MyEvent::getJets(){return getJets("raw");}
vector<MyJet> MyEvent::getExtraObjects(){return extraObjects;}

vector<MyJet> MyEvent::getJets(string jetCorrectionType){
	vector<MyJet> returnJets;
	for(vector<MyJet>::const_iterator i = jets.begin();
                                          i!= jets.end(); i++){
		returnJets.push_back(i->recalculateEnergy(jetCorrectionType));
	}
	return returnJets;
}

vector<MyJet> MyEvent::getTaujets(string jetCorrectionType){
        vector<MyJet> returnJets;
        for(vector<MyJet>::const_iterator i = taujets.begin();
                                          i!= taujets.end(); i++){
                returnJets.push_back(i->recalculateEnergy(jetCorrectionType));
        }
        return returnJets;
}

void MyEvent::listJetCorrections(){
	vector<string> foundCorrections;
	for(vector<MyJet>::const_iterator i = jets.begin();
                                          i!= jets.end(); i++){
      		foundCorrections = i->getCorrectionNames();
    	}
    	cout << " Event " << eventNumber << ", found jet corrections:" << endl;
    	for(vector<string>::const_iterator i = foundCorrections.begin();
                                           i!= foundCorrections.end(); i++){
      		cout << "      " << *i << endl;
    	}
}

MyMET MyEvent::getMET(){return MET;}
MyMET MyEvent::getMCMET(){return mcMET;}

vector<MyMCParticle> MyEvent::getMCParticles(){return mcParticles;}

vector<MySimTrack> MyEvent::getSimTracks(){return simTracks;}


void MyEvent::printReco(){
    print();

        if(triggerResults.size() > 0) cout << " Trigger " << endl;
        for(map<string,bool>::const_iterator i = triggerResults.begin();
                                             i!= triggerResults.end(); ++i){
                cout << "           " << i->first << " " << i->second << endl;
        }


    if(HLTobjects.size() > 0) cout << " HLT objects " << HLTobjects.size() << endl;
    for(vector<MyJet>::const_iterator i = HLTobjects.begin(); i!= HLTobjects.end(); i++){
       	cout << "    type = " << i->type 
             << ", Et = " << i->Et() 
             << ", eta = " << i->eta() 
             << ", phi = " << i->phi() 
             << ", tracks = " << i->tracks.size() << endl;
	i->print();
    }

    if(electrons.size() > 0) cout << " Electrons " << electrons.size() << endl;
    for(vector<MyJet>::const_iterator i = electrons.begin(); i!= electrons.end(); i++){
       	cout << "    type = " << i->type
             << ", Et = " << i->Et()
             << ", eta = " << i->eta()
             << ", phi = " << i->phi()
             << ", tracks = " << i->tracks.size() << endl;
	i->print();
    }

    if(photons.size() > 0) cout << " Photons " << photons.size() << endl;
    for(vector<MyJet>::const_iterator i = photons.begin(); i!= photons.end(); i++){
       	cout << "    type = " << i->type
             << ", Et = " << i->Et()
             << ", eta = " << i->eta()
             << ", phi = " << i->phi()
             << ", tracks = " << i->tracks.size() << endl;
	i->print();
    }

    if(muons.size() > 0) cout << " Muons " << muons.size() << endl;
    for(vector<MyJet>::const_iterator i = muons.begin(); i!= muons.end(); i++){
       	cout << "    type = " << i->type
             << ", Et = " << i->Et()
             << ", eta = " << i->eta()
             << ", phi = " << i->phi()
             << ", tracks = " << i->tracks.size() << endl;
	i->print();
    }

    if(taujets.size() > 0) cout << " Taujets " << taujets.size() << endl;
    for(vector<MyJet>::const_iterator i = taujets.begin(); i!= taujets.end(); i++){
       	cout << "    Et = " << i->Et()
             << ", eta = " << i->eta()
             << ", phi = " << i->phi()
             << ", tracks = " << i->tracks.size() << endl;
	i->print();
    }

    if(pftaus.size() > 0) cout << " PFTaus " << pftaus.size() << endl;
    for(vector<MyJet>::const_iterator i = pftaus.begin(); i!= pftaus.end(); i++){
       	cout << "    Et = " << i->Et()
             << ", eta = " << i->eta()
             << ", phi = " << i->phi()
             << ", tracks = " << i->tracks.size() << endl;
        i->print();
    }

    if(jets.size() > 0) cout << " Jets " << jets.size() << endl;
    for(vector<MyJet>::const_iterator i = jets.begin(); i!= jets.end(); i++){
	cout << "    Et = " << i->Et()
             << ", eta = " << i->eta()
             << ", phi = " << i->phi()
             << ", tracks = " << i->tracks.size() << endl;
	i->print();
    }

    if(extraObjects.size() > 0) cout << " Extra objects " << extraObjects.size() << endl;
    for(vector<MyJet>::const_iterator i = extraObjects.begin(); i!= extraObjects.end(); i++){
       	cout << "    Et = " << i->Et()
             << ", eta = " << i->eta()
             << ", phi = " << i->phi()
             << ", tracks = " << i->tracks.size() << endl;
       	i->print();
    }

    cout << " MET    = " << getMET().value() << endl;
    getMET().printCorrections();
}

void MyEvent::printAll(){

    printReco();

    cout << " MC MET = " << getMCMET().value() << endl;

    if(mcParticles.size() > 0) cout << " MC particles " << mcParticles.size() << endl;
    for(vector<MyMCParticle>::const_iterator i = mcParticles.begin(); i!= mcParticles.end(); i++){
       	cout << "    pid = " << i->pid
             << ", Et = " << i->pt()
             << ", eta = " << i->eta()
             << ", phi = " << i->phi() << endl;
    }

}

void MyEvent::printCorrections(){
        cout << endl;

//	cout << "      Tau energy corrections" << endl;
        if(taujets.size() > 0) taujets[0].printCorrections();

//	cout << "      Jet energy corrections" << endl;
        if(jets.size() > 0) jets[0].printCorrections();

        MET.printCorrections();
}
