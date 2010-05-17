#include <math.h>
// 9.12.2004/S.Lehti

static const double PI = 3.1415926535;

double etafun(double px, double py, double pz){

    double p = sqrt(px*px + py*py + pz*pz);
    double cosT = 0;
    if(p > 0) cosT = pz/p;

    double eta = 999;
    if(fabs(cosT) < 1) eta = 0.5*log((1+cosT)/(1-cosT));
    return eta;
}

double phifun(double px, double py){

    double phi = PI/2;
    if(px != 0) phi = atan(py/px);
    if(px < 0)  phi += PI;
    if(px > 0 && py < 0) phi += 2*PI;

    return phi;
}

double deltaPhi(double phi1, double phi2){

    // in ORCA phi = [0,2pi], in TLorentzVector phi = [-pi,pi].
    // With the conversion below deltaPhi works ok despite the
    // 2*pi difference in phi definitions.
    if(phi1 < 0) phi1 += 2*PI;
    if(phi2 < 0) phi2 += 2*PI;

    double dphi = fabs(phi1-phi2);

    if(dphi > PI) dphi = 2*PI - dphi;
    return dphi;
}

double phiDis(double phi1, double phi2){ return deltaPhi(phi1,phi2); }

double deltaR(double eta1, double eta2, double phi1, double phi2){

    double dphi = deltaPhi(phi1,phi2);
    double deta = fabs(eta1-eta2);
    return sqrt(dphi*dphi + deta*deta);
}
