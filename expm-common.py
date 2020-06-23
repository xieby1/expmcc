#!/usr/bin/python3
import os
import subprocess
import argparse
import sys

import common as c

# 1. Config
# 1.1 Read from environ
# 1.2 TODO: Read from config files, if not defined in envrion,
#     when directly executing expmcc/expmxx falls into this situation
if c.EXPMCC in os.environ:
    compiler_cc = os.environ[c.EXPMCC]
else:
    compiler_cc = "gcc" # TODO
if c.EXPMXX in os.environ:
    compiler_cxx = os.environ[c.EXPMXX]
else:
    compiler_cxx = "g++" # TODO

# 2. Select compiler
parser = argparse.ArgumentParser()
parser.add_argument(c.arg_expmcc, action="store_true")
parser.add_argument(c.arg_expmxx, action="store_true")
(namespace, rest_argv) = parser.parse_known_args()
directly_exec = True
if namespace.expmcc:
    compiler = compiler_cc
    if c.EXPMCC in os.environ:
        directly_exec = False
else:
    compiler = compiler_cxx
    if c.EXPMXX in os.environ:
        directly_exec = False

# 3. Execute the original command
original_command_completed = subprocess.run([compiler] + rest_argv)
if directly_exec or original_command_completed.returncode!=0:
    sys.exit(original_command_completed.returncode)

# 4. Get original output absolute path.
# 4.1 TODO:Add "-o", if there not exists one, and
if "-o" not in rest_argv:
    # 4.1.1 Find the real path of this source code, be ware of "gcc dir/helloword.c"
    pass
# 4.2 Find "-o"
output_path_index = rest_argv.index("-o") + 1
output_path = rest_argv[output_path_index]
output_path = os.path.abspath(output_path)

# 5. Modify original output absolute path, 
#    place all expanded-marco source file under directory "expm"
expm_root_path = os.environ[c.EXPM_ROOT_PATH]
common_path = os.path.commonpath([output_path, expm_root_path])
modified_output_path = os.path.join(
    expm_root_path, c.expm,
    os.path.relpath(output_path, start=common_path))
# 5.1 Create directories if path not exist
if not os.path.exists(os.path.dirname(modified_output_path)):
    os.makedirs(os.path.dirname(modified_output_path))
# 5.2 TODO:Check and Modify the file name,
#     e.g. CC:  dir/helloworld.o => dir/helloworld.c
#     e.g. CXX: dir/helloworld.o => dir/helloworld.cpp

rest_argv[output_path_index] = modified_output_path
subprocess.run([compiler, "-E"] + rest_argv)