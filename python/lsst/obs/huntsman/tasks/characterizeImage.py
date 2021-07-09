from lsst.pipe.tasks.characterizeImage import CharacterizeImageTask
from lsst.pipe.tasks.calibrate import CalibrateTask
from lsst.meas.algorithms.detection import SourceDetectionTask

from huntsman.drp.core import get_logger
LOGGER = get_logger()

"""
https://community.lsst.org/t/calculating-exposure-ids-for-obs-lsst-cameras-and-beyond/3572/26
"""


class HuntsmanSourceDetectionTask(SourceDetectionTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HuntsmanCharacterizeImageTask(CharacterizeImageTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        kwargs.pop("exposureIdInfo")
        return super().run(*args, **kwargs)


class HuntsmanCalibrateTask(CalibrateTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        kwargs.pop("exposureIdInfo")
        return super().run(*args, **kwargs)
