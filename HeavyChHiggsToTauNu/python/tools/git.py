import subprocess
import errno

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

def getCommitId():
    cmd = ["git", "show", "--pretty=format:%H"]
    output = _execute(cmd)
    if output == None:
        return None
    return output.split("\n")[0]

def getStatus():
    return _execute(["git", "status"])

def getDiff():
    return _execute(["git", "diff"])
