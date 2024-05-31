from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_HOST

from .browser import CarrollEccBrowser

class CarrollEccHass:
    """Bridge between HomeAssistant and Carroll Electric APIs"""

    def __init__(self, hass: HomeAssistant, cecc_config: dict):
        self.hass = hass
        self.account = cecc_config[CONF_USERNAME]
        self.password = cecc_config[CONF_PASSWORD]
        self.selenium_host = cecc_config[CONF_HOST]

    def _get_browser(self):
        return CarrollEccBrowser(self.selenium_host, self.account, self.password)

    async def test_connection(self):
        test_browser = self._get_browser()

        await self.hass.async_add_executor_job(test_browser.test_connection)

    async def test_login(self):
        test_browser = self._get_browser()

        await self.hass.async_add_executor_job(test_browser.test_login)
