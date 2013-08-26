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

import subprocess
import errno

## Wrapper for executing the git commands
#
# \param cmd   The command and arguments as a list (forwarded to subprocess.Popen)
def _execute(cmd):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
