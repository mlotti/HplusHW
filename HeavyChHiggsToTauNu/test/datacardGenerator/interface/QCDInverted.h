#ifndef QCDINVERTED
#define QCDINVERTED

#include <vector>
#include <string>
#include "Extractable.h"
#include "Dataset.h"
#include "NormalisationInfo.h"

class QCDInverted : public Extractable {
    public:
	QCDInverted(int, std::string, std::string, std::string);
  	QCDInverted(std::string, std::string, std::string, std::string);
        QCDInverted(std::string, std::string, std::string, std::string, std::string, std::string);                                                                  
  	virtual ~QCDInverted();

  	double doExtract(std::vector<Dataset*> datasets, NormalisationInfo* info, double additionalNormalisation = 1.0);
  	void addHistogramsToFile(std::string, std::string, TFile*);
  
    private:
//	TFile* fIN;
//	TH1*   h_mtInv;

  	std::string sCounterHisto;
  	std::string sCounterItem;
	std::string path;
};

#endif
