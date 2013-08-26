#!/bin/sh

if [ "x$ASCIIDOC" = "x" ]; then
    ASCIIDOC=asciidoc
fi

PARAM="-a toc" # -a icons

echo "Generating other documentation"
for i in *.txt; do
    $ASCIIDOC $PARAM $i
done

if [ ! -e html ]; then
    mkdir html
fi

mv *.html html