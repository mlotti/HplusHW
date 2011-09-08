#include "TFile.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TAxis.h"
#include "TTree.h"
#include "TCut.h"
#include "TString.h"
#include "TLegend.h"

#include<iostream>
#include<cmath>
#include<limits>

const double luminosity = 1145; // in pb^-1
const double qcdEvents = 7.5; // from QCD measurement, must correspond to the luminosity above!
const bool qcdFromData = true;

double signif(double nSignal,double nBackgr){
  double significance = 0;
  if(nBackgr > 0){
//  significance = nSignal/sqrt(nSignal+nBackgr);
//  significance = nSignal/sqrt(nBackgr);
    significance = sqrt(2*((nSignal+nBackgr)*log(1+nSignal/nBackgr)-nSignal));
  }
  return significance;
}

TH1 *dist2pass(TH1 *hdist, bool lessThan) {
  // bin 0              underflow bin
  // bin 1              first bin
  // bin GetNbinsX()    last bin
  // bin GetNbinsX()+1  overflow bin

  // Here we assume that the all the bins in hdist have equal
  // widths. If this doesn't hold, the output must be TGraph.
  double bw = hdist->GetBinWidth(1);
  for(int bin=1; bin <= hdist->GetNbinsX(); ++bin) {
    if(std::abs(bw - hdist->GetBinWidth(bin))/bw > 0.01) {
      std::cout << "dist2pass: input histogram with variable bin width is not supported (yet)" << std::endl;
      return 0;
    }
  }

  // Construct the low edges of the passed histogram. Set the low
  // edges such that the bin centers correspond to the edges of the
  // distribution histogram. This makes sense because the only
  // sensible cut points in the distribution histogram are the bin
  // edges, and if one draws the passed histogram with points, the
  // points are placed to bin centers.
  int nbins = hdist->GetNbinsX()+1;
  double firstLowEdge = hdist->GetXaxis()->GetBinLowEdge(1) - bw/2;
  double lastUpEdge = hdist->GetXaxis()->GetBinUpEdge(hdist->GetNbinsX()) + bw/2;
  TH1 *hpass = new TH1F(TString("passed_")+hdist->GetName(),
                        TString("Passed ")+hdist->GetTitle(),
                        nbins, firstLowEdge, lastUpEdge);

  /*
  for(int bin=1; bin <= hpass->GetNbinsX(); ++bin) {
    std::cout << "Bin " << bin 
              << " hpass.center " << hpass->GetXaxis()->GetBinCenter(bin)
              << " hdist.low " << hdist->GetXaxis()->GetBinLowEdge(bin)
              << std::endl;
  }
  */

  // Fill the passed histogram
  if(lessThan) {
    // The overflow bin will contain the number of all events
    double passedCumulative = 0;
    for(int bin=0; bin <= hdist->GetNbinsX()+1; ++bin) {
      passedCumulative += hdist->GetBinContent(bin);
      hpass->SetBinContent(bin+1, passedCumulative);
    }
  }
  else {
    // The underflow bin will contain the number of all events
    double passedCumulative = 0;
    for(int bin=hdist->GetNbinsX()+1; bin >= 0; --bin) {
      passedCumulative += hdist->GetBinContent(bin);
      hpass->SetBinContent(bin, passedCumulative);
    }
  }

  return hpass;
}

void test_dist2pass() {
  TH1F *hdist = new TH1F("foo", "foo", 10, 0, 10);
  hdist->SetBinContent(2, 5); // 1-2
  hdist->SetBinContent(6, 2); // 5-6
  TH1 *d1 = dist2pass(hdist, true);
  TH1 *d2 = dist2pass(hdist, false);

  for(int bin=0; bin <= d1->GetNbinsX()+1; ++bin) {
    std::cout << "Bin " << bin << " center " << d1->GetXaxis()->GetBinCenter(bin)
              << " less " << d1->GetBinContent(bin) << " greater " << d2->GetBinContent(bin) << std::endl;
  }
}

struct DistPass {
  DistPass(): dist(0), pass(0) {}
  DistPass(TH1 *d, TH1 *p): dist(d), pass(p) {}
  DistPass clone() const;
  TH1 *dist;
  TH1 *pass;
};

DistPass DistPass::clone() const {
  TH1 *d = 0;
  TH1 *p = 0;
  if(dist) d = dynamic_cast<TH1 *>(dist->Clone(dist->GetName()+TString("_cloned")));
  if(pass) p = dynamic_cast<TH1 *>(pass->Clone(pass->GetName()+TString("_cloned")));

  return DistPass(d, p);
}

DistPass createDistPassHelper(const char *file, TTree *tree, const char *expr, const char *cut, bool lessThan, double scale) {
  Long64_t ret = tree->Draw(expr, cut, "goff");
  if(ret < 0) {
    std::cout << "Error in processing tree from file " << file << std::endl;
    return DistPass();
  }
  if(ret == 0) {
    std::cout << "No entries from file " << file << std::endl;
    //return DistPass();
  }

  TH1 *dist = tree->GetHistogram();
  if(!dist) {
    std::cout << "No histogram from tree?" << std::endl;
    return DistPass();
  }
  dist = dynamic_cast<TH1 *>(dist->Clone(TString(dist->GetName())+"_cloned"));
  if(!dist) {
    std::cout << "No histogram from clone?" << std::endl;
    return DistPass();
  }

  // Normalize the distribution
  dist->Scale(scale);

  // Construct the "number of passed events as a function of cut value" histogram
  TH1 *pass = dist2pass(dist, lessThan);
  if(!pass) {
    std::cout << "No histogram from dist2pass?" << std::endl;
  }

  TString name(file);
  name.Remove(name.First('/'),name.Length()-name.First('/'));
  pass->SetName(name);

  return DistPass(dist, pass);
}


DistPass createDistPassQCDdata(const char *file, const char *expr, const char *cut, bool lessThan) {
  // Open file
  TFile *f = TFile::Open(file);
  if(!f) {
    std::cout << "Unable to open file " << file << std::endl;
    return DistPass();
  }

  // Get the tree
  TTree *tree = dynamic_cast<TTree *>(f->Get("QCDMeasurement/tree"));
  if(!tree) {
    std::cout << "Unable to find tree from " << file << std::endl;
    return DistPass();
  }

  // Get the number of all non-normalized events which pass the MET cut
  Long64_t nentries = tree->GetEntries("met_p4.Et() > 70");
  double scale = qcdEvents/nentries;

  return createDistPassHelper(file, tree, expr, cut, lessThan, scale);
}

DistPass createDistPassMC(const char *file, const char *expr, const char *cut, bool lessThan,
                          double crossSection=std::numeric_limits<double>::quiet_NaN()) {
  // Open file
  TFile *f = TFile::Open(file);
  if(!f) {
    std::cout << "Unable to open file " << file << std::endl;
    return DistPass();
  }

  // Read metadata to calculate the weight of one MC event
  TH1 *counter = dynamic_cast<TH1 *>(f->Get("signalAnalysisCounters/counter"));
  if(!counter) {
    std::cout << "Unable to find counters from " << file << std::endl;
    return DistPass();
  }
 
  if(std::isnan(crossSection)) {
    TH1 *configInfo = dynamic_cast<TH1 *>(f->Get("configInfo/configinfo"));
    if(!configInfo) {
      std::cout << "Unable to find configInfo from " << file << std::endl;
      return DistPass();
    }

    double control = 0;
    for(int bin=1; bin <= configInfo->GetNbinsX(); ++bin) {
      if(TString(configInfo->GetXaxis()->GetBinLabel(bin)) == "control")
        control = configInfo->GetBinContent(bin);
      else if(TString(configInfo->GetXaxis()->GetBinLabel(bin)) == "crossSection")
        crossSection = configInfo->GetBinContent(bin);
    }
    // control holds the number of original files the file has been
    // merged from; thus the cross section must be divided with it.
    crossSection = crossSection / control;
  }
  // The first bin in counter holds the number of all events.
  double mcWeight = crossSection / counter->GetBinContent(1) * luminosity;

  // Get the tree
  TTree *tree = dynamic_cast<TTree *>(f->Get("signalAnalysis/tree"));
  if(!tree) {
    std::cout << "Unable to find tree from " << file << std::endl;
    return DistPass();
  }

  return createDistPassHelper(file, tree, expr, cut, lessThan, mcWeight);
}

class Result {
  public:
  Result clone() const;

    void setXLabel(TString label){xlabel = label;}
    void addSignal(DistPass d){signals.push_back(d);}
    void addBackgr(DistPass d){backgrounds.push_back(d);}

    void Significance();

    // Signals
    std::vector<DistPass> signals;

    // Backgrounds
    std::vector<DistPass> backgrounds;

  private:
    TH1* Significance(TH1*,TH1*);
    DistPass SumBackgrounds();
    TString xlabel;
};

Result Result::clone() const {
  Result res;
  for(size_t i=0; i<signals.size(); ++i) {
    res.signals.push_back(signals[i].clone());
  }
  for(size_t i=0; i<backgrounds.size(); ++i) {
    res.backgrounds.push_back(backgrounds[i].clone());
  }
  return res;
}

void Result::Significance(){
    TCanvas* canvas0 = new TCanvas("Variable_"+xlabel,"",500,500);
    TCanvas* canvas1 = new TCanvas("Integral_"+xlabel,"",500,500);
    TCanvas* canvas2 = new TCanvas("SoverB_"+xlabel,"",500,500);
    TCanvas* canvas3 = new TCanvas("Signif_"+xlabel,"",500,500);

    DistPass background = SumBackgrounds();

     canvas0->cd();
     canvas0->SetLogy();   
  
    background.dist->GetXaxis()->SetTitle(xlabel);
    background.dist->GetYaxis()->SetTitle("Events");
    background.dist->SetName("N events");
    background.dist->SetLineWidth(3);
    background.dist->SetLineStyle(2);
    background.dist->Draw();

     canvas1->cd();

    background.pass->GetXaxis()->SetTitle(xlabel);
    background.pass->GetYaxis()->SetTitle("Sum Events");
    background.pass->SetName("N events");
    background.pass->SetLineWidth(3);
    background.pass->SetLineStyle(2);
    background.pass->Draw();

    TLegend* leg = new TLegend(0.135,0.15,0.5,0.35);

    TH1 *firstSB=0, *firstSignif=0;
    double xMaxSB=0,xMaxSignif=0;
    int color = 1;
    for(size_t i = 0; i < signals.size(); ++i){

	canvas0->cd();
	signals[i].dist->Draw("same");
	signals[i].dist->SetLineColor(color);

        canvas1->cd();
        signals[i].pass->Draw("same");
        signals[i].pass->SetLineColor(color);

	canvas2->cd();
        TH1* S2B = (TH1*)signals[i].pass->Clone();
	S2B->SetName("SoverB");
	S2B->GetXaxis()->SetTitle(xlabel);
	S2B->GetYaxis()->SetTitle("Signal / Background");
        S2B->Divide(background.pass);
        S2B->SetLineColor(color);
	if(i==0) {
	  S2B->Draw();
	  firstSB = S2B;
	  xMaxSB = S2B->GetMaximum();
	}
	else S2B->Draw("same");
	if(S2B->GetMaximum() > xMaxSB ) {
	  firstSB->GetYaxis()->SetRangeUser(0,1.1*S2B->GetMaximum());
	  xMaxSB = S2B->GetMaximum();
	}
	leg->AddEntry(S2B,signals[i].pass->GetName(),"l");

	canvas3->cd();
	//	canvas3->SetLogy();   
	TH1* SSignif = Significance(signals[i].pass,background.pass);
	SSignif->GetXaxis()->SetTitle(xlabel);
	SSignif->GetYaxis()->SetTitle("Significance");
	SSignif->SetLineColor(color);
	if(i==0) {
	  SSignif->Draw();
	  firstSignif = SSignif;
	  xMaxSignif = SSignif->GetMaximum();
	}
	else SSignif->Draw("same");
	if(SSignif->GetMaximum() > xMaxSignif ) {
	  firstSignif->GetYaxis()->SetRangeUser(0.01,1.1*SSignif->GetMaximum());
	  xMaxSignif = SSignif->GetMaximum();
	}

	color++;
	if(color == 3 || color == 5) color++;
    }
    leg->Draw();

    canvas0->SaveAs(".png");
    canvas1->SaveAs(".png");
    canvas2->SaveAs(".png");
    canvas3->SaveAs(".png");
    canvas0->SaveAs(".C");
    canvas1->SaveAs(".C");
    canvas2->SaveAs(".C");
    canvas3->SaveAs(".C");
}

TH1* Result::Significance(TH1* hs,TH1* hb){
    TH1* hSignif = (TH1*)hs->Clone();
    hSignif->Reset();
    hSignif->SetName("significance");

    for(int i = 0; i < hSignif->GetNbinsX(); ++i){
        hSignif->SetBinContent(i,signif(hs->GetBinContent(i),hb->GetBinContent(i)));
    }
    return hSignif;
}

DistPass Result::SumBackgrounds(){
    TH1 *dist = backgrounds[0].dist;
    TH1 *pass = backgrounds[0].pass;
    for(size_t i = 1; i < backgrounds.size();++i){
	dist->Add(backgrounds[i].dist);
	pass->Add(backgrounds[i].pass);
    }
    return DistPass(dist,pass);
}

Result createResult(const char *expr, const char *cut, const char *cutQCD, bool lessThan) {
  Result res;

  // FIXME: change cross section to correct one!
//  res.HplusTB_M190 = createDistPassMC("HplusTB_M190_Summer11/res/histograms-HplusTB_M190_Summer11.root", expr, cut, lessThan, 3.14159);
//  res.QCD_Pt30to50 = createDistPassMC("QCD_Pt30to50_TuneZ2_Summer11/res/histograms-QCD_Pt30to50_TuneZ2_Summer11.root", expr, cut, lessThan);
//  res.TTJets = createDistPassMC("TTJets_TuneZ2_Summer11/res/histograms-TTJets_TuneZ2_Summer11.root", expr, cut, lessThan);

//  res.addSignal(createDistPassMC("HplusTB_M190_Summer11/res/histograms-HplusTB_M190_Summer11.root", expr, cut, lessThan, 0.35));
//  res.addSignal(createDistPassMC("HplusTB_M200_Summer11/res/histograms-HplusTB_M200_Summer11.root", expr, cut, lessThan, 0.32));
//  res.addSignal(createDistPassMC("HplusTB_M220_Summer11/res/histograms-HplusTB_M220_Summer11.root", expr, cut, lessThan, 0.267));
//  res.addSignal(createDistPassMC("HplusTB_M250_Summer11/res/histograms-HplusTB_M250_Summer11.root", expr, cut, lessThan, 0.2067));
//  res.addSignal(createDistPassMC("HplusTB_M300_Summer11/res/histograms-HplusTB_M300_Summer11.root", expr, cut, lessThan, 0.1368));
// normalisation at tanbeta=20
  res.addSignal(createDistPassMC("TTToHplusBWB_M100_Summer11/res/histograms-TTToHplusBWB_M100_Summer11.root", expr, cut, lessThan,7.50));
  res.addSignal(createDistPassMC("TTToHplusBWB_M120_Summer11/res/histograms-TTToHplusBWB_M120_Summer11.root", expr, cut, lessThan,4.707));
  res.addSignal(createDistPassMC("TTToHplusBWB_M140_Summer11/res/histograms-TTToHplusBWB_M140_Summer11.root", expr, cut, lessThan,2.1747));
  res.addSignal(createDistPassMC("TTToHplusBWB_M150_Summer11/res/histograms-TTToHplusBWB_M150_Summer11.root", expr, cut, lessThan,1.163));
  res.addSignal(createDistPassMC("TTToHplusBWB_M155_Summer11/res/histograms-TTToHplusBWB_M155_Summer11.root", expr, cut, lessThan,0.751));
  res.addSignal(createDistPassMC("TTToHplusBWB_M160_Summer11/res/histograms-TTToHplusBWB_M160_Summer11.root", expr, cut, lessThan,0.417));



  res.addBackgr(createDistPassMC("TTJets_TuneZ2_Summer11/res/histograms-TTJets_TuneZ2_Summer11.root", expr, cut, lessThan));
  res.addBackgr(createDistPassMC("WJets_TuneZ2_Summer11/res/histograms-WJets_TuneZ2_Summer11.root", expr, cut, lessThan));

 
  if(qcdFromData) {
    res.addBackgr(createDistPassQCDdata("histograms-QCD-Tau_160431-167913.root", expr, cutQCD, lessThan));
  }
  else {
    res.addBackgr(createDistPassMC("QCD_Pt30to50_TuneZ2_Summer11/res/histograms-QCD_Pt30to50_TuneZ2_Summer11.root", expr, cut, lessThan));
    res.addBackgr(createDistPassMC("QCD_Pt50to80_TuneZ2_Summer11/res/histograms-QCD_Pt50to80_TuneZ2_Summer11.root", expr, cut, lessThan));
    res.addBackgr(createDistPassMC("QCD_Pt50to80_TuneZ2_Summer11/res/histograms-QCD_Pt50to80_TuneZ2_Summer11.root", expr, cut, lessThan));
    res.addBackgr(createDistPassMC("QCD_Pt80to120_TuneZ2_Summer11/res/histograms-QCD_Pt80to120_TuneZ2_Summer11.root", expr, cut, lessThan));
    res.addBackgr(createDistPassMC("QCD_Pt120to170_TuneZ2_Summer11/res/histograms-QCD_Pt120to170_TuneZ2_Summer11.root", expr, cut, lessThan));
    res.addBackgr(createDistPassMC("QCD_Pt170to300_TuneZ2_Summer11/res/histograms-QCD_Pt170to300_TuneZ2_Summer11.root", expr, cut, lessThan));
    res.addBackgr(createDistPassMC("QCD_Pt300to470_TuneZ2_Summer11/res/histograms-QCD_Pt300to470_TuneZ2_Summer11.root", expr, cut, lessThan));
  }
 

  return res;
}

Result subtractResults(const Result& a, const Result& b) {
  Result res = a.clone();
  assert(a.signals.size() == b.signals.size());
  assert(a.backgrounds.size() == b.backgrounds.size());
  for(size_t i=0; i<res.signals.size(); ++i) {
    if(res.signals[i].dist && b.signals[i].dist)
      res.signals[i].dist->Add(b.signals[i].dist, -1);
    if(res.signals[i].pass && b.signals[i].pass)
      res.signals[i].pass->Add(b.signals[i].pass, -1);
  }
  for(size_t i=0; i<res.backgrounds.size(); ++i) {
    if(res.backgrounds[i].dist && b.backgrounds[i].dist)
      res.backgrounds[i].dist->Add(b.backgrounds[i].dist, -1);
    if(res.backgrounds[i].pass && b.backgrounds[i].pass)
      res.backgrounds[i].pass->Add(b.backgrounds[i].pass, -1);
  }
  return res;
}

TString mcWeight(TCut cut) {
  TString expr(cut);
  TString weight = "weightPrescale*weightTrigger*weightPileup";
  
  return TString( "("+weight+")*("+expr+")");
}

void optimisation() {
  TH1::AddDirectory(kFALSE);

  // Cuts on preselection, which can be tightened
  TString tauPt("tau_p4.Pt()"); TCut tauPtCut(tauPt+" > 80");
  TString tauLeadingCandPt("tau_leadPFChargedHadrCand_p4.Pt()"); TCut tauLeadingCandPtCut(tauLeadingCandPt+" > 20");
  TCut jetPtNumCut = "Sum$(jets_p4.Pt() > 30) >= 3";

  // Cuts to be applied on top of preselection
  TString met("met_p4.Et()"); TCut metCut(met+" > 70");
  //  TCut btagCut = "Sum$(jets_btag > 1.7) >= 1";

  TString btagMax("Max$(jets_btag)"); TCut btagCut(btagMax+" > 1.7");
  TString btagJetNum17("Sum$(jets_btag > 1.7)"); 
  TString btag2ndMax("MaxIf$(jets_btag, jets_btag<Max$(jets_btag))");


  // Optional cuts
  TString rtau("tau_leadPFChargedHadrCand_p4.P()/tau_p4.P()"); TCut rtauCut(rtau+" > 0.65");
  TString mt("sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))"); TCut mtCut(mt+" > 80");

  TString deltaPhi("acos((tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/tau_p4.Pt()/met_p4.Et())*57.2958"); TCut deltaPhiCut(deltaPhi+" < 160");
  //  TString deltaPhi("tau_p4.DeltaPhi(met_p4)*57.2958"); TCut deltaPhiCut(deltaPhi+" < 160");

  TCut cut;

  rtau += ">>dist(110,0.,1.1)";
  cut = tauPtCut && metCut;
  Result rtauRes = createResult(rtau, mcWeight(cut && btagCut && mtCut), cut, false);
  rtauRes.setXLabel("rtau");

  met += ">>dist(100,0.,200.)";
  cut = tauPtCut && rtauCut;
  Result metRes = createResult(met, mcWeight(cut && btagCut), cut, false);
  metRes.setXLabel("met");

  tauPt += ">>dist(100,0.,100.)";
  cut = metCut && rtauCut;
  Result tauPtRes = createResult(tauPt, mcWeight(cut && btagCut), cut, false);
  tauPtRes.setXLabel("tauPt");

  mt += ">>dist(50,0.,200.)";
  cut = tauPtCut && metCut && rtauCut;
  Result mtRes = createResult(mt, mcWeight(cut && btagCut), cut, false);
  mtRes.setXLabel("mt");

  btagMax += ">>dist(80,0.,8.)";
  cut = tauPtCut && metCut && rtauCut;
  Result btagRes = createResult(btagMax, mcWeight(cut), cut, false);
  btagRes.setXLabel("btag");

  btag2ndMax += ">>dist(80,0.,8.)";
  Result btag2ndMaxRes = createResult(btag2ndMax, mcWeight(cut), cut, false);
  btag2ndMaxRes.setXLabel("btag 2nd max");

  Result btagExactlyOneRes = subtractResults(btagRes, btag2ndMaxRes);
  btagExactlyOneRes.setXLabel("btag exactly one");
  btagJetNum17 += ">>dist(6,0.,6.)";
  Result btagJetNum17Res = createResult(btagJetNum17, mcWeight(cut), cut, false);
  btagJetNum17Res.setXLabel("N(bjets>1.7)");

  deltaPhi += ">>dist(90.,0.,180.)";
  cut = tauPtCut && metCut && rtauCut;
  Result deltaPhiRes = createResult(deltaPhi, mcWeight(cut && btagCut), cut, false);
  deltaPhiRes.setXLabel("deltaPhi");

/*
  TCanvas *c = new TCanvas("rtau");
  //rtauRes.HplusTB_M190.pass->Draw();
  rtauRes.TTJets.pass->Draw();
  rtauRes.HplusTB_M190.pass->Draw("same");
  std::cout << rtauRes.TTJets.pass->GetBinContent(0) << std::endl;
  c->SaveAs(".png");
*/
//  rtauRes.Significance();
  //  metRes.Significance();
  //  tauPtRes.Significance();
  //  mtRes.Significance();
  btagRes.Significance();
  btag2ndMaxRes.Significance();
  //  btagExactlyOneRes.Significance();
  btagJetNum17Res.Significance();
  //  deltaPhiRes.Significance();

}


