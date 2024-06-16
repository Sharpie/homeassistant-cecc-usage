from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME
from homeassistant.helpers.entity import DeviceInfo
from homoeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntityCallback) -> bool:
    coordinator = hass.data[DOMAIN][entry.data[CONF_USERNAME]]

    entities = []
    for meter, _ in coordinator.data.items():
        device = DeviceInfo(identifiers={(DOMAIN, meter)},
                            name=f"Energy Meter {meter}",
                            manufacturer='Carroll Electric Cooperative')


    

