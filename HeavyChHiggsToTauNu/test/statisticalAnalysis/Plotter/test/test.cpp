#include "interface/Plotter.h"

#include <vector>
using namespace std;

int main(){

	vector<double> x,y,y2,y3,y4;
	x.push_back(0.1); y.push_back(0.1); y2.push_back(0.15); y3.push_back(0.16); y4.push_back(0.06);
	x.push_back(0.9); y.push_back(0.9); y2.push_back(0.95); y3.push_back(0.97); y4.push_back(0.6);

        Plotter* plotter = new Plotter("dummy","x","y",0,0,1,1);
	plotter->setName("testName");
	plotter->setOutputFileName("test.root");
	plotter->setLegend("legendName",0.2,0.7,0.5,0.9);
	plotter->x(x);
	plotter->y(y,1,1,"test1");
	plotter->x(x);
	plotter->y(y2,2,2,"test2");
	plotter->x(x);
        plotter->y(y3,3,3,"test3");
        plotter->x(x);
        plotter->y(y4,1,1);
	plotter->text("TextTest",0.2,0.5);
        plotter->text("TextTest2",0.2,0.2,25);
	plotter->associatedText(0,"TextTest3",0.6,0.01);

	plotter->plot();

	delete plotter;
}
