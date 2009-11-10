#ifndef __MyEvent__
#define __MyEvent__

#include "TMap.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMCParticle.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMET.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MySimTrack.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventVersion.h"

#include<vector>
#include<map>
#include<string>
#include<iostream>

/**
 * \brief Event class for MyEvent dataformat
 *
 * All RECO particle collections are stored as vector<MyJet> in the
 * collections map.
 *
 * Collections of objects are returned as vector of pointers (e.g.
 * vector<MyJet *>). This minimizes the amount of object copying,
 * altough it has the downsides of bare pointers and copying of the
 * vectors themselves (although the latter appears to be relatively
 * cheap).
 *
 * The MC methods return either null or empty collections if there's
 * no MC info (this could also be enforced at analysis time by setting
 * hasMCdata member to false). It might be a good practice to check
 * with hasMCinfo() method if the MC info is accessible or not before
 * doing any analysis with MC. 
 *
 * The error conditions are handled with a print to stdout followed by
 * exit() call. This way we achieve early and noisy notification about
 * failures. If/when this becomes too restrictive, we should probably
 * go with exceptions.
 *
 * It should be noted that every time any \b data field of any MyEvent
 * class is changed, the MYEVENT_VERSION should be incremented. This
 * also implies that the previous MyEvent data may or may not be
 * readable. At least as long as new fields are added to the bottom of
 * the classes, ROOT should be able to read the old data (the new
 * fields are initialized with their default values).
 *
 * The code of the methods is \b not stored and hence it is safe to
 * add/modify the the methods of the classes without the need of
 * changing the actual dataformat.
 */
class MyEvent: public TObject {
    public:
        MyEvent();
        virtual ~MyEvent();

        /**
         * \brief Copy constructor
         *
         * The explicit copy constructor is apparently needed because
         * of the TMap member, which copy constructor is private. The
         * problem seems to come from reflex dictionary generation (in
         * CMSSW), where CINT (or whatever) generates the copy
         * constructor for this class.
         *
         * \see http://root.cern.ch/root/roottalk/roottalk01/0159.html
         */
        MyEvent(const MyEvent& event);

        /**
         * \brief Check if particle collection exists
         *
         * \param name  Name of the collection
         *
         * \return True, if collection exists, otherwise false
         */
        bool hasCollection(const std::string& name) const;

        /**
         * \brief Get particle collection
         *
         * \param name  Name of the collection
         *
         * \return Collection as vector of pointers.
         */
        std::vector<MyJet *> getCollection(const std::string& name);

        /**
         * \brief Get particle collection with correction
         *
         * \param name  Name of the collection
         * \param corr  Name of the (energy) correction
         *
         * \return Collection as vector of pointers.
         */
        std::vector<MyJet *> getCollectionWithCorrection(const std::string& name, const std::string& corr);

        /**
         * \brief Add particle collection
         *
         * If the named collection already exists, exit() is called
         *
         * \param name  Name of the collection
         * \param coll  Collection to be added (the contents are copied)
         *
         * \return Reference to the inserted vector
         */
        std::vector<MyJet>& addCollection(const std::string& name, const std::vector<MyJet>& coll);

        /**
         * \brief Add empty particle collection
         *
         * If the named collection already exists, exit() is called
         *
         * \param name  Name of the collection
         *
         * \return Reference to the inserted vector
         */
        std::vector<MyJet>& addCollection(const std::string& name);

        /**
         * \brief Check if MET exists
         *
         * \param name  Name of the MET object
         *
         * \return True, if MET object exists, otherwise false
         */
        bool hasMET(const std::string& name) const;

        /**
         * \brief Get MET object
         *
         * \param name  Name of the MET object
         * 
         * \return Pointer to the MET object.
         */
        MyMET *getMET(const std::string& name);

        /**
         * \brief Add MET object
         *
         * If the named MET object already exists, the new MET is not
         * added and the return value is false.
         *
         * \param name  Name of the MET object
         * \param met   MET to be added (the contents are copied)
         */
        void addMET(const std::string& name, const MyMET& met);

        /**
         * \brief Check if trigger exists
         *
         * \param name  Name of the trigger
         *
         * \return True, if trigger exists, otherwise false
         */
        bool hasTrigger(const std::string& name) const;

        /**
         * \brief Get trigger value
         *
         * \param name  Name of the trigger
         *
         * \return True, if event passed the trigger, false if not.
         */
        bool trigger(const std::string& name) const;

        /**
         * \brief Add trigger value
         *
         * If the named trigger already exists, the new trigger is not
         * added and the return value is false.
         *
         * \param name    Name of the trigger
         * \param passed  True if event passed the trigger, false if not
         */
        void addTrigger(const std::string& name, bool passed);

        /**
         * \brief Get primary vertex
         *
         * \return Pointer to primary vertex
         */
        MyGlobalPoint *getPrimaryVertex();

        /**
         * \brief Check if MC info is accessible
         *
         * \return True, if MC info is available, otherwise false
         */
        bool hasMCinfo() const;

        /**
         * \brief Get MC primary vertex
         *
         * \return Pointer to MC primary vertex. 
         */
        MyGlobalPoint *getMCPrimaryVertex();

        /**
         * \brief Get MC particle list
         *
         * \return Collection of MC particles as vector of pointers.
         */
        std::vector<MyMCParticle *> getMCParticles();


        /**
         * \brief Get Monte-Carlo MET object
         *
         * \param name  Name of the Monte-Carlo MET object
         *
         * \return Pointer to the Monte-Carlo MET object.
         */
        MyMET *getMCMET();


        /**
         * \brief Get simulated tracks
         *
         * \return Collection of simulated tracks as vector of
         *         pointers.
         */
        std::vector<MySimTrack *> getSimTracks();

        /**
         * \brief Check if extra object exists
         *
         * \param name  Name of the extra object
         *
         * \return True, if the extra object exists, otherwise false
         */
        bool hasExtraObject(const std::string& name) const;

        /**
         * \brief Get extra object
         *
         * \param name  Name of the extra object
         *
         * \return TObject pointer to the extra object; you must cast
         *         (preferrably with dynamic_cast) the object to the
         *         correct type by yourself. If the named object
         *         doesn't exist, null pointer is returned.
         */
        TObject *getExtraObject(const std::string& name);

        /**
         * \brief Add extra object
         *
         * If the named extra object already exists, the new trigger
         * is not added and the return value is false.
         *
         * Note that the extra object must inherit from TObject. This
         * is in order to have relatively general solution without
         * heavy framework.
         *
         * MyEvent claims the ownership of the extra object. In case
         * of failures, the object is deleted by MyEvent (here one has
         * to be careful in order to avoid memory leaks).
         *
         * \param name  Name of the extra object
         * \param obj   Pointer to extra object (ownership is transferred to MyEvent)
         */
        void addExtraObject(const std::string& name, TObject *obj);
      
        /**
         * \brief Get event number
         */
        unsigned int event() const;

        /**
         * \brief Get run number
         */
        unsigned int run() const;

        /**
         * \brief Get lumiSection id
         */
        unsigned int lumiSection() const;

        /**
         * \brief Print summary
         */
        void printSummary(std::ostream& out = std::cout) const;

        /**
         * \brief Print available energy corrections
         */
        void printCorrections(std::ostream& out = std::cout) const;

        /**
         * \brief Print reco data
         */
        void printReco(std::ostream& out = std::cout) const;

        /**
         * \brief Print whole event
         */
        void printAll(std::ostream& out = std::cout) const;


        /*** Members ***/
        typedef std::vector<MyJet> JetCollection;
        typedef std::map<std::string, JetCollection> CollectionMap;
        typedef std::map<std::string, MyMET> METMap;
        typedef std::map<std::string, bool> TriggerMap;

        // RECO data
        CollectionMap collections;
        METMap mets;
        TriggerMap triggerResults;

        MyGlobalPoint primaryVertex;

        // MC and SIM data
        std::vector<MyMCParticle> mcParticles;
        std::vector<MySimTrack>   simTracks;
	MyMET            	  mcMET;
        MyGlobalPoint mcPrimaryVertex;
        // std::map<std::string, MyGlobalPoint> vertices ?

        // for the case of testing something without changing data format
        TMap extraObjects;

        // event id
        unsigned int eventNumber;
        unsigned int runNumber;
        unsigned int lumiNumber;

        bool hasMCdata; /// Does the event contain MC info?


    private:
    	ClassDef(MyEvent, MYEVENT_VERSION) // The macro
};

#endif
