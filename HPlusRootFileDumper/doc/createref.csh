#!/bin/csh

if ( ! -d html) then
  mkdir html
endif

set VERSION = "Private_development_version"
set DATE = `date "+/%d.%b.%Y/%T"`
echo Parsing doxygen config file
sed 's?REPLACEME?'$VERSION$DATE'?g' doxygen.config >! doxyconfig.active

echo Generating documentation
cd ..
doxygen doc/doxyconfig.active
cd doc
rm doxyconfig.active

echo "Created documentation to doc/html directory"
