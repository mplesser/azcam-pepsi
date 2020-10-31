"""
Contains the Pepsi class.
"""


import typing

import azcam


class Pepsi(object):
    """
    These methods are called remotely thorugh the command server with syntax such as:
    pepsi.expose 1.0 "zero" "/home/obs/a.001.fits" "some image title".
    """

    def __init__(self):
        """
        Creates pepsi object.
        """

        azcam.api.pepsi = self
        azcam.db.cli_cmds["pepsi"] = self

        return

    def initialize(self):
        """
        Initialize AzCam system.
        """

        azcam.api.exposure.reset()

        return

    def reset(self):
        """
        Reset exposure.
        """

        azcam.api.exposure.reset()

        return

    def open(self):
        """
        Open controller shutter.
        """

        reply = azcam.api.exposure.set_shutter(1, 0)

        return reply

    def close(self):
        """
        Close controller shutter.
        """

        reply = azcam.api.exposure.set_shutter(0, 0)

        return reply

    def totalcount(self):
        """
        Pixels in image.
        """
        reply = azcam.api.exposure.get_par("numpiximage")

        return reply

    def flush(self, cycles=1):
        """
        Flush sensor "cycles" times.
        """

        reply = self.db.exposure.flush(cycles)

        return

    def setexp(self, et: float = 1.0) -> str:
        """
        Set camera exposure time in seconds.
        """

        self.db.exposure.set_exposuretime(et)

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

        reply = azcam.api.exposure.expose1(exposure_time, image_type, image_title)

        return reply

    def resend(self):
        """
        Send local temp image to remote image server.
        """

        azcam.api.exposure.image.send_image(f"{self.exposure.temp_image_file}.fits")

        return

    def readout(self):
        """
        Stop current integration and readout.
        """

        self.db.exposure.start_readout()

        return

    def abort(self):
        """
        Stop current integration and readout.
        """

        azcam.api.exposure.abort()

        return

    def get_pixels_remaining(self):
        """
        Return current number of pixels remaing in readout.
        """

        reply = self.db.exposure.get_pixels_remaining()

        return reply

    def pixelcount(self):
        """
        Pixels remaing until readout is finished.
        """

        reply = self.db.get_pixels_remaining()

        return reply

    def get_exposuretime_remaining(self):
        """
        Return exposure time remaining in intration in seconds.
        """

        reply = self.db.exposure.get_exposuretime_remaining()

        return float(reply)
