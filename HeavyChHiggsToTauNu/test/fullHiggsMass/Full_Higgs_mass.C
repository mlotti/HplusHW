{
//=========Macro generated from canvas: Full_Higgs_mass/
//=========  (Sat Feb 16 12:36:01 2013) by ROOT version5.27/06b
   TCanvas *Full_Higgs_mass = new TCanvas("Full_Higgs_mass", "",0,0,600,600);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   Full_Higgs_mass->SetHighLightColor(2);
   Full_Higgs_mass->Range(-101.2658,-21.02426,531.6456,140.7008);
   Full_Higgs_mass->SetFillColor(0);
   Full_Higgs_mass->SetBorderMode(0);
   Full_Higgs_mass->SetBorderSize(2);
   Full_Higgs_mass->SetTickx(1);
   Full_Higgs_mass->SetTicky(1);
   Full_Higgs_mass->SetLeftMargin(0.16);
   Full_Higgs_mass->SetRightMargin(0.05);
   Full_Higgs_mass->SetTopMargin(0.05);
   Full_Higgs_mass->SetBottomMargin(0.13);
   Full_Higgs_mass->SetFrameFillStyle(0);
   Full_Higgs_mass->SetFrameBorderMode(0);
   Full_Higgs_mass->SetFrameFillStyle(0);
   Full_Higgs_mass->SetFrameBorderMode(0);
   
   TH1F *hframe__1 = new TH1F("hframe__1","",1000,0,500);
   hframe__1->SetMinimum(0);
   hframe__1->SetMaximum(132.6146);
   hframe__1->SetDirectory(0);
   hframe__1->SetStats(0);
   hframe__1->SetLineStyle(0);
   hframe__1->SetMarkerStyle(20);
   hframe__1->GetXaxis()->SetTitle("m(b, #tau, #nu_{#tau}) (GeV)");
   hframe__1->GetXaxis()->SetLabelFont(43);
   hframe__1->GetXaxis()->SetLabelOffset(0.007);
   hframe__1->GetXaxis()->SetLabelSize(27);
   hframe__1->GetXaxis()->SetTitleSize(33);
   hframe__1->GetXaxis()->SetTitleOffset(0.9);
   hframe__1->GetXaxis()->SetTitleFont(43);
   hframe__1->GetYaxis()->SetTitle("Events");
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
   TLatex *   tex = new TLatex(0.2,0.96,"#sqrt{s} = 7 TeV");
tex->SetNDC();
   tex->SetTextFont(43);
   tex->SetTextSize(27);
   tex->SetLineWidth(2);
   tex->Draw();
   
   TH1F *#splitline{ID bad}{#Delta R > 0.4}__2 = new TH1F("#splitline{ID bad}{#Delta R > 0.4}__2","Higgs mass",100,0,500);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetBinContent(18,1.207236);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetBinContent(20,120.5587);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetBinContent(32,1.130148);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetBinContent(39,108.9965);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetBinError(18,1.207236);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetBinError(20,120.5587);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetBinError(32,1.130148);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetBinError(39,108.9964);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetEntries(4);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetDirectory(0);

   Int_t ci;   // for color index setting
   ci = TColor::GetColor("#ff0000");
   #splitline{ID bad}{#Delta R > 0.4}__2->SetLineColor(ci);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetLineWidth(2);

   ci = TColor::GetColor("#ff0000");
   #splitline{ID bad}{#Delta R > 0.4}__2->SetMarkerColor(ci);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetMarkerStyle(27);
   #splitline{ID bad}{#Delta R > 0.4}__2->SetMarkerSize(1.2);
   #splitline{ID bad}{#Delta R > 0.4}__2->GetXaxis()->SetTitle("m_{H^{+}} (GeV)");
   #splitline{ID bad}{#Delta R > 0.4}__2->Draw("HIST same");
   
   TH1F *#splitline{ID good}{#Delta R < 0.4}__3 = new TH1F("#splitline{ID good}{#Delta R < 0.4}__3","Higgs mass",100,0,500);
   #splitline{ID good}{#Delta R < 0.4}__3->SetDirectory(0);

   ci = TColor::GetColor("#0000ff");
   #splitline{ID good}{#Delta R < 0.4}__3->SetLineColor(ci);
   #splitline{ID good}{#Delta R < 0.4}__3->SetLineWidth(2);

   ci = TColor::GetColor("#0000ff");
   #splitline{ID good}{#Delta R < 0.4}__3->SetMarkerColor(ci);
   #splitline{ID good}{#Delta R < 0.4}__3->SetMarkerStyle(26);
   #splitline{ID good}{#Delta R < 0.4}__3->SetMarkerSize(1.2);
   #splitline{ID good}{#Delta R < 0.4}__3->GetXaxis()->SetTitle("m_{H^{+}} (GeV)");
   #splitline{ID good}{#Delta R < 0.4}__3->Draw("HIST same");
   
   TLegend *leg = new TLegend(0.73,0.62,0.93,0.92,NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextFont(62);
   leg->SetTextSize(0.03);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(1);
   leg->SetFillColor(0);
   leg->SetFillStyle(4000);
   TLegendEntry *entry=leg->AddEntry("#splitline{ID good}{#Delta R < 0.4}","#splitline{ID good}{#Delta R < 0.4}","l");

   ci = TColor::GetColor("#0000ff");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(2);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry=leg->AddEntry("#splitline{ID bad}{#Delta R > 0.4}","#splitline{ID bad}{#Delta R > 0.4}","l");

   ci = TColor::GetColor("#ff0000");
   entry->SetLineColor(ci);
   entry->SetLineStyle(1);
   entry->SetLineWidth(2);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   leg->Draw();
   
   TH1F *hframe__4 = new TH1F("hframe__4","",1000,0,500);
   hframe__4->SetMinimum(0);
   hframe__4->SetMaximum(132.6146);
   hframe__4->SetDirectory(0);
   hframe__4->SetStats(0);
   hframe__4->SetLineStyle(0);
   hframe__4->SetMarkerStyle(20);
   hframe__4->GetXaxis()->SetTitle("m(b, #tau, #nu_{#tau}) (GeV)");
   hframe__4->GetXaxis()->SetLabelFont(43);
   hframe__4->GetXaxis()->SetLabelOffset(0.007);
   hframe__4->GetXaxis()->SetLabelSize(27);
   hframe__4->GetXaxis()->SetTitleSize(33);
   hframe__4->GetXaxis()->SetTitleOffset(0.9);
   hframe__4->GetXaxis()->SetTitleFont(43);
   hframe__4->GetYaxis()->SetTitle("Events");
   hframe__4->GetYaxis()->SetLabelFont(43);
   hframe__4->GetYaxis()->SetLabelOffset(0.007);
   hframe__4->GetYaxis()->SetLabelSize(27);
   hframe__4->GetYaxis()->SetTitleSize(33);
   hframe__4->GetYaxis()->SetTitleOffset(1.25);
   hframe__4->GetYaxis()->SetTitleFont(43);
   hframe__4->GetZaxis()->SetLabelFont(43);
   hframe__4->GetZaxis()->SetLabelOffset(0.007);
   hframe__4->GetZaxis()->SetLabelSize(27);
   hframe__4->GetZaxis()->SetTitleSize(33);
   hframe__4->GetZaxis()->SetTitleFont(43);
   hframe__4->Draw("sameaxis");
      tex = new TLatex(0.62,0.96,"CMS Preliminary");
tex->SetNDC();
   tex->SetTextFont(43);
   tex->SetTextSize(27);
   tex->SetLineWidth(2);
   tex->Draw();
   Full_Higgs_mass->Modified();
   Full_Higgs_mass->cd();
   Full_Higgs_mass->SetSelected(Full_Higgs_mass);
}
