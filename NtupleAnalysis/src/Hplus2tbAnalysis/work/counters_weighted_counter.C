void counters_weighted_counter()
{
//=========Macro generated from canvas: counters_weighted_counter/counters_weighted_counter
//=========  (Thu Oct 27 09:47:51 2016) by ROOT version6.02/13
   TCanvas *counters_weighted_counter = new TCanvas("counters_weighted_counter", "counters_weighted_counter",0,0,600,750);
   gStyle->SetOptFit(1);
   gStyle->SetOptStat(0);
   gStyle->SetOptTitle(0);
   counters_weighted_counter->SetHighLightColor(2);
   counters_weighted_counter->Range(0,0,1,1);
   counters_weighted_counter->SetFillColor(0);
   counters_weighted_counter->SetBorderMode(0);
   counters_weighted_counter->SetBorderSize(2);
   counters_weighted_counter->SetTickx(1);
   counters_weighted_counter->SetTicky(1);
   counters_weighted_counter->SetLeftMargin(0.16);
   counters_weighted_counter->SetRightMargin(0.05);
   counters_weighted_counter->SetTopMargin(0.06);
   counters_weighted_counter->SetBottomMargin(0.13);
   counters_weighted_counter->SetFrameFillStyle(0);
   counters_weighted_counter->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: counters_weighted_counter_2
   TPad *counters_weighted_counter_2 = new TPad("counters_weighted_counter_2", "counters_weighted_counter_2",0,0,1,0.304);
   counters_weighted_counter_2->Draw();
   counters_weighted_counter_2->cd();
   counters_weighted_counter_2->Range(-3.848101,-1.04,20.20253,2);
   counters_weighted_counter_2->SetFillColor(0);
   counters_weighted_counter_2->SetFillStyle(4000);
   counters_weighted_counter_2->SetBorderMode(0);
   counters_weighted_counter_2->SetBorderSize(2);
   counters_weighted_counter_2->SetTickx(1);
   counters_weighted_counter_2->SetTicky(1);
   counters_weighted_counter_2->SetLeftMargin(0.16);
   counters_weighted_counter_2->SetRightMargin(0.05);
   counters_weighted_counter_2->SetTopMargin(0);
   counters_weighted_counter_2->SetBottomMargin(0.3421053);
   counters_weighted_counter_2->SetFrameFillStyle(0);
   counters_weighted_counter_2->SetFrameBorderMode(0);
   counters_weighted_counter_2->SetFrameFillStyle(0);
   counters_weighted_counter_2->SetFrameBorderMode(0);
   
   TH1F *hframe1 = new TH1F("hframe1","hframe",19,0,19);
   hframe1->SetMinimum(0);
   hframe1->SetMaximum(2);
   hframe1->SetDirectory(0);
   hframe1->SetStats(0);
   hframe1->SetLineStyle(0);
   hframe1->SetMarkerStyle(20);
   hframe1->GetXaxis()->SetTitle("b-tag SF");
   hframe1->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   hframe1->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   hframe1->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   hframe1->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   hframe1->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   hframe1->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   hframe1->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   hframe1->GetXaxis()->SetBinLabel(8,"All events");
   hframe1->GetXaxis()->SetBinLabel(9,"Passed trigger");
   hframe1->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   hframe1->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   hframe1->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   hframe1->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   hframe1->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   hframe1->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   hframe1->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   hframe1->GetXaxis()->SetBinLabel(17,"b tag SF");
   hframe1->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   hframe1->GetXaxis()->SetBinLabel(19,"Selected events");
   hframe1->GetXaxis()->SetLabelFont(43);
   hframe1->GetXaxis()->SetLabelOffset(0.007);
   hframe1->GetXaxis()->SetLabelSize(10);
   hframe1->GetXaxis()->SetTitleSize(33);
   hframe1->GetXaxis()->SetTitleOffset(2.960526);
   hframe1->GetXaxis()->SetTitleFont(43);
   hframe1->GetYaxis()->SetTitle("Data/MC");
   hframe1->GetYaxis()->SetNdivisions(505);
   hframe1->GetYaxis()->SetLabelFont(43);
   hframe1->GetYaxis()->SetLabelOffset(0.007);
   hframe1->GetYaxis()->SetLabelSize(21);
   hframe1->GetYaxis()->SetTitleSize(33);
   hframe1->GetYaxis()->SetTitleOffset(1.5625);
   hframe1->GetYaxis()->SetTitleFont(43);
   hframe1->GetZaxis()->SetLabelFont(43);
   hframe1->GetZaxis()->SetLabelOffset(0.007);
   hframe1->GetZaxis()->SetLabelSize(27);
   hframe1->GetZaxis()->SetTitleSize(33);
   hframe1->GetZaxis()->SetTitleFont(43);
   hframe1->Draw(" ");
   
   TH1F *counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2 = new TH1F("counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2","Weighted counter",19,0,19);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(1,6.886773e-06);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(2,0.3214207);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(3,0.3214207);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(4,0.3214207);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(5,0.3214207);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(6,0.3252891);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(7,0.3252891);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(8,0.3252891);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(9,0.2905275);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(10,0.2853132);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(11,0.2853132);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(12,0.252152);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(13,0.2520854);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(14,0.2520854);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(15,0.5064331);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(16,0.4813183);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(17,0.4255303);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(18,0.3189308);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinContent(19,0.3189308);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(1,8.10193e-06);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(2,0.2747349);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(3,0.10966);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(4,0.10966);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(5,0.10966);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(6,0.1123154);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(7,0.1123154);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(8,0.1123154);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(9,0.130305);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(10,0.1286247);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(11,0.1286247);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(12,0.1211469);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(13,0.1211452);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(14,0.1211452);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(15,0.04541792);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(16,0.04415138);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(17,0.03968738);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(18,0.01026474);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetBinError(19,0.01026474);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetEntries(141.0662);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetDirectory(0);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetLineWidth(2);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetMarkerStyle(20);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->SetMarkerSize(1.2);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(8,"All events");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetRange(1,19);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetLabelFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetLabelSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetTitleSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetXaxis()->SetTitleFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetYaxis()->SetTitle("Data/MC");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetYaxis()->SetLabelFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetYaxis()->SetLabelSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetYaxis()->SetTitleSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetYaxis()->SetTitleFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetZaxis()->SetLabelFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetZaxis()->SetLabelSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetZaxis()->SetTitleSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->GetZaxis()->SetTitleFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned2->Draw("EP same");
   
   Double_t Graph0_fx1[2] = {
   0,
   19};
   Double_t Graph0_fy1[2] = {
   1,
   1};
   TGraph *graph = new TGraph(2,Graph0_fx1,Graph0_fy1);
   graph->SetName("Graph0");
   graph->SetTitle("Graph");
   graph->SetFillColor(1);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#ff0000");
   graph->SetLineColor(ci);
   graph->SetLineStyle(3);
   graph->SetLineWidth(2);
   graph->SetMarkerStyle(20);
   
   TH1F *Graph_Graph1 = new TH1F("Graph_Graph1","Graph",100,0,20.9);
   Graph_Graph1->SetMinimum(0.9);
   Graph_Graph1->SetMaximum(2.1);
   Graph_Graph1->SetDirectory(0);
   Graph_Graph1->SetStats(0);
   Graph_Graph1->SetLineStyle(0);
   Graph_Graph1->SetMarkerStyle(20);
   Graph_Graph1->GetXaxis()->SetLabelFont(43);
   Graph_Graph1->GetXaxis()->SetLabelOffset(0.007);
   Graph_Graph1->GetXaxis()->SetLabelSize(27);
   Graph_Graph1->GetXaxis()->SetTitleSize(33);
   Graph_Graph1->GetXaxis()->SetTitleOffset(0.9);
   Graph_Graph1->GetXaxis()->SetTitleFont(43);
   Graph_Graph1->GetYaxis()->SetLabelFont(43);
   Graph_Graph1->GetYaxis()->SetLabelOffset(0.007);
   Graph_Graph1->GetYaxis()->SetLabelSize(27);
   Graph_Graph1->GetYaxis()->SetTitleSize(33);
   Graph_Graph1->GetYaxis()->SetTitleOffset(1.25);
   Graph_Graph1->GetYaxis()->SetTitleFont(43);
   Graph_Graph1->GetZaxis()->SetLabelFont(43);
   Graph_Graph1->GetZaxis()->SetLabelOffset(0.007);
   Graph_Graph1->GetZaxis()->SetLabelSize(27);
   Graph_Graph1->GetZaxis()->SetTitleSize(33);
   Graph_Graph1->GetZaxis()->SetTitleFont(43);
   graph->SetHistogram(Graph_Graph1);
   
   graph->Draw("l");
   
   TH1F *hframe_copy3 = new TH1F("hframe_copy3","hframe",19,0,19);
   hframe_copy3->SetMinimum(0);
   hframe_copy3->SetMaximum(2);
   hframe_copy3->SetDirectory(0);
   hframe_copy3->SetStats(0);
   hframe_copy3->SetLineStyle(0);
   hframe_copy3->SetMarkerStyle(20);
   hframe_copy3->GetXaxis()->SetTitle("b-tag SF");
   hframe_copy3->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   hframe_copy3->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   hframe_copy3->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   hframe_copy3->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   hframe_copy3->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   hframe_copy3->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   hframe_copy3->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   hframe_copy3->GetXaxis()->SetBinLabel(8,"All events");
   hframe_copy3->GetXaxis()->SetBinLabel(9,"Passed trigger");
   hframe_copy3->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   hframe_copy3->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   hframe_copy3->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   hframe_copy3->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   hframe_copy3->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   hframe_copy3->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   hframe_copy3->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   hframe_copy3->GetXaxis()->SetBinLabel(17,"b tag SF");
   hframe_copy3->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   hframe_copy3->GetXaxis()->SetBinLabel(19,"Selected events");
   hframe_copy3->GetXaxis()->SetLabelFont(43);
   hframe_copy3->GetXaxis()->SetLabelOffset(0.007);
   hframe_copy3->GetXaxis()->SetLabelSize(10);
   hframe_copy3->GetXaxis()->SetTitleSize(33);
   hframe_copy3->GetXaxis()->SetTitleOffset(2.960526);
   hframe_copy3->GetXaxis()->SetTitleFont(43);
   hframe_copy3->GetYaxis()->SetTitle("Data/MC");
   hframe_copy3->GetYaxis()->SetNdivisions(505);
   hframe_copy3->GetYaxis()->SetLabelFont(43);
   hframe_copy3->GetYaxis()->SetLabelOffset(0.007);
   hframe_copy3->GetYaxis()->SetLabelSize(21);
   hframe_copy3->GetYaxis()->SetTitleSize(33);
   hframe_copy3->GetYaxis()->SetTitleOffset(1.5625);
   hframe_copy3->GetYaxis()->SetTitleFont(43);
   hframe_copy3->GetZaxis()->SetLabelFont(43);
   hframe_copy3->GetZaxis()->SetLabelOffset(0.007);
   hframe_copy3->GetZaxis()->SetLabelSize(27);
   hframe_copy3->GetZaxis()->SetTitleSize(33);
   hframe_copy3->GetZaxis()->SetTitleFont(43);
   hframe_copy3->Draw("sameaxis");
   counters_weighted_counter_2->Modified();
   counters_weighted_counter->cd();
  
// ------------>Primitives in pad: coverpad
   TPad *coverpad = new TPad("coverpad", "coverpad",0.065,0.285,0.158,0.33);
   coverpad->Draw();
   coverpad->cd();
   coverpad->Range(0,0,1,1);
   coverpad->SetFillColor(0);
   coverpad->SetBorderMode(0);
   coverpad->SetBorderSize(2);
   coverpad->SetTickx(1);
   coverpad->SetTicky(1);
   coverpad->SetLeftMargin(0.16);
   coverpad->SetRightMargin(0.05);
   coverpad->SetTopMargin(0.06);
   coverpad->SetBottomMargin(0.13);
   coverpad->SetFrameFillStyle(0);
   coverpad->SetFrameBorderMode(0);
   coverpad->Modified();
   counters_weighted_counter->cd();
  
// ------------>Primitives in pad: counters_weighted_counter_1
   TPad *counters_weighted_counter_1 = new TPad("counters_weighted_counter_1", "counters_weighted_counter_1",0,0.2897959,1,1);
   counters_weighted_counter_1->Draw();
   counters_weighted_counter_1->cd();
   counters_weighted_counter_1->Range(-3.848101,-1.359003,20.20253,16.59112);
   counters_weighted_counter_1->SetFillColor(0);
   counters_weighted_counter_1->SetFillStyle(4000);
   counters_weighted_counter_1->SetBorderMode(0);
   counters_weighted_counter_1->SetBorderSize(2);
   counters_weighted_counter_1->SetLogy();
   counters_weighted_counter_1->SetTickx(1);
   counters_weighted_counter_1->SetTicky(1);
   counters_weighted_counter_1->SetLeftMargin(0.16);
   counters_weighted_counter_1->SetRightMargin(0.05);
   counters_weighted_counter_1->SetTopMargin(0.06);
   counters_weighted_counter_1->SetBottomMargin(0.02);
   counters_weighted_counter_1->SetFrameFillStyle(0);
   counters_weighted_counter_1->SetFrameBorderMode(0);
   counters_weighted_counter_1->SetFrameFillStyle(0);
   counters_weighted_counter_1->SetFrameBorderMode(0);
   
   TH1F *hframe4 = new TH1F("hframe4","hframe",19,0,19);
   hframe4->SetMinimum(0.1);
   hframe4->SetMaximum(3.266752e+15);
   hframe4->SetDirectory(0);
   hframe4->SetStats(0);
   hframe4->SetLineStyle(0);
   hframe4->SetMarkerStyle(20);
   hframe4->GetXaxis()->SetLabelFont(43);
   hframe4->GetXaxis()->SetLabelOffset(0.007);
   hframe4->GetXaxis()->SetLabelSize(0);
   hframe4->GetXaxis()->SetTitleSize(0);
   hframe4->GetXaxis()->SetTitleOffset(0.9);
   hframe4->GetXaxis()->SetTitleFont(43);
   hframe4->GetYaxis()->SetTitle("Events / 1");
   hframe4->GetYaxis()->SetLabelFont(43);
   hframe4->GetYaxis()->SetLabelOffset(0.007);
   hframe4->GetYaxis()->SetLabelSize(27);
   hframe4->GetYaxis()->SetTitleSize(33);
   hframe4->GetYaxis()->SetTitleOffset(1.5625);
   hframe4->GetYaxis()->SetTitleFont(43);
   hframe4->GetZaxis()->SetLabelFont(43);
   hframe4->GetZaxis()->SetLabelOffset(0.007);
   hframe4->GetZaxis()->SetLabelSize(27);
   hframe4->GetZaxis()->SetTitleSize(33);
   hframe4->GetZaxis()->SetTitleFont(43);
   hframe4->Draw(" ");
   
   THStack *StackedMCstackHist = new THStack();
   StackedMCstackHist->SetName("StackedMCstackHist");
   StackedMCstackHist->SetTitle("StackedMCstackHist");
   
   TH1F *StackedMCstackHist_stack_1 = new TH1F("StackedMCstackHist_stack_1","StackedMCstackHist",19,0,19);
   StackedMCstackHist_stack_1->SetMinimum(1.306697e+10);
   StackedMCstackHist_stack_1->SetMaximum(5.226789e+13);
   StackedMCstackHist_stack_1->SetDirectory(0);
   StackedMCstackHist_stack_1->SetStats(0);
   StackedMCstackHist_stack_1->SetLineStyle(0);
   StackedMCstackHist_stack_1->SetMarkerStyle(20);
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(8,"All events");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(9,"Passed trigger");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(17,"b tag SF");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   StackedMCstackHist_stack_1->GetXaxis()->SetBinLabel(19,"Selected events");
   StackedMCstackHist_stack_1->GetXaxis()->SetLabelFont(43);
   StackedMCstackHist_stack_1->GetXaxis()->SetLabelOffset(0.007);
   StackedMCstackHist_stack_1->GetXaxis()->SetLabelSize(27);
   StackedMCstackHist_stack_1->GetXaxis()->SetTitleSize(33);
   StackedMCstackHist_stack_1->GetXaxis()->SetTitleOffset(0.9);
   StackedMCstackHist_stack_1->GetXaxis()->SetTitleFont(43);
   StackedMCstackHist_stack_1->GetYaxis()->SetLabelFont(43);
   StackedMCstackHist_stack_1->GetYaxis()->SetLabelOffset(0.007);
   StackedMCstackHist_stack_1->GetYaxis()->SetLabelSize(27);
   StackedMCstackHist_stack_1->GetYaxis()->SetTitleSize(33);
   StackedMCstackHist_stack_1->GetYaxis()->SetTitleOffset(1.25);
   StackedMCstackHist_stack_1->GetYaxis()->SetTitleFont(43);
   StackedMCstackHist_stack_1->GetZaxis()->SetLabelFont(43);
   StackedMCstackHist_stack_1->GetZaxis()->SetLabelOffset(0.007);
   StackedMCstackHist_stack_1->GetZaxis()->SetLabelSize(27);
   StackedMCstackHist_stack_1->GetZaxis()->SetTitleSize(33);
   StackedMCstackHist_stack_1->GetZaxis()->SetTitleFont(43);
   StackedMCstackHist->SetHistogram(StackedMCstackHist_stack_1);
   
   
   TH1F *counter_TTTT_cloned5 = new TH1F("counter_TTTT_cloned5","Weighted counter",19,0,19);
   counter_TTTT_cloned5->SetBinContent(1,156.865);
   counter_TTTT_cloned5->SetBinContent(2,79.82933);
   counter_TTTT_cloned5->SetBinContent(3,79.82933);
   counter_TTTT_cloned5->SetBinContent(4,79.82933);
   counter_TTTT_cloned5->SetBinContent(5,79.82933);
   counter_TTTT_cloned5->SetBinContent(6,64.83626);
   counter_TTTT_cloned5->SetBinContent(7,64.83626);
   counter_TTTT_cloned5->SetBinContent(8,64.83626);
   counter_TTTT_cloned5->SetBinError(1,156.865);
   counter_TTTT_cloned5->SetBinError(2,79.82933);
   counter_TTTT_cloned5->SetBinError(3,0.2716845);
   counter_TTTT_cloned5->SetBinError(4,0.2716845);
   counter_TTTT_cloned5->SetBinError(5,0.2716845);
   counter_TTTT_cloned5->SetBinError(6,0.2232291);
   counter_TTTT_cloned5->SetBinError(7,0.2232291);
   counter_TTTT_cloned5->SetBinError(8,0.2232291);
   counter_TTTT_cloned5->SetEntries(23);
   counter_TTTT_cloned5->SetDirectory(0);

   ci = TColor::GetColor("#ffffcc");
   counter_TTTT_cloned5->SetFillColor(ci);

   ci = TColor::GetColor("#ffffcc");
   counter_TTTT_cloned5->SetLineColor(ci);
   counter_TTTT_cloned5->SetLineWidth(2);

   ci = TColor::GetColor("#ffffcc");
   counter_TTTT_cloned5->SetMarkerColor(ci);
   counter_TTTT_cloned5->SetMarkerStyle(29);
   counter_TTTT_cloned5->SetMarkerSize(1.2);
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(8,"All events");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_TTTT_cloned5->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_TTTT_cloned5->GetXaxis()->SetRange(1,19);
   counter_TTTT_cloned5->GetXaxis()->SetLabelFont(42);
   counter_TTTT_cloned5->GetXaxis()->SetLabelSize(0.035);
   counter_TTTT_cloned5->GetXaxis()->SetTitleSize(0.035);
   counter_TTTT_cloned5->GetXaxis()->SetTitleFont(42);
   counter_TTTT_cloned5->GetYaxis()->SetLabelFont(42);
   counter_TTTT_cloned5->GetYaxis()->SetLabelSize(0.035);
   counter_TTTT_cloned5->GetYaxis()->SetTitleSize(0.035);
   counter_TTTT_cloned5->GetYaxis()->SetTitleFont(42);
   counter_TTTT_cloned5->GetZaxis()->SetLabelFont(42);
   counter_TTTT_cloned5->GetZaxis()->SetLabelSize(0.035);
   counter_TTTT_cloned5->GetZaxis()->SetTitleSize(0.035);
   counter_TTTT_cloned5->GetZaxis()->SetTitleFont(42);
   StackedMCstackHist->Add(counter_TTTT_cloned,"");
   
   TH1F *counter_TTWJetsToQQ_cloned6 = new TH1F("counter_TTWJetsToQQ_cloned6","Weighted counter",19,0,19);
   counter_TTWJetsToQQ_cloned6->SetBinContent(1,2988.014);
   counter_TTWJetsToQQ_cloned6->SetBinContent(2,2074.979);
   counter_TTWJetsToQQ_cloned6->SetBinContent(3,2074.979);
   counter_TTWJetsToQQ_cloned6->SetBinContent(4,2074.979);
   counter_TTWJetsToQQ_cloned6->SetBinContent(5,2074.979);
   counter_TTWJetsToQQ_cloned6->SetBinContent(6,1963.123);
   counter_TTWJetsToQQ_cloned6->SetBinContent(7,1963.123);
   counter_TTWJetsToQQ_cloned6->SetBinContent(8,1963.123);
   counter_TTWJetsToQQ_cloned6->SetBinError(1,2988.014);
   counter_TTWJetsToQQ_cloned6->SetBinError(2,2074.979);
   counter_TTWJetsToQQ_cloned6->SetBinError(3,5.287806);
   counter_TTWJetsToQQ_cloned6->SetBinError(4,5.287806);
   counter_TTWJetsToQQ_cloned6->SetBinError(5,5.287806);
   counter_TTWJetsToQQ_cloned6->SetBinError(6,5.000904);
   counter_TTWJetsToQQ_cloned6->SetBinError(7,5.000904);
   counter_TTWJetsToQQ_cloned6->SetBinError(8,5.000904);
   counter_TTWJetsToQQ_cloned6->SetEntries(23);
   counter_TTWJetsToQQ_cloned6->SetDirectory(0);

   ci = TColor::GetColor("#99cc00");
   counter_TTWJetsToQQ_cloned6->SetFillColor(ci);

   ci = TColor::GetColor("#99cc00");
   counter_TTWJetsToQQ_cloned6->SetLineColor(ci);
   counter_TTWJetsToQQ_cloned6->SetLineWidth(2);

   ci = TColor::GetColor("#99cc00");
   counter_TTWJetsToQQ_cloned6->SetMarkerColor(ci);
   counter_TTWJetsToQQ_cloned6->SetMarkerStyle(25);
   counter_TTWJetsToQQ_cloned6->SetMarkerSize(1.2);
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(8,"All events");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetRange(1,19);
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetLabelFont(42);
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetLabelSize(0.035);
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetTitleSize(0.035);
   counter_TTWJetsToQQ_cloned6->GetXaxis()->SetTitleFont(42);
   counter_TTWJetsToQQ_cloned6->GetYaxis()->SetLabelFont(42);
   counter_TTWJetsToQQ_cloned6->GetYaxis()->SetLabelSize(0.035);
   counter_TTWJetsToQQ_cloned6->GetYaxis()->SetTitleSize(0.035);
   counter_TTWJetsToQQ_cloned6->GetYaxis()->SetTitleFont(42);
   counter_TTWJetsToQQ_cloned6->GetZaxis()->SetLabelFont(42);
   counter_TTWJetsToQQ_cloned6->GetZaxis()->SetLabelSize(0.035);
   counter_TTWJetsToQQ_cloned6->GetZaxis()->SetTitleSize(0.035);
   counter_TTWJetsToQQ_cloned6->GetZaxis()->SetTitleFont(42);
   StackedMCstackHist->Add(counter_TTWJetsToQQ_cloned,"");
   
   TH1F *counter_TTZToQQ_cloned7 = new TH1F("counter_TTZToQQ_cloned7","Weighted counter",19,0,19);
   counter_TTZToQQ_cloned7->SetBinContent(1,11721.67);
   counter_TTZToQQ_cloned7->SetBinContent(2,8127.632);
   counter_TTZToQQ_cloned7->SetBinContent(3,8127.632);
   counter_TTZToQQ_cloned7->SetBinContent(4,8127.632);
   counter_TTZToQQ_cloned7->SetBinContent(5,8127.632);
   counter_TTZToQQ_cloned7->SetBinContent(6,7717.536);
   counter_TTZToQQ_cloned7->SetBinContent(7,7717.536);
   counter_TTZToQQ_cloned7->SetBinContent(8,7717.536);
   counter_TTZToQQ_cloned7->SetBinError(1,11721.67);
   counter_TTZToQQ_cloned7->SetBinError(2,8127.632);
   counter_TTZToQQ_cloned7->SetBinError(3,24.11998);
   counter_TTZToQQ_cloned7->SetBinError(4,24.11998);
   counter_TTZToQQ_cloned7->SetBinError(5,24.11998);
   counter_TTZToQQ_cloned7->SetBinError(6,22.9716);
   counter_TTZToQQ_cloned7->SetBinError(7,22.9716);
   counter_TTZToQQ_cloned7->SetBinError(8,22.9716);
   counter_TTZToQQ_cloned7->SetEntries(23);
   counter_TTZToQQ_cloned7->SetDirectory(0);

   ci = TColor::GetColor("#6699ff");
   counter_TTZToQQ_cloned7->SetFillColor(ci);

   ci = TColor::GetColor("#6699ff");
   counter_TTZToQQ_cloned7->SetLineColor(ci);
   counter_TTZToQQ_cloned7->SetLineWidth(2);

   ci = TColor::GetColor("#6699ff");
   counter_TTZToQQ_cloned7->SetMarkerColor(ci);
   counter_TTZToQQ_cloned7->SetMarkerStyle(33);
   counter_TTZToQQ_cloned7->SetMarkerSize(1.2);
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(8,"All events");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_TTZToQQ_cloned7->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_TTZToQQ_cloned7->GetXaxis()->SetRange(1,19);
   counter_TTZToQQ_cloned7->GetXaxis()->SetLabelFont(42);
   counter_TTZToQQ_cloned7->GetXaxis()->SetLabelSize(0.035);
   counter_TTZToQQ_cloned7->GetXaxis()->SetTitleSize(0.035);
   counter_TTZToQQ_cloned7->GetXaxis()->SetTitleFont(42);
   counter_TTZToQQ_cloned7->GetYaxis()->SetLabelFont(42);
   counter_TTZToQQ_cloned7->GetYaxis()->SetLabelSize(0.035);
   counter_TTZToQQ_cloned7->GetYaxis()->SetTitleSize(0.035);
   counter_TTZToQQ_cloned7->GetYaxis()->SetTitleFont(42);
   counter_TTZToQQ_cloned7->GetZaxis()->SetLabelFont(42);
   counter_TTZToQQ_cloned7->GetZaxis()->SetLabelSize(0.035);
   counter_TTZToQQ_cloned7->GetZaxis()->SetTitleSize(0.035);
   counter_TTZToQQ_cloned7->GetZaxis()->SetTitleFont(42);
   StackedMCstackHist->Add(counter_TTZToQQ_cloned,"");
   
   TH1F *counter_TTBB_cloned8 = new TH1F("counter_TTBB_cloned8","Weighted counter",19,0,19);
   counter_TTBB_cloned8->SetBinContent(1,97501.88);
   counter_TTBB_cloned8->SetBinContent(2,66752.21);
   counter_TTBB_cloned8->SetBinContent(3,66752.21);
   counter_TTBB_cloned8->SetBinContent(4,66752.21);
   counter_TTBB_cloned8->SetBinContent(5,66752.21);
   counter_TTBB_cloned8->SetBinContent(6,66752.21);
   counter_TTBB_cloned8->SetBinContent(7,66752.21);
   counter_TTBB_cloned8->SetBinContent(8,66752.21);
   counter_TTBB_cloned8->SetBinError(1,97501.88);
   counter_TTBB_cloned8->SetBinError(2,66752.21);
   counter_TTBB_cloned8->SetBinError(3,201.7686);
   counter_TTBB_cloned8->SetBinError(4,201.7686);
   counter_TTBB_cloned8->SetBinError(5,201.7686);
   counter_TTBB_cloned8->SetBinError(6,201.7686);
   counter_TTBB_cloned8->SetBinError(7,201.7686);
   counter_TTBB_cloned8->SetBinError(8,201.7686);
   counter_TTBB_cloned8->SetEntries(23);
   counter_TTBB_cloned8->SetDirectory(0);

   ci = TColor::GetColor("#ff3399");
   counter_TTBB_cloned8->SetFillColor(ci);

   ci = TColor::GetColor("#ff3399");
   counter_TTBB_cloned8->SetLineColor(ci);
   counter_TTBB_cloned8->SetLineWidth(2);

   ci = TColor::GetColor("#ff3399");
   counter_TTBB_cloned8->SetMarkerColor(ci);
   counter_TTBB_cloned8->SetMarkerStyle(28);
   counter_TTBB_cloned8->SetMarkerSize(1.2);
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(8,"All events");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_TTBB_cloned8->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_TTBB_cloned8->GetXaxis()->SetRange(1,19);
   counter_TTBB_cloned8->GetXaxis()->SetLabelFont(42);
   counter_TTBB_cloned8->GetXaxis()->SetLabelSize(0.035);
   counter_TTBB_cloned8->GetXaxis()->SetTitleSize(0.035);
   counter_TTBB_cloned8->GetXaxis()->SetTitleFont(42);
   counter_TTBB_cloned8->GetYaxis()->SetLabelFont(42);
   counter_TTBB_cloned8->GetYaxis()->SetLabelSize(0.035);
   counter_TTBB_cloned8->GetYaxis()->SetTitleSize(0.035);
   counter_TTBB_cloned8->GetYaxis()->SetTitleFont(42);
   counter_TTBB_cloned8->GetZaxis()->SetLabelFont(42);
   counter_TTBB_cloned8->GetZaxis()->SetLabelSize(0.035);
   counter_TTBB_cloned8->GetZaxis()->SetTitleSize(0.035);
   counter_TTBB_cloned8->GetZaxis()->SetTitleFont(42);
   StackedMCstackHist->Add(counter_TTBB_cloned,"");
   
   TH1F *counter_Diboson_cloned9 = new TH1F("counter_Diboson_cloned9","Weighted counter",19,0,19);
   counter_Diboson_cloned9->SetBinContent(1,338771.8);
   counter_Diboson_cloned9->SetBinContent(2,269569.8);
   counter_Diboson_cloned9->SetBinContent(3,269569.8);
   counter_Diboson_cloned9->SetBinContent(4,269569.8);
   counter_Diboson_cloned9->SetBinContent(5,269569.8);
   counter_Diboson_cloned9->SetBinContent(6,269569.8);
   counter_Diboson_cloned9->SetBinContent(7,269569.8);
   counter_Diboson_cloned9->SetBinContent(8,269569.8);
   counter_Diboson_cloned9->SetBinError(1,338771.8);
   counter_Diboson_cloned9->SetBinError(2,269569.9);
   counter_Diboson_cloned9->SetBinError(3,302.1964);
   counter_Diboson_cloned9->SetBinError(4,302.1964);
   counter_Diboson_cloned9->SetBinError(5,302.1964);
   counter_Diboson_cloned9->SetBinError(6,302.1964);
   counter_Diboson_cloned9->SetBinError(7,302.1964);
   counter_Diboson_cloned9->SetBinError(8,302.1964);
   counter_Diboson_cloned9->SetEntries(23);
   counter_Diboson_cloned9->SetDirectory(0);

   ci = TColor::GetColor("#3333ff");
   counter_Diboson_cloned9->SetFillColor(ci);

   ci = TColor::GetColor("#3333ff");
   counter_Diboson_cloned9->SetLineColor(ci);
   counter_Diboson_cloned9->SetLineWidth(2);

   ci = TColor::GetColor("#3333ff");
   counter_Diboson_cloned9->SetMarkerColor(ci);
   counter_Diboson_cloned9->SetMarkerStyle(5);
   counter_Diboson_cloned9->SetMarkerSize(1.2);
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(8,"All events");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_Diboson_cloned9->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_Diboson_cloned9->GetXaxis()->SetRange(1,19);
   counter_Diboson_cloned9->GetXaxis()->SetLabelFont(42);
   counter_Diboson_cloned9->GetXaxis()->SetLabelSize(0.035);
   counter_Diboson_cloned9->GetXaxis()->SetTitleSize(0.035);
   counter_Diboson_cloned9->GetXaxis()->SetTitleFont(42);
   counter_Diboson_cloned9->GetYaxis()->SetLabelFont(42);
   counter_Diboson_cloned9->GetYaxis()->SetLabelSize(0.035);
   counter_Diboson_cloned9->GetYaxis()->SetTitleSize(0.035);
   counter_Diboson_cloned9->GetYaxis()->SetTitleFont(42);
   counter_Diboson_cloned9->GetZaxis()->SetLabelFont(42);
   counter_Diboson_cloned9->GetZaxis()->SetLabelSize(0.035);
   counter_Diboson_cloned9->GetZaxis()->SetTitleSize(0.035);
   counter_Diboson_cloned9->GetZaxis()->SetTitleFont(42);
   StackedMCstackHist->Add(counter_Diboson_cloned,"");
   
   TH1F *counter_WJetsToQQ_HT_600ToInf_cloned10 = new TH1F("counter_WJetsToQQ_HT_600ToInf_cloned10","Weighted counter",19,0,19);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinContent(1,695462.1);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinContent(2,691876.9);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinContent(3,691876.9);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinContent(4,691876.9);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinContent(5,691876.9);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinContent(6,691876.9);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinContent(7,691876.9);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinContent(8,691876.9);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinError(1,695462.1);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinError(2,691876.9);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinError(3,685.1539);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinError(4,685.1539);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinError(5,685.1539);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinError(6,685.1539);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinError(7,685.1539);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetBinError(8,685.1539);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetEntries(23);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetDirectory(0);

   ci = TColor::GetColor("#cc3300");
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetFillColor(ci);

   ci = TColor::GetColor("#cc3300");
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetLineColor(ci);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetLineWidth(2);

   ci = TColor::GetColor("#cc3300");
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetMarkerColor(ci);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetMarkerStyle(3);
   counter_WJetsToQQ_HT_600ToInf_cloned10->SetMarkerSize(1.2);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(8,"All events");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetRange(1,19);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetLabelFont(42);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetLabelSize(0.035);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetTitleSize(0.035);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetXaxis()->SetTitleFont(42);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetYaxis()->SetLabelFont(42);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetYaxis()->SetLabelSize(0.035);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetYaxis()->SetTitleSize(0.035);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetYaxis()->SetTitleFont(42);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetZaxis()->SetLabelFont(42);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetZaxis()->SetLabelSize(0.035);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetZaxis()->SetTitleSize(0.035);
   counter_WJetsToQQ_HT_600ToInf_cloned10->GetZaxis()->SetTitleFont(42);
   StackedMCstackHist->Add(counter_WJetsToQQ_HT_600ToInf_cloned,"");
   
   TH1F *counter_ST_tW_top_5f_inclusiveDecays_cloned11 = new TH1F("counter_ST_tW_top_5f_inclusiveDecays_cloned11","Weighted counter",19,0,19);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinContent(1,777355.2);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinContent(2,605932.5);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinContent(3,605932.5);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinContent(4,605932.5);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinContent(5,605932.5);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinContent(6,605932.5);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinContent(7,605932.5);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinContent(8,605932.5);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinError(1,604529);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinError(2,485143.8);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinError(3,207.9491);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinError(4,207.9491);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinError(5,207.9491);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinError(6,207.9491);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinError(7,207.9491);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetBinError(8,207.9491);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetEntries(42);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetDirectory(0);

   ci = TColor::GetColor("#669900");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetFillColor(ci);

   ci = TColor::GetColor("#669900");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetLineColor(ci);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetLineWidth(2);

   ci = TColor::GetColor("#669900");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetMarkerColor(ci);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetMarkerStyle(2);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->SetMarkerSize(1.2);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(8,"All events");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetRange(1,19);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetLabelFont(42);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetLabelSize(0.035);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetTitleSize(0.035);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetXaxis()->SetTitleFont(42);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetYaxis()->SetLabelFont(42);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetYaxis()->SetLabelSize(0.035);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetYaxis()->SetTitleSize(0.035);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetYaxis()->SetTitleFont(42);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetZaxis()->SetLabelFont(42);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetZaxis()->SetLabelSize(0.035);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetZaxis()->SetTitleSize(0.035);
   counter_ST_tW_top_5f_inclusiveDecays_cloned11->GetZaxis()->SetTitleFont(42);
   StackedMCstackHist->Add(counter_ST_tW_top_5f_inclusiveDecays_cloned,"");
   
   TH1F *counter_ZJetsToQQ_HT600toInf_cloned12 = new TH1F("counter_ZJetsToQQ_HT600toInf_cloned12","Weighted counter",19,0,19);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(1,4075061);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(2,663051.8);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(3,663051.8);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(4,663051.8);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(5,663051.8);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(6,663051.8);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(7,663051.8);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(8,663051.8);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(9,374268.1);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(10,370445.9);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(11,370445.9);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(12,405084.2);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(13,404889.9);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(14,404889.9);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(15,379716.5);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(16,370350.3);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(17,405556.9);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(18,19040.34);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinContent(19,19040.34);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(1,4075061);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(2,663051.8);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(3,1649.893);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(4,1649.893);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(5,1649.893);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(6,1649.893);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(7,1649.893);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(8,1649.893);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(9,1239.577);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(10,1233.231);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(11,1233.231);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(12,1377.641);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(13,1377.306);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(14,1377.306);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(15,1333.98);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(16,1317.488);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(17,1460.63);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(18,295.2202);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetBinError(19,295.2202);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetEntries(23);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetDirectory(0);

   ci = TColor::GetColor("#ff6666");
   counter_ZJetsToQQ_HT600toInf_cloned12->SetFillColor(ci);

   ci = TColor::GetColor("#ff6666");
   counter_ZJetsToQQ_HT600toInf_cloned12->SetLineColor(ci);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetLineWidth(2);

   ci = TColor::GetColor("#ff6666");
   counter_ZJetsToQQ_HT600toInf_cloned12->SetMarkerColor(ci);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetMarkerStyle(34);
   counter_ZJetsToQQ_HT600toInf_cloned12->SetMarkerSize(1.2);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(8,"All events");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetRange(1,19);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetLabelFont(42);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetLabelSize(0.035);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetTitleSize(0.035);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetXaxis()->SetTitleFont(42);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetYaxis()->SetLabelFont(42);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetYaxis()->SetLabelSize(0.035);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetYaxis()->SetTitleSize(0.035);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetYaxis()->SetTitleFont(42);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetZaxis()->SetLabelFont(42);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetZaxis()->SetLabelSize(0.035);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetZaxis()->SetTitleSize(0.035);
   counter_ZJetsToQQ_HT600toInf_cloned12->GetZaxis()->SetTitleFont(42);
   StackedMCstackHist->Add(counter_ZJetsToQQ_HT600toInf_cloned,"");
   
   TH1F *counter_TT_cloned13 = new TH1F("counter_TT_cloned13","Weighted counter",19,0,19);
   counter_TT_cloned13->SetBinContent(1,7.617367e+07);
   counter_TT_cloned13->SetBinContent(2,6312329);
   counter_TT_cloned13->SetBinContent(3,6312329);
   counter_TT_cloned13->SetBinContent(4,6312329);
   counter_TT_cloned13->SetBinContent(5,6312329);
   counter_TT_cloned13->SetBinContent(6,5762943);
   counter_TT_cloned13->SetBinContent(7,5762943);
   counter_TT_cloned13->SetBinContent(8,5762943);
   counter_TT_cloned13->SetBinContent(9,4764118);
   counter_TT_cloned13->SetBinContent(10,4721030);
   counter_TT_cloned13->SetBinContent(11,4721030);
   counter_TT_cloned13->SetBinContent(12,5048343);
   counter_TT_cloned13->SetBinContent(13,5038845);
   counter_TT_cloned13->SetBinContent(14,5038845);
   counter_TT_cloned13->SetBinContent(15,4655096);
   counter_TT_cloned13->SetBinContent(16,4642064);
   counter_TT_cloned13->SetBinContent(17,4669396);
   counter_TT_cloned13->SetBinContent(18,300625);
   counter_TT_cloned13->SetBinContent(19,300625);
   counter_TT_cloned13->SetBinError(1,7.617367e+07);
   counter_TT_cloned13->SetBinError(2,6312329);
   counter_TT_cloned13->SetBinError(3,2274.724);
   counter_TT_cloned13->SetBinError(4,2274.724);
   counter_TT_cloned13->SetBinError(5,2274.724);
   counter_TT_cloned13->SetBinError(6,2087.564);
   counter_TT_cloned13->SetBinError(7,2087.564);
   counter_TT_cloned13->SetBinError(8,2087.564);
   counter_TT_cloned13->SetBinError(9,1901.26);
   counter_TT_cloned13->SetBinError(10,1892.67);
   counter_TT_cloned13->SetBinError(11,1892.67);
   counter_TT_cloned13->SetBinError(12,2064.724);
   counter_TT_cloned13->SetBinError(13,2062.629);
   counter_TT_cloned13->SetBinError(14,2062.629);
   counter_TT_cloned13->SetBinError(15,1982.092);
   counter_TT_cloned13->SetBinError(16,1979.279);
   counter_TT_cloned13->SetBinError(17,2006.635);
   counter_TT_cloned13->SetBinError(18,467.5117);
   counter_TT_cloned13->SetBinError(19,467.5117);
   counter_TT_cloned13->SetEntries(23);
   counter_TT_cloned13->SetDirectory(0);

   ci = TColor::GetColor("#993399");
   counter_TT_cloned13->SetFillColor(ci);

   ci = TColor::GetColor("#993399");
   counter_TT_cloned13->SetLineColor(ci);
   counter_TT_cloned13->SetLineWidth(2);

   ci = TColor::GetColor("#993399");
   counter_TT_cloned13->SetMarkerColor(ci);
   counter_TT_cloned13->SetMarkerStyle(21);
   counter_TT_cloned13->SetMarkerSize(1.2);
   counter_TT_cloned13->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(8,"All events");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_TT_cloned13->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_TT_cloned13->GetXaxis()->SetRange(1,19);
   counter_TT_cloned13->GetXaxis()->SetLabelFont(42);
   counter_TT_cloned13->GetXaxis()->SetLabelSize(0.035);
   counter_TT_cloned13->GetXaxis()->SetTitleSize(0.035);
   counter_TT_cloned13->GetXaxis()->SetTitleFont(42);
   counter_TT_cloned13->GetYaxis()->SetLabelFont(42);
   counter_TT_cloned13->GetYaxis()->SetLabelSize(0.035);
   counter_TT_cloned13->GetYaxis()->SetTitleSize(0.035);
   counter_TT_cloned13->GetYaxis()->SetTitleFont(42);
   counter_TT_cloned13->GetZaxis()->SetLabelFont(42);
   counter_TT_cloned13->GetZaxis()->SetLabelSize(0.035);
   counter_TT_cloned13->GetZaxis()->SetTitleSize(0.035);
   counter_TT_cloned13->GetZaxis()->SetTitleFont(42);
   StackedMCstackHist->Add(counter_TT_cloned,"");
   
   TH1F *counter_QCD_Pt_1000to1400_cloned14 = new TH1F("counter_QCD_Pt_1000to1400_cloned14","Weighted counter",19,0,19);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(1,1.696821e+13);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(2,3.762274e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(3,3.762274e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(4,3.762274e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(5,3.762274e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(6,3.762274e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(7,3.762274e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(8,3.762274e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(9,3.002881e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(10,2.989557e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(11,2.989557e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(12,3.413485e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(13,3.413463e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(14,3.413463e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(15,1.079652e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(16,1.045995e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(17,1.242588e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(18,158614);
   counter_QCD_Pt_1000to1400_cloned14->SetBinContent(19,158614);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(1,1.569922e+13);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(2,1.883685e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(3,1.577668e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(4,1.577668e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(5,1.577668e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(6,1.577668e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(7,1.577668e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(8,1.577668e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(9,1.577289e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(10,1.577283e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(11,1.577283e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(12,1.902025e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(13,1.902025e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(14,1.902025e+07);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(15,1419772);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(16,1419268);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(17,1632213);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(18,15334.6);
   counter_QCD_Pt_1000to1400_cloned14->SetBinError(19,15334.6);
   counter_QCD_Pt_1000to1400_cloned14->SetEntries(289);
   counter_QCD_Pt_1000to1400_cloned14->SetDirectory(0);

   ci = TColor::GetColor("#ffcc33");
   counter_QCD_Pt_1000to1400_cloned14->SetFillColor(ci);

   ci = TColor::GetColor("#ffcc33");
   counter_QCD_Pt_1000to1400_cloned14->SetLineColor(ci);
   counter_QCD_Pt_1000to1400_cloned14->SetLineWidth(2);

   ci = TColor::GetColor("#ffcc33");
   counter_QCD_Pt_1000to1400_cloned14->SetMarkerColor(ci);
   counter_QCD_Pt_1000to1400_cloned14->SetMarkerStyle(22);
   counter_QCD_Pt_1000to1400_cloned14->SetMarkerSize(1.2);
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(8,"All events");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetRange(1,19);
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetLabelFont(42);
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetLabelSize(0.035);
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetTitleSize(0.035);
   counter_QCD_Pt_1000to1400_cloned14->GetXaxis()->SetTitleFont(42);
   counter_QCD_Pt_1000to1400_cloned14->GetYaxis()->SetLabelFont(42);
   counter_QCD_Pt_1000to1400_cloned14->GetYaxis()->SetLabelSize(0.035);
   counter_QCD_Pt_1000to1400_cloned14->GetYaxis()->SetTitleSize(0.035);
   counter_QCD_Pt_1000to1400_cloned14->GetYaxis()->SetTitleFont(42);
   counter_QCD_Pt_1000to1400_cloned14->GetZaxis()->SetLabelFont(42);
   counter_QCD_Pt_1000to1400_cloned14->GetZaxis()->SetLabelSize(0.035);
   counter_QCD_Pt_1000to1400_cloned14->GetZaxis()->SetTitleSize(0.035);
   counter_QCD_Pt_1000to1400_cloned14->GetZaxis()->SetTitleFont(42);
   StackedMCstackHist->Add(counter_QCD_Pt_1000to1400_cloned,"");
   StackedMCstackHist->Draw("hist same");
   
   Double_t counter_QCD_Pt_1000to1400_cloned_sum_errors_fx3001[19] = {
   0.5,
   1.5,
   2.5,
   3.5,
   4.5,
   5.5,
   6.5,
   7.5,
   8.5,
   9.5,
   10.5,
   11.5,
   12.5,
   13.5,
   14.5,
   15.5,
   16.5,
   17.5,
   18.5};
   Double_t counter_QCD_Pt_1000to1400_cloned_sum_errors_fy3001[19] = {
   1.696829e+13,
   4.624253e+07,
   4.624253e+07,
   4.624253e+07,
   4.624253e+07,
   4.56926e+07,
   4.56926e+07,
   4.56926e+07,
   3.51672e+07,
   3.498704e+07,
   3.498704e+07,
   3.958828e+07,
   3.957836e+07,
   3.957836e+07,
   1.583133e+07,
   1.547236e+07,
   1.750083e+07,
   478279.3,
   478279.3};
   Double_t counter_QCD_Pt_1000to1400_cloned_sum_errors_felx3001[19] = {
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5};
   Double_t counter_QCD_Pt_1000to1400_cloned_sum_errors_fely3001[19] = {
   1.569922e+13,
   1.989732e+07,
   1.577668e+07,
   1.577668e+07,
   1.577668e+07,
   1.577668e+07,
   1.577668e+07,
   1.577668e+07,
   1.577289e+07,
   1.577283e+07,
   1.577283e+07,
   1.902025e+07,
   1.902025e+07,
   1.902025e+07,
   1419774,
   1419270,
   1632215,
   15344.56,
   15344.56};
   Double_t counter_QCD_Pt_1000to1400_cloned_sum_errors_fehx3001[19] = {
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5,
   0.5};
   Double_t counter_QCD_Pt_1000to1400_cloned_sum_errors_fehy3001[19] = {
   1.569922e+13,
   1.989732e+07,
   1.577668e+07,
   1.577668e+07,
   1.577668e+07,
   1.577668e+07,
   1.577668e+07,
   1.577668e+07,
   1.577289e+07,
   1.577283e+07,
   1.577283e+07,
   1.902025e+07,
   1.902025e+07,
   1.902025e+07,
   1419774,
   1419270,
   1632215,
   15344.56,
   15344.56};
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(19,counter_QCD_Pt_1000to1400_cloned_sum_errors_fx3001,counter_QCD_Pt_1000to1400_cloned_sum_errors_fy3001,counter_QCD_Pt_1000to1400_cloned_sum_errors_felx3001,counter_QCD_Pt_1000to1400_cloned_sum_errors_fehx3001,counter_QCD_Pt_1000to1400_cloned_sum_errors_fely3001,counter_QCD_Pt_1000to1400_cloned_sum_errors_fehy3001);
   grae->SetName("counter_QCD_Pt_1000to1400_cloned_sum_errors");
   grae->SetTitle("Graph");
   grae->SetFillColor(1);
   grae->SetFillStyle(3345);
   grae->SetLineColor(0);
   grae->SetLineStyle(0);
   grae->SetLineWidth(0);
   grae->SetMarkerStyle(0);
   
   TH1F *Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001 = new TH1F("Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001","Graph",100,0,20.9);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->SetMinimum(416641.3);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->SetMaximum(3.593427e+13);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->SetDirectory(0);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->SetStats(0);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->SetLineStyle(0);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->SetMarkerStyle(20);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetXaxis()->SetLabelFont(43);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetXaxis()->SetLabelOffset(0.007);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetXaxis()->SetLabelSize(27);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetXaxis()->SetTitleSize(33);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetXaxis()->SetTitleOffset(0.9);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetXaxis()->SetTitleFont(43);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetYaxis()->SetLabelFont(43);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetYaxis()->SetLabelOffset(0.007);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetYaxis()->SetLabelSize(27);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetYaxis()->SetTitleSize(33);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetYaxis()->SetTitleOffset(1.25);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetYaxis()->SetTitleFont(43);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetZaxis()->SetLabelFont(43);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetZaxis()->SetLabelOffset(0.007);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetZaxis()->SetLabelSize(27);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetZaxis()->SetTitleSize(33);
   Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001->GetZaxis()->SetTitleFont(43);
   grae->SetHistogram(Graph_counter_QCD_Pt_1000to1400_cloned_sum_errors3001);
   
   grae->Draw("e2 ");
   
   TH1F *counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15 = new TH1F("counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15","Weighted counter",19,0,19);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(1,1.168568e+08);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(2,1.48633e+07);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(3,1.48633e+07);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(4,1.48633e+07);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(5,1.48633e+07);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(6,1.48633e+07);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(7,1.48633e+07);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(8,1.48633e+07);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(9,1.021704e+07);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(10,9982263);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(11,9982263);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(12,9982263);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(13,9977129);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(14,9977129);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(15,8017510);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(16,7447132);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(17,7447132);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(18,152538);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinContent(19,152538);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(1,8.491371e+07);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(2,1.097731e+07);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(3,3855.296);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(4,3855.296);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(5,3855.296);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(6,3855.296);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(7,3855.296);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(8,3855.296);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(9,3196.41);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(10,3159.472);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(11,3159.472);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(12,3159.472);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(13,3158.659);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(14,3158.659);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(15,2831.521);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(16,2728.943);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(17,2728.943);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(18,390.5611);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetBinError(19,390.5611);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetEntries(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetDirectory(0);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetLineWidth(2);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetMarkerStyle(20);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->SetMarkerSize(1.2);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(1,"ttree: skimCounterAll");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(2,"ttree: skimCounterPassed");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(3,"Base::AllEvents");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(4,"Base::PUReweighting");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(5,"Base::Prescale");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(6,"Base::Weighted events with top pT");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(7,"Base::Weighted events for exclusive samples");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(8,"All events");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(9,"Passed trigger");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(10,"passed METFilter selection ()");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(11,"Primary vertex selection");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(12,"Met trigger SF");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(13,"passed e selection (Veto)");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(14,"passed mu selection (Veto)");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(15,"passed jet selection ()");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(16,"passed b-jet selection ()");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(17,"b tag SF");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(18,"passed MET selection ()");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetBinLabel(19,"Selected events");
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetRange(1,19);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetLabelFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetLabelSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetTitleSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetXaxis()->SetTitleFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetYaxis()->SetLabelFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetYaxis()->SetLabelSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetYaxis()->SetTitleSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetYaxis()->SetTitleFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetZaxis()->SetLabelFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetZaxis()->SetLabelSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetZaxis()->SetTitleSize(0.035);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->GetZaxis()->SetTitleFont(42);
   counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned15->Draw("EP same");
   
   TLegend *leg = new TLegend(0.68,0.52,0.88,0.92,NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextFont(62);
   leg->SetTextSize(0.035);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(1);
   leg->SetFillColor(0);
   leg->SetFillStyle(4000);
   TLegendEntry *entry=leg->AddEntry("counter_JetHT_Run2016C_PromptReco_v2_275420_276283_cloned","Data","peL");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(2);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(20);
   entry->SetMarkerSize(1.2);
   entry->SetTextFont(62);
   entry=leg->AddEntry("counter_QCD_Pt_1000to1400_cloned_forLegend","QCD","F");

   ci = TColor::GetColor("#ffcc33");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("counter_TT_cloned_forLegend","t#bar{t}","F");

   ci = TColor::GetColor("#993399");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("counter_ZJetsToQQ_HT600toInf_cloned_forLegend","Z+jets","F");

   ci = TColor::GetColor("#ff6666");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("counter_ST_tW_top_5f_inclusiveDecays_cloned_forLegend","Single t","F");

   ci = TColor::GetColor("#669900");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("counter_WJetsToQQ_HT_600ToInf_cloned_forLegend","W+jets","F");

   ci = TColor::GetColor("#cc3300");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("counter_Diboson_cloned_forLegend","Diboson","F");

   ci = TColor::GetColor("#3333ff");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("counter_TTBB_cloned_forLegend","t#bar{t}b#bar{b}","F");

   ci = TColor::GetColor("#ff3399");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("counter_TTZToQQ_cloned_forLegend","Z+t#bar{t}","F");

   ci = TColor::GetColor("#6699ff");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("counter_TTWJetsToQQ_cloned_forLegend","W+t#bar{t}","F");

   ci = TColor::GetColor("#99cc00");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("counter_TTTT_cloned_forLegend","t#bar{t}t#bar{t}","F");

   ci = TColor::GetColor("#ffffcc");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   entry=leg->AddEntry("counter_QCD_Pt_1000to1400_cloned_sum_errors_forLegend","Sim. stat. unc.","F");
   entry->SetFillColor(1);
   entry->SetFillStyle(3345);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(62);
   leg->Draw();
   
   TH1F *hframe_copy16 = new TH1F("hframe_copy16","hframe",19,0,19);
   hframe_copy16->SetMinimum(0.1);
   hframe_copy16->SetMaximum(3.266752e+15);
   hframe_copy16->SetDirectory(0);
   hframe_copy16->SetStats(0);
   hframe_copy16->SetLineStyle(0);
   hframe_copy16->SetMarkerStyle(20);
   hframe_copy16->GetXaxis()->SetLabelFont(43);
   hframe_copy16->GetXaxis()->SetLabelOffset(0.007);
   hframe_copy16->GetXaxis()->SetLabelSize(0);
   hframe_copy16->GetXaxis()->SetTitleSize(0);
   hframe_copy16->GetXaxis()->SetTitleOffset(0.9);
   hframe_copy16->GetXaxis()->SetTitleFont(43);
   hframe_copy16->GetYaxis()->SetTitle("Events / 1");
   hframe_copy16->GetYaxis()->SetLabelFont(43);
   hframe_copy16->GetYaxis()->SetLabelOffset(0.007);
   hframe_copy16->GetYaxis()->SetLabelSize(27);
   hframe_copy16->GetYaxis()->SetTitleSize(33);
   hframe_copy16->GetYaxis()->SetTitleOffset(1.5625);
   hframe_copy16->GetYaxis()->SetTitleFont(43);
   hframe_copy16->GetZaxis()->SetLabelFont(43);
   hframe_copy16->GetZaxis()->SetLabelOffset(0.007);
   hframe_copy16->GetZaxis()->SetLabelSize(27);
   hframe_copy16->GetZaxis()->SetTitleSize(33);
   hframe_copy16->GetZaxis()->SetTitleFont(43);
   hframe_copy16->Draw("sameaxis");
   
   TH1F *hframe_copy17 = new TH1F("hframe_copy17","hframe",19,0,19);
   hframe_copy17->SetMinimum(0.1);
   hframe_copy17->SetMaximum(3.266752e+15);
   hframe_copy17->SetDirectory(0);
   hframe_copy17->SetStats(0);
   hframe_copy17->SetLineStyle(0);
   hframe_copy17->SetMarkerStyle(20);
   hframe_copy17->GetXaxis()->SetLabelFont(43);
   hframe_copy17->GetXaxis()->SetLabelOffset(0.007);
   hframe_copy17->GetXaxis()->SetLabelSize(0);
   hframe_copy17->GetXaxis()->SetTitleSize(0);
   hframe_copy17->GetXaxis()->SetTitleOffset(0.9);
   hframe_copy17->GetXaxis()->SetTitleFont(43);
   hframe_copy17->GetYaxis()->SetTitle("Events / 1");
   hframe_copy17->GetYaxis()->SetLabelFont(43);
   hframe_copy17->GetYaxis()->SetLabelOffset(0.007);
   hframe_copy17->GetYaxis()->SetLabelSize(27);
   hframe_copy17->GetYaxis()->SetTitleSize(33);
   hframe_copy17->GetYaxis()->SetTitleOffset(1.5625);
   hframe_copy17->GetYaxis()->SetTitleFont(43);
   hframe_copy17->GetZaxis()->SetLabelFont(43);
   hframe_copy17->GetZaxis()->SetLabelOffset(0.007);
   hframe_copy17->GetZaxis()->SetLabelSize(27);
   hframe_copy17->GetZaxis()->SetTitleSize(33);
   hframe_copy17->GetZaxis()->SetTitleFont(43);
   hframe_copy17->Draw("sameaxis");
   TLatex *   tex = new TLatex(0.95,0.952,"7.0 fb^{-1} (13 TeV)");
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
      tex = new TLatex(0.2706,0.952,"Preliminary");
tex->SetNDC();
   tex->SetTextFont(53);
   tex->SetTextSize(22.8);
   tex->SetLineWidth(2);
   tex->Draw();
   counters_weighted_counter_1->Modified();
   counters_weighted_counter->cd();
   counters_weighted_counter->Modified();
   counters_weighted_counter->cd();
   counters_weighted_counter->SetSelected(counters_weighted_counter);
}
