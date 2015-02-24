// -*- c++ -*-
#ifndef DataFormat_ParticleIterator_h
#define DataFormat_ParticleIterator_h

template <typename Coll>
class ParticleIterator {
public:
  using value_type = typename Coll::value_type;

  ParticleIterator(Coll *coll, size_t index):
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

template <typename Coll>
class ParticleIteratorAdaptor {
public:
  using iterator = ParticleIterator<Coll>;

  iterator begin() {
    return iterator(static_cast<Coll *>(this), 0);
  }

  iterator end() {
    return iterator(static_cast<Coll *>(this), static_cast<Coll *>(this)->size());
  }
};

#endif
