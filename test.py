import sys
from subprocess import run, PIPE, TimeoutExpired
import os
import tempfile
import json
import time


CLINGO = "/usr/share/miniconda/bin/clingo"
PYTHON = "/usr/share/miniconda/bin/python"
INSTANCES = "instances/"
REF_ENC = "checker.lp"
DUMMY = "dummy.lp"
SOLUS = "925"
SOLUTIONS = "solutions/"


def call_python(input_names, timeout):
    cmd = [PYTHON, "multi-jobshop.py",  "multi-jobshop.lp",  "--outf=3", "--opt-mode=optN",  "1", "-c w=3", "--warn=no-atom-undefined", "--warn=no-file-included", "--warn=no-operation-undefined", "--warn=no-variable-unbounded", "--warn=no-global-variable"] + input_names
    start = time.time()
    output = run(cmd, stdout=PIPE, stderr=PIPE, timeout=timeout)
    end = time.time()
    if output.stderr:
        raise RuntimeError("Clingo: %s" % output.stderr)
    return output.stdout, end-start

def test(inst, timeout):
    try:
        stdout, time = call_python([INSTANCES+inst], timeout)
    except RuntimeError as e:
        raise e

    solutions = stdout.decode('utf-8').replace(" ", '*').replace("Answer:\n",'')
    solutions = solutions[:-1]
    solutions = solutions.split("\n")
    for i in range(len(solutions)):
        solutions[i] = solutions[i].split("*")
        solutions[i].sort()
    solutions.sort()

    # check optimal solution
    inst_sol = inst[:-2]+"json"
    with open(SOLUTIONS+inst_sol,"r") as infile:
        ref_solutions = infile.read()
    ref_solutions = ref_solutions[2:-2].replace("),",")*")
    ref_solutions = ref_solutions.split(",\n")
    for i in range(len(ref_solutions)):
        ref_solutions[i] = ref_solutions[i][2:-1].split("*")
        ref_solutions[i].sort()
    ref_solutions.sort()
    for s in ref_solutions:
    return solutions[-1] in ref_solutions, time

def main():
    # check input
    if len(sys.argv) < 1:
        raise RuntimeError("not enough arguments (%d instead of 3)" % (len(sys.argv) - 1))
    timeout = sys.argv[1]
    timeout = int(timeout)

    dir = os.listdir(INSTANCES)
    dir.sort()
    success = True

    message = ""
    #loop over all instances
    for inst in dir:
        result = 0
        error = False
        try:
            res, time = test(inst, timeout)
            if not res:
                success = False
        except Exception as e:
            success = False
            if isinstance(e, TimeoutExpired):
                result = "timeout\n"
            else:
                result = "error\n"
                error = e
        message += "$"+inst+ ": "
        if result:
            message += result
            if error:
                message += str(error)+"\n"
        else:
            message += "success" if res else "failure"
            message += " in "+str(1000*time)[:7]+" ms\n"
    return success, message

if __name__ == '__main__':
    try:
        success, message = main()
        if success:
            message += "SUCCESS\n"
        else:
            message += "FAILURE\n"
        sys.stdout.write(message)
    except Exception as e:
        sys.stderr.write("ERROR: %s\n" % str(e))
        exit(1)
