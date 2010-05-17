#ifndef __MyTrack__
#define __MyTrack__

#include "TLorentzVector.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyGlobalPoint.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyImpactParameter.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEventVersion.h"

#include<vector>
#include<iostream>

/**
 * \brief Track class for MyEvent dataformat
 */
class MyTrack : public TLorentzVector {
   public:
      	MyTrack();

        /**
         * \brief Constructor with 4-momentum
         *
         * \param px  momentum x component
         * \param py  momentum y component
         * \param pz  momentum z component
         * \param E   total energy
         */
        MyTrack(double px, double py, double pz, double E);

      	virtual ~MyTrack();

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
         * \brief Get the charge of the track
         *
         * \see trackCharge
         */
	double charge() const;

        /**
         * \brief Get the normalized chi2 of the track
         */
        double normalizedChi2() const;

        /**
         * \brief Get the number of valid hits of the track
         */
	unsigned int numberOfValidHits() const;

        /**
         * \brief Get the Particle Flow type of the track
         *
         * The types are X=0, h=1, e=2, mu=3, gamma=4, h0=5
         *
         * \b Todo: this description should be updated by an expert
         */
        int pfType() const;

        /**
         * \brief Get the impact parameter of the track
         */
	MyImpactParameter impactParameter() const;

        /**
         * \brief Get the track (extrapolated) impact point at the ECAL
         */
        MyGlobalPoint ecalHitPoint() const;

	void print(std::ostream& out = std::cout) const;


//	inline vector<MyHit>::const_iterator hits_begin() const { return hits.begin(); }
//	inline vector<MyHit>::const_iterator hits_end() const { return hits.end(); }

        /* Members */

//        vector<MyHit> hits; // Hit information of track // LAW 11.02.08
	MyImpactParameter ip;             ///< Track impact parameter
        MyGlobalPoint trackEcalHitPoint;  ///< ECAL hit point (extrapolated)

        /**
         * \brief Charge of the track
         *
         * The character of this variable is integer. However, the
         * reco::PFTrack::charge() returns double, and hence we are
         * sticking to double too. If this gives real problems, we
         * should think something else.
         */
      	double trackCharge;               ///< Charge of the track
        double normChiSquared;            ///< Normalized chi2
        unsigned int nHits;               ///< Number of valid hits
        unsigned int nPixHits;            ///< Number of valid hits in pixel tracker
        int particleType;                 ///< Particle Flow type of the track

  private:
        ClassDef(MyTrack, MYEVENT_VERSION)
};

std::ostream& operator<<(std::ostream& out, const MyTrack& track);

#endif
