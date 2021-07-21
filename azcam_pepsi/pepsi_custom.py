"""
Contains the Pepsi class.
"""


import typing

import azcam
from azcam import db


class Pepsi(object):
    """
    These methods are called remotely thorugh the command server with syntax such as:
    pepsi.expose 1.0 "zero" "/home/obs/a.001.fits" "some image title".
    """

    def __init__(self):
        """
        Creates pepsi tool.
        """

        db.pepsi = self
        db.cli_tools["pepsi"] = self

        return

    def initialize(self):
        """
        Initialize AzCam system.
        """

        db.exposure.reset()

        return

    def reset(self):
        """
        Reset exposure.
        """

        db.exposure.reset()

        return

    def open(self):
        """
        Open controller shutter.
        """

        return db.exposure.set_shutter(1, 0)

    def close(self):
        """
        Close controller shutter.
        """

        return db.exposure.set_shutter(0, 0)

    def totalcount(self):
        """
        Pixels in image.
        """

        return db.exposure.image.focalplane.numpix_image

    def flush(self, cycles=1):
        """
        Flush sensor "cycles" times.
        """

        db.exposure.flush(cycles)

        return "OK"

    def setexp(self, et: float = 1.0) -> str:
        """
        Set camera exposure time in seconds.
        """

        db.exposure.set_exposuretime(et)

        return "OK"

    def expose(
        self, exposure_time: float = -1, image_type: str = "", image_title: str = ""
    ) -> typing.Optional[str]:
        """
        Make a complete exposure.

        :param exposure_time: the exposure time in seconds
        :param image_type: type of exposure ('zero', 'object', 'flat', ...)
        :param image_title: image title, usually surrounded by double quotes.
        """

        return db.exposure.expose1(exposure_time, image_type, image_title)

    def resend(self):
        """
        Send local temp image to remote image server.
        """

        azcam.db.sendimage.send_image(f"{self.exposure.temp_image_file}.fits")

        return

    def readout(self):
        """
        Stop current integration and readout.
        """

        db.exposure.start_readout()

        return

    def abort(self):
        """
        Stop current integration and readout.
        """

        db.exposure.abort()

        return

    def get_pixels_remaining(self):
        """
        Return current number of pixels remaing in readout.
        """

        return db.exposure.get_pixels_remaining()

    def pixelcount(self):
        """
        Pixels remaing until readout is finished.
        """

        return db.get_pixels_remaining()

    def get_exposuretime_remaining(self):
        """
        Return exposure time remaining in intration in seconds.
        """

        reply = db.exposure.get_exposuretime_remaining()

        return float(reply)
