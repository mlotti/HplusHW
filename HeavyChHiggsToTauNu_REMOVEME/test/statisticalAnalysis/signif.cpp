#include <iostream>
#include <math.h>
/*
double signif(double nSignal,double nBackgr){

  double significance;

  if(nBackgr > 0){
////    significance = nSignal/sqrt(nSignal+nBackgr);
//    if(nBackgr > 50){
//      significance = nSignal/sqrt(nBackgr);
//    }else{
      significance = sqrt(2*((nSignal+nBackgr)*log(1+nSignal/nBackgr)-nSignal));
//    }
  }else{
    significance = 0;
  }

  return significance;
}
*/
double signif(double nSignal,double nBackgr, double sysErrorBackgr = 0){

  double significance;

  if(sysErrorBackgr > 1 || sysErrorBackgr < 0) {
    std::cout << "give error between [0,1]! " << std::endl;
    return 0;
  }
  if(nBackgr > 0){

//    if(nBackgr > 50){
//      significance = nSignal/sqrt(nBackgr*(1+sysErrorBackgr));
//    }else{
      significance = sqrt(2*((nSignal+nBackgr)*
                     log(1+nSignal/(nBackgr*(1+sysErrorBackgr)))-nSignal));
//    }
  }else{
    significance = 0;
  }

  return significance;
}

