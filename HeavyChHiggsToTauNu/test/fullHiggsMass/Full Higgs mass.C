{
//=========Macro generated from canvas: Full Higgs mass/
//=========  (Tue Feb  5 09:28:16 2013) by ROOT version5.27/06b
   TCanvas *Full Higgs mass = new TCanvas("Full Higgs mass", "",0,0,600,600);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   Full Higgs mass->SetHighLightColor(2);
   Full Higgs mass->Range(-101.2658,-1.160932,531.6456,7.769316);
   Full Higgs mass->SetFillColor(0);
   Full Higgs mass->SetBorderMode(0);
   Full Higgs mass->SetBorderSize(2);
   Full Higgs mass->SetTickx(1);
   Full Higgs mass->SetTicky(1);
   Full Higgs mass->SetLeftMargin(0.16);
   Full Higgs mass->SetRightMargin(0.05);
   Full Higgs mass->SetTopMargin(0.05);
   Full Higgs mass->SetBottomMargin(0.13);
   Full Higgs mass->SetFrameFillStyle(0);
   Full Higgs mass->SetFrameBorderMode(0);
   Full Higgs mass->SetFrameFillStyle(0);
   Full Higgs mass->SetFrameBorderMode(0);
   
   TH1F *hframe__1 = new TH1F("hframe__1","",1000,0,500);
   hframe__1->SetMinimum(0);
   hframe__1->SetMaximum(7.322803);
   hframe__1->SetDirectory(0);
   hframe__1->SetStats(0);
   hframe__1->SetLineStyle(0);
   hframe__1->SetMarkerStyle(20);
   hframe__1->GetXaxis()->SetTitle("m_{H^{+}} (GeV)");
   hframe__1->GetXaxis()->SetLabelFont(43);
   hframe__1->GetXaxis()->SetLabelOffset(0.007);
   hframe__1->GetXaxis()->SetLabelSize(27);
   hframe__1->GetXaxis()->SetTitleSize(33);
   hframe__1->GetXaxis()->SetTitleOffset(0.9);
   hframe__1->GetXaxis()->SetTitleFont(43);
   hframe__1->GetYaxis()->SetLabelFont(43);
   hframe__1->GetYaxis()->SetLabelOffset(0.007);
   hframe__1->GetYaxis()->SetLabelSize(27);
   hframe__1->GetYaxis()->SetTitleSize(33);
   hframe__1->GetYaxis()->SetTitleOffset(1.25);
   hframe__1->GetYaxis()->SetTitleFont(43);
   hframe__1->GetZaxis()->SetLabelFont(43);
   hframe__1->GetZaxis()->SetLabelOffset(0.007);
   hframe__1->GetZaxis()->SetLabelSize(27);
   hframe__1->GetZaxis()->SetTitleSize(33);
   hframe__1->GetZaxis()->SetTitleFont(43);
   hframe__1->Draw(" ");
   Full Higgs mass->Modified();
   Full Higgs mass->cd();
   Full Higgs mass->SetSelected(Full Higgs mass);
}
