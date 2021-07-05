__all__ = ["HuntsmanCameraRawFormatter"]

from lsst.obs.base import FitsRawFormatterBase

from lsst.obs.huntsman import HuntsmanCamera
from lsst.obs.huntsman.translator import HuntsmanTranslator
from lsst.obs.huntsman.filters import HUNTSMAN_FILTER_DEFINITIONS


class HuntsmanCameraRawFormatter(FitsRawFormatterBase):

    translatorClass = HuntsmanTranslator
    filterDefinitions = HUNTSMAN_FILTER_DEFINITIONS

    def getDetector(self, id):
        return HuntsmanCamera().getCamera()[id]
