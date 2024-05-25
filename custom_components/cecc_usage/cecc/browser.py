from selenium import webdriver

class CarrollEccBrowser:
    def __init__(self, host_port, headless=True):
        self.host_port = host_port
        self.headless = headless

        self._browser = None

    def _init_browser(self):
        options = webdriver.FirefoxOptions()
        if self.headless:
            options.add_argument('--headless')

        connection = webdriver.remote.remote_connection.RemoteConnection(self.host_port)
        connection.set_timeout(15)

        browser = webdriver.Remote(command_executor = connection, options = options)
        browser.implicitly_wait(10)

        self._browser = browser

    def _close_browser(self):
        if self._browser is not None:
            self._browser.quit()
            self._browser = None

    def test_connection(self):
        try:
            self._init_browser()
        finally:
            self._close_browser()
