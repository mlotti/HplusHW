#!/usr/bin/env python

import os
import sys
import time
import glob
import shutil
from optparse import OptionParser

def main(opts):
    if os.path.exists(opts.output):
        backup = opts.output+".backup"
        if os.path.exists(backup):
            print "Removing old backup %s" % backup
            shutil.rmtree(backup)
        print "Moving %s to %s" % (opts.output)
        shutil.move(opts.output, backup)

    os.mkdir(opts.output)
    outputDirs = []
    for i in xrange(0, len(opts.dir)):
        d = os.path.join(opts.output, str(i))
        os.mkdir(d)
        outputDirs.append(d)
    if opts.subdir is None:
        plotDirs = opts.dir
    else:
        plotDirs = [os.path.join(d, opts.subdir) for d in opts.dir]

    title = "Validation report"
    if opts.title != "":
        title += ": "+opts.title

    output = [
        "<html>",
        " <head>",
        "  <title>Validation results</title>",
        " </head>",
        " <body>",
        " <h1>%s</h1>" % title,
        ]
    if opts.message != "":
        output.append(" <p>%s</p>" % opts.message)
    output.append(' <table border="1">')

    if len(opts.name) > 0:
        output.append(" <tr>")
        for n in opts.name:
            output.append("  <th>%s</th>" % n)
        output.append(" </tr>")

    pngs = [os.path.basename(x) for x in glob.glob(os.path.join(plotDirs[0], "*.png"))]
    pngs.sort()
    for p in pngs:
        anchor = os.path.splitext(p)[0] # strip off extension
        output.append(' <tr><td align="center" colspan="%d"><a name="%s"><b>%s</b></a> <a href="#%s">link</a></td></tr>' % (len(opts.dir), anchor, p, anchor))

        output.append(" <tr>")
        for i, d in enumerate(plotDirs):
            shutil.copy(os.path.join(d, p), os.path.join(outputDirs[i], p))
            output.append('  <td><img src="%d/%s"></td>' % (i, p))
        output.append(" </tr>")

    # Look for directory
    output.append(" <tr>")
    for d in opts.dir:
        output.append("  <td>From %s</td>" % os.path.split(os.path.abspath(d))[1])
    output.append(" </tr>")

    # Look for code version
    output.append(" <tr>")
    for d in opts.dir:
        cvFile = os.path.join(d, "codeVersion.txt")
        row = "  <td>"
        if os.path.exists(cvFile):
            f = open(cvFile)
            codeVersion = f.readline().rstrip()
            row += "Git commit id %s" % codeVersion
        row += "</td>"
        output.append(row)

    output.append(" </tr>")

    output.extend([
            " </table>",
            "</html>"
            ])
    f = open(os.path.join(opts.output, "index.html"), "w")
    for o in output:
        f.write(o)
        f.write("\n")
    f.close()

    f = open(os.path.join(opts.output, "command.txt"), "w")
    def fmt(s):
        if " " in s:
            return '"%s"' % s
        return s
    f.write(" ".join([fmt(s) for s in sys.argv]))
    f.write("\n")
    f.close()

    print "Plots copied and HTML generated to", opts.output
    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-d", "--dir", dest="dir", action="append", default=[],
                      help="Directory to look for PNGs (can be given multiple times)")
    parser.add_option("--subdir", dest="subdir", type="string", default=None,
                      help="Subdirectory inside DIRs to look the plots.")
    parser.add_option("-n", "--name", dest="name", action="append", default=[],
                      help="Name of a directory (corresponding to a directory)")
    parser.add_option("-o", "--output", dest="output", default="validation",
                      help="Output directory name (timestamp is added)")
    parser.add_option("-t", "--title", dest="title", default="",
                      help="Optional title")
    parser.add_option("-m", "--message", dest="message", default="",
                      help="Optional message")
    (opts, args) = parser.parse_args()

    if len(opts.dir) == 0:
        parser.error("No directories given (-d/--dir)")
    if len(opts.name) != 0 and len(opts.name) != len(opts.dir):
        parser.error("If names are given (-n/--name), their count (%d) must match to the number of directories (%d)" % (len(opts.name), len(opts.dir)))

    opts.output += "_"+time.strftime("%y%m%d_%H%M%S")

    sys.exit(main(opts))
