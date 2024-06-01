from selenium import webdriver
from selenium.webdriver.common.by import By
from http.cookiejar import Cookie, CookieJar

from urllib3.exceptions import MaxRetryError, ReadTimeoutError
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from .exceptions import BrowserUnreachable, BrowserBadHost, BrowserBusy, InvalidLogin

class CarrollEccBrowser:
    LOGIN_PAGE = 'https://myaccount.carrollecc.com/onlineportal/Customer-Login'
    USAGE_PAGE = 'https://myaccount.carrollecc.com/onlineportal/My-Account/Usage-History'

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

        try:
            browser = webdriver.Remote(command_executor = connection, options = options)
        except MaxRetryError as e:
            raise BrowserUnreachable from e
        except WebDriverException as e:
            raise BrowserBadHost from e
        except ReadTimeoutError as e:
            raise BrowserBusy from e

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

        try:
            browser.find_element(By.ID, 'dnn_ctr401_ContentPane')

            # Usage page goes through a short loading screen that appears to activate additional
            # cookie data. Likely related to fetching meter IDs.
            browser.get(self.USAGE_PAGE)
            # Wait for graph to load in
            browser.find_element(By.CSS_SELECTOR, 'svg')
        except NoSuchElementException as e:
            raise InvalidLogin from e

    def _convert_cookie(self, cookie_dict):
        return Cookie(
            version=0,
            name=cookie_dict['name'],
            value=cookie_dict['value'],
            # The port has to be 80 for some odd reason, even though this gets
            # used in HTTPS requests.
            port='80',
            port_specified=False,
            domain=cookie_dict['domain'],
            domain_specified=True,
            domain_initial_dot=False,
            path=cookie_dict['path'],
            path_specified=True,
            secure=cookie_dict['secure'],
            # Expiry may not always be set, get() returns None when absent.
            expires=cookie_dict.get('expiry'),
            discard=False,
            comment=None,
            comment_url=None,
            rest=None,
            rfc2109=False
        )

    def _extract_cookies(self):
        return [self._convert_cookie(cookie) for cookie in self._browser.get_cookies()]


    def test_connection(self):
        try:
            self._init_browser()
            self._login()
        finally:
            self._close_browser()

    def add_session_cookies(self, jar: CookieJar):
        try:
            self._init_browser()
            self._login()

            for cookie in self._extract_cookies():
                jar.set_cookie(cookie)
        finally:
            self._close_browser()
