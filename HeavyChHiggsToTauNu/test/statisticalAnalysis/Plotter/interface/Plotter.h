#ifndef __Plotter__
#define __Plotter__

#include <vector>
#include <string>

#include "TFile.h"
#include "TCanvas.h"
#include "TGraph.h"

class Plotter {
    public:
	Plotter();
	Plotter(std::string,std::string,std::string,double,double,double,double);
	~Plotter();

	void setFrame(std::string,std::string,std::string,double,double,double,double);
	void x(std::vector<double>);
	void y(std::vector<double>,int lineColor = 1,int lineStyle = 1,std::string legend = "");
        void plot();
//	void plot(std::string);
	void setLogY(bool);
	void setLineWidth(int);
	void setName(std::string);
	void setOutputFileName(std::string);
	void setLegend(std::string,double,double,double,double);
	void text(std::string,double,double,double size = 0.05,double angle = 0);
	void associatedText(int,std::string,double,double size = 0.05);
	void addAssocTexts(int,TGraph*,TCanvas*);
	void line(double,double,double,double,int lineColor = 1,int lineStyle = 1);

	void clear();

	struct Text {
	   Text(){}
	   Text(std::string tIN,double xIN, double yIN, double sIN, double aIN){
		text = tIN;
		x    = xIN;
		y    = yIN;
		angle = aIN;
		size = sIN;
	   } 
	   std::string text;
	   double x,y,angle,size;
	};

    private:
	std::string figTitle,
	            figXLabel,
	            figYLabel;
	double figXmin,
	       figXmax,
	       figYmin,
	       figYmax;

	std::vector< std::vector<double> > xValues;
	std::vector< std::vector<double> > yValues;
	std::vector<int> yLineStyle;
	std::vector<int> yLineColor;
	std::vector<std::string> yLegend;

	bool logY;
	int lineWidth;
	std::string canvasName;
	std::string legendName;
	double legendXmin,
               legendXmax,
               legendYmin,
               legendYmax;

	TFile* fOUT;
	std::vector<Text> texts;
	std::vector<Text> assocTexts;
};
#endif
