void WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight()
{
//=========Macro generated from canvas: WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight/
//=========  (Thu Apr 13 15:28:44 2017) by ROOT version6.06/02
   TCanvas *WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight = new TCanvas("WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight", "",0,0,600,600);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetHighLightColor(2);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->Range(-65.18987,-3.481481,529.7468,0.2222222);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetFillColor(0);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetBorderMode(0);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetBorderSize(2);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetLogy();
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetTickx(1);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetTicky(1);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetLeftMargin(0.16);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetRightMargin(0.05);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetTopMargin(0.06);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetBottomMargin(0.13);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetFrameFillStyle(0);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetFrameBorderMode(0);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetFrameFillStyle(0);
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetFrameBorderMode(0);
   
   TH1F *hframe__5 = new TH1F("hframe__5","",1000,30,500);
   hframe__5->SetMinimum(0.001);
   hframe__5->SetMaximum(1);
   hframe__5->SetDirectory(0);
   hframe__5->SetStats(0);
   hframe__5->SetLineStyle(0);
   hframe__5->SetMarkerStyle(20);
   hframe__5->GetXaxis()->SetTitle("Jet p_{T} (GeV)");
   hframe__5->GetXaxis()->SetLabelFont(43);
   hframe__5->GetXaxis()->SetLabelOffset(0.007);
   hframe__5->GetXaxis()->SetLabelSize(27);
   hframe__5->GetXaxis()->SetTitleSize(33);
   hframe__5->GetXaxis()->SetTitleOffset(0.9);
   hframe__5->GetXaxis()->SetTitleFont(43);
   hframe__5->GetYaxis()->SetTitle("Probability for passing b tagging");
   hframe__5->GetYaxis()->SetLabelFont(43);
   hframe__5->GetYaxis()->SetLabelOffset(0.007);
   hframe__5->GetYaxis()->SetLabelSize(27);
   hframe__5->GetYaxis()->SetTitleSize(33);
   hframe__5->GetYaxis()->SetTitleOffset(1.25);
   hframe__5->GetYaxis()->SetTitleFont(43);
   hframe__5->GetZaxis()->SetLabelFont(43);
   hframe__5->GetZaxis()->SetLabelOffset(0.007);
   hframe__5->GetZaxis()->SetLabelSize(27);
   hframe__5->GetZaxis()->SetTitleSize(33);
   hframe__5->GetZaxis()->SetTitleFont(43);
   hframe__5->Draw(" ");
   Double_t xAxis9[3] = {30, 340, 500}; 
   
   TEfficiency * AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9 = new TEfficiency("AllLightjets_WJetsToLNu_HT_100To200_cloned_clone","",2,xAxis9);
   
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetConfidenceLevel(0.6826895);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetBetaAlpha(1);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetBetaBeta(1);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetWeight(1);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetStatisticOption(1);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetPosteriorMode(0);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetShortestInterval(0);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetUseWeightedEvents();
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetTotalEvents(0,0);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetPassedEvents(0,0);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetTotalEvents(1,7109.944);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetPassedEvents(1,20.63599);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetTotalEvents(2,964.1642);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetPassedEvents(2,6.917469);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetTotalEvents(3,356.124);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetPassedEvents(3,3.588482);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetFillColor(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#ff00ff");
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetLineColor(ci);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetLineWidth(2);

   ci = TColor::GetColor("#ff00ff");
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetMarkerColor(ci);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetMarkerStyle(24);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->SetMarkerSize(1.2);
   AllLightjets_WJetsToLNu_HT_100To200_cloned_clone9->Draw(" samep");
   Double_t xAxis10[8] = {30, 60, 90, 140, 200, 300, 400, 500}; 
   
   TEfficiency * AllGjets_WJetsToLNu_HT_100To200_cloned_clone10 = new TEfficiency("AllGjets_WJetsToLNu_HT_100To200_cloned_clone","",7,xAxis10);
   
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetConfidenceLevel(0.6826895);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetBetaAlpha(1);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetBetaBeta(1);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetWeight(1);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetStatisticOption(1);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetPosteriorMode(0);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetShortestInterval(0);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetUseWeightedEvents();
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetTotalEvents(0,0);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetPassedEvents(0,0);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetTotalEvents(1,4281.939);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetPassedEvents(1,34.70705);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetTotalEvents(2,2169.507);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetPassedEvents(2,25.49811);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetTotalEvents(3,1848.809);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetPassedEvents(3,23.78036);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetTotalEvents(4,1294.326);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetPassedEvents(4,20.19141);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetTotalEvents(5,1135.711);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetPassedEvents(5,18.69771);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetTotalEvents(6,544.4878);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetPassedEvents(6,9.753057);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetTotalEvents(7,260.824);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetPassedEvents(7,5.584297);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetTotalEvents(8,183.2239);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetPassedEvents(8,4.213139);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetFillColor(0);

   ci = TColor::GetColor("#009900");
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetLineColor(ci);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetLineWidth(2);

   ci = TColor::GetColor("#009900");
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetMarkerColor(ci);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetMarkerStyle(23);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->SetMarkerSize(1.2);
   AllGjets_WJetsToLNu_HT_100To200_cloned_clone10->Draw(" samep");
   Double_t xAxis11[3] = {30, 290, 500}; 
   
   TEfficiency * AllCjets_WJetsToLNu_HT_100To200_cloned_clone11 = new TEfficiency("AllCjets_WJetsToLNu_HT_100To200_cloned_clone","",2,xAxis11);
   
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetConfidenceLevel(0.6826895);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetBetaAlpha(1);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetBetaBeta(1);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetWeight(1);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetStatisticOption(1);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetPosteriorMode(0);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetShortestInterval(0);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetUseWeightedEvents();
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetTotalEvents(0,0);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetPassedEvents(0,0);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetTotalEvents(1,1044.061);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetPassedEvents(1,28.48033);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetTotalEvents(2,170.3749);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetPassedEvents(2,6.104901);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetTotalEvents(3,26.12687);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetPassedEvents(3,0.808183);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetFillColor(0);

   ci = TColor::GetColor("#ff0000");
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetLineColor(ci);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetLineWidth(2);

   ci = TColor::GetColor("#ff0000");
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetMarkerColor(ci);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetMarkerStyle(27);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->SetMarkerSize(1.2);
   AllCjets_WJetsToLNu_HT_100To200_cloned_clone11->Draw(" samep");
   Double_t xAxis12[8] = {30, 70, 110, 150, 220, 310, 460, 500}; 
   
   TEfficiency * AllBjets_WJetsToLNu_HT_100To200_cloned_clone12 = new TEfficiency("AllBjets_WJetsToLNu_HT_100To200_cloned_clone","",7,xAxis12);
   
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetConfidenceLevel(0.6826895);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetBetaAlpha(1);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetBetaBeta(1);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetWeight(1);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetStatisticOption(1);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetPosteriorMode(0);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetShortestInterval(0);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetUseWeightedEvents();
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetTotalEvents(0,0);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetPassedEvents(0,0);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetTotalEvents(1,80.03256);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetPassedEvents(1,26.89593);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetTotalEvents(2,49.22769);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetPassedEvents(2,21.24209);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetTotalEvents(3,26.78683);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetPassedEvents(3,12.90198);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetTotalEvents(4,29.91252);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetPassedEvents(4,12.22628);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetTotalEvents(5,26.33793);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetPassedEvents(5,10.63997);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetTotalEvents(6,18.94011);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetPassedEvents(6,6.907845);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetTotalEvents(7,1.954656);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetPassedEvents(7,0.4928772);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetTotalEvents(8,4.301558);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetPassedEvents(8,1.422325);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetFillColor(0);

   ci = TColor::GetColor("#0000ff");
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetLineColor(ci);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetLineWidth(2);

   ci = TColor::GetColor("#0000ff");
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetMarkerColor(ci);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetMarkerStyle(26);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->SetMarkerSize(1.2);
   AllBjets_WJetsToLNu_HT_100To200_cloned_clone12->Draw(" samep");
   
   TLegend *leg = new TLegend(0.73,0.16,0.93,0.46,NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextFont(62);
   leg->SetTextSize(0.035);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(1);
   leg->SetFillColor(0);
   leg->SetFillStyle(4000);
   TLegendEntry *entry=leg->AddEntry("AllBjets_WJetsToLNu_HT_100To200_cloned_clone","b#rightarrowb","P");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);

   ci = TColor::GetColor("#0000ff");
   entry->SetMarkerColor(ci);
   entry->SetMarkerStyle(26);
   entry->SetMarkerSize(1.2);
   entry->SetTextFont(62);
   entry=leg->AddEntry("AllCjets_WJetsToLNu_HT_100To200_cloned_clone","c#rightarrowb","P");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);

   ci = TColor::GetColor("#ff0000");
   entry->SetMarkerColor(ci);
   entry->SetMarkerStyle(27);
   entry->SetMarkerSize(1.2);
   entry->SetTextFont(62);
   entry=leg->AddEntry("AllGjets_WJetsToLNu_HT_100To200_cloned_clone","g#rightarrowb","P");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);

   ci = TColor::GetColor("#009900");
   entry->SetMarkerColor(ci);
   entry->SetMarkerStyle(23);
   entry->SetMarkerSize(1.2);
   entry->SetTextFont(62);
   entry=leg->AddEntry("AllLightjets_WJetsToLNu_HT_100To200_cloned_clone","uds#rightarrowb","P");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);

   ci = TColor::GetColor("#ff00ff");
   entry->SetMarkerColor(ci);
   entry->SetMarkerStyle(24);
   entry->SetMarkerSize(1.2);
   entry->SetTextFont(62);
   leg->Draw();
   
   TH1F *hframe_copy__6 = new TH1F("hframe_copy__6","",1000,30,500);
   hframe_copy__6->SetMinimum(0.001);
   hframe_copy__6->SetMaximum(1);
   hframe_copy__6->SetDirectory(0);
   hframe_copy__6->SetStats(0);
   hframe_copy__6->SetLineStyle(0);
   hframe_copy__6->SetMarkerStyle(20);
   hframe_copy__6->GetXaxis()->SetTitle("Jet p_{T} (GeV)");
   hframe_copy__6->GetXaxis()->SetLabelFont(43);
   hframe_copy__6->GetXaxis()->SetLabelOffset(0.007);
   hframe_copy__6->GetXaxis()->SetLabelSize(27);
   hframe_copy__6->GetXaxis()->SetTitleSize(33);
   hframe_copy__6->GetXaxis()->SetTitleOffset(0.9);
   hframe_copy__6->GetXaxis()->SetTitleFont(43);
   hframe_copy__6->GetYaxis()->SetTitle("Probability for passing b tagging");
   hframe_copy__6->GetYaxis()->SetLabelFont(43);
   hframe_copy__6->GetYaxis()->SetLabelOffset(0.007);
   hframe_copy__6->GetYaxis()->SetLabelSize(27);
   hframe_copy__6->GetYaxis()->SetTitleSize(33);
   hframe_copy__6->GetYaxis()->SetTitleOffset(1.25);
   hframe_copy__6->GetYaxis()->SetTitleFont(43);
   hframe_copy__6->GetZaxis()->SetLabelFont(43);
   hframe_copy__6->GetZaxis()->SetLabelOffset(0.007);
   hframe_copy__6->GetZaxis()->SetLabelSize(27);
   hframe_copy__6->GetZaxis()->SetTitleSize(33);
   hframe_copy__6->GetZaxis()->SetTitleFont(43);
   hframe_copy__6->Draw("sameaxis");
   TLatex *   tex = new TLatex(0.95,0.952,"13 TeV");
tex->SetNDC();
   tex->SetTextAlign(31);
   tex->SetTextFont(43);
   tex->SetTextSize(24);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.16,0.952,"CMS");
tex->SetNDC();
   tex->SetTextFont(63);
   tex->SetTextSize(30);
   tex->SetLineWidth(2);
   tex->Draw();
      tex = new TLatex(0.2706,0.952,"Simulation");
tex->SetNDC();
   tex->SetTextFont(53);
   tex->SetTextSize(22.8);
   tex->SetLineWidth(2);
   tex->Draw();
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->Modified();
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->cd();
   WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight->SetSelected(WJetsHT_btageff_Run2016_80to1000_OptBjetDiscrpfCombinedInclusiveSecondaryVertexV2BJetTagsBjetDiscrWorkingPointTight);
}
