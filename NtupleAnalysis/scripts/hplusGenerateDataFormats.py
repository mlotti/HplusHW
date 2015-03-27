#!/usr/bin/env python

import os
import re
import sys
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

re_vector = re.compile("vector<(?P<type>.*)>")

def generateParticle(types, particle):
    particleBranches = [particle+"s_"+x for x in ["pt", "eta", "phi", "e", "pdgId"]] # these are handled by Particle class
    branchNames = filter(lambda n: n[0:len(particle)+2] == particle+"s_", types.keys())
    branchNames.sort(key=lambda n: types[n]+n)

    particleFloatType = None
    branchObjects = []
    branchAccessors = []
    branchBooks = []
    for branch in branchNames:
        name = branch[len(particle)+2:]
        capname = name[0].upper()+name[1:]
        vectype = types[branch]
        m = re_vector.search(vectype)
        if not m:
            raise Exception("Could not interpret type %s as vector" % vectype)
        realtype = m.group("type")
        if branch in particleBranches:
            if particleFloatType is None:
                particleFloatType = realtype
            elif particleFloatType != realtype:
                raise Exception("Mismatch in 4-vector branch types: all of them must be of the same type, and now {branch} has {type} while others have {otype}".format(branch=branch, type=realtype, otype=particleFloatType))
        else:
            branchObjects.append("  Branch<std::{vectype}> *f{vecname};".format(vectype=vectype, vecname=capname))
            branchAccessors.append("  {type} {name}() {{ return this->fCollection->f{capname}->value()[this->index()]; }}".format(type=realtype, name=name, capname=capname))
            branchBooks.append("  mgr.book(prefix()+\"_{name}\", &f{capname});".format(name=name, capname=capname))


    if particleFloatType is None:
        raise Exception("Unable to infer the floating point type for {particle}".format(particle=particle))

    header = """// -*- c++ -*-
#ifndef DataFormat_{type}_h
#define DataFormat_{type}_h

#include "DataFormat/interface/Particle.h"

class {type}Collection: public ParticleCollection<{particleFloatType}> {{
public:
  explicit {type}Collection(const std::string& prefix="{particle}s"): ParticleCollection(prefix) {{}}
  ~{type}Collection() {{}}

  void setupBranches(BranchManager& mgr);

protected:
{branchObjects}
}};


template <typename Coll>
class {type}: public Particle<Coll> {{
public:
  {type}() {{}}
  {type}(Coll* coll, size_t index): Particle<Coll>(coll, index) {{}}
  ~{type}() {{}}

{branchAccessors}
}};

#endif
""".format(type=particle+"Generated", particle=particle, particleFloatType=particleFloatType, branchObjects="\n".join(branchObjects), branchAccessors="\n".join(branchAccessors))

    source = """
#include "DataFormat/interface/{type}.h"

#include "Framework/interface/BranchManager.h"

void {type}Collection::setupBranches(BranchManager& mgr) {{
  ParticleCollection::setupBranches(mgr);
{branchBooks}
}}
""".format(type=particle+"Generated", branchBooks="\n".join(branchBooks))

    basedir = os.path.join(os.environ["HPLUSANALYSIS_BASE"], "src", "DataFormat")
    hfile = os.path.join(basedir, "interface", particle+"Generated.h")
    ccfile = os.path.join(basedir, "src", particle+"Generated.cc")
    f = open(hfile, "w")
    f.write(header)
    f.close()
    f = open(ccfile, "w")
    f.write(source)
    f.close()

    print "Generated "+hfile
    print "Generated " +ccfile


def main(opts, args):
    if not "HPLUSANALYSIS_BASE" in os.environ:
        print "Environment variable $HPLUSANALYSIS_BASE not set, please source setup.sh"
        return 1

    f = ROOT.TFile.Open(args[0])
    tree = f.Get(opts.tree)
    types = {}
    for branch in tree.GetListOfBranches():
        t = branch.GetClassName() # objects
        if t == "":
            t = branch.GetListOfLeaves()[0].GetTypeName() # basic types
        types[branch.GetName()] = t
    f.Close()

    generateParticle(types, "Tau")
    generateParticle(types, "Jet")
    generateParticle(types, "Muon")
    generateParticle(types, "Electron")

    return 0


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] root_file")
    parser.add_option("--tree", dest="tree", default="Events",
                      help="Generate data format from this tree (default: 'Events')")

    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("You should give exactly one root_file, got %d" % len(args))


    sys.exit(main(opts, args))
