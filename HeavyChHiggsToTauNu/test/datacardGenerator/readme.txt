Datacard generator
Purpose:
Generates a directory that contains the necessary datacards (*.txt files) and shape files (*.root files) for LandS to be run on that directory. The 
user should be able to control the program fully from a config file. The running of LandS is described elsewhere (see test/brlimit/README for further 
info).

Location of files:
test/datacardGenerator
The code is in the respective src and interface subdirectories and the main directory contains the makefile and config files.

Setup of paths to multicrab directories:
Make symbolic links to the multicrab directories of
- signal analysis (default link name signal_data; used for data, signal, and EWK with fake taus)
- signal analysis on EWK control sample (default link name ewkpath)
- QCD measurement (default link name QCDpath)
example:
ln -s path_to_the_multicrab_dir signal_data

How to compile and run:
set up ROOT environment, if necessary
cd test/datacardGenerator
make
./datacardgenerator config_file_name
The list of additional options is:
  -h (shows the list of options)
  -v (shows additional detailed info; good for debugging the config file)
  --noshapes (disables the production of a root file containing the shape histograms for LandS)

How to edit the config file:
For latest example, see the file HPlusHadronic_A_rtau_deltaphi160.config.
The config file has two type of entries: comment lines that start with '#' character and commands that have a list of parameters (the command and its 
parameters must be on the same line in the current implementation).
Here's the list of commands:
- description = string : take a string, the description is used for both the datacard description line and for the name of the created results 
directory (no spaces or special characters besides '_' should be used). If multiple description commands are given, only the last one is used.
- masspoint = int : is the id of the mass point (used to tell to samples the mass points for which they are enabled). Multiple masspoint commands can 
be used.
- luminosity = double : the luminosity in 1/fb.
- luminosityScaling = double : a factor for making naive extrapolations to some given value luminosity * luminosityScaling. If a luminosityScaling 
command is used, orange warning messages will be printed upon execution as a safety feature.
- shapeSource = string : the prefix of the created root files containing the shape histograms.
- configInfoHisto = string : path and name of the configInfo histogram in the input root files (used for normalisation)
- counterHisto = string : obsolete feature, not used in current implementation
- observation = { channel=int, function="function_name", function_parameters, mTPlot="string", filePath="string", files={"string", "string", ...} } : 
Provides info to extract the number of observed events. Channel is the LandS specific ID for the final state (use 1 if one uses a separate datacard 
for each final state); function should be a function which can be used to extract the observation value (Constant or Counter). mTPlot is the path and 
histogram name of the mT plot. filePath is the path used for all files and files is a list of root files used as input. Only one observation command 
should be made.
- rate = { id="sample_name", function="function_name", function_parameters } : Provides info to extract the number of events after the selections for 
a given sample or set of samples. The id is used as a tag to identify which files are used (see column command). Function should be a function which 
can be used to extract the rate value (Constant, Counter, or QCDMeasurement). Multiples rate commands can be used (they need to have unique id's).
- nuisance = { id="string", distribution="string", description="string", function="function_name", function_parameters } : Provides info to extract 
the relative uncertainty for a given nuisance parameter from a given sample or set of samples. One nuisance command creates one line into the 
datacard (exception: if nuisances are merged with the mergeNuisances command, only the merged nuisance creates a line into the datacards). The id is 
used to tell which for which columns the nuiscance parameter is active (Note: the id string is used to identify between separate cards, eg. fully 
hadronic and leptonic ones, which are the nuisances that are fully correlated; therefore, before changing the id's check that full correlation 
happens only where appropriate). The distribution is one of the LandS keywords to describe the distribution (tip: use lnN unless convinced to do 
otherwise). Description is a string that is printed in the datacard as a comment to describe the nuisance. Function should be a function which can be 
used to extract a nuisance parameter value (Constant, Counter, maxCounter, Ratio, Shape, or QCDMeasurement). Multiple nuisance commands can be used 
(they need to have unique id's).
- mergeNuisances = { id="string", id2="string" } : Merges two nuisances to be printed on the same line (practical to use for cases, where the 
nuisances are fully correlated, but need to be extracted with different functions and/or parameters). The id of the first nuisance will be printed as 
the id on the datacard.
- column = { channel=int, process=int, mass={int, int, ...}, label="string", rate="string", nuisances={"string", "string", ...}, 
additionalNormalisationFactor=double, mTPlot="string", files={"string", "string", ...} } : This command produces a column into the LandS datacard 
(i.e. a signal or a background). Channel is the LandS specific ID for the final state (use 1 if one uses a separate datacard for each final state). 
Process is a LandS keyword (note: for hplus analysis, use -1 for tt->bHbH signal, 0 for tt->bHbW signal, 1 and 2 for the SM ttbar backgrounds and 3- 
for all other backrounds; note: in current analysis, do not change process numbers because of the hard-coded additional 10 % uncert. of MET leg to 
the trg). mass is the list of masses to which the column is active (tip: use -1 to enable the column for all mass points). label is the name to be 
printed on the column in the datacards (Note: no special characters besides '_' or spaces! Tip: for readability, use max 7 characters). rate is the 
id of the rate command used to exctract the number of events after the full selection. nuisances is the list of id's of nuisance commands used to 
extract the nuisance parameter values for this column. additionalNormalisationFactor is a factor to multiply the number of entries (note: use with 
care! in current implementation only used for EWK w. taus). mTPlot is the path and histogram name of the mT plot. files is a list of root files 
(including path) used as input.

The available functions are:
- Constant : value=double : just a constant rate or relative uncertainty
- Constant : lowerValue=double, upperValue=double : a constant asymmetric relative uncertainty
- Counter: counterHisto="string", counterName="string" : extracts the rate or relative uncertainty from a counter. counterHisto is the path and name 
of the counter histogram. counterName is the name of the counter (a label in the counter histogram).
- maxCounter: counterPaths={"string", "string", ... }, counterName="string" : extracts the rates of N-1 different sources and compares them to the 
nominal rate (tip: usable for JES/MET/Rtau). counterPaths are the names of the counter histograms (incl. path), where the first one is the nominal 
and the other ones are the reference ones. counterName is the name of the counter (a label in the counter histogram).
- Ratio: counterHisto="string", nominatorCounter="string", denominatorCounter="string", scale=double : Calculates the ratio of two different rates 
and scales them to the scale (tip: usable for lepton veto uncertainty). counterHisto is the path and name of the counter histogram. nominatorCounter 
and denominatorCounter are the names of the counter (a label in the counter histogram). scale is the factor which is used to scale the ratio.
- QCDMeasurement: counterHisto="string", histoPrefix="string", QCDBasicSelectionsHisto="string", QCDMETLegHisto="string", QCDTauLegHisto="string", 
QCDBasicMtHisto="string", filePath="string", dataFiles={"string", "string", ... }, EWKMCFiles={"string", "string", ... } : Dedicated function to 
extract the rate or the stat. or syst. uncertainty of the factorised QCD measurement. counterHisto is the name of the counter histogram (incl. path) 
used for normalisation of EWK MC. histoPrefix is the path for the METleg and tau leg and the mT histograms. QCDBasicSelectionsHisto, QCDMETLegHisto, 
and QCDTauLegHisto are histograms that contain event counts as a function of tau pt bin. QCDBasicMtHisto is the name of mT histograms as a function 
of tau pT bin (for the basic mT shape method). filePath is the path to the multicrab directory. dataFiles is a list of input root files for data. 
EWKMCFiles is a list of input root files for EWK MC.

How to add extracting functions:
- create a class that is derived from Extractable.h
- add the interface to the function to ConfigManager (ConfigManager reads and processes the config file and creates the Extractable objects and 
associates them to the appropriate columns/nuisances/rates).
- add/change a config file to use the new function

Notes of usage:
- When executing, check the output for red or orange entries (errors or warnings). If there are errors, the output datacards are most probably 
incorrect.
- More elaborate functions such as QCD measurement should provide some validation histograms (see QCDMeasurementCalculator). These appear usually 
only in the root file produced for the first mass point and do not interfere with LandS.
- For ugly hacks to alter values (if it cannot be done via the existing functions), it is possible to apply changes to specific numbers in 
DatacardGenerator.cc (see as an example the scaling of some values for the luminosity extrapolation). Such hacks should never be propagated to the 
public repository and extra care should be taken to validate that the hack has only the desired effect.
