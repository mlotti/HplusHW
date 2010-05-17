#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyHit.h"

MyHit::MyHit() {
}
 // LAW 11.02.08
MyHit::~MyHit() {

}

void MyHit::print(std::ostream& out) const {
  out << "- hit at (" << X()
      << ", " << Y()
      << ", " << Z()
      << "), cxx=" << dxx
      << ", cxy=" << dxy
      << " estimate=" << theEstimate
      << " comp.count=" << theCompositeCount << std::endl;
}
