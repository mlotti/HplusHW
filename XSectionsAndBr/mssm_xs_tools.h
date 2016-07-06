#ifndef mssm_xs_tools_h
#define mssm_xs_tools_h

#include <map>
#include <cmath>
#include <string>
#include <iostream>

#include "TH2F.h"
#include "TFile.h"

/* ________________________________________________________________________________________________
 * Class: mssm_xs_tools
 * 
 * This is a class to provide a facilitated interface to mass relations, decay widths, branching 
 * fractions and production cross sections for all Higgs bosons (A/H/h/H+) of various benchmark 
 * models of the MSSM. This information is usually provided in form of 2d (TH2F) histograms in root 
 * input files linked to the LHCXSWG-3 TWiki page (*). It is usually parametrized as a function of
 * the pseudoscalar neutral Higgs boson mass, mA, and the ratio between the vacuum expectation 
 * values, tanb=v1/v2, of the two Higgs doublets in the MSSM, in the case of neutral Higgs boson 
 * cross sections and in as a function of the charged Higgs boson mass mH+ and tanb in the case of 
 * charged Higgs boson cross sections.   
 * 
 * The access functions provided in this class are supposed to facilitate the process of finding 
 * the proper histogram (following LHCXSWG-3 internal naming conventions) and the proper bin in the 
 * 2d histogram corresponding to mA (resp. mH+) and tanb, of which the latter is a root technicali-
 * ty (cf. mssm_xs_tools::read for more details).   
 * 
 * The names of the 2d histograms are build from building block separated by "_", to identify the 
 * contained information. The following building blocks exist:
 * 
 * [MASS]   : indicating mass ("m"); 
 * [WIDTH]  : indicating width ("width");
 * [BOSON]  : indicating the boson type, used for cross section and decay info ("A", "H", "h");
 * [PROD]   : indicating the production type, separated by gluon-gluon fusion and production in 
 *            association with b-quarks (in various flavour schemes, "gg", "bb4F", "bb5f", bbSantander); 
 * [UNCERT] : indicating the kind of variation corresponding to a given uncertainty ("scaleUp", 
 *            "scaleDown", pdfasUp", "pdfasDown");
 * [DECAY]  : indicating the decay type (e.g. "tautau", "mumu", "bb", ...).
 * 
 * The exact conventions of these building blocks are not always defined in a unique way and might 
 * change with time. The user should not worry about such changes. For this reasons the access 
 * functions provided by this class make use of a set of internal translation rules from a more 
 * intuitive naming scheme to the histogram names. For the sake of simplicity this naming scheme 
 * partially makes use use of the naming conventions as used for the individual building blocks of 
 * the histogram names. For more information check the documentation for each individual transla-
 * tion rule in the class implementation. In the naming scheem used throughtout this class the 
 * following rules apply:
 * 
 * Production: separate building block for [PROD] from building block for [BOSON] by "->" (e.g. 
 *             "gg->A"). This will provide you with the corresponding central value for the cross 
 *             section. There is a way to obtain the cross sections after uncertainty shifts by 
 *             appending a tag for the [UNCERT] type to the production string, separated by "::" (
 *             "gg->A::scaleUp"). 
 * Decay     : separate building block for [BOSON] from building block for [DECAY] by "->" (e.g.
 *             "A->tautau"). This will provide you with the branching fraction for the correspon-
 *             ding decay.
 * Mass/Width: just give the building block for the [BOSON] type as function argument (e.g. "A", 
 *             "H", "h", "Hp"). 
 * 
 * In case that called histograms so not exist in the root input file a WARNING is issued and a 
 * NULL pointer for TH2F is returned. Make sure you catch these WARNINGS in further use of this 
 * class. To hide away also this simple logic from the user a full set of fully documented pre-de-
 * fined access functions for all available information is also provided. These function can also 
 * be used as reference for fuerther examples of the access logic described above (e.g. concerning 
 * further conventions used for numerous building blocks of type [DECAY]).
 * 
 * PHYSICS CONTENT:
 * 
 * (*)
 * https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHXSWG3
 */
class mssm_xs_tools{
  
 public:
  /// constructor
  mssm_xs_tools(const char* filename="", bool kINTERPLOTATION=false, unsigned verbosity=0);
  /// destructor
  ~mssm_xs_tools(){};

  /// a save way to access a histogram from the stack; returns NULL if histogram does not exist on stack
  TH2F* hist(std::string name);
  /// get mass of a given Higgs boson for given values of mA and tanb (in GeV)
  double mass(const char* boson, double mA, double tanb){ return read(boson, mA, tanb, &mssm_xs_tools::mass_rule); }
  /// get totla decay width of a given Higgs boson for given values of mA and tanb (in GeV)
  double width(const char* boson, double mA, double tanb){ return read(boson, mA, tanb, &mssm_xs_tools::width_rule); }
  /// get branching fraction for a given decay of a given Higgs boson for given values of mA and tanb
  double br(const char* decay, double mA, double tanb){ return read(decay, mA, tanb, &mssm_xs_tools::br_rule); }
  /// get production cross section for a given production model of a given Higgs boson for given values of mA and tanb (in pb)
  double xsec(const char* mode, double mA, double tanb){ return read(mode, mA, tanb, &mssm_xs_tools::xsec_rule); }

  /*
   * pre-defined access function for the masses for A/H/h/H+
   */
  /// get mH for given value of mA and tanb (in GeV)
  double mH(double mA, double tanb){ return mass("H", mA, tanb); }
  /// get mh for given value of mA and tanb (in GeV)
  double mh(double mA, double tanb){ return mass("h", mA, tanb); }
  /// get mH+ for given value of mA and tanb (in GeV)
  double mHp(double mA, double tanb){ return mass("Hp", mA, tanb); }
  /// get mA for given value of mu in low-mH scenario (need a more complex name
  /// name of the member function here not to shadow it by the function arg in 
  /// GeV)
  double mu2mA(double mu, double tanb){ return mass("A", mu, tanb); }

  /*
   * pre-defined access functions for total decay widths for A/H/h/H+
   */
  // get total decay width for A  (in GeV)
  double width_A(double mA, double tanb){ return width("A", mA, tanb); }
  // get total decay width for H  (in GeV)
  double width_H(double mA, double tanb){ return width("H", mA, tanb); }
  // get total decay width for h  (in GeV)
  double width_h(double mA, double tanb){ return width("h", mA, tanb); }
  // get total decay width for H+  (in GeV)
  double width_Hp(double mA, double tanb){ return width("Hp", mA, tanb); }
  // get total decay width for t->H+b  (in GeV)
  double width_tHpb(double mA, double tanb){ return width("t_Hpb", mA, tanb); }
  
  /*
   * pre-defined access functions for A/H/h/H+ decays into quarks
   */
  /// get BR(A->tt) for given value of mA and tanb
  double br_Att(double mA, double tanb){ return br("A->tt", mA, tanb); }
  /// get BR(H->tt) for given value of mA and tanb
  double br_Htt(double mA, double tanb){ return br("H->tt", mA, tanb); }
  /// get BR(h->tt) for given value of mA and tanb
  double br_htt(double mA, double tanb){ return br("h->tt", mA, tanb); }
  /// get BR(A->bb) for given value of mA and tanb
  double br_Abb(double mA, double tanb){ return br("A->bb", mA, tanb); }
  /// get BR(H->bb) for given value of mA and tanb
  double br_Hbb(double mA, double tanb){ return br("H->bb", mA, tanb); }
  /// get BR(h->bb) for given value of mA and tanb
  double br_hbb(double mA, double tanb){ return br("h->bb", mA, tanb); }
  /// get BR(A->cc) for given value of mA and tanb
  double br_Acc(double mA, double tanb){ return br("A->cc", mA, tanb); }
  /// get BR(H->cc) for given value of mA and tanb
  double br_Hcc(double mA, double tanb){ return br("H->cc", mA, tanb); }
  /// get BR(h->cc) for given value of mA and tanb
  double br_hcc(double mA, double tanb){ return br("h->cc", mA, tanb); }
  /// get BR(A->ss) for given value of mA and tanb
  double br_Ass(double mA, double tanb){ return br("A->ss", mA, tanb); }
  /// get BR(H->ss) for given value of mA and tanb
  double br_Hss(double mA, double tanb){ return br("H->ss", mA, tanb); }
  /// get BR(h->ss) for given value of mA and tanb
  double br_hss(double mA, double tanb){ return br("h->ss", mA, tanb); }
  /// get BR(A->uu) for given value of mA and tanb
  double br_Auu(double mA, double tanb){ return br("A->uu", mA, tanb); }
  /// get BR(H->uu) for given value of mA and tanb
  double br_Huu(double mA, double tanb){ return br("H->uu", mA, tanb); }
  /// get BR(h->uu) for given value of mA and tanb
  double br_huu(double mA, double tanb){ return br("h->uu", mA, tanb); }
  /// get BR(A->dd) for given value of mA and tanb
  double br_Add(double mA, double tanb){ return br("A->dd", mA, tanb); }
  /// get BR(H->dd) for given value of mA and tanb
  double br_Hdd(double mA, double tanb){ return br("H->dd", mA, tanb); }
  /// get BR(h->dd) for given value of mA and tanb
  double br_hdd(double mA, double tanb){ return br("h->dd", mA, tanb); }
  /// get BR(t->H+b) for given value of mA and tanb
  double br_tHpb(double mA, double tanb){ return br("t->Hpb", mA, tanb); }
  /// get BR(H+->tbb) for given value of mA and tanb
  double br_Hptbb(double mA, double tanb){ return br("Hp->tbb", mA, tanb); }
  /// get BR(H+->tsb) for given value of mA and tanb
  double br_Hptsb(double mA, double tanb){ return br("Hp->tsb", mA, tanb); }
  /// get BR(H+->tdb) for given value of mA and tanb
  double br_Hptdb(double mA, double tanb){ return br("Hp->tdb", mA, tanb); }
  /// get BR(H+->cbb) for given value of mA and tanb
  double br_Hpcbb(double mA, double tanb){ return br("Hp->cbb", mA, tanb); }
  /// get BR(H+->csb) for given value of mA and tanb
  double br_Hpcsb(double mA, double tanb){ return br("Hp->csb", mA, tanb); }
  /// get BR(H+->cdb) for given value of mA and tanb
  double br_Hpcdb(double mA, double tanb){ return br("Hp->cdb", mA, tanb); }
  /// get BR(H+->ubb) for given value of mA and tanb
  double br_Hpubb(double mA, double tanb){ return br("Hp->ubb", mA, tanb); }
  /// get BR(H+->usb) for given value of mA and tanb
  double br_Hpusb(double mA, double tanb){ return br("Hp->usb", mA, tanb); }
  /// get BR(H+->udb) for given value of mA and tanb
  double br_Hpudb(double mA, double tanb){ return br("Hp->udb", mA, tanb); }
  
  /*
   * pre-defined access functions for A/H/h/H+ decays into leptons
   */
  /// get BR(A->tautau) for given value of mA and tanb
  double br_Atautau(double mA, double tanb){ return br("A->tautau", mA, tanb); }
  /// get BR(H->tautau) for given value of mA and tanb
  double br_Htautau(double mA, double tanb){ return br("H->tautau", mA, tanb); }
  /// get BR(h->tautau) for given value of mA and tanb
  double br_htautau(double mA, double tanb){ return br("h->tautau", mA, tanb); }
  /// get BR(A->mumu) for given value of mA and tanb
  double br_Amumu(double mA, double tanb){ return br("A->mumu", mA, tanb); }
  /// get BR(H->tautau) for given value of mA and tanb
  double br_Hmumu(double mA, double tanb){ return br("H->mumu", mA, tanb); }
  /// get BR(h->mumu) for given value of mA and tanb
  double br_hmumu(double mA, double tanb){ return br("h->mumu", mA, tanb); }
  /// get BR(A->ee) for given value of mA and tanb
  double br_Aee(double mA, double tanb){ return br("A->ee", mA, tanb); }
  /// get BR(H->ee) for given value of mA and tanb
  double br_Hee(double mA, double tanb){ return br("H->ee", mA, tanb); }
  /// get BR(h->ee) for given value of mA and tanb
  double br_hee(double mA, double tanb){ return br("h->ee", mA, tanb); }
  /// get BR(H+->taunu) for given value of mA and tanb
  double br_Hptaunu(double mA, double tanb){ return br("Hp->taunu", mA, tanb); }
  /// get BR(H+->munu) for given value of mA and tanb
  double br_Hpmunu(double mA, double tanb){ return br("Hp->munu", mA, tanb); }
  /// get BR(H+->enu) for given value of mA and tanb
  double br_Hpenu(double mA, double tanb){ return br("Hp->enu", mA, tanb); }

  /*
   * pre-defined access functions for A/H/h decays into gauge bosons
   */
  /// get BR(A->WW) for given value of mA and tanb
  double br_AWW(double mA, double tanb){ return br("A->WW", mA, tanb); }
  /// get BR(H->WW) for given value of mA and tanb
  double br_HWW(double mA, double tanb){ return br("H->WW", mA, tanb); }
  /// get BR(h->WW) for given value of mA and tanb
  double br_hWW(double mA, double tanb){ return br("h->WW", mA, tanb); }
  /// get BR(A->ZZ) for given value of mA and tanb
  double br_AZZ(double mA, double tanb){ return br("A->ZZ", mA, tanb); }
  /// get BR(H->ZZ) for given value of mA and tanb
  double br_HZZ(double mA, double tanb){ return br("H->ZZ", mA, tanb); }
  /// get BR(h->ZZ) for given value of mA and tanb
  double br_hZZ(double mA, double tanb){ return br("h->ZZ", mA, tanb); }
  /// get BR(A->gg) for given value of mA and tanb
  double br_Agg(double mA, double tanb){ return br("A->gluglu", mA, tanb); }
  /// get BR(H->gg) for given value of mA and tanb
  double br_Hgg(double mA, double tanb){ return br("H->gluglu", mA, tanb); }
  /// get BR(h->gg) for given value of mA and tanb
  double br_hgg(double mA, double tanb){ return br("h->gluglu", mA, tanb); }
  /// get BR(A->Zgamma) for given value of mA and tanb
  double br_AZgamma(double mA, double tanb){ return br("A->Zgam", mA, tanb); }
  /// get BR(H->gammagamma) for given value of mA and tanb
  double br_HZgamma(double mA, double tanb){ return br("H->Zgam", mA, tanb); }
  /// get BR(h->Zgamma) for given value of mA and tanb
  double br_hZgamma(double mA, double tanb){ return br("h->Zgamm", mA, tanb); }
  /// get BR(A->gammagamma) for given value of mA and tanb
  double br_Agammagamma(double mA, double tanb){ return br("A->gamgam", mA, tanb); }
  /// get BR(H->gammagamma) for given value of mA and tanb
  double br_Hgammagamma(double mA, double tanb){ return br("H->gamgam", mA, tanb); }
  /// get BR(h->gammagamma) for given value of mA and tanb
  double br_hgammagamma(double mA, double tanb){ return br("h->gamgam", mA, tanb); }

  /*
   * pre-defined access functions for Higgs to Higgs/SUSY decays
   */
  /// get BR(H->hh) for given value of mA and tanb
  double br_Hhh(double mA, double tanb){ return br("H->hh", mA, tanb); }
  /// get BR(A->Zh) for given value of mA and tanb
  double br_AZh(double mA, double tanb){ return br("A->Zh", mA, tanb); }
  /// get BR(H+->Wh) for given value of mA and tanb
  double br_HpWh(double mA, double tanb){ return br("Hp->hW", mA, tanb); }
  /// get BR(H+->WA) for given value of mA and tanb
  double br_HpWA(double mA, double tanb){ return br("Hp->AW", mA, tanb); }
  /// get BR(H+->HHA) for given value of mA and tanb
  double br_HpHHW(double mA, double tanb){ return br("Hp->HHW", mA, tanb); }
  /// get BR(A->SUSY) for given value of mA and tanb
  double br_ASUSY(double mA, double tanb){ return br("A->SUSY", mA, tanb); }
  /// get BR(H->SUSY) for given value of mA and tanb
  double br_HSUSY(double mA, double tanb){ return br("H->SUSY", mA, tanb); }
  /// get BR(h->SUSY) for given value of mA and tanb
  double br_hSUSY(double mA, double tanb){ return br("h->SUSY", mA, tanb); }
  /// get BR(H+->SUSY) for given value of mA and tanb
  double br_HpSUSY(double mA, double tanb){ return br("Hp->SUSY", mA, tanb); }

  /*
   * pre-defined access functions for A/H/h/H+ production 
   */
  /// get cross section for production of A in gluon-gluon fusion (in pb) 
  double ggH_A(double mA, double tanb){ return xsec("gg->A", mA, tanb); }
  /// get cross section for production of H in gluon-gluon fusion (in pb) 
  double ggH_H(double mA, double tanb){ return xsec("gg->H", mA, tanb); }
  /// get cross section for production of h in gluon-gluon fusion (in pb) 
  double ggH_h(double mA, double tanb){ return xsec("gg->h", mA, tanb); }
  /// get cross section for production of A in association with b quarks (5FS) (in pb) 
  double bbH5F_A(double mA, double tanb){ return xsec("bb5F->A", mA, tanb); }
  /// get cross section for production of H in association with b quarks (5FS) (in pb) 
  double bbH5F_H(double mA, double tanb){ return xsec("bb5F->H", mA, tanb); }
  /// get cross section for production of h in association with b quarks (5FS) (in pb) 
  double bbH5F_h(double mA, double tanb){ return xsec("bb5F->h", mA, tanb); }
  /// get cross section for production of A in association with b quarks (4FS) (in pb) 
  double bbH4F_A(double mA, double tanb){ return xsec("bb4F->A", mA, tanb); }
  /// get cross section for production of H in association with b quarks (4FS) (in pb) 
  double bbH4F_H(double mA, double tanb){ return xsec("bb4F->H", mA, tanb); }
  /// get cross section for production of h in association with b quarks (4FS) (in pb) 
  double bbH4F_h(double mA, double tanb){ return xsec("bb4F->h", mA, tanb); }
  /// get cross section for production of A in association with b quarks (using Santander matching scheme) (in pb) 
  double bbHSantander_A(double mA, double tanb);
  /// get cross section for production of H in association with b quarks (using Santander matching scheme) (in pb) 
  double bbHSantander_H(double mA, double tanb);
  /// get cross section for production of h in association with b quarks (using Santander matching scheme) (in pb) 
  double bbHSantander_h(double mA, double tanb);

  /*
   * pre-defined access functions for A/H/h/H+ production uncertainties in several flavours
   */
  /// get uncertainties for gluon-gluon fusion production of A from mu scale variations (in pb)  
  double ggH_A_scale(double mA, double tanb, const bool kUP){ return xsec(kUP ? "gg->A::scaleUp" : "gg->A::scaleDown", mA, tanb); } 
  /// get uncertainties for gluon-gluon fusion production of H from mu scale variations (in pb)  
  double ggH_H_scale(double mA, double tanb, const bool kUP){ return xsec(kUP ? "gg->H::scaleUp" : "gg->H::scaleDown", mA, tanb); } 
  /// get uncertainties for gluon-gluon fusion production of h from mu scale variations (in pb)  
  double ggH_h_scale(double mA, double tanb, const bool kUP){ return xsec(kUP ? "gg->h::scaleUp" : "gg->h::scaleDown", mA, tanb); } 
  /// get uncertainties for gluon-gluon fusion production of A from variations of pdfs and alphas (in pb)  
  double ggH_A_pdfas(double mA, double tanb, const bool kUP){ return xsec((kUP ? "gg->A::pdfasUp" : "gg->A::pdfasDown"), mA, tanb); } 
  /// get uncertainties for gluon-gluon fusion production of H from variations of pdfs and alphas (in pb)  
  double ggH_H_pdfas(double mA, double tanb, const bool kUP){ return xsec((kUP ? "gg->H::pdfasUp" : "gg->H::pdfasDown"), mA, tanb); }
  /// get uncertainties for gluon-gluon fusion production of h from variations of pdfs and alphas (in pb)  
  double ggH_h_pdfas(double mA, double tanb, const bool kUP){ return xsec((kUP ? "gg->h::pdfasUp" : "gg->h::pdfasDown"), mA, tanb); }
  /// get uncertainties for A production in association with b quarks from mu scale variations (5FS, in pb)  
  double bbH5F_A_scale(double mA, double tanb, const bool kUP){ return xsec(kUP ? "bb5F->A::scaleUp" : "bb5F->A::scaleDown", mA, tanb); } 
  /// get uncertainties for H production in association with b quarks from mu scale variations (5FS, in pb)  
  double bbH5F_H_scale(double mA, double tanb, const bool kUP){ return xsec(kUP ? "bb5F->H::scaleUp" : "bb5F->H::scaleDown", mA, tanb); } 
  /// get uncertainties for h production in association with b quarks from mu scale variations (5FS, in pb)  
  double bbH5F_h_scale(double mA, double tanb, const bool kUP){ return xsec(kUP ? "bb5F->h::scaleUp" : "bb5F->h::scaleDown", mA, tanb); }   
  /// get uncertainties for A production in association with b quarks from mu scale variations (4FS, in pb)  
  double bbH4F_A_scale(double mA, double tanb, const bool kUP){ return xsec(kUP ? "bb4F->A::scaleUp" : "bb4F->A::scaleDown", mA, tanb); } 
  /// get uncertainties for H production in association with b quarks from mu scale variations (4FS, in pb)  
  double bbH4F_H_scale(double mA, double tanb, const bool kUP){ return xsec(kUP ? "bb4F->H::scaleUp" : "bb4F->H::scaleDown", mA, tanb); } 
  /// get uncertainties for h production in association with b quarks from mu scale variations (4FS, in pb)  
  double bbH4F_h_scale(double mA, double tanb, const bool kUP){ return xsec(kUP ? "bb4F->h::scaleUp" : "bb4F->h::scaleDown", mA, tanb); } 
  /// get uncertainties for A production in association with b quarks from variations of pdfs and alphas (same for 4FS and 5FS, in pb)  
  double bbH5F_A_pdfas(double mA, double tanb, const bool kUP){ return xsec((kUP ? "bb5F->A::pdfasUp" : "bb5F->A::pdfasDown"), mA, tanb); } 
  /// get uncertainties for H production in association with b quarks from variations of pdfs and alphas (same for 4FS and 5FS, in pb)  
  double bbH5F_H_pdfas(double mA, double tanb, const bool kUP){ return xsec((kUP ? "bb5F->H::pdfasUp" : "bb5F->H::pdfasDown"), mA, tanb); } 
  /// get uncertainties for h production in association with b quarks from variations of pdfs and alphas (same for 4FS and 5FS, in pb)  
  double bbH5F_h_pdfas(double mA, double tanb, const bool kUP){ return xsec((kUP ? "bb5F->h::pdfasUp" : "bb5F->h::pdfasDown"), mA, tanb); } 
  /// get uncertainties for A production in association with b quarks from mu variations (Santander matching scheme, in pb)  
  double bbHSantander_A_scale(double mA, double tanb, const bool kUP);
  /// get uncertainties for H production in association with b quarks from mu variations (Santander matching scheme, in pb)  
  double bbHSantander_H_scale(double mA, double tanb, const bool kUP);
  /// get uncertainties for h production in association with b quarks from mu variations (Santander matching scheme, in pb)  
  double bbHSantander_h_scale(double mA, double tanb, const bool kUP);
  /// get uncertainties for A production in association with b quarks from pdf+alphas variations (Santander matching scheme, in pb)  
  double bbHSantander_A_pdfas(double mA, double tanb, const bool kUP);
  /// get uncertainties for H production in association with b quarks from pdf+alphas variations (Santander matching scheme, in pb)  
  double bbHSantander_H_pdfas(double mA, double tanb, const bool kUP);
  /// get uncertainties for h production in association with b quarks from pdf+alphas variations (Santander matching scheme, in pb)  
  double bbHSantander_h_pdfas(double mA, double tanb, const bool kUP);

 private:
  /// open input file to access histograms (only needed if input file was not specified in the constructor)
  void setup(const char* filename);
  /// rule to determine histogram names related to branching fractions in the input file
  std::string br_rule(const char* br);
  /// rule to determine histogram names related to full decay widths in the input file
  std::string width_rule(const char* b);
  /// rule to determine histogram names related to cross sections in the input file
  std::string xsec_rule(const char* xs);
  /// rule to determine histogram names related to masses in the input file
  std::string mass_rule(const char* b);
  /// a common function to return histograms from the input file. Apart from mA and tanb it takes an 
  /// identification string for the object in the input file [key] and a conversion rule to transform 
  /// this string into the histogram name [rule]. The conversion rule is a pointer-to-member-function.
  /// The conversion rules are provided as private member functions of the class. The function "read" 
  /// will determine the histogram name from the rule, determine the bin containing mA and tanb and 
  /// return the bin content. Alternatiely it returns a bilinear interpolation corresponding to the 
  /// values mA and tanb, if kINTERPOL_ has been set to true during the instantiation of the class. 
  double read(const char* key, double mA, double tanb, std::string (mssm_xs_tools::*rule)(const char* key)){
     std::string name = (this->*rule)(key);
     if(name.find("Santander")!=std::string::npos){
       if(name.find("_h")!=std::string::npos){
	       if(name.find( "scaleDown" )!=std::string::npos){return bbHSantander_h_scale(mA, tanb, false);} else
	       if(name.find( "scaleUp"   )!=std::string::npos){return bbHSantander_h_scale(mA, tanb, true );} else
	       if(name.find( "pdfasDown" )!=std::string::npos){return bbHSantander_h_pdfas(mA, tanb, false);} else
	       if(name.find( "pdfasUp"   )!=std::string::npos){return bbHSantander_h_pdfas(mA, tanb, true );}
	       else{
	         return bbHSantander_h(mA, tanb);
	       }
       } else 
       if(name.find("_H")!=std::string::npos){
	       if(name.find( "scaleDown" )!=std::string::npos){return bbHSantander_H_scale(mA, tanb, false);} else
	       if(name.find( "scaleUp"   )!=std::string::npos){return bbHSantander_H_scale(mA, tanb, true );} else
	       if(name.find( "pdfasDown" )!=std::string::npos){return bbHSantander_H_pdfas(mA, tanb, false);} else
	       if(name.find( "pdfasUp"   )!=std::string::npos){return bbHSantander_H_pdfas(mA, tanb, true );}
	       else{
	         return bbHSantander_H(mA, tanb);
	       }
       } else
       if(name.find("_A")!=std::string::npos){
	       if(name.find( "scaleDown" )!=std::string::npos){return bbHSantander_A_scale(mA, tanb, false);} else
	       if(name.find( "scaleUp"   )!=std::string::npos){return bbHSantander_A_scale(mA, tanb, true );} else
	       if(name.find( "pdfasDown" )!=std::string::npos){return bbHSantander_A_pdfas(mA, tanb, false);} else
	       if(name.find( "pdfasUp"   )!=std::string::npos){return bbHSantander_A_pdfas(mA, tanb, true );}
	       else{
	         return bbHSantander_A(mA, tanb);
	       }
       }
       else{
         return -1;
       }
     }
     else {
       if(kINTERPOL_){
	       // restrict interplolation to boundaries of histogram, at the boundaries fall back to plain bin
	       // content
	       if(hist(name)->GetXaxis()->FindBin(mA  )<nbinsX_-1 && hist(name)->GetYaxis()->FindBin(tanb)<nbinsY_-1){
	         return hist(name) ? hist(name)->Interpolate(mA,tanb) : -1.;
	       }
	       else{
	         return hist(name) ? hist(name)->GetBinContent(hist(name)->FindBin(mA,tanb)) : -1.;    
	       }    
       }
       else{
	       return hist(name) ? hist(name)->GetBinContent(hist(name)->FindBin(mA,tanb)) : -1.;    
       }
     }
  }
  /// verbosity level
  unsigned verbosity_;
  /// apply bilinear interpolation (built-in to TH2F) or get bin content, plain as it is
  bool kINTERPOL_;
  /// root input file (opened in constructor)
  TFile* input_;
  /// histogram container (filled in constructor)
  std::map<std::string, TH2F*> hists_;
  /// maximal number of bins on x-axis (mA)   of TH2F (filled in function hist; used in 
  /// function read in interpolation mode)
  int nbinsX_;
  /// maximal number of bins on y-axis (tanb) of TH2F (filled in function hist; used in
  /// function read in interpolation mode)
  int nbinsY_;
};

inline double 
mssm_xs_tools::bbHSantander_A(double mA, double tanb){
  double t=log(mA/4.92)-2.;
  double fourflav=this->bbH4F_A(mA,tanb);
  double fiveflav=this->bbH5F_A(mA,tanb);
  return (1./(1.+t))*(fourflav+t*fiveflav);
}

inline double 
mssm_xs_tools::bbHSantander_H(double mA, double tanb){
  double t=log(this->mH(mA,tanb)/4.92)-2.;
  double fourflav=this->bbH4F_H(mA,tanb);
  double fiveflav=this->bbH5F_H(mA,tanb);
  return (1./(1.+t))*(fourflav+t*fiveflav);
}

inline double 
mssm_xs_tools::bbHSantander_h(double mA, double tanb){
  double t=log(this->mh(mA,tanb)/4.92)-2.;
  double fourflav=this->bbH4F_h(mA,tanb);
  double fiveflav=this->bbH5F_h(mA,tanb);
  return (1./(1.+t))*(fourflav+t*fiveflav);
}

double 
mssm_xs_tools::bbHSantander_A_scale(double mA, double tanb, const bool kUP){
  double t=log(mA/4.92)-2.;
  double unc4F=this->bbH4F_A_scale(mA, tanb, kUP);
  double unc5F=this->bbH5F_A_scale(mA, tanb, kUP);
  return 1./(1+t)*(unc4F+(t*unc5F));
}

double 
mssm_xs_tools::bbHSantander_H_scale(double mA, double tanb, const bool kUP){
  double t=log(this->mH(mA, tanb)/4.92)-2.;
  double unc4F=this->bbH4F_H_scale(mA, tanb, kUP);
  double unc5F=this->bbH5F_H_scale(mA, tanb, kUP);
  return 1./(1+t)*(unc4F+(t*unc5F));
}

double 
mssm_xs_tools::bbHSantander_h_scale(double mA, double tanb, const bool kUP){
  double t=log(this->mh(mA, tanb)/4.92)-2.;
  double unc4F=this->bbH4F_h_scale(mA, tanb, kUP);
  double unc5F=this->bbH5F_h_scale(mA, tanb, kUP);
  return 1./(1+t)*(unc4F+(t*unc5F));
}

double 
mssm_xs_tools::bbHSantander_A_pdfas(double mA, double tanb, const bool kUP){
  return bbH5F_A_pdfas(mA, tanb, kUP)/bbH5F_A(mA, tanb) * bbHSantander_A(mA, tanb);
}

double 
mssm_xs_tools::bbHSantander_H_pdfas(double mA, double tanb, const bool kUP){
  return bbH5F_H_pdfas(mA, tanb, kUP)/bbH5F_H(mA, tanb) * bbHSantander_H(mA, tanb);
}

double 
mssm_xs_tools::bbHSantander_h_pdfas(double mA, double tanb, const bool kUP){
  return bbH5F_h_pdfas(mA, tanb, kUP)/bbH5F_h(mA, tanb) * bbHSantander_h(mA, tanb);
}

/* ________________________________________________________________________________________________
 * Class: mssm_xs_tools
 * 
 * External C wrapper to make core functionality available in python, too.
 */

extern "C" {
  /// constructor
  mssm_xs_tools* mssm_xs_tools_new(const char* filename="", bool kINTERPLOTATION=false, unsigned verbosity=0){
    return new mssm_xs_tools(filename, kINTERPLOTATION, verbosity);
  };
  /// destructor
  void mssm_xs_tools_delete(mssm_xs_tools* obj){ 
    delete obj; 
  };
  /// get mass of a given Higgs boson for given values of mA and tanb (in GeV)
  double mssm_xs_tools_mass(mssm_xs_tools* obj, const char* boson, double mA, double tanb){
    //std::cout << obj->read(boson, mA, tanb, &mssm_xs_tools::mass_rule) << std::endl;
    return obj->mass(boson, mA, tanb); 
  }
  /// get total decay width of a given Higgs boson for given values of mA and tanb (in GeV)
  double mssm_xs_tools_width(mssm_xs_tools* obj, const char* boson, double mA, double tanb){ 
    return obj->width(boson, mA, tanb); 
  }
  /// get branching fraction for a given decay of a given Higgs boson for given values of mA and tanb
  double mssm_xs_tools_br(mssm_xs_tools* obj, const char* decay, double mA, double tanb){ 
    return obj->br(decay, mA, tanb); 
  }
  /// get production cross section for a given production model of a given Higgs boson for given values of mA and tanb (in pb)
  double mssm_xs_tools_xsec(mssm_xs_tools* obj, const char* mode, double mA, double tanb){ 
    return obj->xsec(mode, mA, tanb); 
  }
}

#endif // MSSM_XS_TOOLS_H
