import os
import datetime

import azcam
import azcam.azcamserver
from azcam.ds9display import Ds9Display
from azcam.azcamserver.telescopes.telescope import Telescope
from azcam.azcamserver.systemheader import SystemHeader
from azcam.azcamserver.controllers.controller_archon import ControllerArchon
from azcam.azcamserver.instruments.instrument import Instrument
from azcam.azcamserver.tempcons.tempcon import TempCon
from azcam.azcamserver.exposures.exposure_archon import ExposureArchon
from azcam.azcamserver.cmdserver import CommandServer
import system_config as config

azcam.db.verbosity = config.verbosity

systemname = "pepsired"
azcam.db.systemname = systemname

systemfolder = azcam.utils.fix_path(os.path.dirname(__file__))
azcam.utils.add_searchfolder(systemfolder, 0)
azcam.db.systemfolder = systemfolder

datafolder = config.datafolder_root_red
azcam.db.datafolder = datafolder

parfile = f"{datafolder}/azcam/parameters_{systemname}.ini"
azcam.db.parfile = parfile

# ****************************************************************
# start logging
# ****************************************************************
logfile = os.path.join(datafolder, "azcam/logs", "azcamserver.log")
logfile = azcam.utils.fix_path(logfile)
azcam.utils.start_logging(logfile)
azcam.utils.log(f"Configuring azcamserver for {systemname}")

# ****************************************************************
# common assets
# ****************************************************************
azcam.utils.add_searchfolder(config.commonfolder)

# ****************************************************************
# display
# ****************************************************************
display = Ds9Display()
azcam.db.objects["display"] = display
setattr(azcam, "display", display)
display.initialize()
del azcam.ds9display

# ****************************************************************
# ipython config
# ****************************************************************
azcam.utils.config_ipython()

# ****************************************************************
# command server
# ****************************************************************
cmdserver = CommandServer()
cmdserver.port = 2422  # note port!
azcam.db.cmdserver = cmdserver
azcam.utils.log(f"Starting command server listening on port {cmdserver.port}")
cmdserver.start()

# ****************************************************************
# controller
# ****************************************************************
controller = ControllerArchon()
azcam.db.controller = controller
controller.camserver.port = 4242
# controller.camserver.host = "10.0.0.2"
controller.camserver.host = "10.0.1.1"
controller.timing_file = os.path.join(
    systemfolder, "archon_code", "pepsired_100KHz.acf"
)
controller.reset_flag = 1  # reset by uploading code

# ****************************************************************
# instrument
# ****************************************************************
instrument = Instrument()
azcam.db.instrument = instrument

# ****************************************************************
# temperature controller
# ****************************************************************
tempcon = TempCon()
azcam.db.tempcon = tempcon

# ****************************************************************
# dewar
# ****************************************************************
controller.header.set_keyword("DEWAR", "pepsired", "Dewar name")

# ****************************************************************
# exposure
# ****************************************************************
filetype = "MEF"
exposure = ExposureArchon()
azcam.db.exposure = exposure
exposure.filetype = azcam.db.filetypes[filetype]
exposure.image.filetype = azcam.db.filetypes[filetype]
exposure.aztime.sntp.servers = ["time.nist.gov"]
exposure.display_image = 0
# remote_imageserver_host = "192.168.164.14"
remote_imageserver_host = "10.0.1.11"
remote_imageserver_port = 6543
exposure.set_remote_server(remote_imageserver_host, remote_imageserver_port)
# exposure.set_remote_server()

# ****************************************************************
# header
# ****************************************************************
def update_header():
    """
    Update header, reading current data.
    """

    # make custom changes
    if enabled:
        pass

    return

template = f'{azcam.db.datafolder}/templates/FitsTemplate_pepsired.txt'
system = SystemHeader("pepsired", template)
azcam.utils.set_header("system", system)
system.update_header = (
    update_header
)  # update system header info for each exposure

# ****************************************************************
# detector
# ****************************************************************
from detector_sta1600_pepsi import detector_sta1600

detector_sta1600["ctype"] = ["LINEAR", "LINEAR"]
exposure.set_detpars(detector_sta1600)
exposure.fileconverter.set_detector_config(detector_sta1600)
# WCS - plate scale
sc = 1.0  # ChangeMe
exposure.image.focalplane.wcs.scale1 = 16 * [sc]
exposure.image.focalplane.wcs.scale2 = 16 * [sc]

from pepsi import Pepsi

pepsi = Pepsi()
azcam.utils.set_object("pepsi", pepsi)

# ****************************************************************
# telescope
# ****************************************************************
telescope = Telescope()
telescope.enabled = 0
azcam.utils.set_object("telescope", telescope)

# ****************************************************************
# read par file
# ****************************************************************
if config.readparfile:
    azcam.api.parfile_read(parfile)

# ****************************************************************
# apps
# ****************************************************************
if config.start_azcamtool:
    import start_azcamtool
if config.start_webapp:
    import start_webapp

# ****************************************************************
# finish
# ****************************************************************
azcam.utils.log("Configuration complete")

# ****************************************************************
# debug and testing
# ****************************************************************
def test():

    azcam.utils.log("Running debug mode commands")

    return

# test mode
if config.test_mode:
    test()

# debugger only
if 0:
    test()
