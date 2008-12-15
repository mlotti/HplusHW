#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMET.h"

double phifun(double,double);

ClassImp(MyMET)

MyMET::MyMET(){
  use("2D");
}
MyMET::~MyMET(){}


double MyMET::getX() const {
    double component = x;
    for(vector<string>::const_iterator i = usedCorrections.begin();
                                       i!= usedCorrections.end(); i++){

	for(vector<MyGlobalPoint>::const_iterator p = corrections.begin();
                                                  p!= corrections.end(); p++){
	    if(p->name == *i) component += p->getX();
	}
    }
    return component;
}

double MyMET::getY() const {
    double component = y;
    for(vector<string>::const_iterator i = usedCorrections.begin();
                                       i!= usedCorrections.end(); i++){

        for(vector<MyGlobalPoint>::const_iterator p = corrections.begin();
                                                  p!= corrections.end(); p++){
            if(p->name == *i) component += p->getY();
        }
    }
    return component;
}

double MyMET::value() const { 
	return sqrt(getX()*getX()+getY()*getY());
}

double MyMET::getPhi() const {
    return phifun(getX(),getY());
}

double MyMET::phi() const {
	return getPhi();
}


void MyMET::useCorrection(string correction){
	if(correction == "none"){
		usedCorrections.clear();
	}else{

		if(!correctionExists(correction)) cout << "Warning: unknown MET correction " << correction << endl;

		bool alreadyUsed = false;
		for(vector<string>::const_iterator i = usedCorrections.begin();
        	                                   i!= usedCorrections.end(); i++){
			if(*i == correction) alreadyUsed = true;
		}
		if(!alreadyUsed) usedCorrections.push_back(correction);
	}
}

void MyMET::print(){
    cout << " MET value,x,y,phi " << value() << " " 
         << getX() << " " << getY() << " " << getPhi() << endl;
    cout << "     caloMET without corrections x,y " << this->x << " "
                                                    << this->y << endl;

    cout << "     Used corrections: " << endl;
    for(vector<string>::const_iterator i = usedCorrections.begin();
                                       i!= usedCorrections.end(); i++){
        for(vector<MyGlobalPoint>::const_iterator p = corrections.begin();
                                                  p!= corrections.end(); p++){
            if(p->name == *i) {
                cout << "          " << *i << " " << p->getX() << " " << p->getY() << endl;
            }
        }
    }
    cout << endl;
}

bool MyMET::correctionExists(string correction){
	bool exists = false;
	for(vector<MyGlobalPoint>::const_iterator p = corrections.begin();
                                                  p!= corrections.end(); p++){
		if(p->name == correction) exists = true;
	}
	return exists;
}

void MyMET::printCorrections(){
        cout << "      MET corrections " << corrections.size() << ", used(*) " << endl;
        for(vector<MyGlobalPoint>::const_iterator p = corrections.begin();
                                                  p!= corrections.end(); p++){
                bool used = false;
                for(vector<string>::const_iterator i = usedCorrections.begin();
                                       i!= usedCorrections.end(); i++){
                        if(p->name == *i) used = true;
                }
                cout << "          " << p->name;
                if(used) cout << "*";
                cout << endl;
        }
}

