"""
    syntx.py - Uses Houdini's vcc compiler to query the vex function list.
    First argument to the script is the path to vcc. With no arguments, make
    sure VCC_PATH is pointing to the correct location.

    :author: Shawn Lipowski
    :date: 2025-11-16
    :license: MIT, see LICENSE for details.
"""

import os
import sys
import re
import subprocess

VCC_PATH  = 'C:/Program Files/Side Effects Software/Houdini 21.0.440/bin/vcc.exe'
SYN_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
FUNC_PATH = os.path.join(SYN_PATH, 'VexFunctions.txt')

def contexts(vcc_path=VCC_PATH):
    """Return a sorted list of all vex contexts."""
    ctxs = subprocess.check_output([vcc_path, '-X'])
    ctxs = ctxs.decode('ascii').split('\n')
    return sorted([x for x in ctxs if x != '' and x != None])

def context_functions(context, vcc_path=VCC_PATH, as_set=False):
    """Return the sorted list of all function names for a vex context."""
    ctx_info = subprocess.check_output([vcc_path, '-X', context])
    ctx_info = ctx_info.decode('ascii')

    funcs = set()
    for f in re.findall(r'\w+\(', ctx_info):
        if len(f) > 1:
            funcs.add(f[:-1])

    if as_set:
        return funcs
    else:
        return sorted(funcs)

def all_functions(vcc_path=VCC_PATH, function_path=FUNC_PATH):
    """Returns a sorted list of all vex functions in all contexts."""
    all_funcs = set()
    for ctx in contexts():
        all_funcs.update(context_functions(ctx, as_set=True))

    all_funcs_sorted = sorted(all_funcs)

    with open(function_path, 'w') as out:
        for func in all_funcs_sorted[:-1]:
            out.write(f'{func}\n')
        out.write(f'{all_funcs_sorted[-1]}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        all_functions()
    elif len(sys.argv) == 2:
        all_functions(sys.argv[1])
    else:
        raise Exception('To many arguments.')