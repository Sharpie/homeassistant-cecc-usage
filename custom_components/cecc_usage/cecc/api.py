import requests

from datetime import date, datetime
from http.cookiejar import CookieJar
from itertools import groupby
from operator import itemgetter

class CarrollEccAPI:
    DAILY_USAGE_URL = 'https://myaccount.carrollecc.com/onlineportal/DesktopModules/MeterUsage/API/MeterData.aspx/GetDailyUsageData'

    def __init__(self, acct_num: str, cookie_jar: CookieJar):
        self.acct_num = acct_num
        # Leading part of the account number, as an eight-digit
        # zero padded string.
        self._keymbr = '%08i' % int(acct_num.split('-')[0])
        self.cookie_jar = cookie_jar

    def get_raw_daily_usage(self, start: date, end: date|None=None) -> dict:
        if end is None:
            # Default to 1 day of data.
            end = start

        with requests.Session() as s:
            s.cookies = self.cookie_jar

            response = s.post(self.DAILY_USAGE_URL,
                              headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                              json={'MemberSep': self.acct_num,
                                    'keymbr': self._keymbr,
                                    'StartDate': start.strftime('%m/%d/%Y'),
                                    'EndDate': end.strftime('%m/%d/%Y'),
                                    'IsEnergy': 'false',
                                    'IsPPM': 'false',
                                    'IsCostEnable': '3'})

            response.raise_for_status()

            return response.json()

    def get_daily_usage(self, start: date, end: date|None=None) -> dict:
        raw_data = self.get_raw_daily_usage(start, end)
        readings = []

        for i, v in enumerate(raw_data['d']['Items']):
            try:
                total_kwh = int(v['ENDREADING'])
            except (TypeError, ValueError):
                # Reading not available yet
                continue

            readings.append({'meter_id': raw_data['d']['DyExports'][i]['METER'],
                             'date': datetime.strptime(v['DAILYTIMESTAMPFORMAT'], '%m/%d/%Y').date(),
                             'total_kwh': total_kwh,
                             'daily_usage_kwh': int(v['TOTALENERGY']),
                             'daily_cost': float(v['Cost'])})

        return {meter: sorted(readings, key=itemgetter('date'), reverse=True)
                for meter, readings in groupby(readings, itemgetter('meter_id'))}
