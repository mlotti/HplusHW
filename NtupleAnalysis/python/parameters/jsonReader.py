from HiggsAnalysis.NtupleAnalysis.main import PSet
import json
import csv
import os

# This file contains all the QGL values and their uncertainties used in the analysis

def setupQGLInformation(QGLRPset, jsonname_Light, jsonname_Gluon):
    
    # Process the json produced with QGLR and add the relevant information to the PSet 
    QGLRPset.LightJetsQGL = _setupQGL(jsonname_Light)
    QGLRPset.GluonJetsQGL = _setupQGL(jsonname_Gluon)

def _setupQGL(jsonname):
        # Read json
        _jsonpath = os.path.join(os.getenv("HIGGSANALYSIS_BASE"), "NtupleAnalysis", "data", "QGLR")
        
        filename = os.path.join(_jsonpath, jsonname)
        
        if not os.path.exists(filename):
            raise Exception("Error: file '%s' does not exist!"%filename)
        f = open(filename)
        contents = json.load(f)
                
        f.close()
        
        # Loop over the contents to convert as list of PSets the requested information
        psetList = []
        for row in contents:
            
            p = PSet(jetType   = row["Jet"],
                     prob      = float(row["prob"]),
                     probError = float(row["probError"]),
                     QGLmin    = float(row["QGLmin"]),
                     QGLmax    = float(row["QGLmax"]),
                     Ptmin     = float(row["Ptmin"]),
                     Ptmax     = float(row["Ptmax"]),
                     )

            psetList.append(p)
            
        return psetList
