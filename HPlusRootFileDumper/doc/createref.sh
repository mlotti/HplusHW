#!/bin/sh

if [ "x$VERSION" = "x" ]; then
    VERSION="Private_development_version"
fi
DATE=$(date "+/%d.%b.%Y/%T")

echo "Creating doxygen config file"
sed "s?REPLACEME?$VERSION$DATE?g" doxygen.config > doxyconfig.active

echo "Generating reference manual"
if [ ! -d html ]; then
    mkdir html
fi
cd ..
doxygen doc/doxyconfig.active

cd doc
rm doxyconfig.active