#include "tmvaglob.C"

// this macro plots the correlation matrix of the various input
// variables used in TMVA (e.g. running TMVAnalysis.C).  Signal and
// Background are plotted separately

   // --------- S t y l e ---------------------------
   static Bool_t UsePaperStyle = 0;

   static Int_t c_Canvas         = TColor::GetColor( "#f0f0f0" );
   static Int_t c_FrameFill      = TColor::GetColor( "#fffffd" );
   static Int_t c_TitleBox       = TColor::GetColor( "#5D6B7D" );
   static Int_t c_TitleBorder    = TColor::GetColor( "#7D8B9D" );
   static Int_t c_TitleText      = TColor::GetColor( "#FFFFFF" );
   static Int_t c_SignalLine     = TColor::GetColor( "#0000ee" );
   static Int_t c_SignalFill     = TColor::GetColor( "#7d99d1" );
   static Int_t c_BackgroundLine = TColor::GetColor( "#ff0000" );
   static Int_t c_BackgroundFill = TColor::GetColor( "#ff0000" );
   static Int_t c_NovelBlue      = TColor::GetColor( "#2244a5" );
   // -----------------------------------------------

   // used to create output file for canvas
   void imgconv( TCanvas* c, const TString & fname )
   {
      // return;
      if (NULL == c) {
         cout << "*** Error in TMVAGlob::imgconv: canvas is NULL" << endl;
      }
      else {
         // create directory if not existing
         TString f = fname;
         TString dir = f.Remove( f.Last( '/' ), f.Length() - f.Last( '/' ) );
         gSystem->mkdir( dir );

         TString pdfName = fname + ".pdf";
         TString pngName = fname + ".png";
         TString cName = fname + ".C";
         c->cd();

         // create eps (other option: c->Print( epsName ))
         if (UsePaperStyle) {
            c->Print(pdfName);
         } 
         else {
            cout << "--- --------------------------------------------------------------------" << endl;
            cout << "--- If you want to save the image as eps, gif or png, please comment out " << endl;
            cout << "--- the corresponding lines (line no. 239-241) in tmvaglob.C" << endl;
            cout << "--- --------------------------------------------------------------------" << endl;
            c->Print(pngName);
            c->Print(pdfName);
	    c->Print(cName);
            // c->Print(gifName);
         }
      }
   }

   TFile* OpenFile( const TString& fin )
   {
      TFile* file = gDirectory->GetFile();
      if (file==0 || fin != file->GetName()) {
         if (file != 0) {
            gROOT->cd();
            file->Close();
         }
         cout << "--- Opening root file " << fin << " in read mode" << endl;
         file = TFile::Open( fin, "READ" );
      }
      else {
         file = gDirectory->GetFile();
      }

      file->cd();
      return file;
   }

   void SetTMVAStyle() {
      
      TStyle *TMVAStyle = gROOT->GetStyle("TMVA");
      if(TMVAStyle!=0) {
         gROOT->SetStyle("TMVA");
         return;
      }
			
      TMVAStyle = new TStyle(*gROOT->GetStyle("Plain")); // our style is based on Plain
      TMVAStyle->SetName("TMVA");
      TMVAStyle->SetTitle("TMVA style based on \"Plain\" with modifications defined in tmvaglob.C");
      gROOT->GetListOfStyles()->Add(TMVAStyle);
      gROOT->SetStyle("TMVA");
			
      TMVAStyle->SetLineStyleString( 5, "[52 12]" );
      TMVAStyle->SetLineStyleString( 6, "[22 12]" );
      TMVAStyle->SetLineStyleString( 7, "[22 10 7 10]" );

      // the pretty color palette of old
      TMVAStyle->SetPalette((UsePaperStyle ? 18 : 1),0);

      // use plain black on white colors
      TMVAStyle->SetFrameBorderMode(0);
      TMVAStyle->SetCanvasBorderMode(0);
      TMVAStyle->SetPadBorderMode(0);
      TMVAStyle->SetPadColor(0);
      TMVAStyle->SetFillStyle(0);

      TMVAStyle->SetLegendBorderSize(0);

      // title properties
      // TMVAStyle->SetTitleW(.4);
      // TMVAStyle->SetTitleH(.10);
      // MVAStyle->SetTitleX(.5);
      // TMVAStyle->SetTitleY(.9);
      TMVAStyle->SetTitleFillColor( c_TitleBox );
      TMVAStyle->SetTitleTextColor( c_TitleText );
      TMVAStyle->SetTitleBorderSize( 1 );
      TMVAStyle->SetLineColor( c_TitleBorder );
      if (!UsePaperStyle) {
         TMVAStyle->SetFrameFillColor( c_FrameFill );
         TMVAStyle->SetCanvasColor( c_Canvas );
      }

      // set the paper & margin sizes
      TMVAStyle->SetPaperSize(20,26); //20, 26
      TMVAStyle->SetPadTopMargin(0.10);
      TMVAStyle->SetPadRightMargin(0.05);
      TMVAStyle->SetPadBottomMargin(0.11);
      TMVAStyle->SetPadLeftMargin(0.12 + 0.2);

      // use bold lines and markers
      TMVAStyle->SetMarkerStyle(21);
      TMVAStyle->SetMarkerSize(0.3);
      TMVAStyle->SetHistLineWidth(2);
      TMVAStyle->SetLineStyleString(2,"[12 12]"); // postscript dashes

      // do not display any of the standard histogram decorations
      TMVAStyle->SetOptTitle(1);
      TMVAStyle->SetTitleH(0.052);

      TMVAStyle->SetOptStat(0);
      TMVAStyle->SetOptFit(0);

      // put tick marks on top and RHS of plots
      TMVAStyle->SetPadTickX(1);
      TMVAStyle->SetPadTickY(1);

   }

   void DestroyCanvases()
   {

      TList* loc = (TList*)gROOT->GetListOfCanvases();
      TListIter itc(loc);
      TObject *o(0);
      while ((o = itc())) delete o;
   }

   void Initialize( Bool_t useTMVAStyle = kTRUE )
   {
     // destroy canvas'
     DestroyCanvases();
     
     // set style
     if (!useTMVAStyle) {
       gROOT->SetStyle("Plain");
       gStyle->SetOptStat(0);
       return;
     }
     
     SetTMVAStyle();
   }

// input: - Input file (result from TMVA),
//        - use of colors or grey scale
//        - use of TMVA plotting TStyle
void correlations( TString fin = "TMVA.root", Bool_t isRegression = kFALSE, 
                   Bool_t greyScale = kFALSE, Bool_t useTMVAStyle = kTRUE )
{

  gROOT->SetBatch(1); //Do not display canvases
   // set style and remove existing canvas'
   Initialize( useTMVAStyle );

   // checks if file with name "fin" is already open, and if not opens one
   TFile* file = OpenFile( fin );  

   // signal and background or regression problem
   Int_t ncls = (isRegression ? 1 : 2 );
   TString hName[2] = { "CorrelationMatrixS", "CorrelationMatrixB" };
   if (isRegression) hName[0]= "CorrelationMatrix";
   const Int_t width = 200; //canvas size
   for (Int_t ic=0; ic<ncls; ic++) {

     TH2* h2 = (TH2D*)file->Get( hName[ic] );
      if(!h2) {
         cout << "Did not find histogram " << hName[ic] << " in " << fin << endl;
         continue;
      }

      TCanvas* c = new TCanvas( hName[ic], 
                                Form("Correlations between MVA input variables (%s)", 
                                     (isRegression ? "" : (ic==0 ? "signal" : "background"))), 
                                ic*(width+5)+200, 0, width, width ); 
      Float_t newMargin1 = 0.13;
      Float_t newMargin2 = 0.15;
      if (UsePaperStyle) newMargin2 = 0.13;

      c->SetGrid();
      c->SetTicks();
      c->SetLeftMargin  ( newMargin2); // + 0.02
      c->SetBottomMargin( newMargin2 );
      c->SetRightMargin ( newMargin1 - 0.02); //- 0.02
      c->SetTopMargin   ( newMargin1 );
      gStyle->SetPalette( 1, 0 );


      gStyle->SetPaintTextFormat( "3g" );

      h2->SetMarkerSize( 1.1 ); //soti Number size
      h2->SetMarkerColor( 0 );
      Float_t labelSize = 0.032; //soti label size (default: 0.040 )
      h2->GetXaxis()->SetLabelSize( labelSize );
      h2->GetYaxis()->SetLabelSize( labelSize );
      h2->GetZaxis()->SetLabelSize( 0.028 ); //0.030
      //h2->LabelsOption( "d" );
      h2->SetLabelOffset( 0.011 );// label offset on x axis

      h2->Draw("colz"); // color pads   
      c->Update();

      // modify properties of paletteAxis
      TPaletteAxis* paletteAxis = (TPaletteAxis*)h2->GetListOfFunctions()->FindObject( "palette" );
      paletteAxis->SetLabelSize( 0.03 );
      paletteAxis->SetX1NDC( paletteAxis->GetX1NDC() + 0.02 );

      h2->Draw("textsame");  // add text

      // add comment    
      TText* t = new TText( 0.53, 0.88, "Linear correlation coefficients in %" );
      t->SetNDC();
      t->SetTextSize( 0.026 ); //soti 0.026
      t->AppendPad();    

      // plot_logo( );
      c->Update();

      TString fname = "plots/";
      fname += hName[ic];
      imgconv( c, fname );
   }
}
