//HPlus SelectorImpl
#ifdef __CINT__
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
#pragma link C++ nestedclasses;

#pragma link C++ class SelectorImpl+;
#pragma link C++ class SelectorImplParams+;
// rootcint complains that this is already defined, but without TTree
// complains that it is not
#pragma link C++ class std::vector<float>+;
#pragma link C++ class vector<short> +;
#pragma link C++ class vector<vector<short> >+;

#endif
