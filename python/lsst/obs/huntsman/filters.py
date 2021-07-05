"""
- lambdaMin and lambdaMax are chosen to be where the filter rises above 1%
- physical_filter specifies names of individual filters, e.g. g2_8
- abstract_filter is the generic name of the filter e.g. "g", "r" etc.
"""
from lsst.obs.base import FilterDefinition, FilterDefinitionCollection

# Note that these aren't the proper measurements, just guesses for now.
# TODO: Update!

HUNTSMAN_FILTER_DEFINITIONS = FilterDefinitionCollection(
    FilterDefinition(physical_filter="g2_8",        # Retained for testing purposes
                     band="g_band",
                     lambdaEff=550, lambdaMin=500, lambdaMax=600),
    FilterDefinition(physical_filter="g_band",
                     band="g_band",
                     lambdaEff=550, lambdaMin=500, lambdaMax=600),
    FilterDefinition(physical_filter="r_band",
                     band="r_band",
                     lambdaEff=550, lambdaMin=500, lambdaMax=600),
    FilterDefinition(physical_filter="blank", band="blank",
                     lambdaEff=0.0,
                     alias={"no_filter", "blank"}),
    FilterDefinition(physical_filter="UNKNOWN", band="unknown",
                     lambdaEff=0.0,
                     alias={"unknown"})
)
