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
        Creates rts2 object.
        """

        self.exposure = azcam.utils.get_object("exposure")
        self.tempcon = azcam.utils.get_object("tempcon")
        self.instrument = azcam.utils.get_object("instrument")
        self.controller = azcam.utils.get_object("controller")

        return

    def reset(self):
        """
        Reset camera. 
        """

        reply = azcam.api.reset()

        return reply

    def open(self):
        """
        Open controller shutter. 
        """

        reply = azcam.api.set_shutter(1, 0)

        return reply

    def close(self):
        """
        Close controller shutter. 
        """

        reply = azcam.api.set_shutter(0, 0)

        return reply

    def totalcount(self):
        """
        Pixels in image. 
        """
        reply = azcam.api.get_par("numpiximage")

        return reply

    def flush(self, cycles=1):
        """
        Flush sensor "cycles" times.
        """

        reply = self.exposure.flush(cycles)

        return

    def setexp(self, et: float = 1.0) -> str:
        """
        Set camera exposure time in seconds.
        """

        self.exposure.set_exposuretime(et)

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

        reply = azcam.api.expose1(exposure_time, image_type, image_title)

        return reply

    def resend(self):
        """
        Send local temp image to remote image server.
        """

        azcam.utils.get_object("exposure").image.send_image(f"{self.exposure.temp_image_file}.fits")

        return

    def readout(self):
        """
        Stop current integration and readout.
        """
        
        self.exposure.start_readout()

        return

    def abort(self):
        """
        Stop current integration and readout.
        """

        azcam.utils.get_object("exposure").abort()

        return

    def get_pixels_remaining(self):
        """
        Return current number of pixels remaing in readout.
        """
        
        reply = self.exposure.get_pixels_remaining()

        return reply
        
        
    def pixelcount(self):
        """
        Pixels remaing until readout is finished. 
        """
        
        reply = self.get_pixels_remaining()

        return reply

    def get_exposuretime_remaining(self):
        """
        Return exposure time remaining in intration in seconds. 
        """
        
        reply = self.exposure.get_exposuretime_remaining()

        return float(reply)
