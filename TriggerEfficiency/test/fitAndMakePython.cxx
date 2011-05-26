#include <iostream>
#include <time.h> 
#include <string>

#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"

#include "functions.cxx"  
#include "tdrstyle.cxx"

using namespace std;

static const int nBins = 2; // binning in pt
static const int nPar = 3; // number of parameters in the fit

class Binning {
    public:
	Binning(int nBins, double xMin, double xMax){
		nBins_ = nBins;
		xMin_  = xMin;
		xMax_  = xMax;
	}
	int bin(double pt){
		int theBin = -1;
		if(pt >= xMin_ && pt < xMax_){
		  theBin = int(nBins_ * (pt - xMin_)/(xMax_ - xMin_));
		}
		return theBin;
	}
	double binMin(int iBin){
		return 0;
	}
	double binMax(int iBin){
		return 0;
	}

    private:
	int nBins_;
	double xMin_,xMax_;
};

class PythonWriter {
    public:
	PythonWriter(string triggerName,string fileName){

		fName = fileName;

		fOUT.open(fileName.c_str(),ios::out);
		time_t rawtime;
		time ( &rawtime );

	        fOUT << "# Generated on "    
	             << ctime (&rawtime)
	             << "# by fitAndMakePython.cxx" << endl;
        
	        fOUT << "import FWCore.ParameterSet.Config as cms" << endl << endl;

	        fOUT << triggerName << " = cms.PSet(" << endl;
	        fOUT << "    # par[0]*(TMath::Freq((sqrt(x)-sqrt(par[1]))/(2*par[2])))" << endl;
	        fOUT << "    # par[0]=Plateau, par[1]=x when y = 0.5, par[2]=Width" << endl;  

		iCurrentBin = 0;
		trueTauBeingFilled = false;
		fakeTauBeingFilled = false;
	}
	~PythonWriter(){
		if(trueTauBeingFilled) {
                        fOUT << "    )" << endl;  
                        trueTauBeingFilled = false;
                }
		if(fakeTauBeingFilled) {
                        fOUT << "    )" << endl;  
                        fakeTauBeingFilled = false;
                }
		fOUT << ")" << endl;
		fOUT.close();
        
        	cout << "Generated file " << fName << endl;
	}

	void fillFakeTauParameters(){
		if(trueTauBeingFilled) {
			fOUT << "    )," << endl;
			trueTauBeingFilled = false;
		}
		fakeTauBeingFilled = true;
		fOUT << "    fakeTauParameters = cms.VPSet(" << endl;
		iCurrentBin = 0;
	}
	void fillTrueTauParameters(){
		if(fakeTauBeingFilled) {
			fOUT << "    )," << endl;
			fakeTauBeingFilled = false;
		}
		trueTauBeingFilled = true;
		fOUT << "    trueTauParameters = cms.VPSet(" << endl;
		iCurrentBin = 0;
	}
/*
	void addBin(float binMin,float binMax,double *parameters){

		fOUT << "        binMin = cms.double(" << binMin << "),"<< endl;
		fOUT << "        binMax = cms.double(" << binMax << "),"<< endl;
		fOUT << "        parameters = cms.vdouble([";
		for(size_t i = 0; i < nBins; ++i){
			fOUT << parameters[i];
			if(i < nBins-1) fOUT << ",";
		}
		fOUT << "])" << endl;
*/
	void addBin(double binmin,double binmax,double par0, double par1, double par2){
		fOUT << "        bin" << iCurrentBin << " = cms.PSet(" << endl;
                fOUT << "            binMin = cms.double(" << binmin << "),"<< endl;
                fOUT << "            binMax = cms.double(" << binmax << "),"<< endl;
                fOUT << "            parameters = cms.vdouble([";
		fOUT << par0 << ",";
		fOUT << par1 << ",";
		fOUT << par2;
		fOUT << "])" << endl;
		fOUT << "        )";
		if(iCurrentBin < nBins - 1) fOUT << ",";
		fOUT << endl;

		iCurrentBin++;
	}


    private:
	std::ofstream fOUT;
	string fName;
	int iCurrentBin;
	bool trueTauBeingFilled,fakeTauBeingFilled;
};

//void fit(TH1F* histo, Double_t parameters[nPar]){
void fit(TH1F* histo, double par0, double par1, double par2){
	cout << "check histo " << histo->GetEntries() << endl;

	Double_t fitRangeMin = 0,
                 fitRangeMax = 200;

	TF1* theFit = new TF1("theFit",fitFunction,fitRangeMin,fitRangeMax,nPar);
        theFit->SetParameter(0,1.); 
        theFit->SetParameter(1,50.);
        theFit->SetParameter(2,50.); 
        
        theFit->SetParLimits(0,0.5,1.);

        TCanvas* canvas = new TCanvas("canvas","",700,500);
        canvas->SetFillColor(0); 
        canvas->Divide(2,1);
        
        setTDRStyle();
        
        ////////////////////////////////////////
         
        canvas->cd(1);

        histo->Draw("PAE");
        histo->Fit("theFit","R0"); 
        theFit->SetRange(0,200);
        theFit->SetLineColor(kBlack);
        theFit->Draw("SAME");
        
        Double_t parameters[nPar] = {0,0,0};
        theFit->GetParameters(parameters);
        for(int i = 0; i < nPar; ++i){
                cout << "par" << i << " = " << parameters[i] << endl;
        }
	par0 = parameters[0];
	par1 = parameters[1];
	par2 = parameters[2];
}

void fitAndMakePython(){

	TFile* fIN = TFile::Open("efficiencyTree.root");
	fIN->cd("triggerEfficiencyAnalyzer");
	fIN->ls();

	TTree* TriggerEfficiencyTree = (TTree*)fIN->Get("triggerEfficiencyAnalyzer/TriggerEfficiencyTree");

	string triggerName = TriggerEfficiencyTree->GetTitle();
	int nEntries = TriggerEfficiencyTree->GetEntries();
	cout << "Trigger : " << triggerName << endl;
	cout << "Tree entries " << nEntries << endl;

	int passed = 0;
	int all    = nEntries;


	Binning* binning = new Binning(nBins,0.,100.);

	TH1F* h_passed[nBins];
	TH1F* h_all[nBins];
	for(size_t i = 0; i < nBins; ++i){
		TString hName = "h_met_passed";
		hName += i;
		h_passed[i] = new TH1F(hName,"",25,0.,100.);
		TString hName2 = "h_met_all";
		hName2 += i;
		h_all[i]    = new TH1F(hName2,"",25,0.,100.);
	}



	int triggerBit;
	float tauPt,tauEta,MET;

	TriggerEfficiencyTree->SetBranchAddress("TriggerBit",&triggerBit);
	TriggerEfficiencyTree->SetBranchAddress("TauPt",&tauPt);
	TriggerEfficiencyTree->SetBranchAddress("TauEta",&tauEta);
	TriggerEfficiencyTree->SetBranchAddress("MET",&MET);

	for(size_t i = 0; i < nEntries; ++i){
		TriggerEfficiencyTree->GetEntry(i);
		int iBin = binning->bin(MET);
		h_all[iBin]->Fill(tauPt);
		if(triggerBit == 1) {
			passed++;
			h_passed[iBin]->Fill(tauPt);
		}
	}

	PythonWriter* writer = new PythonWriter(triggerName,"TriggerEfficiency_cfi.py");
	writer->fillFakeTauParameters();

	for(size_t i = 0; i < nBins; ++i){
		TH1F* h_eff = h_passed[i];
		h_eff->Divide(h_all[i]);
 		double binMin = binning->binMin(iBin);
		double binMax = binning->binMax(iBin);
		double p0,p1,p2;//parameters[nPar];// = new double[nPar];
		fit(h_eff,p0,p1,p2);
		writer->addBin(binMin,binMax,p0,p1,p2);
//		writer->addBin(binMin,binMax,parameters);
	}

	writer->fillTrueTauParameters();
	for(size_t i = 0; i < nBins; ++i){
                TH1F* h_eff = h_passed[i];
                h_eff->Divide(h_all[i]);
                double binMin = binning->binMin(iBin);
                double binMax = binning->binMax(iBin);
                double p0,p1,p2;//parameters[nPar];// = new double[nPar];
                fit(h_eff,p0,p1,p2);
                writer->addBin(binMin,binMax,p0,p1,p2);  
        }

	delete writer;

	cout << "All events       = " << all << endl;
	cout << "Passed trigger   = " << passed << endl;
	cout << "Total efficiency = " << float(passed)/all << endl;

	exit(0);
}
