import os.path
from lsst.utils import getPackageDir

# Grab the path to this config directory
configDir = os.path.join(getPackageDir("obs_huntsman"), "config")

# Load ISR configurations
config.isr.load(os.path.join(configDir, "isr.py"))

# Make sure to subtract the bias, apply dark correction and mask bad pixels
config.isr.doBias = True
config.isr.doDark = True
config.isr.doDefect = True
