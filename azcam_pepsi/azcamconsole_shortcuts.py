"""
Shortcuts for command line.

Defines: sav, bf, p, sroi, sf, gf
"""

import azcam


def sav():
    """Shortcut to parfile_write() to save current folder in database."""
    azcam.utils.curdir()  # update wd

    conpars = azcam.db.get("parfile_dict")
    if conpars:
        conpars["azcamconsole"]["wd"] = azcam.utils.curdir()

    azcam.api.parfile_write()

    return None


def bf():
    """Shortcut for file_browser()."""

    folder = azcam.utils.file_browser("", "folder", "Select folder")
    if isinstance(folder, list):
        folder = folder[0]
    azcam.utils.curdir(folder)

    return


def sroi():
    """Alias for set_image_roi()."""
    azcam.itldetchar.utils.set_image_roi()

    return


def sf():
    """Shortcut to set imagefolder to current folder"""

    folder = azcam.utils.curdir()
    azcam.api.set_par("imagefolder", folder)

    return


def gf():
    """
    Shortcut to Go to image folder.
    Also issues sav() command to save folder location.
    """

    folder = azcam.api.get_par("imagefolder")
    if folder is None:
        return

    azcam.utils.curdir(folder)
    azcam.db.wd = folder
    sav()

    return
