#!/usr/bin/env python


import sys,ConfigParser,os,string,commands,time,re

# for json support
try: # FUTURE: Python 2.6, prior to 2.6 requires simplejson
    import json
except:
    try:
        import simplejson as json
    except:
        print "Please use lxplus or set an environment (for example crab) with json lib available"
        sys.exit(1)


#######################################################################################
#main starts here#


# reading config file
if len(sys.argv)!=5:
    print "Usage: ",sys.argv[0],"<runmin> <runmax> <oldjson> <filteredjson>"
    sys.exit(1)


RUNMINstr=sys.argv[1]
RUNMAXstr=sys.argv[2]
JSON=sys.argv[3]
JSONNEW=sys.argv[4]

if not RUNMINstr.isdigit():
    print "RUNMIN paramente not understood:"+RUNMINstr
    sys.exit(1)
if not RUNMAXstr.isdigit():
    print "RUNMIN paramente not understood:"+RUNMINstr
    sys.exit(1)

RUNMIN=int(RUNMINstr)
RUNMAX=int(RUNMAXstr)

if RUNMIN>RUNMAX:
    print "RUNMIN is > than RUNMAX"
    sys.exit(1)

jsondict={}
jsonfiltered={}
# read json file
jsonfile=file(JSON,'r')
jsondict = json.load(jsonfile)

for run in jsondict.keys():
    print "Reading run: "+run
    if int(run)>=RUNMIN and int(run)<=RUNMAX:
        jsonfiltered[run]=jsondict[run]
        print "-----------> accepted"

newfile = open(JSONNEW, 'w')
json.dump(jsonfiltered, newfile,sort_keys=True)
newfile.close() 

print "New filtered json file produced in: "+JSONNEW

