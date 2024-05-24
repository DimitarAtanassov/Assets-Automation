import requests
import logging
import xml.etree.ElementTree as ET
import concurrent.futures
import time 
class Automator:
    
    qualys_username = ""                                # Enter Qualys Username        
    qualys_password = ""                    # Enter Qualys Password
    qualys_guard_url = "https://qualysapi.qg4.apps.qualys.com"   # Enter url 
    search_assets_url = "/qps/rest/2.0/search/am/asset"
    
    def __init__(self):
        self.session = self._session(self.qualys_username,self.qualys_password,self.qualys_guard_url)
        self.cookies = {}

    def _session(self,*args):
        requests.adapters.DEFAULT_POOLSIZE = 20
        session = requests.Session()
        session.auth = (args[0],args[1])
        session.headers.update({'X-Requested-With': 'SearchAssets-Automation-Script' })
        session.url = args[2]
        return session

    def _request(self,method, relative_path, log_id=None, login=False, logout=False, **kwargs):
        try:
            response = getattr(self.session, method)(self.qualys_guard_url + relative_path, **kwargs)
        except requests.exceptions.ConnectionError as errc:
            print(repr(errc))
            raise
        except requests.exceptions.Timeout as errt:
            print(repr(errt))
            raise
        except requests.exceptions.RequestException as err:
            print(repr(err))
            raise
        http_error_msg = ''
        if isinstance(response.reason, bytes):
            try:
                reason = response.reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = response.reason.decode('iso-8859-1')
        else:
            reason = response.reason
        if 400 <= response.status_code < 500:
            http_error_msg = u'%s Client Error: %s for url: %s' % (response.status_code, reason, response.url)

        elif 500 <= response.status_code < 600:
            http_error_msg = u'%s Server Error: %s for url: %s' % (response.status_code, reason, response.url)
        if http_error_msg:
            print(http_error_msg)
            return False
        return response
        
    def _create_session(self, log_id, **params):
        logging.info("Creating a session")
        params = {'action': 'login', 'username': self.session.auth[0], 'password': self.session.auth[1]}
        response = self._request('post', '/api/2.0/fo/session/', data=params, log_id=log_id, login=True)
        if response is None or response is False:
            return False
        raw_session_key = dict(response.headers)['Set-Cookie']
        split_key = raw_session_key.split(';')
        session_key, session_val = split_key[0].split('=')
        self.cookies = {session_key: session_val}
        logging.info("Session Created")
        return True
    
    def _close_session(self, log_id, **params):
        print("Closing the session")
        if self.cookies == {}:
             print('Qualys session is already closed.')
             return
        params = {'action': 'logout'}
        response = self._request('post','/api/2.0/fo/session/', data=params, cookies=self.cookies, log_id = log_id, logout = True)
        print("Session closed")
        return

    def get_all_assets(self):
        total_asset_count = int(input("Enter asset count: "))  # Manually set the total asset count
        tag_name = "MS Azure Running Systems"
        batch_size = 100  # 100 = API Limit
        all_assets = []

        def fetch_assets(offset):
            payload = f"""
            <ServiceRequest>
                <filters>
                    <Criteria field="tagName" operator="EQUALS">{tag_name}</Criteria>
                </filters>
                <preferences>
                    <startFromOffset>{offset}</startFromOffset>
                    <limit>{batch_size}</limit>
                </preferences>
            </ServiceRequest>
            """
            api_response = self._request('post', self.search_assets_url, data=payload, headers={'Content-Type': 'text/xml'})
            if api_response is None or api_response.status_code != 200:
                print("Failed to retrieve assets")
                return None
            response_data = ET.fromstring(api_response.text)
            response_code = response_data.find('.//responseCode').text
            if response_code != 'SUCCESS':
                print(f"API request failed with response code: {response_code}")
                return None
            assets = response_data.findall('.//Asset')
            return assets

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for offset in range(1, total_asset_count + 1, batch_size):
                futures.append(executor.submit(fetch_assets, offset))
                time.sleep(1)  # 1-second delay between API calls

            for future in concurrent.futures.as_completed(futures):
                assets = future.result()
                if assets:
                    all_assets.extend(assets)

        print(f"Total assets retrieved: {len(all_assets)}")
        return all_assets