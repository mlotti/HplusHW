#include <vector>
#include <iostream>
#include <math.h>
#include <string>

#include "Plotter/interface/Plotter.h"

extern double BR_top_Hplus_function(double,double,double);
extern double signif(double,double,double);

struct NBackGroundForMass {
        NBackGroundForMass(double ns, double tgb, double nb,double m){
                nSignal = ns;
                tanb = tgb;
                nBackgr = nb;
                mass = m;
        }
        double nSignal;
        double tanb;
        double nBackgr;
        double mass;
};

class TanbReach {
    public:
	TanbReach(){}
	~TanbReach(){}

	void SetLuminosity(double value) {luminosity = value;}
	void SetSysError(double value) {sysError = value;}
	void SetCrossSection(double value) {cross_section = value;}
	void SetHiggsMass(double value) {higgsMass = value;}
	void SetMu(double value){mu = value;}
	double TanbLimit(NBackGroundForMass point){
		double nSignalAtLimit = signalAtNsigma(point.nBackgr);
//std::cout << "check nSignalAtLimit " << nSignalAtLimit << std::endl;
		double xSecAtLimit = signalXsecAtNsigma(point.nSignal,point.tanb,nSignalAtLimit);
//std::cout << "check xSecAtLimit " << xSecAtLimit << std::endl;
		return tanbForXsec(xSecAtLimit,higgsMass,mu);
	}
	void PrintRefPoint(NBackGroundForMass point){
		std::cout << "Ref point, mass = " << higgsMass
		          << ", tanb = " << point.tanb
		          << ", Ns = " << point.nSignal
		          << ", Nb = " << point.nBackgr
		          << ", signif = " << signif(point.nSignal,point.nBackgr,0)
		          << ", signif(err) = " << signif(point.nSignal,point.nBackgr,sysError) 
		          << ", Ns@5sigma = " << signalAtNsigma(point.nBackgr)
		          << ", signif(Ns@5sigma) = " << signif(signalAtNsigma(point.nBackgr),point.nBackgr,sysError)
		          << std::endl;
	}

    private:
	double tanbForXsec(double refXsec,double mass,double mu){
		double tanb = 20; // initial guess
		double BR_top_Hplus = BR_top_Hplus_function(mass,tanb,mu);
		double xSec = cross_section*BR_top_Hplus;
		while(fabs(xSec - refXsec) > 0.001 && tanb < 100){
//std::cout << "check tanb " << tanb << std::endl;
			tanb = tanb - 0.1*(xSec - refXsec)/refXsec*tanb;
			BR_top_Hplus = BR_top_Hplus_function(mass,tanb,mu);
			xSec = cross_section*BR_top_Hplus;
		}
		if(tanb > 100) return -1;
		return tanb;
	}

	double signalAtNsigma(double nBackgr, int Nsigma = 5){

		double nSignal = Nsigma*sqrt(nBackgr); //initial guess

		double significance = signif(nSignal,nBackgr,sysError);
		while(fabs(significance - Nsigma) > 0.001){
		    nSignal = nSignal - (significance - Nsigma);
//		    if((significance - Nsigma) > 0) {
//		      nSignal = nSignal - fabs(significance - Nsigma);
//		    }else{
//		      nSignal = nSignal + fabs(significance - Nsigma);
//		    }
		    significance = signif(nSignal,nBackgr,sysError);
		}
		return nSignal;
	}

	double signalXsecAtNsigma(double nSignalAtRef,double tanbAtRef,double nSignalAtLimit){
		double BR_top_Hplus_atRef = BR_top_Hplus_function(higgsMass,tanbAtRef,mu);
		double xSec_atRef = cross_section*BR_top_Hplus_atRef;
		return xSec_atRef*nSignalAtLimit/nSignalAtRef;
	}

	double luminosity;
	double cross_section;
	double higgsMass;
	double mu;
	double sysError;
};

#include <map>

int main(){
    double luminosity = 100;
    std::string algo = "";
    std::map<std::string,std::vector<double> > values;
    for(int iSelection = 0; iSelection < 2;++ iSelection){

	std::vector<int> muPoints;
	muPoints.push_back(-1000);
	muPoints.push_back(-200);
	muPoints.push_back(200);
	muPoints.push_back(1000);

	std::vector<NBackGroundForMass> massPoints;
//Cut based
	if(iSelection == 0) {
	std::cout << "PFTau, cut based" << std::endl; 
	algo = "PFTauCutBased";
//        massPoints.push_back(NBackGroundForMass(luminosity*0.149,20,luminosity*(0.3601+0.2010),80));
        massPoints.push_back(NBackGroundForMass(luminosity*0.1359,20,luminosity*(0.3601+0.2010),90));
	massPoints.push_back(NBackGroundForMass(luminosity*0.1262,20,luminosity*(0.3601+0.2010),100));
	massPoints.push_back(NBackGroundForMass(luminosity*0.0943,20,luminosity*(0.3601+0.2010),120));
	massPoints.push_back(NBackGroundForMass(luminosity*0.0381,20,luminosity*(0.3601+0.2010),140));
	massPoints.push_back(NBackGroundForMass(luminosity*0.00833,20,luminosity*(0.3601+0.2010),160));
	}
//Tanc
	if(iSelection == 1) {
	std::cout << "PFTau, TaNC based" << std::endl;
	algo = "PFTauTaNCBased";
//        massPoints.push_back(NBackGroundForMass(luminosity*0.1579,20,luminosity*(0.1297+0.2192),80));
        massPoints.push_back(NBackGroundForMass(luminosity*0.148,20,luminosity*(0.1297+0.2192),90));
        massPoints.push_back(NBackGroundForMass(luminosity*0.1349,20,luminosity*(0.1297+0.2192),100));
        massPoints.push_back(NBackGroundForMass(luminosity*0.1015,20,luminosity*(0.1297+0.2192),120));
        massPoints.push_back(NBackGroundForMass(luminosity*0.0520,20,luminosity*(0.1297+0.2192),140));
        massPoints.push_back(NBackGroundForMass(luminosity*0.0095,20,luminosity*(0.1297+0.2192),160));
	}

	TanbReach* reach = new TanbReach();
//	reach->SetLuminosity(luminosity);
//	reach->SetSysError(0.1);
	double tt_xsec = 165;
	double BRtauHadronic = 0.648;
	reach->SetCrossSection(tt_xsec*BRtauHadronic);
/*
        double xmin = 50,
               ymin = 0,
               xmax = 180,
               ymax = 100;
	Plotter* plotter = new Plotter("title","m_{H^{#pm}}","tan#beta",xmin,ymin,xmax,ymax);
//	plotter->setOutputFileName("discoveryReach.root");
*/
	for(int iMu = 0; iMu < muPoints.size(); ++iMu){
	    std::cout << "mu = " << muPoints[iMu] << std::endl;
	    reach->SetMu(muPoints[iMu]);

	    std::vector<double> x;
	    std::vector<double> y;
	    std::vector<double> y_err;

	    for(int iMass = 0; iMass < massPoints.size(); ++iMass){

        	reach->SetHiggsMass(massPoints[iMass].mass);

		reach->SetSysError(0);
		double tanbReach = reach->TanbLimit(massPoints[iMass]);
//		reach->PrintRefPoint(massPoints[iMass]);

		reach->SetSysError(0.1);
		double tanbReachWithSysErr = reach->TanbLimit(massPoints[iMass]);
		std::cout << "m = " << massPoints[iMass].mass << " " 
                          << ", tanb reach = " << tanbReach << " " 
                          << ", tanb reach (sys err) = " << tanbReachWithSysErr << std::endl;
//		reach->PrintRefPoint(massPoints[iMass]);

		if(tanbReach > 0){
		  x.push_back(massPoints[iMass].mass);
		  y.push_back(tanbReach);
		  y_err.push_back(tanbReachWithSysErr);
		}
	    }

            char buffer[50];
            if(muPoints[iMu] > 0) sprintf (buffer, "discoveryReach_mu%d", abs(muPoints[iMu]));
            else sprintf (buffer, "discoveryReach_muMinus%d", abs(muPoints[iMu]));
	    std::string plotFileName = std::string(buffer) + "_" + algo;

	    values[plotFileName+"_x"] = x;
	    values[plotFileName+"_y"] = y;
	    values[plotFileName+"_y_err"] = y_err;
	    std::cout << "File name " << plotFileName << std::endl;
/*
//	    plotter->setName(buffer);
            plotter->setName(plotFileName);
//	    plotter->setLegend("",0.2,0.7,0.5,0.9);

	    plotter->x(x);
	    plotter->y(y);

	    plotter->x(x);
	    plotter->y(y_err);

	    plotter->text("CMS",xmin + 0.2*(xmax - xmin),ymin + 0.9*(ymax - ymin));
	    plotter->text("Very preliminary",xmin + 0.1*(xmax - xmin),ymin + 0.82*(ymax - ymin));
            char lumiBuffer[20];
            sprintf (lumiBuffer, "L = %d pb^{-1}", int(luminosity));
	    plotter->text(lumiBuffer,xmin + 0.6*(xmax - xmin),ymin + 0.85*(ymax - ymin));

	    char muBuffer[20];
	    sprintf (muBuffer, "mu = %d GeV/c^{2}", int(muPoints[iMu]));
	    plotter->text(muBuffer,xmin + 0.1*(xmax - xmin),ymin + 0.1*(ymax - ymin));
	    plotter->text("m_{H}^{max} scenario",xmin + 0.1*(xmax - xmin),ymin + 0.2*(ymax - ymin));
	    plotter->text("t#rightarrowbH#pm#rightarrowb#tau#nu#rightarrowhadrons + #nu",xmin + 0.1*(xmax - xmin),ymin + 0.3*(ymax - ymin));


	    plotter->associatedText(0,"No errors",90,0.025);
	    plotter->associatedText(1,"With sys errors",90,0.025);

	    plotter->plot();
*/
	}
    }

    double xmin = 50,
           ymin = 0,
           xmax = 180,
           ymax = 100;
    Plotter* plotter = new Plotter("title","m_{H^{#pm}}","tan#beta",xmin,ymin,xmax,ymax);
    plotter->setName("discoveryReach_mu200");

    std::string plotFileName = "discoveryReach_mu200_PFTauTaNCBased";
    plotter->x(values[plotFileName+"_x"]);
    plotter->y(values[plotFileName+"_y"],1,1,"PFTauTaNCBased");

    plotter->x(values[plotFileName+"_x"]);
    plotter->y(values[plotFileName+"_y_err"],2,1,"PFTauTaNCBased+err");

    plotFileName = "discoveryReach_mu200_PFTauCutBased";
    plotter->x(values[plotFileName+"_x"]);
    plotter->y(values[plotFileName+"_y"],1,2,"PFTauCutBased");

    plotter->x(values[plotFileName+"_x"]);
    plotter->y(values[plotFileName+"_y_err"],2,2,"PFTauCutBased+err");

    plotter->text("CMS",xmin + 0.2*(xmax - xmin),ymin + 0.9*(ymax - ymin));
    plotter->text("Very preliminary",xmin + 0.1*(xmax - xmin),ymin + 0.82*(ymax - ymin));
    char lumiBuffer[20];
    sprintf (lumiBuffer, "L = %d pb^{-1}", int(luminosity));
    plotter->text(lumiBuffer,xmin + 0.6*(xmax - xmin),ymin + 0.85*(ymax - ymin));

    char muBuffer[20];
    sprintf (muBuffer, "mu = %d GeV/c^{2}", 200);
    plotter->text(muBuffer,xmin + 0.1*(xmax - xmin),ymin + 0.1*(ymax - ymin));
    plotter->text("m_{H}^{max} scenario",xmin + 0.1*(xmax - xmin),ymin + 0.2*(ymax - ymin));
    plotter->text("t#rightarrowbH#pm#rightarrowb#tau#nu#rightarrowhadrons + #nu",xmin + 0.1*(xmax - xmin),ymin + 0.3*(ymax - ymin));

//    plotter->associatedText(0,"No errors",90,0.025);
//    plotter->associatedText(1,"With sys errors",90,0.025);

    plotter->setLegend("legendName",0.2,0.7,0.5,0.9);

    plotter->plot();

    return 0;
}
