#ifndef __MyConvertCollection__
#define __MyConvertCollection__

#include<vector>

/**
 * \brief Template function for converting vector<T> to vector<T *>
 */
template <class T>
std::vector<T *> convertCollection(std::vector<T>& coll) {
  std::vector<T *> ret;
  ret.reserve(coll.size());
  for(typename std::vector<T>::iterator iter = coll.begin(); iter != coll.end(); ++iter) {
    ret.push_back(&(*iter));
  }
  return ret;
}

#endif
