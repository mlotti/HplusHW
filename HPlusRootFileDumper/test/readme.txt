H+ ROOT file dumper
===================

Aim of the code:
----------------
To dump all the relevant variables from CMSSW/PAT to a ROOT tree for
more thorough analysis and plotting. The use case is selected by the
python files in the test-directory.

Current working version
-----------------------
CMSSW_3_6_1

To install:
-----------
setup your local CMSSW area:
scram project CMSSW CMSSW_x_y_z
cd CMSSW_x_y_z/src
git clone http://cmsdoc.cern.ch/~wendland/HiggsAnalysis.git
cvs co -r V03-28-04 DataFormats/JetReco
cvs co -r V00-16-00 DataFormats/TauReco
cvs co -r V00-23-00 RecoTauTag/RecoTau
cvs co -r V00-21-00 RecoTauTag/Configuration
cvs co HiggsAnalysis/Skimming
rm HiggsAnalysis/Skimming/python/earlyDataInterestingEvents_cff.py

To compile:
-----------
Compile everything from CMSSW_x_y_z/src   
  scram b -r -j 4

To submit with crab:
--------------------
(compile first)
cd HiggsAnalysis/HPlusRootFileDumper/test
(choose tau collection / parameters in the python file)
(setup environment for grid and crab:)
source /afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.csh
cmsenv
source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh
(edit the desired crab.cfg file as needed)
crab -cfg (config file; default: crab.cfg) -create -submit all

To merge the crab output files:
-------------------------------
Old info:
Copy the directory
  test/combineAnalysisPackRootFiles
to a machine with access to the StorageElement (e.g. jade).
Follow the instructions in the readme.txt file in that directory.

In the future the handling of multiple data files should occur
automatically by crab.

tau-jet identification
======================
Classes:
HPlusTauDumperBase
HPlusTauDumperCaloTau : public HPlusTauDumperBase
HPlusTauDumperPF : public HPlusTauDumperBase
HPlusTauIDRootFileDumper : public edm::EDAnalyzer

Python file:
test/HPlusTauIDRootFileDumper_cfg.py

Select the appropriate tau collection name (tauCollectionName) in the
python file. Select also the input file(s).

To run (interactively) type:
cd HPlusRootFileDumper/test
cmsenv
cmsRun HPlusTauIDRootFileDumper_cfg.py

Guidelines for filling root tree items
======================================
The dataformat is edm ROOT trees with short (and unique) aliases. The
data is written by an EDProducer. You need to add the following
things:
- produce-declarations in constructor, for example:
    std::string alias;
    produces<std::vector<math::XYZVector> >(alias = "jetE").setBranchAlias(alias);
(note: the alias must be unique)
- filling via auto_ptr to be called for each event or jet, for example:
    std::auto_ptr<std::vector<math::XYZVector> >
      myDataJetE(new std::vector<math::XYZVector>);
    for ( ... loop over PF taus ... )
      myDataJetE->push_back(myPFJetRef->momentum());
    iEvent.put(myDataJetE, "jetE");

Supported types range from int, float, double to std::vector and CMSSW
objects. Note: TVector3 or TLorentzVector are not supported; please
use math::XYZVector instead.

For data output with several items per event (such as tauID,
i.e. multiple jets saved per event), use std::vector to save each jet.

For a tutorial about EDProducers, see
https://twiki.cern.ch/twiki/bin/viewauth/CMS/WorkBookEDMTutorialProducer

Event selection
===============
Event selection is done via EDFilters. They are capable of producing
data items to the edm ROOT tree.

... work in progress ...

Event counters and histogramming
================================
Full support for these properties are given via the base class
HPlusAnalysisBase, which has a pointer to these objects. The
histograms and counters will be saved to a separate ROOT file via
TFileService.

Note: in the future, the counters could be included in the luminosity
block data. Then an EDAnalyzer could be used to print the counters.

Example for the usage of event counters:
(in private part of class header)
  int fCounterIdAllEvents;
(in constructor / job begin method)
  fCounterIdAllEvents = fCounter->addCounter("All events");
(in appropriate place when one wants to add the counter by one)
  fCounter->addCount(fCounterIdAllEvents);

Example for the usage of histogramming:
(in private part of class header)
  TH1F* hMyHistogram;
(in constructor / job begin method)
  hMyHistogram = fFileService->make<TH1F>("SubCounters",
  "SubCounters;SubCounter;N", 100, 0, 200);
(the syntax here: name to appear in the root file, title:x axis
title:y axis title, number of bins, minimum x value, maximum x value)
(in appropriate place when one wants to fill the histogram)
  hMyHistogram->Fill(1234134);
