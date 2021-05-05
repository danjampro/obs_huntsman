""" Huntsman overrides for ProcessCcdTask.

ProcessCcd runs a lot of subtasks, but they are split into three broad sections:
- ISR (instrument signature removal);
- Image Characterisation (background subtraction, PSF modelling, CR repair);
- Image Calibration (astrometric and photometric calibration).
"""
import os.path
from lsst.utils import getPackageDir

from huntsman.drp.lsst.tasks.characterizeImage import HuntsmanCharacterizeImageTask

configDir = os.path.join(getPackageDir("obs_huntsman"), "config")

# ~~~~~ ISR subtask ~~~~

config.isr.load(os.path.join(configDir, "isr.py"))
config.isr.doBias = True
config.isr.doFlat = True
config.isr.doDark = True

# ~~~~~ Characterise image subtask ~~~~

# Load default config
config.charImage.load(os.path.join(configDir, "characterise.py"))

# Retarget this subtask to use Huntsman override
config.charImage.retarget(HuntsmanCharacterizeImageTask)

# Yes we want the outputs to be written to file
config.charImage.doWrite = True
config.charImage.doWriteExposure = False

# ~~~~~ Calibrate subtask ~~~~

config.doCalibrate = True
config.calibrate.load(os.path.join(configDir, "calibrate.py"))
