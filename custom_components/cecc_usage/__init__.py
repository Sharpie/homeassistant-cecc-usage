from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "cecc_usage"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.states.async_set("cecc_usage.message", "hello, world.")

    return True
