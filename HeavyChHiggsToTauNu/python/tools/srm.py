## \package srm
# Provides python interface to srm tools
#
# Main usage is from hplusSrm.py tool

import os, re, math
import subprocess
import getopt

def srmls(count, offset):
    return ["srmls",  "-srm_protocol_version=2",  "-server_mode=passive",  "-streams_num=1",
            "-count=%d" % count,
            "-offset=%d" % offset]
def srmrm():
    return ["srmrm", "-srm_protocol_version=2",  "-server_mode=passive"]

def srmrmdir():
    return ["srmrmdir",  "-srm_protocol_version=2",  "-server_mode=passive"]

skip_re = [re.compile("^java -cp"), re.compile("^SRM_debugging")]

class SrmException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

def execute(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output = p.communicate()[0]
    ret = []
    for line in output.split("\n"):
        skip = False
        for x in skip_re:
            m = x.search(line)
            if m:
                skip = True
                break
        if skip:
            continue
        
        ret.append(line.replace("\n", ""))

    return ret

def ls_internal(url):
    def isNotEmpty(str):
        return len(str) > 0
    def removeSlashes(str):
        host_re = re.compile("^(?P<host>[^:/]+://[^:/]+(:\d+)?/)(?P<dir>.*)$")
        m = host_re.search(str)
        return m.group("host")+"/".join(filter(isNotEmpty, m.group("dir").split("/")))
        
    ret = []
    max_size = 1

    file_re = re.compile("(?P<size>\d+)\s+(?P<file>\S+)")
    url = removeSlashes(url)

    count = 950
    iter = 0
    while iter < 100:
        offset = iter*count
        iter += 1

        output = execute(srmls(count, offset) + [url])
        if len(output) > 0 and ("srm" in output[0] and "client" in output[0] and "error" in output[0]):
            raise SrmException("\n".join(output))


        files = []

#        first_line_found = False
        for line in output:
            m = file_re.search(line)
            if m:
                size = int(m.group("size"))
                max_size = max(max_size, size)
                files.append((m.group("file"), size)) 
                          
#                if not first_line_found and int(m.group("size")) == 0:
#                    first_line_found = True
#                elif first_line_found:
#                    size = int(m.group("size"))

        for f, s in files:
            comp = filter(isNotEmpty, f.split("/"))
            bn = comp[-1]
            path = "/".join(comp[:-1])
            ind = url.find(path)
            name = url[:ind]+path+"/"+bn
            isDir = False
            if f[-1] == "/":
                isDir = True

            ret.append((name, s, isDir))

        if len(files) < count:
            break

    # If srmls returns multiple files for one URL, the directory URL
    # is also one of them. Here we remove all occurrences of the
    # directory.
    if len(ret) > 1:
        ret2 = []
        for r in ret:
            if r[0] != url:
                # If entry is a directory, append slash to the name
                t = (r[0], r[1])
                if r[2]:
                    t = (r[0]+"/", r[1])
                
                ret2.append(t)
        ret = ret2
        ret.sort()
    else:
        t = ret[0]
        if t[2]:
            # One entry, which is directory => the directory is empty, let's return nothing
            ret = []
        else:
            ret = [(t[0], t[1])]

    # If srmls returns multiple files for one URL, the URL represents
    # a directory. After sorting, this directory is first, and we
    # remove it.
    #if len(ret) > 1:
    #    ret = ret[1:]

    return (ret, max_size)

def ls(urls):
    def ls_recursive(filelist, max_size, level):
        if level != None:
            if level == 0:
                return (filelist, max_size)
            level -= 1

        ret = []
        for f, size in filelist:
            if f[-1] == "/":
                (res, res_max_size) = ls_internal(f)
                (res, res_max_size) = ls_recursive(res, res_max_size, level)
                if len(res) > 0:
                    ret.extend(res)
                    max_size = max(max_size, res_max_size)
                else:
                    ret.append( (f, size) )
            else:
                ret.append( (f, size) )
        return (ret, max_size)

    long = False
    recursive = False
    recursiveLevel = None
    if len(urls) > 1:
        if "-l" in urls:
            long = True
            del urls[urls.index("-l")]
        if "-r" in urls:
            recursive = True
            i = urls.index("-r")
            if i+1 < len(urls):
                val = urls[i+1]
                try:
                    recursiveLevel = int(val)
                except ValueError:
                    pass
                if recursiveLevel != None:
                    del urls[i+1]
            del urls[i]
    if len(urls) != 1:
        raise SrmException("ls expects exactly ONE URL (got %d)" % len(urls))

    (ret, max_size) = ls_internal(urls[0])
    if recursive:
        (ret, max_size) = ls_recursive(ret, max_size, recursiveLevel)
    if long:
        formstr = "%%%dd  %%s"%(int(math.log10(max_size)) +1)
        ret = [formstr % (x[1], x[0]) for x in ret]
    else:
        ret = [x[0] for x in ret]
    
    return ret

def du_pretty(bytes, print_mode):
    ret = "%6d   B" % bytes
    if print_mode == "b":
        return ret
    
    div = bytes
    for lab in ["kiB", "MiB", "GiB", "TiB"]:
        div = div/1024.
        if div < 1.0:
            break
        ret = "%6.2f %s" % (div, lab)
    return ret

def du_recursive(url, print_mode):
    files = ls_internal(url)[0]
    total = 0
    for file, size in files:
        if file == url:
            continue
        total += size
        if file[-1] == "/":
            #print "Recursing to directory %s" % file
            total += du_recursive(file[:-1], print_mode)

    print "%s  %s" % (du_pretty(total, print_mode), url)
    return total
    
    
def du(urls):
    mode = "h"
    if len(urls) == 2:
        option = urls[0]
        if option == "-b":
            mode = "b"
        elif option == "h":
            mode = "h"
        urls = urls[1:]
    if len(urls) != 1:
        raise SrmException("du expects exactly ONE URL (got %d)" % len(urls))
    bytes = du_recursive(urls[0], mode)

def rm(urls):
    verbose = False
    recursive = False
    def internal_rm_wrapper(urls):
        if len(urls) == 0:
            return
        cmd = srmrm() + urls
        if verbose:
            print " ".join(cmd)
        output = execute(cmd)
        print "\n".join(output)
        
    def internal_rm(urls):
        split = 10

        buffer = []
        for u in urls:
            if recursive and u[-1] == "/":
                print "Recursing to directory %s" % u
                sub_urls = ls([u])
                internal_rm(sub_urls)
                p = [u]
                if verbose:
                    p = ["-v", u]
                rmdir(p)
            else:
                buffer.append(u)
            if len(buffer) >= split:
                internal_rm_wrapper(buffer)
                buffer = []
        internal_rm_wrapper(buffer)

    try:
        opts, urls = getopt.getopt(urls, "rv")
    except getopt.GetoptError, e:
        raise SrmException(str(e))

    for o, a in opts:
        if o == "-r":
            recursive = True
        elif o == "-v":
            verbose = True

    if len(urls) == 0:
        raise SrmException("rm expects at least one url")

    if recursive:
        for u in urls:
            sub_urls = ls([u])
            internal_rm(sub_urls)
            p = [u]
            if verbose:
                p = ["-v", u]
            rmdir(p)
    else:
        internal_rm(urls)

def rmdir(urls):
    verbose = False

    try:
        opts, urls = getopt.getopt(urls, "v")
    except getopt.GetoptError, e:
        raise SrmException(str(e))

    for o, a in opts:
        if o == "-v":
            verbose = True

    if len(urls) == 0:
        raise SrmException("rmdir expects at least one url")

    split = 10
    i = 0
    while i < len(urls):
        suburls = urls[i:i+split]
        i += split
        cmd = srmrmdir() + suburls
        if verbose:
            print " ".join(cmd)
        output = execute(cmd)
        print "\n".join(output)
