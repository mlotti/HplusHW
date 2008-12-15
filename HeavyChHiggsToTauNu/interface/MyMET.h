#ifndef MY_MET
#define MY_MET

#include "TROOT.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyGlobalPoint.h"

#include <iostream>
#include <vector>
#include <string>
#include <map>

using namespace std;

class MyMET : public MyGlobalPoint {
   public:
      	MyMET();
      	virtual ~MyMET();

      	double getX() const;
      	double getY() const;
        double value() const;
        double getPhi() const;
        double phi() const;

      	void useCorrection(string);
      	void print();
	void printCorrections();

      	vector<MyGlobalPoint> corrections;
	inline vector<MyGlobalPoint>::const_iterator corrections_begin() { return corrections.begin(); }
        inline vector<MyGlobalPoint>::const_iterator corrections_end() { return corrections.end(); }

   private:
	bool correctionExists(string);

      	vector<string> usedCorrections;

   ClassDef(MyMET,1)
};
#endif
