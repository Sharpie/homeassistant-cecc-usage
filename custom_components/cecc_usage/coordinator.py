from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .cecc import CarrollEccHass
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class CarrollEccCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, cecc_api: CarrollEccHass):
        super().__init__(hass, _LOGGER, name="Carroll Electric", update_interval=timedelta(days=1))
        self.cecc_api = cecc_api
        self.update_method = cecc_api.get_last_daily_usage
