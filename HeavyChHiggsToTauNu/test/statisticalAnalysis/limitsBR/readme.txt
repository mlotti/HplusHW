===== making BR limit plots =====================

1) precalculations

You don't necessarily need to precalculate the needed 
Poisson CL values, but please consider this (see below).  

2) plotting

To make the plots, start with

 root poisson.C

You will then see the instructions, for instance:

 Usage in root: .x poisson.C(n)
 where n=1 for hard cuts, 3 jets
       n=2 for soft cuts, 3 jets
       ...

Then continue by typing for instance ".x poisson.C(2)"
to produce the plots for the case of soft cuts, 3 jets.
The png files are generated automatically.

3) making new kind of plots

To make plots for new cuts, you need to hard-code the 
new values.

To change luminosity, just change this hard-coded value,
the value in the plots changes accordingly:

 Double_t myLuminosity = 40;//pb-1

To use 100% uncertainty in QCD, toggle this global 
variable (bad style, yes...):

 bool QCDuncertainty100 = true;

Tevatron results: toggle the following to show/hide 
Tevatron results:
 
 bool plotTevatron1fb = true

===== precalculation of Poisson CLs =============

To run BR limit plotting, it is strongly suggested to
first calculate the needed Poisson CL values in a 
separate file with 

 root -l makePoissonFile.C .

This can take several tens of minutes but makes the 
plotting approximately ten times faster.  It is enough
to run this calculation only once.

=================================================
