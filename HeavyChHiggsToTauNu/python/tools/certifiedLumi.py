
files = {
    "Sep17ReReco": "Cert_132440-144114_7TeV_Sep17ReReco_Collisions10_JSON.txt",
    "StreamExpress": "Cert_132440-149442_7TeV_StreamExpress_Collisions10_JSON_v3.txt",
    "Nov4ReReco": "Cert_136033-149442_7TeV_Nov4ReReco_Collisions10_JSON.txt",
}

def getFile(name):
    return files[name]

if __name__ == "__main__":
    print "Lumi files"
    for name,fname in files.iteritems():
        print "%s: %s" % (name, fname)
