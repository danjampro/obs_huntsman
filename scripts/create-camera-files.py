""" Script to create the FITS tables describing each camera, located in the camera directory.
Useful links:
https://pipelines.lsst.io/modules/lsst.afw.cameraGeom/cameraGeom.html
https://github.com/lsst/obs_lsstSim/blob/86d1dc5cd3953c6b359c3f5e9ab69ae0c075f781/bin.src/makeLsstCameraRepository.py
"""
import os
import numpy as np
from contextlib import suppress

import lsst.afw.table as afwTable
import lsst.geom as lsstGeom
from lsst.afw import cameraGeom
from lsst.utils import getPackageDir


PRESETS = {"zwo": {'width': 5496, 'height': 3672, 'saturation': 4095, 'gain': 1.145,
                   'readNoise': 2.4}}

CAMERAS = {"1815420013090900": {"preset": "zwo"},
           "371d420013090900": {"preset": "zwo"},
           "0e2c420013090900": {"preset": "zwo"},
           "0f1d420013090900": {"preset": "zwo"},
           "361d420013090900": {"preset": "zwo"},
           "3528420013090900": {"preset": "zwo"},
           "370d420013090900": {"preset": "zwo"},
           "1919420013090900": {"preset": "zwo"},
           "2d194b0013090900": {"preset": "zwo"},
           "2014420013090900": {"preset": "zwo"},
           "testingcam00": {"preset": "zwo", "width": 100, "height": 100},
           "testingcam01": {"preset": "zwo", "width": 500, "height": 500}}

# TODO: Move camera config to a config file


def get_camera_config(camera_name):
    """ Load the camera config using the camera name as a key, loading the presets. """
    config = {}
    with suppress(KeyError):
        preset = CAMERAS[camera_name]["preset"]
        config.update(PRESETS[preset])
    for key, value in CAMERAS[camera_name].items():
        if key != "preset":
            config[key] = value
    return config


def make_amplifier(name, readNoise, gain, width, height, saturation, overscan):
    """ Make an "amplifier" object. In LSST, a single detector can be comprised of multiple
    amplifiers. This is not the case for Huntsman.
    """
    if overscan != 0:
        raise NotImplementedError("Non-zero overscan not yet implemented.")

    amplifier = cameraGeom.Amplifier.Builder()

    bbox = lsstGeom.Box2I(lsstGeom.Point2I(0, 0), lsstGeom.Extent2I(width, height))

    readoutCorner = cameraGeom.ReadoutCorner.LR   # <----------- TODO: check this
    linearityCoeffs = (1.0, np.nan, np.nan, np.nan)
    linearityType = "None"
    rawBBox = lsstGeom.Box2I(lsstGeom.Point2I(0, 0), lsstGeom.Extent2I(width, height))
    rawXYOffset = lsstGeom.Extent2I(0, 0)
    rawDataBBox = lsstGeom.Box2I(lsstGeom.Point2I(0, 0), lsstGeom.Extent2I(width, height))
    rawHorizontalOverscanBBox = lsstGeom.Box2I(lsstGeom.Point2I(0, 0),
                                               lsstGeom.Extent2I(width, height))
    emptyBox = lsstGeom.BoxI()

    amplifier.setRawFlipX(False)
    amplifier.setRawFlipY(False)
    amplifier.setBBox(bbox)
    amplifier.setName(name)
    amplifier.setGain(gain)
    amplifier.setSaturation(saturation)
    amplifier.setReadNoise(readNoise)
    amplifier.setReadoutCorner(readoutCorner)
    amplifier.setLinearityCoeffs(linearityCoeffs)
    amplifier.setLinearityType(linearityType)
    amplifier.setRawBBox(rawBBox)
    amplifier.setRawXYOffset(rawXYOffset)
    amplifier.setRawDataBBox(rawDataBBox)
    amplifier.setRawHorizontalOverscanBBox(rawHorizontalOverscanBBox)
    amplifier.setRawVerticalOverscanBBox(emptyBox)
    amplifier.setRawPrescanBBox(emptyBox)

    return amplifier


def make_camera(camera_name, **kwargs):
    """ Make a camera (a detectorTable object), which can in principle contain multiple amplifiers.
    Huntsman's cameras only have one amplifier per camera.
    """
    amplifier = make_amplifier(**kwargs)

    # Create detectorTable (can add more than one CCD here later)
    protoTypeSchema = cameraGeom.Amplifier.getRecordSchema()
    detectorTable = afwTable.BaseCatalog(protoTypeSchema)

    record = detectorTable.makeRecord()
    tempAmp = amplifier.finish()
    tempAmp.toRecord(record)
    detectorTable.append(record)

    # Write the detector to file
    fname = os.path.join(getPackageDir("obs_huntsman"), 'camera', f'{camera_name}.fits')
    return detectorTable.writeFits(fname)


if __name__ == "__main__":

    for camera_name in CAMERAS.keys():
        make_camera(camera_name, **get_camera_config(camera_name))
