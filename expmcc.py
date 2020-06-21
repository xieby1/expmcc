#!/usr/bin/python3
import sys
import subprocess
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
expm_common_path = os.path.join(script_dir, "expm-common.py")
subprocess.check_call([expm_common_path] + ["--expmcc"] + sys.argv[1:])