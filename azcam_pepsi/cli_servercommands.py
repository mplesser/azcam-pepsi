# imports for azcamserver command line

import azcam
from azcam import api
from azcamserver_shortcuts import *

# put the db["objects"] items in the current name space for CLI use
for obj in azcam.db.objects:
    globals()[obj] = azcam.utils.get_object(obj)
