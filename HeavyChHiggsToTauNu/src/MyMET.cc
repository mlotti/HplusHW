#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMET.h"

#include<cmath>
using std::endl;

//ClassImp(MyMET)

MyMET::MyMET(): TVector2(0, 0), name("") {}
MyMET::MyMET(double x, double y): TVector2(x, y), name("") {}
MyMET::~MyMET() {}


double MyMET::value() const { 
    return Mod(); // TVector2::Mod() returns the length of the 2D vector
}

double MyMET::x() const { return X(); }
double MyMET::y() const { return Y(); }

double MyMET::phi() const {
    return Phi();
}

void MyMET::print(std::ostream& out) const {
    out << " MET value,x,y,phi " << value() << " " 
         << X() << " " << Y() << " " << Phi() << endl;
    out << "     caloMET without corrections x,y " << X() << " "
         << Y() << endl;
}
