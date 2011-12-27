
void plot(int mass) {
  //std::string infile = "EPS_data_nodeltaphi/hplus_100.root";
  //std::string infile = "EPS_data_deltaphi160/hplus_100.root";
  std::stringstream s;
  s << "hplus" << mass << ".root";

  std::string infile = s.str();
  double br = 0.05;

  bool log = false;

  Int_t ci;

  TFile* f = TFile::Open(infile.c_str());
  s.str("");
  s << "HW" << mass << "_1";
  TH1* hw = (TH1*)f->Get(s.str().c_str());
  s.str("");
  s << "HH" << mass << "_1";
  TH1* hh = (TH1*)f->Get(s.str().c_str());
  TH1* data = (TH1*)f->Get("data_obs");
  data->SetLineWidth(2);
  data->SetMarkerStyle(20);
  data->SetMarkerSize(1.2);

  TH1* ewktau = (TH1*)f->Get("EWKTau");
  ci = TColor::GetColor("#993399");
  ewktau->SetFillColor(ci);
  ewktau->SetLineWidth(0);
  TH1* qcd = (TH1*)f->Get("QCD");
  ci = TColor::GetColor("#ffcc33");
  qcd->SetFillColor(ci);
  qcd->SetLineWidth(0);
  TH1* fakett = (TH1*)f->Get("fakett");
  ci = TColor::GetColor("#669900");
  fakett->SetFillColor(ci);
  fakett->SetLineWidth(0);
  TH1* fakeW = (TH1*)f->Get("fakeW");
  ci = TColor::GetColor("#cc3300");
  fakeW->SetFillColor(ci);
  fakeW->SetLineWidth(0);

  // Frame
  TCanvas *transverseMass = new TCanvas("transverseMass", "",0,0,600,600);
  gStyle->SetOptFit(1);
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(0);
  transverseMass->SetHighLightColor(2);
  transverseMass->Range(-81.01265,-3.836876,425.3165,2.600629);
  transverseMass->SetFillColor(0);
  transverseMass->SetBorderMode(0);
  transverseMass->SetBorderSize(2);
  if (log)
    transverseMass->SetLogy();
  transverseMass->SetTickx(1);
  transverseMass->SetTicky(1);
  transverseMass->SetLeftMargin(0.16);
  transverseMass->SetRightMargin(0.05);
  transverseMass->SetTopMargin(0.05);
  transverseMass->SetBottomMargin(0.13);
  transverseMass->SetFrameFillStyle(0);
  transverseMass->SetFrameBorderMode(0);
  transverseMass->SetFrameFillStyle(0);
  transverseMass->SetFrameBorderMode(0);
  
  TH1F *frame = new TH1F("frame","",1000,0,400);
  frame->SetMinimum(0.001);
  if (log)
    frame->SetMaximum(190);
  else
    frame->SetMaximum(25);
  frame->SetDirectory(0);
  frame->SetStats(0);
  frame->SetLineStyle(0);
  frame->SetMarkerStyle(20);
  frame->SetXTitle("Transverse mass (tau,MET), GeV/c^{2}");
  frame->SetYTitle("N_{events} / 10 GeV/c^{2}");
  frame->GetXaxis()->SetLabelSize(0.05);
  frame->GetXaxis()->SetTitleSize(0.05);
  frame->GetYaxis()->SetLabelSize(0.05);
  frame->GetYaxis()->SetTitleSize(0.05);
  frame->GetYaxis()->SetTitleOffset(1.3);
  frame->Draw();



  // signal
  hh->Scale(br*br);
  hw->Scale(2*br*(1.0-br));
  TH1* signal = (TH1*)hh->Clone();
  signal->Add(hw);

  ci = TColor::GetColor("#ff3399");
  signal->SetLineColor(ci);
  signal->SetLineStyle(2);
  signal->SetLineWidth(2);

  // Fakes
  TH1* fakes = (TH1*)(fakett->Clone());
  fakes->Add(fakeW);

  // stacked backgrounds
  THStack *exp = new THStack();
  exp->SetName("exp");
  exp->SetTitle("exp");
  exp->Add(fakes);
  exp->Add(ewktau);
  exp->Add(qcd);
  exp->Add(signal);
  exp->Draw("hist same");

  // uncertainty
  TH1* uncert = (TH1*)fakeW->Clone();
  uncert->Add(fakett);
  uncert->Add(ewktau);
  uncert->Add(qcd);
  uncert->SetFillColor(1);
  uncert->SetFillStyle(3354);
  uncert->SetLineColor(0);
  uncert->SetLineStyle(0);
  uncert->SetLineWidth(0);
  uncert->Draw("E2 same");

  // Data
  data->Draw("same");
  
  //signal->Draw("same");


  TLegend *leg = new TLegend(0.55,0.68,0.9,0.93,NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextFont(62);
  leg->SetTextSize(0.03);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(0);
  leg->SetFillStyle(4000);
  TLegendEntry* entry = leg->AddEntry(data, "Data", "P");
  s.str("");
  s << "HH+HW(" << mass << "), br=" << br;
  entry = leg->AddEntry(signal, s.str().c_str(), "L");
  entry = leg->AddEntry(qcd, "QCD (meas.)", "F");
  entry = leg->AddEntry(ewktau, "EWK w. taus (meas.)", "F");
  entry = leg->AddEntry(fakes, "EWK fake taus (MC)", "F");
  leg->Draw();


   TLatex *   tex = new TLatex(0.62,0.96,"CMS Preliminary");
tex->SetNDC();
   tex->SetTextFont(43);
   tex->SetTextSize(27);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.2,0.96,"#sqrt{s} = 7 TeV");
tex->SetNDC();
   tex->SetTextFont(43);
   tex->SetTextSize(27);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.43,0.96,"2.2 fb^{-1}");
tex->SetNDC();
   tex->SetTextFont(43);
   tex->SetTextSize(27);
   tex->SetLineWidth(2);
   tex->Draw();

   transverseMass->Draw("SAME");

   s.str("");
   s << "mT_datadriven_m" << mass << ".png";
   transverseMass->Print(s.str().c_str());
}

void combineMt(){
  plot(80);
  plot(100);
  plot(120);
  plot(140);
  plot(150);
  plot(155);
  plot(160);
}
