# Make directories
if ( ! -e localpython ) then
  mkdir localpython
endif
if ( ! -e localpython/HiggsAnalysis ) then
  mkdir localpython/HiggsAnalysis
  echo "#" >! localpython/HiggsAnalysis/__init__.py 
  ln -s `pwd`/../../python localpython/HiggsAnalysis/HeavyChHiggsToTauNu
endif
# Add inits to where necessary
if ( ! -e `pwd`/../../python/__init__.py ) then
   echo "#" >! `pwd`/../../python/__init__.py
endif
if ( ! -e `pwd`/../../python/datacardtools/__init__.py ) then
   echo "#" >! `pwd`/../../python/datacardtools/__init__.py
endif
if ( ! -e `pwd`/../../python/tools/__init__.py ) then
   echo "#" >! `pwd`/../../python/tools/__init__.py
endif
if ( ! -e `pwd`/../../python/tauEmbedding/__init__.py ) then
   echo "#" >! `pwd`/../../python/tauEmbedding/__init__.py
endif

setenv PYTHONPATH ${PYTHONPATH}:`pwd`/localpython

echo "Local python environment has been set up"
echo "You may now run datacard generator on your local machine"
