#!/bin/sh

if [ "x$VERSION" = "x" ]; then
    VERSION="Private_development_version"
fi
if [ "x$DOXYGEN" = "x" ]; then
    DOXYGEN=doxygen
fi
DATE=$(date "+/%d.%b.%Y/%T")

echo "Creating doxygen config file"
sed "s?REPLACEME?$VERSION$DATE?g" doxygen_py.config > doxyconfig_py.active
sed "s?REPLACEME?$VERSION$DATE?g" doxygen_cpp.config > doxyconfig_cpp.active

echo "Generating reference manual"
cd ..
$DOXYGEN doc/doxyconfig_py.active
$DOXYGEN doc/doxyconfig_cpp.active

cd doc
rm doxyconfig_py.active
rm doxyconfig_cpp.active
