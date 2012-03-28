#! /usr/bin/env python

import sys
import os
import hashlib
import imp
import re

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
	print "check the file with 'python",code_path,"'"
	sys.exit()

def sort(list):
    value_re = re.compile("(^\d+)(\D*$)")
    for t in list:
        i = len(list)
        while i > 1:
            match1 = value_re.search(list[i-1])
            match2 = value_re.search(list[i-2])  
            if int(match1.group(1)) < int(match2.group(1)):
                 swap(list,i-1,i-2)
            i = i - 1
    return list
        
def swap(list,n1,n2):
    tmp = list[n1]
    list[n1] = list[n2]
    list[n2] = tmp
