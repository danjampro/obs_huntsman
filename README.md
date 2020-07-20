# obs_huntsman

Huntsman-specific configuration and tasks for the LSST Data Management Stack

## Creating and ingesting the astrometry catalogue
```
# Prepare the reference catalogue in LSST format
python $OBS_HUNTSMAN/scripts/ingestSkyMapperReference.py

# Move the ingested catalogue into the desired repo's ref_cats directory
cd $LSST_HOME
mkdir DATA/ref_cats
ln -s testdata/ref_cats/skymapper_test/ref_cats/skymapper_dr3 DATA/ref_cats/
```
