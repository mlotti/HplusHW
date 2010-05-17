#ifndef __MyJet__
#define __MyJet__

#include "TLorentzVector.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyTrack.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyVertex.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyCaloTower.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEventVersion.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyHit.h"

#include<vector>
#include<map>
#include<iostream>
#include<string>

/**
 * \brief Jet class for MyEvent dataformat
 *
 * Besides jets this class is also used for all other RECO particles.
 *
 * \b Note: Before this class had 0-mass assumption. This no longer
 *          holds since the 4-vector is taken as it is from CMSSW.
 *
 */
class MyJet: public TLorentzVector {
  public:
    	MyJet();

        /**
         * Constructor with 4-momentum
         *
         * For the case of massless 4-vectors, the parameters are
         * "energy components". For massive 4-vectors, the parameters
         * are the 3-momentum and the total energy, as usual.
         *
         * \param px  momentum (energy) x component
         * \param py  momentum (energy) y component
         * \param pz  momentum (energy) z component
         * \param E   total energy
         */
        MyJet(double px, double py, double pz, double E);

    	virtual ~MyJet();

        double Ex() const;
        double Ey() const;
        double Ez() const;

        double eta() const;
        double phi() const;
        double px() const;
        double py() const;
        double pz() const;
        double pt() const;
        double p() const;
        double energy() const;

        /**
         * \brief Get the 4-momentum
         *
         * \return Copy of the 4-momentum
         */
        TLorentzVector p4() const;

        /**
         * \brief Set 4-momentum
         *
         * \b Note: this only sets the \b current 4-momentum. If anyone
         *          applies energy corrections, this change will be
         *          lost.
         *
         * \param p4  4-momentum to be set
         *
         */
        void setP4(const TLorentzVector& p4);

        /**
         * \brief Add energy correction
         *
         * If the named correction already exists, std::exit() is called
         *
         * \param name     Name of the correction
         * \param factor   Correction factor with respect to the original energy
         */
        void addEnergyCorrection(const std::string& name, double factor);

        /**
         * \brief Set the current energy correction
         *
         * If the correction is not found, std::exit() is called
         *
         * \b Note: if there are multiple pointers to this jet object,
         *          naturally the corrections appreas to them too
         *
         * \see getEnergyCorrectionFactor(const std::string&) const
         *
         * \param name     Name of the correction
         */
        void setEnergyCorrection(const std::string& name);

        /**
         * \brief Get energy correction factor
         *
         * If the name is empty or it has the values raw or none, the
         * correction factor w.r.t. to the original 4-vector is 1.
         *
         * \param name   Name of the energy correction
         *
         * \return Energy correction factor.
         */
        double getEnergyCorrectionFactor(const std::string& name) const;

        /**
         * \brief Check if energy correction exists
         */
        bool hasEnergyCorrection(const std::string& name) const;

        /**
         * \brief Get the name of active energy correction
         */
        const std::string& getActiveEnergyCorrectionName() const;

        /**
         * \brief Get the factor of active energy correction
         */
        double getActiveEnergyCorrectionFactor() const;

        /**
         * \brief Get tracks of the jet
         *
         * \param signalCone     Consider only tracks in this cone around the jet
         *
         * \return Vector of pointers to selected tracks
         */
        std::vector<MyTrack *> getTracks(double signalCone = 0.7);

        /**
         * \brief Get tracks of the jet around the leading track
         *
         * \param signalCone     Consider only tracks in this cone around the leading track
         * \param matchingCone   Leading track matching cone
         *
         * \return Vector of pointers to selected tracks
         */
        std::vector<MyTrack *> getTracksAroundLeadingTrack(double signalCone, double matchingCone = 0.1);

        /**
         * \brief Get leading track
         *
         * Leading track is the track with highest Pt inside the
         * matching cone around the jet.
         *
         * \param matchingCone   Leading track matching cone
         *
         * \return Pointer to the leading track, null if leading track not found
         */
        const MyTrack *leadingTrack(double matchingCone = 0.1) const;

        /**
         * \brief Get secondary vertices
         */
        std::vector<MyVertex *> getSecVertices();

        /**
         * \brief Get track hits
         */
        std::vector<MyHit *> getHits();

        /**
         * \brief Get calorimeter information
         */
        std::vector<MyCaloTower *> getCaloInfo();

        /**
         * \brief Check if tag exists
         */
        bool hasTag(const std::string& name) const;

        /**
         * \brief Get tag value
         *
         * \param name   Name of the tag
         *
         * \return Value of the tag.
         */
        double tag(const std::string& name) const;

        /**
         * \brief Sum of 4-vectors of the tracks inside the signal cone
         *
         * \param signalCone    Consider only tracks in this cone around the leading track
         * \param matchingCone  Leading track matching cone
         *
         * \return Sum of track 4-vectors
         */
        TLorentzVector      combinedTracksMomentum(double signalCone, double matchingCone = 0.1) const;

        /**
         * \brief Sum of ECAL cluster 3-vectors inside the signal cone
         *
         * \param signalCone    Consider only ECAL clusters in this cone around the leading track
         * \param matchingCone  Leading track matching cone
         *
         * \return Sum of cluster 3-vectors
         */
	TLorentzVector	    ecalClusterMomentum(double signalCone, double matchingCone = 0.1) const;

        /**
         * \brief Sum of HCAL cluster 3-vectors inside the signal cone
         *
         * \param signalCone    Consider only HCAL clusters in this cone around the leading track
         * \param matchingCone  Leading track matching cone
         *
         * \return Sum of cluster 3-vectors
         */
        TLorentzVector      hcalClusterMomentum(double signalCone ,double matchingCone = 0.1) const;

        /**
         * \brief Get clusters (valid for electrons and taus)
         *
         * Currently this method is meaningfull only for electrons and
         * taus. The clusters are modeled as TLorentzVectors, where
         * the 3-vector represents the position of the cluster and the
         * energy component represents the energy of the cluster.
         *
         * For electrons, the vector has only one element which is the
         * supercluster.
         *
         * For taus, the vector has all ECAL clusters.
         *
         * \return Vector of pointers to clusters
         */
        std::vector<TLorentzVector *> getClusters();


	void printTracks(std::ostream& out = std::cout) const;
	void printVertices(std::ostream& out = std::cout) const;
	void printCaloInfo(std::ostream& out = std::cout) const;
	void printTagInfo(std::ostream& out = std::cout) const;
	void printEnergyCorrections(std::ostream& out = std::cout) const;
	void printCorrections(std::ostream& out = std::cout) const;
	void print(std::ostream& out = std::cout) const;

        /* Members */

        std::vector<MyTrack>          tracks;      ///< Tracks associated to the jet
        std::vector<MyHit>            hits;        ///< Hits associated to tracks
        std::vector<MyVertex>         secVertices; ///< Secondary vertices associated to the jet
        std::vector<MyCaloTower>      caloInfo;    ///< Calorimeter info associated to the jet
        std::vector<TLorentzVector>   clusters;    ///< SuperClusters for electrons, ECAL clusters for taus
        std::map<std::string, double> tagInfo;     ///< Various jet tags, e.g. b-tag discriminators
        std::map<std::string, double> jecs;        ///< Jet energy corrections
        TLorentzVector                originalP4;  ///< Original jet 4-vector, this shouldn't be modified after setting it
        std::string            currentCorrection;  //!< Name of current correction, not to be stored in the TTree (hence !)

        int type;  ///< type of the jet/particle, not really used currently

  private:
        /**
         * \brief Internal helper method
         *
         * \see getTracks(double)
         * \see getTracksAroundLeadingTrack(double, double)
         */
        std::vector<MyTrack *> getTracksAroundP4(const TLorentzVector& p4, double signalCone);

    	ClassDef(MyJet, MYEVENT_VERSION)
};

/**
 * \brief Switch energy corrections for entire collection of particles
 *
 * If the correction is not found for some particle, the program is
 * aborted.
 * 
 * \param jets   Particle collection
 * \param name   Name of correction
 */
void useCorrection(std::vector<MyJet *>& jets, const std::string& name);

#endif
