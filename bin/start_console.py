"""
Script to start an azcamconsole application.

Usage: Execute this file from File Explorer
"""

import os
import sys

# select which python to use (virtual environments)
# python = "/data/code/venvs/qt/Scripts/ipython.exe"
python = "/python38/Scripts/ipython.exe"
interactive = "-i"  # "-i" or ""

# parse arguments for command script
if len(sys.argv) > 1:
    arguments = sys.argv[1:]
else:
    arguments = [""]
    # arguments = ["-system VIRUS"]
    # arguments = ["-system VIRUS -data \data"]

configscript = "azcam_pepsi.console"

profile = "azcamconsole"
import_command = f"import {configscript}; from azcam.cli import *; del azcam.cli"

# execute
cl = (
    f"{python} --profile {profile} "
    f"--TerminalInteractiveShell.term_title_format={profile} {interactive} "
    f'-c "{import_command}" -- {" ".join(arguments)}'
)
os.system(cl)
