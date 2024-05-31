class CarrollEccException(Exception):
    pass

class BrowserUnreachable(CarrollEccException):
    pass

class BrowserBadHost(CarrollEccException):
    pass

class BrowserBusy(CarrollEccException):
    pass

class InvalidLogin(CarrollEccException):
    pass
