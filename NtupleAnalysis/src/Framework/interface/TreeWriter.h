
// -*- c++ -*-
#ifndef Framework_TreeWriter_h
#define Framework_TreeWriter_h

#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/TransverseMass.h"
#include "TDirectory.h"

#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/CommonPlotsHelper.h"
#include "EventSelection/interface/CommonPlotsBase.h"
#include "EventSelection/interface/PUDependencyPlots.h"
#include "Framework/interface/ParameterSet.h"

#include <sstream>
#include <string>
#include <vector>

class ParameterSet;

//
// This class enables the user to write information to Trees after custom selections
// Main application of this class is to create "Skimmed" multicrabs for MVA training purposses
//

class TreeWriter {
public:

  TreeWriter();

  void initialize();

  void write(const Event& event,
		TauSelection::Data tauData,
		ElectronSelection::Data electronData,
		MuonSelection::Data muonData,
  		JetSelection::Data jetData,
	 	BJetSelection::Data bJetData,
  		METSelection::Data METData
		);

  void terminate();

  void book(TDirectory *dir);

  ~TreeWriter();

protected: // Protected for easier unit testing

private:

  TauSelection::Data fTauData;
  ElectronSelection::Data fElectronData;
  MuonSelection::Data fMuonData;
  JetSelection::Data fJetData;
  BJetSelection::Data fBJetData;
  METSelection::Data fMETData;

  std::string name;
  const char *b;

  TFile *f;
  TTree *t;

};


#endif
