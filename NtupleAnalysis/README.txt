Dependencies
============

- C++11-capable compiler (tested on gcc 4.8.2)
- Recent ROOT5 (tested on 5.34/20), with PyROOT and xrootd compiled in
  * xrootd is not yet a real requirement, but PyROOT is
- Python 2.7
- GNU make


- boost/property_tree and its dependencies are now included in this package

Tested configurations
- Matti's laptop
- lxplus within CMSSW_7_4_0_pre6 environment
- lxplus with auto-sourced gcc and ROOT
- jade with auto-sourced gcc and ROOT (+ some dependencies)

Building
========

In the root directory, just type 'make'.

Other make targets
- 'clean'  Deletes generated files (objects, dictionary files, library)
- 'test'   Compile and run tests (see further below)

All object files are placed under generated 'obj' directory. All
non-test object files are linked to a single shared object library
'lib/libHPlusAnalysis.so'.


Running
=======

After compilation, in the main directory run './exampleAnalysis.py'.


Data handling
=============

Data handling is still rather premature. Currently datasets are
defined in 'data' directory as a text files, which have one file per
line (everything after '#' is ignored, i.e. treated like a comment).

In the analysis executable, list of datasets has to be provided
explicitly. There is also a possiblity to create aliases to dataset
names (in 'python/HPlusAnalysis/datasets.py') to allow changing e.g.
version names of the datasets without changing the name used by users.
Some mechanism for providing dataset lists (like the various
multicrab.cfg's with CMSSW+crab) is clearly needed. Matti can think of
several ways for that, but is not sure what would be the "best".

Matti is also thinking the possibility of the following scenario
- the ntuples would be stored on madhatter and read over xrootd
- there would be an option to cache the files locally
  * i.e. the code would copy the files (xrdcp) automatically on the first use
  * the location of the cache could be configurable
This would have the following implications on dependencies
- xrootd (tested on 4.1.1), compiled with crypto support
  * needs 'sudo apt-get install libssl-dev'
- for authentication with certificate user needs to (in Ubuntu 14.04)
  * sudo apt-get install voms-clients
  * sudo add-apt-repository 'deb http://repository.egi.eu/sw/production/cas/1/current egi-igtf core'
  * wget -q -O - https://dist.eugridpma.info/distribution/igtf/current/GPG-KEY-EUGridPMA-RPM-3 | sudo apt-key add -
  * sudo apt-get update
  * sudo apt-get install ca-policy-egi-core

After making this exercise, Matti is no longer sure if this is worth
of the effort (from deployment point of view)... But if this is not
done, some other "good plan" for distributing the data will be needed.


General design
==============

Framework
---------

Framework borrows some ideas from what we had in HipProofAnalysis and
heavily the concepts we have in our CMSSW analysis package (e.g.
EventWeight, EventCounter, HistoWrapper are there). The configuration
is done with python, with a syntax similar to (but lighter than)
CMSSW. A clear difference to CMSSW is that here the program is run by
python, i.e. everything is set up in python, and we return from C++ to
python between datasets. Analysis code itself is still (compiled) C++.

The analyzer classes should inherit from BaseSelector class, and have
the following requirements:
- constructor must take exatly one parameter of type const boost::property_tree::ptree&
- this argument must be passed also to BaseSelector
- the following methods must be implemented (please add the C++11 keyword 'override' to their declaration!)
  * void book(TDirectory *dir)
  * void setupBranches(BranchManager& branchManager)
  * void process(Long64_t entry)
- in the .cc file, the following macro must be called
  * 'REGISTER_SELECTOR(<analyzer class name>);'
It should be noted that while the framework internally wraps
everything to TSelector, the analyzer classes are "free" from the
burdens of the TSelector interface.

Data format
-----------

The main idea is that the data are stored in a flat TTree (most
complex data type being an std::vector of a basic data type, e.g.
vector<float>), while the users are provided an interface that mimics
"traditional" object-oriented interface. This allows that we can store
much information of each particle type such that we pay the I/O price
only when they are accessed (as opposed to proper OO model where the
whole objects would be stored in the TTree). The downside is the need
for manual updating of the data format (possibly conceptually similar
to ROOT's custom streamers).

Here is an inheritance diagram of the particle *collection* classes

ParticleCollection
^
|\- ElectronGeneratedCollection
|   ^
|   \- ElectronCollection
|
|\- MuonGeneratedCollection
|   ^
|   \- MuonCollection
|
|\- TauGeneratedCollection
|   ^
|   \- TauCollection
|
\-- JetGeneratedCollection
    ^
    \- JetCollection


The point of the "*GeneratedCollection" classes is that they are
generated with a script "hplusGenerateDataFormats.py" based on the
contents of an ntuple file (this should make the data format updates
less laborious compared to fully manual approach).

Having "non-generated" classes inheriting from the generated ones
allows to add helper methods that make use of the data from the
generated base classes (e.g. a general "isolation" method for muon).

Each Collection is accompanied by a "Particle" class, such that each
of the collections have "operator[]()" that returns an object of this
type (by value). Each such "Particle" class inherits from a
'Particle<>' template with the Collection class passed as the template
argument.

IMPORTANT NOTE: For both Collections and Particles the inheritance is
NON-VIRTUAL. This means that "Particle" objects should always be
passed by value (or by reference). Especially Particle objects should
be "constructed" only by calling the operator[]() of the corresponding
Collection, and NEVER with 'new'. And users should always use the most
derived classes.


The collections (and other data classes that are not particles) are
collected as members of Event class. The Event object should be a
member of the analyzer class (see ExampleAnalysis for an example).


Some missing pieces
- allowe to overwrite the p4 of a particle
- something to help the selections with HLT path names


Software organization
=====================

- bin                 Useful scripts
- data                Dataset definitions 
- lib                 Final shared library are be placed here
- obj                 Temporary objects files are placed here
- python              Python code
- src                 C++ code, organized in subpackages
  - DataFormat        Data format code
  - ExampleAnalysis   Code for example analysis
  - Framework         Framework code
- test                C++ unit test code

The analysis code to be added could be organized inside 'src' e.g. as follows
- CommonAnalysis      Code common to more than 1 analysis
- SignalAnalysis      Code related only to signal analysis
- QCDMeasurement      Code related only to QCD measurement
- TriggerEfficiency   Code related only to trigger efficiency measurements

Note that the structure above is just a suggestion, and some other
scheme might be better (just try to avoid polluting Framework and
DataFormat with analysis-specific code)

Unit tests
==========

It would be good if the newly added code would be
a) designed such that it is testable
b) have unit tests implemented

The C++ unit tests should be implemented under the 'test' directory,
using a rather recent Catch unit test framework
(https://github.com/philsquared/Catch). For usage, please see the
existing tests, and visit the GitHub page for more documentation.
Catch is by far easiest-to-use C++ testing framework Matti has
encountered, and the amount of required boilerplate code in the tests
is negligible.

The Python unit tests should be implemented directly in the python
"library" files using the unittest library, along
----
if __name__ == "__main__":
    import unittest
    class TestFoo(unittest.TestCase):
    ....
    unittest.main()
----
Please see the existing code for examples.

The executable './test/main' runs all C++ unit tests. To run also all
Python unit tests, there is a script './test/runTests.sh'. The make
target 'test' runs this script after compiling the C++ tests.



Open questions
==============

- Data delivery
  * xrootd vs. something else?
- Output directory format
  * crab2 vs. something else (crab3?)?
- How to know if dataset is data or MC?
  * Straightforward option would be store metadata along the files
  * What other metadata could be useful?
    * Number of events (used in estimating the time left, now obtained via TChain::GetEntries() which leads to file opens)
    * Luminosity for data (assuming the lumi workflow stays roughly the same, i.e. run a script after crab)

