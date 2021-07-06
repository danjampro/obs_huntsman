import os
from functools import lru_cache

from lsst.utils import getPackageDir
from lsst.daf.butler.core.utils import getFullTypeName
from lsst.afw.cameraGeom import makeCameraFromPath, CameraConfig
from lsst.obs.base import Instrument

from lsst.obs.huntsman.translator import HuntsmanTranslator
from lsst.obs.huntsman.filters import HUNTSMAN_FILTER_DEFINITIONS

__all__ = ("HuntsmanCamera",)

OBS_PACKAGE_NAME = "obs_huntsman"


class HuntsmanCamera(Instrument):
    """ Huntsman-specific logic for the Gen3 Butler. """

    policyName = "huntsman"
    configPaths = [os.path.join(getPackageDir("obs_huntsman"), "config")]
    filterDefinitions = HUNTSMAN_FILTER_DEFINITIONS
    translatorClass = HuntsmanTranslator

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.configPaths = [os.path.join(getPackageDir(OBS_PACKAGE_NAME), "config")]

    # Class methods

    @classmethod
    def getName(cls):
        """ Return the short (dimension) name for this instrument. """
        return "Huntsman"

    # Methods

    def getCamera(self):
        """ Retrieve the cameraGeom representation of this instrument. """
        path = os.path.join(getPackageDir(OBS_PACKAGE_NAME), "camera")
        return self._getCameraFromPath(path)

    def register(self, registry):
        """ Insert instrument, physical_filter, and detector entries into a `Registry`. """

        camera = self.getCamera()

        obsMax = self.translatorClass.max_exposure_id()

        with registry.transaction():
            registry.syncDimensionData(
                "instrument", {"name": self.getName(),
                               "detector_max": self.translatorClass.max_num_detectors,
                               "visit_max": obsMax,
                               "exposure_max": obsMax,
                               "class_name": getFullTypeName(self)})

            for detector in camera:
                registry.syncDimensionData(
                    "detector", {"instrument": self.getName(),
                                 "id": detector.getId(),
                                 "full_name": detector.getName(),
                                 "name_in_raft": detector.getName()[1:],
                                 "raft": detector.getName()[0],
                                 "purpose": str(detector.getType()).split(".")[-1]})

            self._registerFilters(registry)

    def getRawFormatter(self, dataId=None):
        """ Return the Formatter class that should be used to read raw files. """
        # local import to prevent circular dependency
        from lsst.obs.huntsman.formatter import HuntsmanCameraRawFormatter
        return HuntsmanCameraRawFormatter

    def makeDataIdTranslatorFactory(self):
        """ Return a factory for creating Gen2->Gen3 data ID translators. """
        raise NotImplementedError("Not implemented.")

    # Private methods

    @staticmethod
    @lru_cache()
    def _getCameraFromPath(path):
        """ Return the camera geometry given the path to the location of its definition. """
        config = CameraConfig()
        config.load(os.path.join(path, "camera.py"))
        return makeCameraFromPath(cameraConfig=config, ampInfoPath=path,
                                  shortNameFunc=lambda name: name)
