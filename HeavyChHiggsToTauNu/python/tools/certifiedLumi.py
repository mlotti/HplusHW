## \package certifiedLumi
# Name -> JSON file mapping

## JSON file mapping
#
# The JSON files are assumed to exist in <tt>test</tt> directory.
files = {
    # 2011
    "DCSONLY11": "json_DCSONLY_2011.txt",
    "PromptReco11": "Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt",
    # 42X ReRecos
    "May10ReReco": "Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt",
    "Aug05ReReco": "Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v3.txt",
    # 44X ReRecos
    "Nov08ReReco": "Cert_160404-180252_7TeV_ReRecoNov08_Collisions11_JSON.txt",

    # 2012
    "DCSONLY12": "json_DCSONLY_2012.txt",
    # 53X PromptReco and ReRecos
    "PromptReco12": "Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt",
    "13Jul2012ReReco": "Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON_v2.txt",
    "06Aug2012ReReco": "Cert_190782-190949_8TeV_06Aug2012ReReco_Collisions12_JSON.txt",
    "24Aug2012ReReco": "Cert_198022-198523_8TeV_24Aug2012ReReco_Collisions12_JSON.txt",
    "11Dec2012ReReco": "Cert_201191-201191_8TeV_11Dec2012ReReco-recover_Collisions12_JSON.txt",
    # 53X Winter13 ReReco
    "22Jan2013ReReco": "Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt",
}

## Get a JSON file name
def getFile(name):
    try:
        return files[name]
    except KeyError:
        raise Exception("No key '%s' for certified lumi file" % name)

if __name__ == "__main__":
    print "Lumi files"
    for name,fname in files.iteritems():
        print "%s: %s" % (name, fname)
