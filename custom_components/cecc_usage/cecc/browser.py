from selenium import webdriver
from selenium.webdriver.common.by import By

class CarrollEccBrowser:
    LOGIN_PAGE = 'https://myaccount.carrollecc.com/onlineportal/Customer-Login'

    def __init__(self, host_port, username, password, headless=True):
        self.host_port = host_port
        self.username = username
        self.password = password
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

    def _login(self):
        browser = self._browser

        browser.get(self.LOGIN_PAGE)

        username = browser.find_element(By.ID, 'txtUsername')
        password = browser.find_element(By.ID, 'txtPassword')
        submit_login = browser.find_element(By.ID, 'dnn_ctr384_CustomerLogin_btnLogin')

        username.send_keys(self.username)
        password.send_keys(self.password)
        submit_login.click()

        browser.find_element(By.ID, 'dnn_ctr401_ContentPane')

    def test_connection(self):
        try:
            self._init_browser()
        finally:
            self._close_browser()

    def test_login(self):
        try:
            self._init_browser()
            self._login()
        finally:
            self._close_browser()
