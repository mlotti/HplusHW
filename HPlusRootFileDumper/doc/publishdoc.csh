#!/bin/csh

set MYDIR = $PWD

if ( ! -d ${SCRATCH}/doctmp) then
  mkdir ${SCRATCH}/doctmp
endif
cd  ${SCRATCH}/doctmp
git clone http://cmsdoc.cern.ch/~slehti/HipProofAnalysis.git
cd HipProofAnalysis
if ( ! -d doc) then
  mkdir doc
endif

set VERSION = ""
# get version
foreach TAG (`git tag -l`)
  set VERSION = $TAG
end
echo Latest version is $VERSION

if ( ! -d doctmp) then
  mkdir doctmp
endif

#switch git version to latest tag
git checkout $VERSION

set DATE = `date "+/%d.%b.%Y/%T"`
echo Parsing doxygen config file
sed 's?REPLACEME?'$VERSION$DATE'?g' doxygen.config >! doxyconfig.active

echo Generating documentation
doxygen doxyconfig.active

cd doc
tar cvfz ${MYDIR}/doc_${VERSION}.tgz html
cd ${MYDIR}
rm -rf ${SCRATCH}/doctmp

echo "Created documentation file to doc_${VERSION}.tgz"
