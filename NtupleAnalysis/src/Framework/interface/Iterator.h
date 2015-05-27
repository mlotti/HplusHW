// -*- c++ -*-
#ifndef Framework_Iterator_h
#define Framework_Iterator_h

template <typename Coll>
class Iterator {
public:
  using value_type = typename Coll::value_type;

  Iterator(Coll *coll, size_t index):
    fColl(coll),
    fIndex(index)
  {}

  value_type operator*() {
    return (*fColl)[fIndex];
  }

  value_type operator++() {
    ++fIndex;
    return (*fColl)[fIndex];
  }

  bool operator==(const ParticleIterator<Coll>& other) {
    return fIndex == other.fIndex;
  }

  bool operator!=(const ParticleIterator<Coll>& other) {
    return !operator==(other);
  }

private:
  Coll *fColl;
  size_t fIndex;
};

#endif
