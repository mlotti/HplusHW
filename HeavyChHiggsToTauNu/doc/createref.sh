#!/bin/sh

if [ "x$VERSION" = "x" ]; then
    VERSION="Private_development_version"
fi
if [ "x$DOXYGEN" = "x" ]; then
    DOXYGEN=doxygen
fi
COMMIT=$(git show | head -n 1 | cut -d ' ' -f 2)

echo "Creating doxygen config file"
sed "s?REPLACEME?$VERSION/$COMMIT?g" doxygen_py.config > doxyconfig_py.active
sed "s?REPLACEME?$VERSION/$COMMIT?g" doxygen_cpp.config > doxyconfig_cpp.active

cd ..
echo "Generating reference manual for C++"
$DOXYGEN doc/doxyconfig_py.active
echo "Generating reference manual for Python"
$DOXYGEN doc/doxyconfig_cpp.active

cd doc
rm doxyconfig_py.active
rm doxyconfig_cpp.active
echo "Generating done"
