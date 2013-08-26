#!/usr/bin/env python

import subprocess
import shutil
import time
import sys
import os
from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def execute(command, log):
    log.write("========================================\n")
    log.write("Running command '%s'\n" % " ".join(command))
        
#    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
#    output = p.communicate()[0]
#    log.write(output)
    p.communicate()
    log.write("\n")
    log.flush()

    return p.returncode

def publish(task, log):
    print "Publishing task %s" % task
    cmd = ["crab", "-c", task, "-publish"]
    return execute(cmd, log)

def report(task, log):
    print "Reporting task %s" % task
    cmd = ["crab", "-c", task, "-report"]
    return execute(cmd, log)

def main(opts):
    taskDirs = multicrab.getTaskDirectories(opts)

    logfile = "publish_%s.log" % time.strftime("%y%m%d_%H%M%S")
    log = open(logfile, "w")

    for task in taskDirs:
        if not os.path.exists(task):
            print "Skipping task %s, directory doesnt exist" %  task
            continue
        ret = publish(task, log) 
        if ret != 0:
            print "Publish error (%d) with task %s, see %s for details" % (ret, task, logfile)
            log.close()
            return 1

        if opts.report:
            ret = report(task, log)
            if ret != 0:
                print "Report error (%d) with task %s, see %s for details" % (ret, task, logfile)
                log.close()
                return 1

        if opts.move:
            shutil.move(task, task+"_published")

    log.close()    
    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    multicrab.addOptions(parser)
    parser.add_option("--mv", dest="move", default=False, action="store_true",
                      help="Rename the task dirs with '_published_' postfix after succesful publish")
    parser.add_option("--report", dest="report", default=False, action="store_true",
                      help="Run also crab -report")
    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)

    sys.exit(main(opts))
