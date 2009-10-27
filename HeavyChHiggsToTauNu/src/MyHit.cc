#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyHit.h"

#include <iostream>

using namespace std;

MyHit::MyHit() {
  // Initialize data members
  theEstimate = 0;
}
 // LAW 11.02.08
MyHit::~MyHit() {

}

void MyHit::print() {
  cout << "- hit at (" << x 
       << ", " << y
       << ", " << z
       << "), cxx=" << dxx
       << ", cxy=" << dxy
       << " estimate=" << theEstimate
       << " comp.count=" << theCompositeCount << endl;
}
