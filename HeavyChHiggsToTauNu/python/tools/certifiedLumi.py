
files = {
    "Nov4ReReco": "Cert_136033-149442_7TeV_Nov4ReReco_Collisions10_JSON.txt",
    "Dec22ReReco": "Cert_136033-149442_7TeV_Dec22ReReco_Collisions10_JSON_v4.txt",
    "PromptReco": "Cert_160404-161312_7TeV_PromptReco_Collisions11_JSON.txt",
    "DCSOnly": "json_DCSONLY.txt_160404-161312",
}

def getFile(name):
    try:
        return files[name]
    except KeyError:
        raise Exception("No key '%s' for certified lumi file" % name)

if __name__ == "__main__":
    print "Lumi files"
    for name,fname in files.iteritems():
        print "%s: %s" % (name, fname)
