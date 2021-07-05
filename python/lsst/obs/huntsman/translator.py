""" The translator class is responsible for converting FITS header values into standardised
quantities understood by the LSST stack, as defined in the ObservationInfo class. """
import re

from astropy.time import Time
from astropy import units as u

from panoptes.utils.utils import get_quantity_value

from huntsman.drp.core import get_config
from huntsman.drp.utils.date import parse_date
from huntsman.drp.utils import header as header_utils

from astrometadata_translator.translator import cache_translation
from astro_metadata_translator.translators.fits import FitsTranslator


__all__ = ("HuntsmanTranslator", )


def _make_trivial_map_from_config():
    """ Return trivial mappings specified in the huntsman-drp config file.
    These are direct mappings between quantities and FITS headers.
    Returns:
        dict: Trivial mapping dict.
    """
    hunts_config = get_config()

    return hunts_config["fits_header"]["mappings"]


class HuntsmanTranslator(FitsTranslator):
    """Metadata translator for DECam standard headers.
    """
    name = "Huntsman"
    supported_instrument = "Huntsman"

    # Translator classes require trivial (direct) mappings to be defined at the class level
    # TODO: Implement units and "checker" functions (see base class documentation)
    _trivial_map = _make_trivial_map_from_config()

    # Constant mappings do not depend on the header
    _const_map = {"detector_group": "Huntsman"}

    # Translation methods

    @cache_translation
    def to_visit_id(self):
        """ Return the visit ID integer.
        ID of the Visit this Exposure is associated with.
        Returns:
            int: The visit ID.
        """
        date_obs = self._header['DATE-OBS']  # This is a string
        datestr = ''.join([s for s in date_obs if s.isdigit()])

        if len(datestr) != 17:
            raise ValueError("Date string expected to contain 17 numeric characters.")

        return int(datestr)

    # TODO
    @cache_translation
    def to_exposure_id(self):
        """ Calculate exposure ID.
        Unique (with instrument) integer identifier for this observation.
        Returns:
            int: ID of exposure.
        """
        return self.to_visit_id()

    # NOTE: We don't actually count exposures so this probably doesn't work properly
    @cache_translation
    def to_observation_counter(self):
        """ Return the lifetime exposure number.
        Counter of this observation. Can be counter within observing_day or a global counter.
        Returns:
            int: observation count.
        """
        return self.to_exposure_id()

    @cache_translation
    def to_datetime_begin(self):
        """ Calculate start time of observation.
        Returns:
            astropy.time.Time: Time corresponding to the start of the observation.
        """
        key = "DATE_OBS"
        date_begin = Time(parse_date(self._header[key]))
        self._used_these_cards(key)
        return date_begin

    @cache_translation
    def to_datetime_end(self):
        """ Calculate end time of observation.
        Returns:
            astropy.time.Time: Time corresponding to the end of the observation.
        """
        exptime = get_quantity_value(self.to_exposure_time(), u.second)
        return self.to_datetime_begin() + exptime

    @cache_translation
    def to_observation_type(self):
        """ Calculate the observation type.
        Returns:
            str: The observation type normalized to standard set (e.g. science, dark, bias).
        """
        obs_type, used_cards = header_utils.header_to_observation_type(self._header,
                                                                       get_used_cards=True)
        self._used_these_cards(*used_cards)
        return obs_type

    @cache_translation
    def to_location(self):
        """ Calculate the observatory location.
        Returns:
            astropy.coordinates.EarthLocation: An object representing the location of the telescope.
        """
        location, used_cards = header_utils.header_to_location(self._header, get_used_cards=True)
        self._used_these_cards(*used_cards)
        return location

    @cache_translation
    def to_tracking_radec(self):
        """ Requested RA/Dec to track.
        Returns:
            astropy.coordinates.SkyCoord: The ra dec object.
        """
        radec, used_cards = header_utils.header_to_radec(self._header, get_used_cards=True)
        self._used_these_cards(*used_cards)
        return radec

    @cache_translation
    def to_altaz_begin(self):
        """ Telescope boresight azimuth and elevation at start of observation.
        Returns:
            astropy.coordinates.AltAz: The alt az object.
        """
        radec, used_cards = header_utils.header_to_altaz(self._header, get_used_cards=True)
        self._used_these_cards(*used_cards)
        return radec

    # TODO: Check this
    @cache_translation
    def to_detector_exposure_id(self):
        """ Return a unique integer identifier for this detector in this exposure.
        Returns:
            int: The detector exposure ID.
        """
        exp_id = self.to_exposure_id()
        det_num = self.to_detector_num()
        return int(f"{exp_id}{det_num}")

    # Private methods

    # TODO: Do we need this? It was originally copied from the DEcam translator
    def _translate_from_calib_id(self, key):
        """ Get key value from the CALIB_ID header.
        Calibration products made with constructCalibs have some metadata saved in its FITS header
        CALIB_ID card.
        Args:
            key (str): The key to retrieve.
        Returns:
            str: The key value.
        """
        data = self._header["CALIB_ID"]
        match = re.search(r".*%s=(\S+)" % key, data)
        self._used_these_cards("CALIB_ID")
        return match.groups()[0]
