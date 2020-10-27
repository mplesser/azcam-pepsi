# imports for azcamserver command line

from azcamserver_shortcuts import *

import azcam
from azcam import api

# put the db["objects"] items in the current name space for CLI use
for obj in azcam.db.objects:
    globals()[obj] = azcam.utils.get_object(obj)
