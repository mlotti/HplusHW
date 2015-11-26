#!/bin/sh

if [ "x$HIGGSANALYSIS_BASE" = "x" ]; then
    echo "Environment variable \$HIGGSANALYSIS_BASE not set, please source setup.sh"
    exit 1
fi

echo "Running C++ unit tests"
$HIGGSANALYSIS_BASE/NtupleAnalysis/test/main
RET=$?

echo "Running python unit tests"
for dir in NtupleAnalysis HeavyChHiggsToTauNu; do
    for i in $(find $HIGGSANALYSIS_BASE/$dir/python -name "*.py" | xargs fgrep "import unittest" | cut -d : -f 1); do
        echo $i
        python $i
        FOO=$?
        if [ $RET = 0 -a $FOO != 0 ]; then
            RET=$FOO
        fi
    done
done
# Unit tests under NtupleAnalysis/src
for i in $(find $HIGGSANALYSIS_BASE/NtupleAnalysis/src/*/python -name "*.py" | xargs fgrep "import unittest" | cut -d : -f 1); do
    echo $i
    python $i
    FOO=$?
    if [ $RET = 0 -a $FOO != 0 ]; then
        RET=$FOO
    fi
done

echo
echo
if [ $RET = 0 ]; then
    echo -e "\033[32;1mAll tests succeeded.\033[0m"
else
    echo -e "\033[31;1mThere was at least one failed test, please see the log above.\033[0m"
fi

exit $RET

