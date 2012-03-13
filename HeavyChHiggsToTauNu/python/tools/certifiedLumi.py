## \package certifiedLumi
# Name -> JSON file mapping

## JSON file mapping
#
# The JSON files are assumed to exist in <tt>test</tt> directory.
files = {
    "Apr21ReReco": "Cert_136033-149442_7TeV_Apr21ReReco_Collisions10_JSON.txt",
    "May10ReReco": "Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt",
    "Aug05ReReco": "Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v3.txt",
    "PromptReco": "Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt",
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
