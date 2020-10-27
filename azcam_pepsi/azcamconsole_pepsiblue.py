# azcamconsole configuration for pepsiblue

import os

import system_config as config

import azcam
import azcam.azcamconsole

azcam.db.verbosity = config.verbosity

systemname = "pepsiblue"
azcam.db.systemname = systemname

systemfolder = azcam.utils.fix_path(os.path.dirname(__file__))
azcam.utils.add_searchfolder(systemfolder, 0)  # top level only
azcam.db.systemfolder = systemfolder

datafolder = config.datafolder_root_blue
azcam.db.datafolder = datafolder

parfile = f"{datafolder}/azcam/parameters_{systemname}.ini"
azcam.db.parfile = parfile

# ****************************************************************
# start logging
# ****************************************************************
logfile = os.path.join(datafolder, "azcam/logs", "azcamconsole.log")
logfile = azcam.utils.fix_path(logfile)
azcam.utils.start_logging(logfile)
azcam.utils.log(f"Configuring azcamconsole for {systemname}")

# ****************************************************************
# common assets
# ****************************************************************
azcam.utils.add_searchfolder(config.commonfolder)

# ****************************************************************
# config ipython if in use
# ****************************************************************
azcam.utils.config_ipython()

# ****************************************************************
# display
# ****************************************************************
from azcam.ds9display import Ds9Display

display = Ds9Display()
azcam.db.objects["display"] = display
setattr(azcam, "display", display)
display.initialize()
del azcam.ds9display

# ****************************************************************
# try to connect to azcamserver
# ****************************************************************
connected = azcam.api.connect()
if connected:
    azcam.utils.log("Connected to azcamserver")
else:
    azcam.utils.log("Not connected to azcamserver")

# ****************************************************************
# read par file
# ****************************************************************
if config.readparfile:
    azcam.api.parfile_read(parfile)

# ****************************************************************
# finish
# ****************************************************************
azcam.utils.log("Configuration complete")

# ****************************************************************
# debug and testing
# ****************************************************************
def test(self):

    azcam.utils.log("Running debug mode commands")
    exposure = azcam.utils.get_object("exposure")
    instrument = azcam.utils.get_object("instrument")
    tempcon = azcam.utils.get_object("tempcon")


# test mode
if config.test_mode:
    test()

# for debugger only
if 0:
    test()
