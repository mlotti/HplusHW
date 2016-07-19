#include "Auxiliary/interface/Tools.h"
#include <string>
#include <sstream>
#include <iostream>

//****************************************************************************
void Tools::ProgressBar(long entry,
			long total, 
			int resolution,
			int barWidth)
//****************************************************************************  
{  

  // Correct for loop index
  entry = entry + 1;

  // Sanity check (otherwise crashes)
  if (total < resolution) resolution = total;

  // Only update "resolution" times.
  if ( entry % (total/resolution) != 0 ) return;

  // Calculuate the ratio of complete-to-incomplete.
  double ratio      = (double) entry / (double) total;
  double percentage = 100.0*ratio;
  int completed     = ratio*barWidth;

  // Show the percentage completed
  std::cout << "Progress: " << std::setprecision(3) << percentage << " % ";
  
  // Show the progress bar
  for (int j=completed; j < barWidth; j++) std::cout << " ";
  
  // Move to the first column and flush
  std::cout << "\r";
  fflush(stdout);
  
  return;
}


//****************************************************************************
long long Tools::nCr(int n,
		     int r)
//****************************************************************************
{

  if(r > n / 2) r = n - r; // because C(n, r) == C(n, n - r)
  long long ans = 1;
  int i;

  for(i = 1; i <= r; i++) {
    ans *= n - r + i;
    ans /= i;
  }

  return ans;  
}
 

//****************************************************************************
template<class TYPE> double Tools::Sgn(TYPE myNumber)
//****************************************************************************
{

  if (myNumber >= 0) return +1.0;
  else return -1.0;
  
}


//****************************************************************************  
double Tools::DeltaPhi(const double phi1, 
		       const double phi2)
//****************************************************************************  
{
  // See: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_4_4_2/doc/html/d1/d92/DataFormats_2Math_2interface_2deltaPhi_8h_source.html
  double result = phi1 - phi2;
  while (result > PI) result -= 2*PI;
  while (result <= -PI) result += 2*PI; 

  return result;
}


//****************************************************************************  
double Tools::DeltaEta(const double eta1, 
		       const double eta2)
//****************************************************************************  
{
  // See: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_4_4_2/doc/html/d1/d92/DataFormats_2Math_2interface_2deltaPhi_8h_source.html
  double deltaEta = fabs ( eta1 - eta2 );
  return deltaEta;
}


//****************************************************************************  
double Tools::DeltaR(const double eta1, 
		     const double phi1, 
		     const double eta2, 
		     const double phi2)
//****************************************************************************  
{
  // See: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_5_3_9/doc/html/d5/d6b/DataFormats_2Math_2interface_2deltaR_8h_source.html
  double deltaEta = DeltaEta(eta1, eta2);
  double deltaPhi = DeltaPhi(phi1, phi2);
  double deltaR   = sqrt( pow(deltaPhi, 2) + pow(deltaEta, 2) );
  return deltaR;
}


//****************************************************************************  
TLorentzVector Tools::GetTLorentzVector( double pt, 
					 double eta, 
					 double phi, 
					 double e)
//****************************************************************************  
{

  TLorentzVector v4;      // initialized by (0., 0., 0., 0.) 
  v4.SetPtEtaPhiE(pt,eta,phi,e);

  return v4;
}


//****************************************************************************  
TVector3 Tools::GetTVector3(double px, 
			    double py, 
			    double pz)
//****************************************************************************  
{

  TVector3 v3(px , py , pz);

  return v3;
}


//****************************************************************************  
TVector2 Tools::GetTVector2(double eta, 
			    double phi)
//****************************************************************************  
{

  TVector2 v2(eta , phi);

  return v2;
}


//****************************************************************************  
template<class TYPE> void Tools::EnsureVectorIsSorted(const std::vector<TYPE> myVector, 
						      Bool_t bDescendingOrder)
//****************************************************************************  
{
  if (myVector.size() < 2) return;
  
  // Get value of first element
  double firstVal = myVector.front();  // last elemet is: myVector.back()
  
  // For-loop: Vector Elements
  for( Size_t i = 0; i < myVector.size(); i++){

    if(bDescendingOrder){ 
      if (myVector[i] > firstVal){
	std::cout << "E R R O R ! Tools::EnsureVectorIsSorted(...) - [0] = " << myVector[0] << ", ["<< i << "] = " << myVector[i]  << std::endl;
	PrintVector(myVector);
	exit(0);
      }
    }
    else{ 
      if (myVector[i] < firstVal){
	std::cout << "E R R O R ! Tools::EnsureVectorIsSorted(...) - [0] = " << myVector[0] << ", ["<< i << "] = " << myVector[i]  << std::endl;
	PrintVector(myVector);
	exit(0);
      }
    }

  } // For-loop: Vector Elements

  return;

}

//****************************************************************************  
template<class TYPE> Bool_t Tools::VectorIsSorted(const std::vector<TYPE> myVector, 
						  Bool_t bDescendingOrder)
//****************************************************************************  
{
  if (myVector.size() < 2) return true;
  
  // Get value of first element
  double firstVal = myVector.front();  // last elemet is: myVector.back()
  
  // For-loop: Vector Elements
  for( Size_t i = 0; i < myVector.size(); i++){
    
    if(bDescendingOrder){ if (myVector[i] > firstVal) return false; }
    else{ if (myVector[i] < firstVal) return false; }
    
  }// For-loop: Vector Elements
  
  return true;

}

//****************************************************************************  
template<class TYPE> void Tools::PrintVector(const std::vector<TYPE> myVector, 
					     std::string title)
//****************************************************************************  
{
  
  if (myVector.size() < 1) return;

  std::cout << title << std::endl;
  Table table("Index | Value ", "Text", "c c");
  for(int index = 0; index < (int) myVector.size(); index++)
    {       
      table.AddRowColumn(index, std::to_string( index) );
      table.AddRowColumn(index, std::to_string(myVector[index]) );
    }

  table.Print();
  return;
}


//****************************************************************************  
double Tools::Divide(int numerator, 
		     int denominator)
//****************************************************************************  
{

  if (denominator <= 0){
    std::cout << "W A R N I N G ! Tools::Divide(...) - "
              << "denominator has illegal value \"" << denominator;
    std::cout << "Returning 0.";
    return 0.0;
  }
  else return double(numerator)/double(denominator);
}


//****************************************************************************  
void Tools::Efficiency(int nPass, 
		       int nTotal, 
		       const std::string errType, 
		       double &eff, 
		       double &err )
//****************************************************************************  
{
  
  if (nTotal == 0)
    {
      eff = 0.0;
      err = 0.0;
      return;
    }
  
  
  eff = Divide(nPass, nTotal);
  if (errType.compare("binomial") == 0){
    err = (1.0/nTotal) * sqrt(nPass * (1.0 - nPass/nTotal) );
  }
  else{
    std::cout << "W A R N I N G ! Tools::Efficiency(...) - "
	      << "Invalid error type \"" << errType << "\" selected."
	      << "Only the \"binomial\" error type is supported at the moment.";
    std::cout << "Exiting \n";
    exit(1);
  }
  return;
}


//****************************************************************************  
void Tools::StopwatchStart(void)
//****************************************************************************  
{

  stopwatch_start = clock();
  return;

}  


//****************************************************************************  
void Tools::StopwatchStop(const int myPrecision, 
			  const std::string myUnits)
//****************************************************************************  
{
  
  double units = 0.0;
  if (myUnits.compare("seconds") == 0)
    {
      units = 1.0;
    }
  else if (myUnits.compare("minutes") == 0)
    {
      units = 60.0;
    }
  else if (myUnits.compare("hours") == 0)
    {
      units = 3600.0;
    }
  else
    {
      std::cout << "E R R O R ! Tools::StopwatchEnd(...) - Invalid unit of time \"" << myUnits << "\" provided. ";
      std::cout << "Please provide one of the following:\n\"seconds\", \"minutes\", \"hours\". EXIT." << std::endl;
      exit(1);
    }

  stopwatch_stop = clock();
  double elapsed_time_secs  = double(stopwatch_stop - stopwatch_start) / CLOCKS_PER_SEC;
  double elapsed_time_units = elapsed_time_secs/double(units);
  
  std::cout << "Elapsed Time: " << std::setprecision(myPrecision) << elapsed_time_units << " (" << myUnits << ")" << std::endl;
  return;

}  


//****************************************************************************  
char* Tools::AppendCharToCharArray(char* array,
				   char a)
//****************************************************************************  
{
  size_t len = strlen(array);
  char* ret = new char[len+2];

  strcpy(ret, array);    
  ret[len] = a;
  ret[len+1] = '\0';

  return ret;
}


//****************************************************************************
void Tools::ReplaceString(std::string &myString,
			  std::string oldSubstring,
			  std::string newSubstring)
//****************************************************************************
{
  size_t index = 0;
  while (true) {
    
    // Locate the substring to replace
    index = myString.find(oldSubstring, index);
    if (index == std::string::npos) break;

    // Make the replacement
    myString.replace(index, oldSubstring.length(), newSubstring);

    // Advance index forward so the next iteration doesn't pick it up as well
    index += oldSubstring.length();
  }

  return;
}
