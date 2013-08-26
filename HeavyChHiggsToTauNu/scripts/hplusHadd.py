#!/usr/bin/env python

### Adapted from fhadd to H+ needs
#
# Original author: Sebastian Schmitt, sebastian.schmitt@cern.ch
# http://root.cern.ch/phpBB3/viewtopic.php?f=3&t=14881
# /afs/cern.ch/user/s/schmitts/public/fhadd/fhadd.py
#
# Modified by: Matti Kortelainen, matti.kortelainen@cern.ch

"""Fast but memory hungry alternative to ROOT's hadd.

fhadd - the main routine
"""
import logging
import optparse
import shutil
import sys
import os

import ROOT
ROOT.TH1.AddDirectory(False)
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

#@profile
def processDir(outdir, directory, otherdirs, className=None, verbose=False):
    keys = directory.GetListOfKeys()

#    l = ROOT.TList()
#    ROOT.SetOwnership(l, True)

    alreadyProcessed = {}

    for key in keys:
        obj = key.ReadObj()
        if verbose:
            print "Target object: %s/%s" % (outdir.GetPath(), obj.GetName())
        if obj.GetName() in alreadyProcessed:
            print >>sys.stderr, "Error in merging %s/%s, more than 1 object exists" % (directory.GetPath(), obj.GetName())
            continue
        alreadyProcessed[obj.GetName()] = True

        if obj.InheritsFrom("TDirectory"):
            d = outdir.mkdir(obj.GetName())
            processDir(d, obj, [d.GetDirectory(obj.GetName()) for d in otherdirs], className, verbose)
            continue

        if obj.InheritsFrom("TTree"):
            raise Exception("Merging TTree is not supported with hplusHadd.py, use ROOT's hadd instead (encountered TTree %s/%s" % (directory.GetPath(), obj.GetName()))

        if className is not None and not obj.InheritsFrom(className):
            if obj.InheritsFrom("TNamed"):
                outdir.cd()
                obj.Write(obj.GetName(), ROOT.TObject.kOverwrite)
            continue

        # http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=15496
        # This one seems to save quite a lot of "garbage
        # collection" time
#        ROOT.SetOwnership(obj, True)

        l = ROOT.TList()
#        ROOT.SetOwnership(l, True)
#        l2 = []
        for od in otherdirs:
            o = od.Get(obj.GetName())
            ROOT.SetOwnership(o, True)
            o.SetDirectory(0)
            l.Add(o)
#            l2.append(o)
        ret = obj.Merge(l)
        if ret < 0:
            print "  Input histogram %s/%s" % (directory.GetPath(), obj.GetName())
#        l.Clear("nodelete")
#        l.Delete()
#        for o in l2:
#            del o

        if hasattr(obj, "SetDirectory"):
            obj.SetDirectory(outdir)
        else:
            outdir.cd()
            obj.Write(obj.GetName(), ROOT.TObject.kOverwrite)

#    l.Delete()

#@profile
def fhadd(target, sources, force=False, verbose=False):
    """This function will merge objects from a list of root files and write them
    to a target root file. The target file is newly created and must not
    exist, or if -f ("force") is given, must not be one of the source files.

    IMPORTANT: It is required that all files have the same content!

    Fast but memory hungry alternative to ROOT's hadd.

    Arguments:

    target -- name of the target root file
    sources -- list of source root files
    force -- overwrite target file if exists
    """

    classname = "TH1"

    # check if target file exists and exit if it does and not in force mode
    if not force and os.path.exists(target):
        raise RuntimeError("target file %s exists" % target)

    # configure logger
    logger = logging.getLogger("fhadd")
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    # open the target file
    print "fhadd Target file:", target
    outfile = ROOT.TFile.Open(target, "RECREATE")

    # open the seed file - contents is looked up from here
    seedfilename = sources[0]
    print "fhadd Source file 1:", seedfilename
    seedfile = ROOT.TFile.Open(seedfilename)

    # open remaining files
    otherfiles = []
    for n, f in enumerate(sources[1:]):
        print "fhadd Source file %d: %s" % (n+2, f)
        otherfiles.append(ROOT.TFile.Open(f))

    processDir(outfile, seedfile, otherfiles, classname, verbose=verbose)

    for f in [outfile, seedfile]+otherfiles:
        ROOT.gROOT.GetListOfFiles().Remove(f);

    outfile.Write()
    outfile.Close()

#    import psutil
#    p = psutil.Process(os.getpid())
#    print "RSS at end %.1f MB" % (float(p.get_memory_info().rss)/1024/1024)

    return 0

if __name__ == "__main__":
    parser = optparse.OptionParser("Usage: %prog [options] target source [source ...]")
    parser.add_option('-f', '--force', dest="force",
                      help='allow to overwrite target',
                      default=False,
                      action="store_true")
    parser.add_option('-v', '--verbose', dest="verbose",
                      help='verbose',
                      default=False,
                      action="store_true")
    (opts, args) = parser.parse_args()
    if len(args) < 2:
        parser.error("target and at least 1 source are missing")

    try:
        sys.exit(fhadd(args[0], args[1:], opts.force, opts.verbose))
    except KeyboardInterrupt:
        sys.exit(1)
