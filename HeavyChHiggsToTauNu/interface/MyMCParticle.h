#ifndef __MyMCParticle__
#define __MyMCParticle__

#include "TLorentzVector.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyImpactParameter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventVersion.h"

#include<vector>

/**
 * \brief Monte Carlo particle class for MyEvent dataformat
 */
class MyMCParticle: public TLorentzVector {
    public:
        MyMCParticle();

        /**
         * \brief Constructor with 4-momentum
         *
         * \param px  momentum x component
         * \param py  momentum y component
         * \param pz  momentum z component
         * \param E   total energy
         */
	MyMCParticle(double px, double py, double pz, double E);

        virtual ~MyMCParticle();
/*
        MyGlobalPoint GetMCVertex() const;
        MyGlobalPoint GetImpactParameter() const;
*/

      	double   pt()  const;
      	double   eta() const;
      	double   phi() const;

      	double   px()  const;
      	double   py()  const;
      	double   pz()  const;
	double   p()   const;

        /**
         * \brief Get the 4-momentum of the track
         *
         * \return Copy of the 4-momentum
         */
        TLorentzVector p4() const;

        /**
         * \brief Set the 4-momentum of the track
         *
         * \param p4  4-momentum to be set
         */
	void setP4(const TLorentzVector& p4);

        /**
         * \brief Get the charge of the particle
         */
	int charge() const;

        /**
         * \brief Get the impact parameter of the track
         */
        MyImpactParameter impactParameter() const;


        MyImpactParameter ip;             ///< Impact parameter
        int pCharge;                      ///< Particle charge

        std::vector<int> motherIndices;   ///< Index to the mother particle in the vector

        int         pid;                  ///< Particle ID
	int 	    status;               ///< Particle status

    private:

    ClassDef(MyMCParticle, MYEVENT_VERSION)
};
#endif
