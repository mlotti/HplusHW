// -*- c++ -*-
#ifndef EventSelection_TopologySelection_h
#define EventSelection_TopologySelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/Jet.h"
#include "EventSelection/interface/JetSelection.h"
#include "Framework/interface/EventCounter.h"
#include "Tools/interface/DirectionalCut.h"
#include "Auxiliary/interface/Table.h"
#include "Auxiliary/interface/Tools.h"
#include <boost/concept_check.hpp>
#include <string>
#include <vector>

// ROOT
// #include "TDirectory.h"
// #include "Math/VectorUtil.h"
#include "TMatrixDSym.h"
#include "TMatrixDSymEigen.h"

class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

class TopologySelection: public BaseSelection {
public:
  class Data {
  public:
    // The reason for pointer instead of reference is that const
    // reference allows temporaries, while const pointer does not.
    // Here the object pointed-to must live longer than this object.
    Data();
    ~Data();

    /// Status of passing event selection
    bool passedSelection() const { return bPassedSelection; }

    // Sphericity Momentum Tensor (3D)
    const double Sphericity() const { return fSphericity; }
    const double SphericityT() const { return fSphericityT; }
    const double Aplanarity() const { return fAplanarity; }
    const double Planarity() const { return fPlanarity; }
    const double Y() const { return fY; }

    // Sphericity Momentum Tensor (2D)
    const double Circularity() const { return fCircularity; }

    // Third jet resolution
    const double y23() const { return fY23; }

    // Linear Momentum Tensor
    const double Cparameter() const { return fCparameter; }
    const double Dparameter() const { return fDparameter; }
    const double FoxWolframMoment() const { return fFoxWolframMoment; }

    // AlphaT related variables    
    const double AlphaT() const { return fAlphaT; };
    const double HT() const { return fHT; }
    const double JT() const { return fJT; }
    const double MHT() const { return fMHT; }
    const double Centrality() const { return fCentrality; }     

    friend class TopologySelection;

  private:
    // Boolean for passing selection
    bool bPassedSelection;

    // Sphericity Momentum Tensor (3D)
    double fSphericity, fSphericityT, fAplanarity, fPlanarity, fY;

    // Sphericity Momentum Tensor (2D)
    double fCircularity;

    // Third jet resolution
    double fY23;

    // Linear Momentum Tensor (C, D, Second Fox-Wolfram Moment)
    double fCparameter, fDparameter, fFoxWolframMoment;

    // AlphaT related variables
    double fAlphaT, fHT, fJT, fMHT, fCentrality;
 
  };
  
  // Main class
  // Constructor with histogramming
  explicit TopologySelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");

  // Constructor without histogramming
  explicit TopologySelection(const ParameterSet& config);
  virtual ~TopologySelection();
  
  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event, const JetSelection::Data& jetData);

  // analyze does fill histograms and incrementes counters
  Data analyze(const Event& event, const JetSelection::Data& jetData);

private:
  // Initialisation called from constructor
  void initialize(const ParameterSet& config);

  // The actual selection
  Data privateAnalyze(const Event& event, const JetSelection::Data& jetData);
  
  // Routine for calculating the alphaT-variable and related values
  void calculateAlphaT(const JetSelection::Data& jetData, Data& output);

  // Routine for calculating the Momentum Tensor Matrix (3D)
  TMatrixDSym ComputeMomentumTensor(const JetSelection::Data& jetData, Data& output, double r = 2.0);

  // Routine for calculating the Momentum Tensor Matrix (2D)
  TMatrixDSym ComputeMomentumTensor2D(const JetSelection::Data& jetData, Data& output);
  
  // Routine for calculating the Momentum Tensor Matrix Eigeinvalues (3D)
  std::vector<float> GetMomentumTensorEigenValues(const JetSelection::Data& jetData, Data& output);

  // Routine for calculating the Momentum Tensor Matrix Eigeinvalues (2D)
  std::vector<float> GetMomentumTensorEigenValues2D(const JetSelection::Data& jetData, Data& output);

  // Routine for calculating the Sphericity Tensor Matrix Eigeinvalues (2D)
  std::vector<float> GetSphericityTensorEigenValues(const JetSelection::Data& jetData, Data& output);

  // Input parameters
  const DirectionalCut<double> fSphericityCut;
  const DirectionalCut<double> fAplanarityCut;
  const DirectionalCut<double> fPlanarityCut;
  const DirectionalCut<double> fCircularityCut;
  const DirectionalCut<double> fY23Cut;
  const DirectionalCut<double> fCparameterCut;
  const DirectionalCut<double> fDparameterCut;
  const DirectionalCut<double> fFoxWolframMomentCut;
  const DirectionalCut<double> fAlphaTCut;
  const DirectionalCut<double> fCentralityCut;

  // Helper objects
  Tools auxTools;

  // Event counter for passing selection
  Count cPassedTopologySelection;

  // Sub counters
  Count cSubAll;
  Count cSubPassedSphericity;
  Count cSubPassedAplanarity;
  Count cSubPassedPlanarity;
  Count cSubPassedCircularity;
  Count cSubPassedY23;
  Count cSubPassedCparameter;
  Count cSubPassedDparameter;
  Count cSubPassedFoxWolframMoment;
  Count cSubPassedAlphaT;
  Count cSubPassedCentrality;

  // Histograms (1D)
  WrappedTH1 *h_AlphaT_After;
  WrappedTH1 *h_AlphaT_Before;
  WrappedTH1 *h_Aplanarity_After;
  WrappedTH1 *h_Aplanarity_Before;
  WrappedTH1 *h_CParameter_After;
  WrappedTH1 *h_CParameter_Before;
  WrappedTH1 *h_Centrality_After;
  WrappedTH1 *h_Centrality_Before;
  WrappedTH1 *h_Circularity_After;
  WrappedTH1 *h_Circularity_Before;
  WrappedTH1 *h_DParameter_After;
  WrappedTH1 *h_DParameter_Before;
  WrappedTH1 *h_FoxWolframMoment_After;
  WrappedTH1 *h_FoxWolframMoment_Before;
  WrappedTH1 *h_HT_After;
  WrappedTH1 *h_HT_Before;
  WrappedTH1 *h_JT_After;
  WrappedTH1 *h_JT_Before;
  WrappedTH1 *h_MHT_After;
  WrappedTH1 *h_MHT_Before;
  WrappedTH1 *h_Planarity_After;
  WrappedTH1 *h_Planarity_Before;
  WrappedTH1 *h_SphericityT_After;
  WrappedTH1 *h_SphericityT_Before;
  WrappedTH1 *h_Sphericity_After;
  WrappedTH1 *h_Sphericity_Before;
  WrappedTH1 *h_Y_After;
  WrappedTH1 *h_Y_Before;
  WrappedTH1 *h_y23_After;
  WrappedTH1 *h_y23_Before;

  // Histograms (2D)
  WrappedTH2 *h_S_Vs_Y_Before;
  WrappedTH2 *h_S_Vs_Y_After;

};

#endif
