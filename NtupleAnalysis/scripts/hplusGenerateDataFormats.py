#!/usr/bin/env python

import os
import re
import sys
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

re_vector = re.compile("vector<(?P<type>.*)>")

def generateParticle(types, particle, discriminatorCaptions):
    discriminatorList = {}
    for k in discriminatorCaptions.keys():
        discriminatorList[k] = []
  
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
            if particleFloatType == None:
                particleFloatType = realtype
            elif particleFloatType != realtype:
                if realtype in ["float", "double"]:
                    raise Exception("Mismatch in 4-vector branch types: all of them must be of the same type, and now {branch} has {type} while others have {otype}".format(branch=branch, type=realtype, otype=particleFloatType))
        else:
            # Collect branches
            branchObjects.append("  const Branch<std::{vectype}> *f{vecname};".format(vectype=vectype, vecname=capname))
            branchAccessors.append("  {type} {name}() const {{ return this->fCollection->f{capname}->value()[this->index()]; }}".format(type=realtype, name=name, capname=capname))
            branchBooks.append("  mgr.book(prefix()+\"_{name}\", &f{capname});".format(name=name, capname=capname))
            # Collect discriminators
            for k in discriminatorCaptions.keys():
                if branch.startswith(particle) and k in branch:
                    discriminatorList[k].append(name)
    if particleFloatType is None:
        if len(branchObjects):
            raise Exception("Unable to infer the floating point type for {particle}".format(particle=particle))
        else:
            particleFloatType = "double" # default value

    # Getter for discriminator method names
    discriminatorCaptionGetters = ""
    for k in discriminatorCaptions.keys():
        #print k, discriminatorList[k]
        discriminatorCaptionGetters += "  std::vector<std::string> get%sDiscriminatorNames() {\n"%discriminatorCaptions[k]
        discriminatorCaptionGetters += "    static std::vector<std::string> n = { std::string(\"%s\")};\n"%("\"), std::string(\"".join(map(str, discriminatorList[k])))
        discriminatorCaptionGetters += "    return n;\n"
        discriminatorCaptionGetters += "  }\n"
    # Getter for discriminator method values
    discriminatorMethodGetters = ""
    for k in discriminatorCaptions.keys():
        discriminatorMethodGetters += "  std::vector<std::function<bool()>> get%sDiscriminatorValues() {\n"%discriminatorCaptions[k]
        discriminatorMethodGetters += "    static std::vector<std::function<bool()>> values = {\n"
        for i in range(len(discriminatorList[k])):
            if i < len(discriminatorList[k])-1:
                discriminatorMethodGetters += "      [&](){ return this->%s(); },\n"%discriminatorList[k][i]
            else:
                discriminatorMethodGetters += "      [&](){ return this->%s(); }\n"%discriminatorList[k][i]
        discriminatorMethodGetters += "    };\n"
        discriminatorMethodGetters += "    return values;\n"
        discriminatorMethodGetters += "  }\n"

    includes = "#include \"DataFormat/interface/Particle.h\"\n"
    if len(discriminatorCaptions.keys()):
        includes += "#include <string>\n"
        includes += "#include <vector>\n"
        includes += "#include <functional>\n"

    prefix = particle
    if particle != "HLTTau":
        prefix += "s"

    header = """// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_{type}_h
#define DataFormat_{type}_h

{includes}
class {type}Collection: public ParticleCollection<{particleFloatType}> {{
public:
  explicit {type}Collection(const std::string& prefix="{prefix}"): ParticleCollection(prefix) {{}}
  ~{type}Collection() {{}}

  void setupBranches(BranchManager& mgr);

{discrCaptionGetters}
protected:
{branchObjects}
}};


template <typename Coll>
class {type}: public Particle<Coll> {{
public:
  {type}() {{}}
  {type}(const Coll* coll, size_t index): Particle<Coll>(coll, index) {{}}
  ~{type}() {{}}

{discrMethodGetters}
{branchAccessors}

}};

#endif
""".format(type=particle+"Generated", includes=includes, prefix=prefix, particle=particle, particleFloatType=particleFloatType, branchObjects="\n".join(branchObjects), discrCaptionGetters=discriminatorCaptionGetters, discrMethodGetters=discriminatorMethodGetters, branchAccessors="\n".join(branchAccessors))

    source = """
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/{type}.h"

#include "Framework/interface/BranchManager.h"

void {type}Collection::setupBranches(BranchManager& mgr) {{
  ParticleCollection::setupBranches(mgr);
{branchBooks}
}}
""".format(type=particle+"Generated", branchBooks="\n".join(branchBooks))

    basedir = os.path.join(os.environ["HIGGSANALYSIS_BASE"], "NtupleAnalysis", "src", "DataFormat")
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
    if not "HIGGSANALYSIS_BASE" in os.environ:
        print "Environment variable $HIGGSANALYSIS_BASE not set, please source setup.sh"
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

    # The provided dictionaries are for grouping discriminators
    generateParticle(types, "Tau", {"Isolation": "Isolation", "againstElectron": "AgainstElectron", "againstMuon": "AgainstMuon"})
    generateParticle(types, "Jet", {"BJetTags": "BJetTags", "PUID": "PUID"})
    generateParticle(types, "Muon", {"ID": "ID"})
    generateParticle(types, "Electron", {"ID": "ID"})
    #generateParticle(types, "GenParticle", {}) # data fields in the root file are missing at the moment
    generateParticle(types, "GenJet", {})
    generateParticle(types, "HLTTau", {})
    generateParticle(types, "PFCands", {})
    # HLTTau and PFCands contain only generic momentum and pdgId information, no generation needed

    return 0


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] root_file")
    parser.add_option("--tree", dest="tree", default="Events",
                      help="Generate data format from this tree (default: 'Events')")

    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("You should give exactly one root_file, got %d" % len(args))


    sys.exit(main(opts, args))
