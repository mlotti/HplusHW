#include "Plotter/interface/Plotter.h"

using namespace std;

//#include "TCanvas.h"
#include "TH2F.h"
#include "TROOT.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TMath.h"

#include <iostream>

extern void setTDRStyle();
extern void SetLHCHiggsStyle();

Plotter::Plotter(){}
Plotter::Plotter(string title,string x_label,string y_label,double xmin,double ymin,double xmax,double ymax){

	setFrame(title,x_label,y_label,xmin,ymin,xmax,ymax);

	legendXmin = 0;
	legendXmax = 0;
	legendYmin = 0;
	legendYmax = 0;

	clear();
}
Plotter::~Plotter(){
	fOUT->Close();
}

void Plotter::setFrame(string title,string x_label,string y_label,double xmin,double ymin,double xmax,double ymax){
        figTitle = title;
        figXLabel = x_label;
        figYLabel = y_label;
        figXmin   = xmin;
        figXmax   = xmax;
        figYmin   = ymin;
        figYmax   = ymax;
}

void Plotter::clear(){
	xValues.clear();
	yValues.clear();
	yLineStyle.clear();
	yLineColor.clear();
	yLegend.clear();
	texts.clear();
	assocTexts.clear();
	logY = 0;
	lineWidth = 3;
	canvasName = "canvas";
	legendName = "";
}

void Plotter::x(vector<double> values){
	xValues.push_back(values);
}
void Plotter::y(vector<double> values, int lineColor,int lineStyle,string legend){
	yValues.push_back(values);
	yLineStyle.push_back(lineStyle);
	yLineColor.push_back(lineColor);
	yLegend.push_back(legend);
}

void Plotter::setLogY(bool log){
	logY = log;
}

void Plotter::setLineWidth(int value){
	lineWidth = value;
}

void Plotter::setName(string name){
	clear();
        canvasName = name;
}

void Plotter::setOutputFileName(string name){
//        fOUT = TFile::Open(name.c_str(),"RECREATE");
}
void Plotter::setLegend(std::string name,double x1,double y1,double x2,double y2){
	legendName = name;
	legendXmin = x1;//*(figXmax-figXmin);
	legendXmax = x2;//*(figXmax-figXmin);
	legendYmin = y1;//*(figYmax-figYmin);
	legendYmax = y2;//*(figYmax-figYmin);
}

void Plotter::plot(){

	if(xValues.size() != yValues.size()){
		cout << "Number of x and y entries does not match, exiting.." << endl;
		exit(0); 
	}

//	fOUT->cd();

//	SetLHCHiggsStyle();
	setTDRStyle();

	TCanvas* canvas = new TCanvas(canvasName.c_str(),"",500,500);
	canvas->SetFillColor(0);
//	canvas->SetLogy(logY);
	canvas->cd();

	int xBin = 1,
            yBin = 1;

	TH2F* frame = new TH2F("frame","",xBin,figXmin,figXmax,yBin,figYmin,figYmax);
	frame->SetStats(0);
	frame->GetXaxis()->SetTitle(figXLabel.c_str());
	frame->GetYaxis()->SetTitle(figYLabel.c_str());
	frame->Draw();

        TLegend* legend = new TLegend(legendXmin,legendYmin,legendXmax,legendYmax);
	legend->SetFillColor(0);

	if(legendName.length() > 0) legend->SetHeader(legendName.c_str());
	for(size_t j = 0; j < yValues.size(); ++j){
		vector<double> xCurve = xValues[j];
		vector<double> yCurve = yValues[j];
		size_t N = xCurve.size();
		double x[N],y[N];
		for(size_t i = 0; i < N; ++i){
			x[i] = xCurve[i];
			y[i] = yCurve[i];
		}
		TGraph* graph = new TGraph(N,x,y);
		graph->SetName(yLegend[j].c_str());
		graph->SetLineWidth(3);
		graph->SetLineColor(yLineColor[j]);
		graph->SetLineStyle(yLineStyle[j]);
		graph->Draw("C");
		addAssocTexts(j,graph,canvas);
		if(yLegend[j] != "") legend->AddEntry(yLegend[j].c_str(),yLegend[j].c_str(),"L");
	}
	if(legendXmin != legendXmax) legend->Draw();

	for(vector<Text>::const_iterator i = texts.begin();
					 i!= texts.end();++i){
	        TLatex* tex = new TLatex(i->x,i->y,(i->text).c_str());
		tex->SetTextAngle(i->angle);
	        tex->SetLineWidth(2);
		tex->SetTextSize(i->size);
	        tex->Draw();
	}
//legend->Print();
//fOUT->cd();
//	canvas->Write();
	canvas->Print((canvasName+".png").c_str());

	delete frame;
	delete legend;
	delete canvas;
}

void Plotter::text(std::string theText,double xPos,double yPos, double size, double angle){
	texts.push_back(Text(theText,xPos,yPos,size,angle));
}

void Plotter::associatedText(int graphNumber,std::string theText,double xPos,double size){
	assocTexts.push_back(Text(theText,xPos,graphNumber,size,0));
}

void Plotter::addAssocTexts(int graphNumber,TGraph* graph,TCanvas* canvas){
	Text aText;
	bool found = false;
	size_t i = 0;
	while(!found && i < assocTexts.size()){
		if(int(assocTexts[i].y) == graphNumber) {
			aText = assocTexts[i];
			found = true;
		}
		i++;
	}
	if(!found) return;

	double xPos = aText.x;
	double yPos = graph->Eval(xPos);

	double xOffset = 0.05;
	double xPos2 = aText.x + xOffset*(figXmax - figXmin);
	double yPos2 = graph->Eval(xPos2);

	//normalize
	double nxPos  = xPos/(figXmax - figXmin);
	double nxPos2 = xPos2/(figXmax - figXmin);
	double nyPos  = yPos/(figYmax - figYmin);
	double nyPos2 = yPos2/(figYmax - figYmin);

	double angle = 180/TMath::Pi()*TMath::ATan((nyPos2-nyPos)/(nxPos2-nxPos));

	double yOffset = 0.02;
	yPos += yOffset*(figYmax - figYmin)/TMath::Cos(angle*TMath::Pi()/180); 
	texts.push_back(Text(aText.text,xPos,yPos,aText.size,angle));
}

void Plotter::line(double xmin, double ymin, double xmax, double ymax,int lineColor,int lineStyle){
	vector<double> xPoints,yPoints;
	xPoints.push_back(xmin);
	xPoints.push_back(xmax);
	yPoints.push_back(ymin);
	yPoints.push_back(ymax);
	xValues.push_back(xPoints);
	yValues.push_back(yPoints);
        yLineStyle.push_back(lineStyle);
        yLineColor.push_back(lineColor);
}
