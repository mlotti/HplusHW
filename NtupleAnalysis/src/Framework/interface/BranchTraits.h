// -*- c++ -*-
#ifndef Framework_BranchTraits_h
#define Framework_BranchTraits_h

template <typename T>
struct BranchTraits {
  typedef T *DataType;
  typedef const T& ReturnType;
  static ReturnType get(const T* data) { return *data; }
};
template <>
struct BranchTraits<bool> {
  typedef bool DataType;
  typedef bool ReturnType;
  static ReturnType get(bool data) { return data; }
};
template <>
struct BranchTraits<int> {
  typedef int DataType;
  typedef int ReturnType;
  static ReturnType get(int data) { return data; }
};
template <>
struct BranchTraits<unsigned int> {
  typedef unsigned int DataType;
  typedef unsigned int ReturnType;
  static ReturnType get(unsigned int data) { return data; }
};
template <>
struct BranchTraits<unsigned long long> {
  typedef unsigned long long DataType;
  typedef unsigned long long ReturnType;
  static ReturnType get(unsigned long long data) { return data; }
};
template <>
struct BranchTraits<float> {
  typedef float DataType;
  typedef float ReturnType;
  static ReturnType get(float data) { return data; }
};
template <>
struct BranchTraits<double> {
  typedef double DataType;
  typedef double ReturnType;
  static ReturnType get(double data) { return data; }
};

#endif

