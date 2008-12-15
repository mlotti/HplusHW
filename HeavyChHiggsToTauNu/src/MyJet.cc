#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"

ClassImp(MyJet)

MyJet::MyJet(){
        SetXYZT(0,0,0,0);
}
MyJet::MyJet(double Ex,double Ey,double Ez,double E){
	SetXYZT(Ex,Ey,Ez,E);
}

MyJet::~MyJet(){}

///////////////////////////

double MyJet::Et()  const { return Pt(); }
double MyJet::E()   const { return sqrt(Px()*Px() + Py()*Py() + Pz()*Pz()); }

///////////////////////////

double MyJet::Ex() const { return Px(); }
double MyJet::Ey() const { return Py(); }
double MyJet::Ez() const { return Pz(); }

double MyJet::pt()  const { return Pt(); }
double MyJet::eta() const { return Eta(); }
double MyJet::phi() const { return Phi(); }

double MyJet::px()  const { return Px(); }
double MyJet::py()  const { return Py(); }
double MyJet::pz()  const { return Pz(); }
double MyJet::p()  const { return P(); }
double MyJet::energy()  const { return E(); }

TLorentzVector MyJet::p4() const {
        return TLorentzVector(this->Px(),this->Py(),this->Pz(),this->E());
}

void MyJet::setP4(TLorentzVector& vector){
        SetXYZT(vector.Px(),vector.Py(),vector.Pz(),vector.E());
}

////////////////////////////

void MyJet::setJetEnergyCorrection(string name,double value){
	jetEnergyCorrection[name] = value;
}

double MyJet::getCorrectionFactor(string name) const {

        if(name == "raw" || name == "" || name == "none") return 1;

	if(jetEnergyCorrection.find(name) == jetEnergyCorrection.end()){
		cout << "No jet energy correction: " << name << " found " << endl;
		exit(0);
	}
        return jetEnergyCorrection.find(name)->second;
}

vector<string> MyJet::getCorrectionNames() const {
	vector<string> names;
	map<string,double>::const_iterator i;
	for(i = jetEnergyCorrection.begin(); i!= jetEnergyCorrection.end(); i++){
		names.push_back(i->first);
	}
	return names;
}

MyJet MyJet::recalculateEnergy(string name) const {
	MyJet jet = *this;
	double correction = getCorrectionFactor(name);
	double new_Ex = Ex() * correction;
        double new_Ey = Ey() * correction;
        double new_Ez = Ez() * correction;
        double new_E  = E()  * correction;
	jet.SetXYZT(new_Ex,new_Ey,new_Ez,new_E);
	return jet;
}


vector<MyTrack> MyJet::getTracks(double signalCone) const {
	if(signalCone >= 0.7) return tracks;

	vector<MyTrack> selectedTracks;
	vector<MyTrack>::const_iterator i;
	for(i = tracks.begin(); i!= tracks.end(); i++){
		double DR = deltaR(this->Eta(),i->Eta(),
                                   this->Phi(),i->Phi());
		if(DR < signalCone) selectedTracks.push_back(*i);
	}
	return selectedTracks;
}

vector<MyTrack> MyJet::getTracksAroundLeadingTrack(double signalCone,double matchingCone) const {
        if(signalCone >= 0.7) return tracks;

	MyTrack theLeadingTrack = leadingTrack(matchingCone);

        vector<MyTrack> selectedTracks;
        vector<MyTrack>::const_iterator i;
        for(i = tracks.begin(); i!= tracks.end(); i++){
		if(i->charge() == 0) continue;
                double DR = deltaR(theLeadingTrack.Eta(),i->Eta(),
                                   theLeadingTrack.Phi(),i->Phi());
                if(DR < signalCone) selectedTracks.push_back(*i);
        }
        return selectedTracks;
}

vector<MyVertex> MyJet::getSecVertices() const {return secVertices;}
vector<MyCaloTower> MyJet::getCaloInfo() const {return caloInfo;}

double MyJet::tag(string name) const{
	if(tagInfo.find(name) == tagInfo.end()){
		cout << "jet tag " << name << " not found, exiting " << endl;
		exit(0);
	}
	return tagInfo.find(name)->second;
}

bool MyJet::btag(double cut) const{
	bool btagged = false;
	double discriminator = tag("discriminator");
	if( discriminator > cut) btagged = true;
	return btagged;
}

MyTrack MyJet::leadingTrack(double matchingCone) const {

        MyTrack theLeadingTrack(0,0,0,0);
        double ptmax = 0;
        for(vector<MyTrack>::const_iterator i = tracks.begin();
                                            i!= tracks.end(); i++){
		if(i->charge() == 0) continue;
		double DR = deltaR(i->Eta(),this->Eta(),
                                   i->Phi(),this->Phi());
		if(DR > matchingCone) continue;

                if(i->Pt() > ptmax){
                        ptmax = i->Pt();
                        theLeadingTrack = *i;
                }
        }
        return theLeadingTrack;
}

TLorentzVector MyJet::combinedTracksMomentum(double signalCone,double matchingCone) const {

        TLorentzVector p(0,0,0,0);

        MyTrack leadingtrack = this->leadingTrack(matchingCone);
        if(leadingtrack.Pt() > 0) {
		for(vector<MyTrack>::const_iterator i = tracks.begin();
        	                                    i!= tracks.end(); i++){
			if(i->charge() == 0) continue;
                	double DR = deltaR(i->Eta(),leadingtrack.Eta(),
                        	           i->Phi(),leadingtrack.Phi());
                	if(DR > signalCone) continue;

			p += i->p4();
		}
        }
	return p;
}

TLorentzVector MyJet::ecalClusterMomentum(double cone,double matchingCone) const {

	TVector3 ecalHitPoint(0,0,0);

        MyTrack leadingtrack = this->leadingTrack(matchingCone);
	if(leadingtrack.Pt() == 0) {
                ecalHitPoint = this->p4().BoostVector();
        }else{
		ecalHitPoint = leadingtrack.ecalHitPoint().tvector3();
	}

        TVector3 cluster(0,0,0);

        vector<MyCaloTower> caloTowers = this->getCaloInfo();

        vector<MyCaloTower>::const_iterator i;
        for(i = caloTowers.begin(); i!= caloTowers.end(); i++){
                vector<TVector3> cells = i->ECALCells;
                vector<TVector3>::const_iterator j;
                for(j = cells.begin(); j!= cells.end(); j++){
                        double DR = deltaR(ecalHitPoint.Eta(),j->Eta(),
                                           ecalHitPoint.Phi(),j->Phi());
                        if(DR < cone) cluster += *j;
                }
        }
        return TLorentzVector(cluster,cluster.Mag());

}
TLorentzVector MyJet::hcalClusterMomentum(double cone,double matchingCone) const {

        TVector3 ecalHitPoint(0,0,0);

        MyTrack leadingtrack = this->leadingTrack(matchingCone);
        if(leadingtrack.Pt() == 0) {
                ecalHitPoint = this->p4().BoostVector();
        }else{
                ecalHitPoint = leadingtrack.ecalHitPoint().tvector3();
        }

	TVector3 cluster(0,0,0);

        vector<MyCaloTower> caloTowers = this->getCaloInfo();

	vector<MyCaloTower>::const_iterator i;
	for(i = caloTowers.begin(); i!= caloTowers.end(); i++){
		vector<TVector3> cells = i->HCALCells;
		vector<TVector3>::const_iterator j;
		for(j = cells.begin(); j!= cells.end(); j++){
			double DR = deltaR(ecalHitPoint.Eta(),j->Eta(),
                                           ecalHitPoint.Phi(),j->Phi());
			if(DR < cone) cluster += *j;
		}
	}
	return TLorentzVector(cluster,cluster.Mag());
}

void MyJet::printTracks() const {
	if(tracks.size() == 0) return;
        cout << "      tracks " << tracks.size() << endl;
	for(vector<MyTrack>::const_iterator i = tracks_begin(); i!= tracks_end(); ++i){
		i->print();
	}
}
void MyJet::printVertices() const {
	if(secVertices.size() == 0) return;
        cout << "      vertices " << secVertices.size() << endl;
        for(vector<MyVertex>::const_iterator i = secVertices_begin(); i!= secVertices_end(); ++i){
                i->print();
        }
}
void MyJet::printCaloInfo() const {
	if(caloInfo.size() == 0) return;
	cout << "      caloTowers " << caloInfo.size() << endl;
        for(vector<MyCaloTower>::const_iterator i = caloInfo_begin(); i!= caloInfo_end(); ++i){
                i->print();
        }
}
void MyJet::printTagInfo() const {
	if(tagInfo.size() == 0) return;
	cout << "      tagInfo " << tagInfo.size() << endl;
	for(map<string,double>::const_iterator i = tagInfo.begin(); i!= tagInfo.end(); ++i){
		cout << "        " << i->first << " "  << i->second << endl;
	}
}
void MyJet::printEnergyCorrections() const {
	if(jetEnergyCorrection.size() == 0) return;
        cout << "      jetEnergyCorrections " << jetEnergyCorrection.size() << endl;
        for(map<string,double>::const_iterator i = jetEnergyCorrection.begin(); 
                                               i!= jetEnergyCorrection.end(); ++i){
                cout << "        " << i->first << " "  << i->second << endl;
        }
}

void MyJet::printCorrections() const {
        if(jetEnergyCorrection.size() == 0) return;
        for(map<string,double>::const_iterator i = jetEnergyCorrection.begin();
                                               i!= jetEnergyCorrection.end(); ++i){
                cout << "          " << i->first << endl;
        }
}

void MyJet::print() const {
	printTracks();
	printVertices();
	printCaloInfo();
	printTagInfo();
	printEnergyCorrections();
	cout << endl;
}
