from lsst.pipe.tasks.characterizeImage import CharacterizeImageTask
from lsst.meas.algorithms.detection import SourceDetectionTask
from lsst.afw import table as afwTable

from huntsman.drp.core import get_logger
LOGGER = get_logger()


class HuntsmanSourceDetectionTask(SourceDetectionTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, table, exposure, doSmooth=True, sigma=None, clearMask=True, expId=None):

        results = self.detectFootprints(exposure=exposure, doSmooth=doSmooth, sigma=sigma,
                                        clearMask=clearMask, expId=expId)

        LOGGER.info(f"TO RESERVE: {results.numPos + results.numNeg}")
        # sources = afwTable.SourceCatalog(table)
        # sources.reserve(results.numPos + results.numNeg)

        results.numPos = 1000
        results.numNeg = 1000

        LOGGER.info("A")

        sources = afwTable.SourceCatalog(table)
        sources.reserve(results.numPos + results.numNeg)

        ll = dir(sources)
        for a in ll:
            LOGGER.info(a)

        results.positive.makeSources(sources)

        LOGGER.info("B")

        return super().run(table, exposure, doSmooth=True, sigma=None, clearMask=True, expId=None)


class HuntsmanCharacterizeImageTask(CharacterizeImageTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def runQuantum(self, butlerQC, inputRefs, outputRefs):

        dataId = butlerQC.quantum.dataId

        for key, value in dataId.items():
            LOGGER.info(f"{key} = {value}")

        return super().runQuantum(butlerQC, inputRefs, outputRefs)

    def run(self, *args, **kwargs):

        exposureIdInfo = kwargs.get("exposureIdInfo")
        LOGGER.info(f"{exposureIdInfo}")

        return super().run(*args, **kwargs)
