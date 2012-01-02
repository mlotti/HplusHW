Data-driven control plots

Location of files:
test/controlPlots

Setup of paths to multicrab directories
Make symbolic links to the multicrab directories of
- signal analysis (default link name signalpath)
- signal analysis with fake taus (default link name fakespath)
- signal analysis on EWK control sample (default link name ewkpath)
- QCD measurement (default link name qcdpath; current implementation is for the factorisation-based method, see QCDMeasurementBasic class in 
HiggsAnalysis)
example:
ln -s path_to_the_multicrab_dir signalpath

How to compile and run:
cd test/controlPlots
make
./makeControlPlots

How to edit:
edit the file test/controlPlots/controlPlots.cxx
It should be enough to edit only the parts in the main program. To add for example another QCD measurement, it may be necessary to add a new class 
that is derived from ControlPlot (see QCDControlPlot for an example). The main program is structured like the following:
- The definitions of what files are used for input (the supplied name is the sample directory under the multicrab directory, hplusMergeHistograms.py 
should be runned on the multicrab directory)
- The input files are opened and checked that they are ok
- The luminosity, br(t->bH+), and EWK normalisation constants are set; the paths to the counter histograms are defined
- The frame histogram and the Manager for a given plot are defined (change here the x-axis definitions, if necessary)
- Then all Manager contents are normalised and the histograms for the different inputs are obtained
- The merging of the input histograms to one canvas is done under the comment "Make plots". Change here, if necessary, the specifications of the 
y-axis (min and max), the range of the ratio plot (1-delta .. 1+delta), the titles (xtitle, ytitle), the branching ratio (br), the higgs mass (mass, 
currently not used), and choose the linear/log scale (logy). The complete interface is:
 void makePlot(double min, double max, double delta, string xtitle, string ytitle, double br, double mass, bool logy = true);
- The last item is the selection flow plot. The necessary things to change is the number of bins (to optionally include dphi<130 into the plot), the 
names of the plots to be integrated and the y-axis range in the makePlot -command. Note: the integrating of the distributions should be further 
tested. Currently, no underflow/overflow bins are taken into account (also LandS does not take them into account, the shape given to LandS should 
correspond to the number given by TH1::Integral()).

