from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .cecc import CarrollEccHass
from .coordinator import CarrollEccCoordinator
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntityCallback) -> bool:
    hass.data.setdefault(DOMAIN, {})

    cecc_api = CarrollEccHass(hass, entry.data)
    coordinator = CarrollEccCoordinator(hass, cecc_api)

    hass.data[DOMAIN][cecc_api.account] = coordinator

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])

    return True
