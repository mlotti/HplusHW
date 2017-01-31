// -*- c++ -*-
#ifndef Framework_EventCounter_h
#define Framework_EventCounter_h

#include <string>
#include <vector>

class TH1;
class TDirectory;

class EventWeight;

// Represents a single count, possible to construct only via
// EventCounter
class EventCounter;
class Count {
public:
  ~Count();

  void increment();
  long int value();

  friend class EventCounter;

private:
  Count() = delete;
  Count(EventCounter *ec, size_t counterIndex, size_t countIndex);

  EventCounter *fEventCounter;
  size_t fCounterIndex;
  size_t fCountIndex;
};


/// Event counter
class EventCounter {
private:
  class Counter {
  public:
    explicit Counter(const std::string& n);

    // not copyable
    Counter(const Counter&) = delete;
    Counter& operator=(const Counter&) = delete;
    // but movable
    Counter(Counter&&) = default;
    Counter& operator=(Counter&&) = default;

    bool contains(const std::string& l) const;
    size_t getLabelIndex(const std::string& l) const;

    size_t insert(const std::string& label, int initialValue=0);

    void incrementCount(size_t countIndex, double weight);
    long int value(size_t countIndex);

    void book(TDirectory *dir);
    void bookWeighted(TDirectory *dir);
    void serialize();
    
    const std::string& getName() const { return name; }

  private:
    std::string name;
    std::vector<std::string> labels;
    std::vector<long int> values;
    std::vector<double> weights;
    std::vector<double> weightsSquared;

    TH1 *counter;
    TH1 *weightedCounter;    
  };

public:
  explicit EventCounter(const EventWeight& weight);
  ~EventCounter();

  // non-copyable
  EventCounter(const EventCounter&) = delete;
  EventCounter& operator=(const EventCounter&) = delete;

  Count addCounter(const std::string& name, double initialValue=0.0);
  Count addSubCounter(const std::string& subcounterName, const std::string& countName, double initialValue=0.0);

  void setOutput(TDirectory *dir);
  void serialize();
  
  void enable(bool enabled) { fIsEnabled = enabled; }
  bool isEnabled() const { return fIsEnabled; }
  
  long int getValueByName(const std::string& name);
  bool contains(const std::string& name);

private:
  friend class Count;
  void incrementCount(size_t counterIndex, size_t countIndex);
  int value(size_t counterIndex, size_t countIndex);

  size_t findOrInsertCounter(const std::string& name);

  const EventWeight& fWeight;
  bool fIsEnabled;
  std::vector<Counter> fCounters; // main counter has index 0
  bool fOutputHasBeenSet;
};

inline
void Count::increment() {
  if (fEventCounter->isEnabled())
    fEventCounter->incrementCount(fCounterIndex, fCountIndex);
}

inline
long int Count::value() {
  return fEventCounter->value(fCounterIndex, fCountIndex);
}
#endif
