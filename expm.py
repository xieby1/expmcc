#!/usr/bin/python3
import os
import subprocess
import sys
import argparse

import common as c

# 1. Config
# 1.1 Read config from config files
script_dir = os.path.dirname(os.path.realpath(__file__))
VERSION_path = os.path.join(script_dir, "VERSION")
with open(VERSION_path) as f:
    version_from_file = f.readline()
# 1.2 Config from command line arguments
parser = argparse.ArgumentParser(
    prog=c.expm,
    description="To generate non-marco version of the source code when compiling.")
parser.add_argument("--version", "-v", action="version", version=version_from_file)
parser.add_argument(c.arg_expmcc, metavar="CC", help="set CC as c compiler")
parser.add_argument(c.arg_expmxx, metavar="CXX", help="set CXX as c++ compiler")
# 1.2.-1 Finish parsing arguments
(namespace, rest_argv) = parser.parse_known_args()

# 2. Check config
# e.g. Check whether the compiler exists

# 3. Set environment variables for child process
child_env = os.environ.copy()
child_env[c.EXPM_ROOT_PATH] = os.path.abspath(os.getcwd())
if namespace.expmcc:
    child_env[c.EXPMCC] = namespace.expmcc
if namespace.expmxx:
    child_env[c.EXPMXX] = namespace.expmxx

# 4. Call child process
if len(rest_argv)>0:
    subprocess.run(rest_argv, env=child_env)
