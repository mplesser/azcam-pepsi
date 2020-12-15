# azcamserver configuration parameters

use_venv = 1
venv_script = "c:/venvs/azcam/Scripts/activate.bat"

server_profile = "AzCamServer"
console_profile = "AzCamConsole"
server_cmd_red = "import azcamserver_pepsired; from cli_servercommands import *"
server_cmd_blue = "import azcamserver_pepsiblue; from cli_servercommands import *"
console_cmd_red = "import azcamconsole_pepsired; from cli_consolecommands import *"
console_cmd_blue = "import azcamconsole_pepsiblue; from cli_consolecommands import *"

azcamlogfolder = "c:/azcam/azcamlog/azcamlog"
commonfolder = "c:/azcam/systems/common"

datafolder_root_blue = "c:/data/pepsiblue"
datafolder_root_red = "c:/data/pepsired"

verbosity = 1
xmode = "Minimal"  # Minimal, Context, Verbose
test_mode = 0
readparfile = 1
servermode = "interactive"  # prompt, interactive, server
start_azcamtool = 0
start_webserver = 0
