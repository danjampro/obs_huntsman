__all__ = ["HuntsmanCameraRawFormatter"]

import lsst.log
from lsst.obs.base import FitsRawFormatterBase

from lsst.obs.huntsman import HuntsmanCamera
from lsst.obs.huntsman.translator import HuntsmanTranslator
from lsst.obs.huntsman.filters import HUNTSMAN_FILTER_DEFINITIONS


class HuntsmanCameraRawFormatter(FitsRawFormatterBase):

    translatorClass = HuntsmanTranslator
    filterDefinitions = HUNTSMAN_FILTER_DEFINITIONS

    def getDetector(self, id):
        return HuntsmanCamera().getCamera()[id]

    def makeWcs(self, *args, **kwargs):
        """ Use WCS in header by default, rather from boresight info. """
        try:
            return self._createSkyWcsFromMetadata()
        except Exception:
            log = lsst.log.Log.getLogger("fitsRawFormatter")
            log.warn("Unable to create WCS from header.")
        return super().makeWcs(*args, **kwargs)
