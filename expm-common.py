#!/usr/bin/python3
import os
import subprocess
import argparse
import sys

# 1. Config
# 1.1 Read from environ
# 1.2 TODO: Read from config files, if not defined in envrion,
#     when directly executing expmcc/expmxx falls into this situation
if "EXPMCC" in os.environ:
    compiler_cc = os.environ["EXPMCC"]
else:
    compiler_cc = "gcc" # TODO
if "EXPMXX" in os.environ:
    compiler_cxx = os.environ["EXPMXX"]
else:
    compiler_cxx = "g++" # TODO

# 2. Select compiler
parser = argparse.ArgumentParser()
parser.add_argument("--expmcc", action="store_true")
parser.add_argument("--expmxx", action="store_true")
(namespace, rest_argv) = parser.parse_known_args()
directly_exec = True
if namespace.expmcc:
    compiler = compiler_cc
    if "EXPMCC" in os.environ:
        directly_exec = False
else:
    compiler = compiler_cxx
    if "EXPMXX" in os.environ:
        directly_exec = False

# 3. Execute the original command
original_command_completed = subprocess.run([compiler] + rest_argv)
if directly_exec or original_command_completed.returncode!=0:
    sys.exit(original_command_completed.returncode)

# 4. Get original output absolute path.
# 4.1 Find "-o", if there exists one
output_path_index = rest_argv.index("-o") + 1
output_path = rest_argv[output_path_index]
output_path = os.path.abspath(output_path)
# 4.2 TODO:Add "-o", if there not exists one, and

# 5. Modify original output absolute path, 
#    place all expanded-marco source file under directory "expm"
expm_root_path = os.environ["EXPM_ROOT_PATH"]
common_path = os.path.commonpath([output_path, expm_root_path])
modified_output_path = os.path.join(
    expm_root_path, "expm",
    os.path.relpath(output_path, start=common_path))
# 5.1 Create directories if path not exist
if not os.path.exists(os.path.dirname(modified_output_path)):
    os.makedirs(os.path.dirname(modified_output_path))

rest_argv[output_path_index] = modified_output_path
subprocess.run([compiler, "-E"] + rest_argv)