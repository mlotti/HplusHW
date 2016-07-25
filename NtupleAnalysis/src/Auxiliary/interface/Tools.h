// -*- c++ -*-
#ifndef Auxiliary_Tools_h
#define Auxiliary_Tools_h

// System
#include <cmath>
#include <iomanip>
#include <TLorentzVector.h>
#include <ctime>
#include <sstream>
#include <string>

// User
#include "Auxiliary/interface/Constants.h"
#include "Auxiliary/interface/Table.h"

using namespace constants;

class Tools{

 public:
  Tools() { };
  virtual ~Tools() { };

  void ProgressBar(long entry,
		   long total,
		   int resolution, 
		   int barWidth=0);

  template<typename T> inline std::string ToString(const T a_value, const int n=3)
    {
      std::ostringstream out;
      out << std::setprecision(n) << a_value;
      
      return out.str();
    }

  template<class TYPE> inline std::string ConvertIntVectorToString(const std::vector<TYPE> myVector)
    {
      
      if (myVector.size() < 1) return "";
      
      std::string text = "";
      for(int index = 0; index < (int) myVector.size(); index++)
	{
	  
	  TYPE value = myVector[index];
	  if (value == 999999) value = 0;
	  if(index == (int) myVector.size()-1) text += std::to_string( value );
	  else text += std::to_string( value ) + ","; 
	}
      return text;
    }

    
  template<class TYPE> double Sgn(TYPE myNumber);

  long long nCr(int n, int r);


  double DeltaEta(const double eta1, 
		    const double eta2);

  double DeltaPhi(const double phi1, 
		    const double phi2);

  double DeltaR(const double eta1, 
		const double phi1, 
		const double eta2, 
		const double phi2);
  
  TLorentzVector GetTLorentzVector(double pt, 
				   double eta, 
				   double phi, 
				   double e);

  TVector3 GetTVector3(double px, 
		       double py, 
		       double pz);

  TVector2 GetTVector2(double eta, 
		       double phi);
  
  template<class TYPE> void EnsureVectorIsSorted(const std::vector<TYPE> myVector, 
						 bool bDescendingOrder);

  template<class TYPE> bool VectorIsSorted(const std::vector<TYPE> myVector, 
					     bool bDescendingOrder);
  
  template<class TYPE> void PrintVector(const std::vector<TYPE> myVector, 
					std::string title="");  

  double Divide(int numerator, 
		int denominator);

  void Efficiency(int nPass, 
		  int nTotal, 
		  const std::string errType, 
		  double &eff, 
		  double &err);

  void StopwatchStart(void);

  void StopwatchStop(const int myPrecision = 5, 
		     const std::string myUnits = "seconds");

  char* AppendCharToCharArray(char* array,
			      char a);

  void ReplaceString(std::string &myText,
		     std::string oldSubstring,
		     std::string newSubstring);
  
 private:
  clock_t stopwatch_start;
  clock_t stopwatch_stop;
};

#endif
