#!bin/sh

# install boost
if [ ! -e ./NtupleAnalysis/external/boost ]; then
  echo "Getting and installing boost"
  cd ./NtupleAnalysis/external
  #wget http://sourceforge.net/projects/boost/files/boost/1.57.0/boost_1_57_0.tar.gz
  tar xfz boost_1_57_0.tar.gz
  rm boost_1_57_0.tar.gz
  ln -s boost_1_57_0/boost boost
  echo "... boost installed"
  echo "Please recompile your code"
fi
