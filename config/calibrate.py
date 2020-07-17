'''
Override the default calibrate config parameters by putting them in here.
e.g.:
config.doAstrometry = False

Useful info for photocal:
https://community.lsst.org/t/reference-catalogs-camfluxes-and-colorterms/3578
https://community.lsst.org/t/pan-starrs-reference-catalog-in-lsst-format/1572
http://doxygen.lsst.codes/stack/doxygen/x_11_0/load_reference_objects_8py_source.html
'''
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask

REFCAT = "ps1_pv3_3pi_20170110_GmagLT19"

config.astromRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.astromRefObjLoader.ref_dataset_name = REFCAT
config.photoRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.photoRefObjLoader.ref_dataset_name = REFCAT
config.photoCal.photoCatName = REFCAT
config.connections.astromRefCat = REFCAT
config.connections.photoRefCat = REFCAT

config.doPhotoCal = False
config.doAstrometry = True
