from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, CONF_HOST

from datetime import date, timedelta
from http.cookiejar import CookieJar

from .api import CarrollEccAPI
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

    async def get_last_daily_usage(self):
        jar = CookieJar()
        today = date.today()

        def open_cecc_session():
            browser = self._get_browser()
            browser.add_session_cookies(jar)

        await self.hass.async_add_executor_job(open_cecc_session)

        def get_cecc_data():
            api = CarrollEccAPI(self.account, jar)
            usage = api.get_daily_usage(today, today - timedelta(days=3))

            return {meter: readings[0] for meter, readings in usage.items()}

        return await self.hass.async_add_executor_job(get_cecc_data)
