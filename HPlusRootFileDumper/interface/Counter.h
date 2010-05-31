// -*- c++ -*-
#ifndef __HPlusAnalysis_Counter_h__
#define __HPlusAnalysis_Counter_h__

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "HiggsAnalysis/HPlusRootFileDumper/interface/CounterItem.h"
#include <vector>
#include <string>
#include <iostream> 

/**
 * \brief Simple event counter class
 *
 * \author Matti Kortelainen, Lauri A. Wendland
 */

namespace HPlusAnalysis {

class Counter {
public:
  /**
   * \brief Constructor
   */
  Counter();

  /**
   * \brief Destructor
   */
  ~Counter();

  /**
   * \brief Creates a new counter
   * Creates a new counter
   * \param name    Name of the counter
   * \return Index of the created counter
   */
  int addCounter(std::string name);
  /**
   * \brief Creates a new sub counter
   * Creates a new second level counter
   * \param name    Name of the counter
   * \return Index of the created counter
   */
  int addSubCounter(std::string name);
  
  /**
   * \brief Increment counter
   *
   * Increments the counter (default = by one)
   * \param index     Index of the counter
   * \param increment Number of increments
   */
  void addCount(const int index, int increment = 1);

  /**
   * \brief Get number of counts
   *
   * \param index  Index of the counter
   * \return Number of counts for the given counter.
   */
  int getCount(const int index) const;
 
  /**
   * \brief Get individual count name
   *
   * \param index   Index of the counter
   * \return The name of the counter corresponding the index
   */
  std::string getCounterName(unsigned int index) const;

  /**
   * \brief Store counter information to histograms
   * 
   * Creates one histogram for the main counters and another one for the
   * sub-counters and then stores the counter values to the histograms
   * \param fileService   Pointer to the TFileService object (not owner)
   */
  void storeCountersToHistogram(edm::Service<TFileService>& fileService) const;

  void dummy() { std::cout << "counters registered=" << fCounters.size() << std::endl; }
private:
  bool findCounter(std::string aName);
    
  std::vector<CounterItem*> fCounters; ///< List of counter names
  std::vector<int> fMainCountersIndices; ///< List of counter indices that are main counters
  std::vector<int> fSubCountersIndices; ///< List of counter indices that are sub-counters (second-level counters)

};

}
#endif
