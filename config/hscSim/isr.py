# Configuration for HSC ISR

from lsst.obs.subaru.isr import SubaruIsrTask
root.isr.retarget(SubaruIsrTask)
from lsst.obs.subaru.crosstalk import CrosstalkTask
root.isr.crosstalk.retarget(CrosstalkTask)

root.isr.doBias = False # XXX For now
root.isr.doDark = False
root.isr.doWrite = False
root.isr.doCrosstalk = True
root.isr.doGuider = False

# These values from RHL's report on "HSC July Commissioning Data" (2013-08-23)
root.isr.crosstalk.coeffs.values = [
       0.0e-6, -125.0e-6, -149.0e-6, -156.0e-6,
    -124.0e-6,    0.0e-6, -132.0e-6, -157.0e-6,
    -171.0e-6, -134.0e-6,    0.0e-6, -153.0e-6,
    -157.0e-6, -151.0e-6, -137.0e-6,    0.0e-6,
       ]