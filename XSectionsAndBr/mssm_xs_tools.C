#include "mssm_xs_tools.h"
#include <iostream>


mssm_xs_tools::mssm_xs_tools(const char* filename, bool kINT, unsigned verbosity) : verbosity_(verbosity), kINTERPOL_(kINT){
  if(verbosity>99){
    std::cout << "Welcome to the MSSM neutral cross section tool (v1.0). In case of questions contact:"
              << std::endl
              << " Allison Mc Carn /  ATLAS (allison.renae.mc.carn@cern.ch)," << std::endl
              << " Trevor Vickey   /  ATLAS (trevor.vickey@cern.ch),        " << std::endl
              << " Felix Frensch   /  CMS   (felix.frensch@cern.ch)         " << std::endl
              << " Roger Wolf      /  CMS   (roger.wolf@cern.ch),           " << std::endl
              << " Stefan Liebler  / Theory (stefan.liebler@desy.de),       " << std::endl
              << " Michael Spira   / Theory (michael.spira@psi.ch),         " << std::endl
              << " Pietro Slavich  / Theory (slavich@lpthe.jussieu.fr).     " << std::endl;
              
    }
  if(!filename){
    std::cout << "Chose input file using the method mssm_xs_tools::setup()" << std::endl;
  }
  else{
    input_ = new TFile(filename);
  }
}

void 
mssm_xs_tools::setup(const char* filename){
  /* ______________________________________________________________________________________________
   * If not available, yet open input file from full path specified in [filename]. If input_ does
   * already point to a file nothing is done. This quarantees that only one file can be opened for
   * one instance of the class.  
   */
  if(!input_){
    input_ = new TFile(filename);
  }
  return;
}

std::string 
mssm_xs_tools::br_rule(const char* decay){
  /* ______________________________________________________________________________________________
   * Function argument [decay] expected to be of special form (e.g. "A->tautau"). Search for 
   * deliminator "->" required to be present in [decay]. Split argument: first block corresponds to 
   * building block [BOSON], second block to building block [DECAY]. Prefix histogram name with 
   * "br", append [BOSON], append [DECAY], separated by "_" (histogram name in example above: 
   * "br_A_tautau").
   */
  std::string name; 
  std::string source(decay);
  if(source.find("->")!=std::string::npos){
    name = std::string("br")+"_"+source.substr(0, source.find("->"))+"_"+source.substr(source.find("->")+2);
  }
 return name;  
}

std::string
mssm_xs_tools::width_rule(const char* boson){
  /* ______________________________________________________________________________________________
   * Function agrument [boson] expected to be of special form (e.g. "H"). Function argument 
   * corresponds to building block [BOSON] of histogram name. Prefix histogram name with 
   * "width", append [BOSON], separated by "_" (histgoram name in example above: "width_H");
   */
  return std::string("width")+"_"+std::string(boson);
} 

std::string 
mssm_xs_tools::xsec_rule(const char* mode){
  /* ______________________________________________________________________________________________
   * Function argument [mode] expected to be of special form (e.g. "gg->A::scaleUp"); "->" and "::"
   * are deliminators of building blocks; "->" is required to be present, while"::" is optional. 
   * Search for deliminators "->" (required to be present) and "::" (optional) in [mode]. Split 
   * argument: first block corresponds to [PROD], second block to [BOSON], the third block (option-
   * al) to [UNCERT]. Prefix histogram name with "xs", append [PROD], append [BOSON], append 
   * [UNCERT] if available, seperated by "_" (histogram name in example above: "xs_gg_A_scaleUp").
   */
  std::string source(mode);
  std::string process = source.find("->")!=std::string::npos ? source.substr(0, source.find("->")) : std::string();
  std::string uncert  = source.find("::")!=std::string::npos ? source.substr(source.rfind("::")+2) : std::string();
  std::string boson   = source.substr(source.find("->")+2, source.rfind("::")-(source.find("->")+2));
  std::string name; 
  if(!process.empty()){
    name = std::string("xs")+"_"+process+"_"+boson+(uncert.empty()? uncert : std::string("_")+uncert);
  }
 return name;  
}

std::string 
mssm_xs_tools::mass_rule(const char* boson){
  /* ______________________________________________________________________________________________
   * Function agrument [boson] expected to be of special form (e.g. "H"). Function argument corres-
   * ponds to building block [BOSON] of histogram name. Prefix histogram name with "m", append 
   * [BOSON],  seperated by "_" (histgoram name in example above: "m_H");
   */
  return std::string("m")+"_"+std::string(boson);
}

TH2F* 
mssm_xs_tools::hist(std::string histname){
  /* ______________________________________________________________________________________________
   * Check if a histogram with name [histname] is already on stack. If so return historam. If not 
   * try to get a histogram with name [histname] from the input file, cast to TH2F*; add histogram 
   * on stack with key [histogramname]. If getting the histogram from the input file was not 
   * successful issue a WARNING and return a NULL pointer. For verbosity_>2 issue  MESSAGE that a 
   * histogram with name [histname] has been read from the input file upon successful completion. 
   * Save histogram on stack for future use. Return pointer to histogram.
   */  
  if(hists_.find(histname) == hists_.end()){
    // hist not on stack; read from file; if it fails return NULL.
    hists_[std::string(histname)] = (TH2F*) input_->Get(histname.c_str());
    //std::cout << "* " << hists_[std::string(histname)]->GetName() << std::endl;
    if(!hists_.find(histname)->second){
      std::cout << "WARNING: required histogram " 
                << "[" << histname << "] " 
                << "does not exist in input file " 
                << "[" << input_->GetName() << "]" 
                << std::endl
                << "         " 
                << "return NULL..." 
                << std::endl;
      return NULL;
    }
    else{
      // cash maximal number of bins on x- (mA) and y- (tanb) axis of TH2F, 
      // used to define the boundaries of the histogram when running in 
      // interpolation mode
      nbinsX_ = hists_.find(histname)->second->GetXaxis()->GetNbins();
      nbinsY_ = hists_.find(histname)->second->GetYaxis()->GetNbins();     
      if(verbosity_>2){
        std::cout << "MESSAGE: read histogram " 
                  << "[" << histname << "] " 
                  << "from input file " 
                  << "[" << input_->GetName() << "]" 
                  << std::endl;
      }
    } 
  }
  return hists_.find(histname)->second;
}
