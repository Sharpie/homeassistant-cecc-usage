import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_HOST
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType

from .const import DOMAIN

class CeccUsageConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 1

    async def _validate_user_input(self, user_input: dict, errors: dict):
        try:
            vol.Match(r'\d+-\d+')(user_input[CONF_USERNAME])
        except vol.MatchInvalid:
            errors[CONF_USERNAME] = "invalid_account_number"

        try:
            vol.FqdnUrl()(user_input[CONF_HOST])
        except vol.UrlInvalid:
            errors[CONF_HOST] = 'invalid_selenium_url'

    async def async_step_user(self, user_input: dict|None =None) -> config_entries.FlowResult:
        errors = {}

        if user_input is not None:
            await self._validate_user_input(user_input, errors)

            if not errors:
                await self.async_set_unique_id(user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=user_input[CONF_USERNAME], data=user_input)

        user_schema = vol.Schema({vol.Required(CONF_USERNAME, default=(user_input or {}).get(CONF_USERNAME)):
                                      str,
                                  vol.Required(CONF_PASSWORD):
                                      TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD)),
                                  vol.Required(CONF_HOST, default=(user_input or {}).get(CONF_HOST,'http://4b5c1810-selenium-ff.local.hass.io:4444')):
                                      str})

        return self.async_show_form(step_id="user", data_schema=user_schema, errors=errors)

