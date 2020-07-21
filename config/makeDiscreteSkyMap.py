"""
Config for the makeDiscreteSkyMapTask.
"""
# coadd name, e.g. deep, goodSeeing, chiSquared
config.coaddName='deep'

# dimensions of inner region of patches (x,y pixels)
config.skyMap.patchInnerDimensions=[10000, 10000]

# border between patch inner and outer bbox (pixels)
config.skyMap.patchBorder=100

# minimum overlap between adjacent sky tracts, on the sky (deg)
config.skyMap.tractOverlap=0.0
