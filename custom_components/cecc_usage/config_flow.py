import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType

from .const import DOMAIN

USER_SCHEMA = vol.Schema({vol.Required(CONF_USERNAME): str,
                          vol.Required(CONF_PASSWORD):
                              TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD))})

class CeccUsageConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 1

    async def _validate_user_input(self, user_input: dict, errors: dict):
        try:
            vol.Match(r'\d+-\d+')(user_input[CONF_USERNAME])
        except vol.MatchInvalid:
            errors[CONF_USERNAME] = "invalid_account_number"

    async def async_step_user(self, user_input: dict|None =None) -> config_entries.FlowResult:
        errors = {}

        if user_input is not None:
            await self._validate_user_input(user_input, errors)

            if not errors:
                return self.async_create_entry(title=user_input[CONF_USERNAME], data=user_input)

        return self.async_show_form(step_id="user", data_schema=USER_SCHEMA, errors=errors)

