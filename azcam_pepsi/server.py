import datetime
import os
import sys

from azcam.server import azcam
import azcam.shortcuts
from azcam.cmdserver import CommandServer
from azcam.genpars import GenPars
from azcam.system import System
from azcam.instrument import Instrument
from azcam.telescope import Telescope

from azcam_archon.controller_archon import ControllerArchon
from azcam_archon.exposure_archon import ExposureArchon
from azcam_archon.tempcon_archon import TempConArchon
from azcam_ds9.ds9display import Ds9Display
from azcam_pepsi.detector_sta1600_pepsi import detector_sta1600
from azcam_pepsi.pepsi_custom import Pepsi

# ****************************************************************
# parse command line arguments
# ****************************************************************
try:
    i = sys.argv.index("-system")
    sysname = sys.argv[i + 1]
except ValueError:
    sysname = "pepsiblue"

# ****************************************************************
# define folders for system
# ****************************************************************
azcam.db.systemname = sysname
azcam.db.systemfolder = os.path.dirname(__file__)
azcam.db.systemfolder = azcam.utils.fix_path(azcam.db.systemfolder)
azcam.db.datafolder = os.path.join("/data", azcam.db.systemname)
azcam.db.datafolder = azcam.utils.fix_path(azcam.db.datafolder)
azcam.db.verbosity = 2  # useful for controller status
azcam.db.parfile = os.path.join(azcam.db.datafolder, f"parameters_{azcam.db.systemname}.ini")

# ****************************************************************
# enable logging
# ****************************************************************
tt = datetime.datetime.strftime(datetime.datetime.now(), "%d%b%y_%H%M%S")
azcam.db.logger.logfile = os.path.join(azcam.db.datafolder, "logs", f"server_{tt}.log")
azcam.db.logger.start_logging(azcam.db.logger.logfile, "123")
azcam.log(f"Configuring {azcam.db.systemname}")

# ****************************************************************
# define and start command server
# ****************************************************************
cmdserver = CommandServer()
cmdserver.port = 2402
azcam.log(f"Starting command server listening on port {cmdserver.port}")
# cmdserver.welcome_message = "Welcome - azcam-itl server"
cmdserver.start()

# ****************************************************************
# display
# ****************************************************************
display = Ds9Display()

# ****************************************************************
# controller
# ****************************************************************
controller = ControllerArchon()
azcam.db.controller = controller
controller.camserver.port = 4242

if sysname == "pepsired":
    controller.camserver.host = "10.0.1.1"
    controller.timing_file = os.path.join(
        azcam.db.systemfolder, "archon_code", "pepsired_100KHz.acf"
    )
elif sysname == "pepsiblue":
    controller.camserver.host = "10.0.2.2"
    controller.timing_file = os.path.join(
        azcam.db.systemfolder, "archon_code", "pepsiblue_100KHz.acf"
    )
controller.reset_flag = 1  # reset by uploading code

# ****************************************************************
# instrument
# ****************************************************************
instrument = Instrument()

# ****************************************************************
# temperature controller
# ****************************************************************
tempcon = TempConArchon()
controller.heater_board_installed = 1

# ****************************************************************
# exposure
# ****************************************************************
filetype = "MEF"
exposure = ExposureArchon()
azcam.db.exposure = exposure
exposure.filetype = azcam.db.filetypes[filetype]
exposure.image.filetype = azcam.db.filetypes[filetype]
exposure.display_image = 1
# remote_imageserver_host = "192.168.164.14"
remote_imageserver_host = "10.0.2.22"
remote_imageserver_port = 6543
exposure.set_remote_server(remote_imageserver_host, remote_imageserver_port)
# exposure.set_remote_server()
exposure.folder = azcam.db.datafolder

# ****************************************************************
# header
# ****************************************************************
template = os.path.join(
    azcam.db.datafolder, "templates", f"fits_template_{azcam.db.systemname}.txt"
)
system = System(azcam.db.systemname, template)

# ****************************************************************
# detector
# ****************************************************************
detector_sta1600["ctype"] = ["LINEAR", "LINEAR"]
exposure.set_detpars(detector_sta1600)
exposure.fileconverter.set_detector_config(detector_sta1600)
# WCS - plate scale
sc = 1.0  # ChangeMe
exposure.image.focalplane.wcs.scale1 = 16 * [sc]
exposure.image.focalplane.wcs.scale2 = 16 * [sc]

# ****************************************************************
# telescope
# ****************************************************************
telescope = Telescope()
telescope.enabled = 0

# ****************************************************************
# read par file
# ****************************************************************
genpars = GenPars()
pardict = genpars.parfile_read(azcam.db.parfile)["azcamserver"]
azcam.utils.update_pars(0, pardict)
wd = genpars.get_par(pardict, "wd", "default")
azcam.utils.curdir(wd)

# ****************************************************************
# custom commands
# ****************************************************************
pepsi = Pepsi()

# ****************************************************************
# web server
# ****************************************************************
from azcam.webserver.web_server import WebServer

webserver = WebServer()

webserver.start()

# ****************************************************************
# GUIs
# ****************************************************************
if 1:
    import azcam_pepsi.start_azcamtool

# ****************************************************************
# finish
# ****************************************************************
azcam.log("Configuration complete")
