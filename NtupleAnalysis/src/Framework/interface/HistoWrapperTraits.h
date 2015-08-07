// -*- c++ -*-
#ifndef Framework_HistoWrapperTraits_h
#define Framework_HistoWrapperTraits_h

#include <vector>

class TH1;
class TH1C;
class TH1S;
class TH1I;
class TH1F;
class TH1D;

class TH2;
class TH2C;
class TH2S;
class TH2I;
class TH2F;
class TH2D;

class TH3;
class TH3C;
class TH3S;
class TH3I;
class TH3F;
class TH3D;

class WrappedTH1;
class WrappedTH2;
class WrappedTH3;

class WrappedTH1Triplet;
class WrappedTH2Triplet;
class WrappedTH3Triplet;

template <typename T> struct HistoWrapperTraits;

template <> struct HistoWrapperTraits<TH1C> { using type = WrappedTH1; };
template <> struct HistoWrapperTraits<TH1S> { using type = WrappedTH1; };
template <> struct HistoWrapperTraits<TH1I> { using type = WrappedTH1; };
template <> struct HistoWrapperTraits<TH1F> { using type = WrappedTH1; };
template <> struct HistoWrapperTraits<TH1D> { using type = WrappedTH1; };

template <> struct HistoWrapperTraits<TH2C> { using type = WrappedTH2; };
template <> struct HistoWrapperTraits<TH2S> { using type = WrappedTH2; };
template <> struct HistoWrapperTraits<TH2I> { using type = WrappedTH2; };
template <> struct HistoWrapperTraits<TH2F> { using type = WrappedTH2; };
template <> struct HistoWrapperTraits<TH2D> { using type = WrappedTH2; };

template <> struct HistoWrapperTraits<TH3C> { using type = WrappedTH3; };
template <> struct HistoWrapperTraits<TH3S> { using type = WrappedTH3; };
template <> struct HistoWrapperTraits<TH3I> { using type = WrappedTH3; };
template <> struct HistoWrapperTraits<TH3F> { using type = WrappedTH3; };
template <> struct HistoWrapperTraits<TH3D> { using type = WrappedTH3; };

template <typename T> struct HistoWrapperTripletTraits;

template <> struct HistoWrapperTripletTraits<TH1C> { using type = WrappedTH1Triplet; };
template <> struct HistoWrapperTripletTraits<TH1S> { using type = WrappedTH1Triplet; };
template <> struct HistoWrapperTripletTraits<TH1I> { using type = WrappedTH1Triplet; };
template <> struct HistoWrapperTripletTraits<TH1F> { using type = WrappedTH1Triplet; };
template <> struct HistoWrapperTripletTraits<TH1D> { using type = WrappedTH1Triplet; };

template <> struct HistoWrapperTripletTraits<TH2C> { using type = WrappedTH2Triplet; };
template <> struct HistoWrapperTripletTraits<TH2S> { using type = WrappedTH2Triplet; };
template <> struct HistoWrapperTripletTraits<TH2I> { using type = WrappedTH2Triplet; };
template <> struct HistoWrapperTripletTraits<TH2F> { using type = WrappedTH2Triplet; };
template <> struct HistoWrapperTripletTraits<TH2D> { using type = WrappedTH2Triplet; };

template <> struct HistoWrapperTripletTraits<TH3C> { using type = WrappedTH3Triplet; };
template <> struct HistoWrapperTripletTraits<TH3S> { using type = WrappedTH3Triplet; };
template <> struct HistoWrapperTripletTraits<TH3I> { using type = WrappedTH3Triplet; };
template <> struct HistoWrapperTripletTraits<TH3F> { using type = WrappedTH3Triplet; };
template <> struct HistoWrapperTripletTraits<TH3D> { using type = WrappedTH3Triplet; };

template <typename T> struct HistoWrapperTHTraits;
template <> struct HistoWrapperTHTraits<TH1C> { using type = TH1; };
template <> struct HistoWrapperTHTraits<TH1S> { using type = TH1; };
template <> struct HistoWrapperTHTraits<TH1I> { using type = TH1; };
template <> struct HistoWrapperTHTraits<TH1D> { using type = TH1; };
template <> struct HistoWrapperTHTraits<TH1F> { using type = TH1; };

template <> struct HistoWrapperTHTraits<TH2C> { using type = TH2; };
template <> struct HistoWrapperTHTraits<TH2S> { using type = TH2; };
template <> struct HistoWrapperTHTraits<TH2I> { using type = TH2; };
template <> struct HistoWrapperTHTraits<TH2D> { using type = TH2; };
template <> struct HistoWrapperTHTraits<TH2F> { using type = TH2; };

template <> struct HistoWrapperTHTraits<TH3C> { using type = TH3; };
template <> struct HistoWrapperTHTraits<TH3S> { using type = TH3; };
template <> struct HistoWrapperTHTraits<TH3I> { using type = TH3; };
template <> struct HistoWrapperTHTraits<TH3D> { using type = TH3; };
template <> struct HistoWrapperTHTraits<TH3F> { using type = TH3; };

#endif
