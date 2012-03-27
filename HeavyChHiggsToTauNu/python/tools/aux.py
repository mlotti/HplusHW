#! /usr/bin/env python

import sys
import os
import hashlib
import imp

def execute(cmd):
    f = os.popen(cmd)
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
    f.close()
    return ret

def load_module(code_path):
    try:
        try:
	    try:
   	        fIN = open(code_path, 'rb')
                return  imp.load_source(hashlib.sha224(code_path).hexdigest(), code_path, fIN)
	    except IOError:
	        print "File",code_path,"not found"
	        sys.exit()
        finally:
            try: fin.close()
            except: pass
    except:
	print "Problem importing file",code_path
	sys.exit()
