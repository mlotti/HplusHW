// -*- c++ -*-
#ifndef DataFormat_ParticleIterator_h
#define DataFormat_ParticleIterator_h

template <typename Coll>
class ParticleIterator {
public:
  using value_type = typename Coll::value_type;

  ParticleIterator(const Coll *coll, size_t index):
    fColl(coll),
    fIndex(index)
  {}

  value_type operator*() const {
    return (*fColl)[fIndex];
  }

  ParticleIterator<Coll>& operator++() {
    ++fIndex;
    return *this;
  }

  bool operator==(const ParticleIterator<Coll>& other) const {
    return fIndex == other.fIndex;
  }

  bool operator!=(const ParticleIterator<Coll>& other) const {
    return !operator==(other);
  }

private:
  const Coll *fColl;
  size_t fIndex;
};

template <typename Coll>
class ParticleIteratorAdaptor {
public:
  using const_iterator = ParticleIterator<Coll>;

  const_iterator begin() const {
    return const_iterator(static_cast<const Coll *>(this), 0);
  }

  const_iterator cbegin() const {
    return const_iterator(static_cast<const Coll *>(this), 0);
  }

  const_iterator end() const {
    return const_iterator(static_cast<const Coll *>(this),
                          static_cast<const Coll *>(this)->size());
  }

  const_iterator cend() const {
    return const_iterator(static_cast<const Coll *>(this),
                          static_cast<const Coll *>(this)->size());
  }
};

#endif
