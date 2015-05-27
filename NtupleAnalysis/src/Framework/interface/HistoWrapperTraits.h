// -*- c++ -*-
#ifndef Framework_HistoWrapperTraits_h
#define Framework_HistoWrapperTraits_h

#include <vector>

class TH1C;
class TH1S;
class TH1I;
class TH1F;
class TH1D;

class TH2C;
class TH2S;
class TH2I;
class TH2F;
class TH2D;

class TH3C;
class TH3S;
class TH3I;
class TH3F;
class TH3D;

class WrappedTH1;
class WrappedTH2;
class WrappedTH3;

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

#endif
