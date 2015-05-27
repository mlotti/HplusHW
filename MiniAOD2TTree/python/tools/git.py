## \package git
# Minimalist interface to git
#
# Provides functions to obtain information of the current code
# version. These include
# \li commit id of the last commit
# \li 'git status' to see the modified files since the last commit, and files not in version control
# \li 'git diff' to see the mofications in version controlled files since the last commit
#
# Used from CMSSW python configuration (for storing the commit id to
# histogram files), and from multicrab code (to store everything to
# text files in multicrab directories).

import os
import copy
import subprocess
import errno

def _findInPath(exe):
    for p in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(p, exe)):
            return p
    return None

## Wrapper for executing the git commands
#
# \param cmd   The command and arguments as a list (forwarded to subprocess.Popen)
def _execute(cmd):
    gitLocation = _findInPath("git")
    if gitLocation is None:
        print "WARNING: Did not find git in $PATH"
        return None
    env = os.environ
    if gitLocation.find("/usr/bin") == 0:
        # Using copy.deepcopy will result in mysterious failures with crab and voms-proxy-info
        env2 = {}
        env2.update(env)
        env = env2
        if "LD_LIBRARY_PATH" in env:
            del env["LD_LIBRARY_PATH"]
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        (output, error) = p.communicate()
        ret = p.returncode
        if ret != 0:
            raise Exception("Ran %s, got exit code %d with output\n%s\n%s" % (" ".join(cmd), ret, output, error))

        return output
    except OSError, e:
        # ENOENT is given if git is not found from path
        if e.errno != errno.ENOENT:
            raise e

    return None

## Get git commit id
def getCommitId():
    cmd = ["git", "show", "--pretty=format:%H"]
    output = _execute(cmd)
    if output == None:
        return None
    return output.split("\n")[0]

## Output of 'git status'
def getStatus():
    return _execute(["git", "status"])

## Output of 'git diff'
def getDiff():
    return _execute(["git", "diff"])
