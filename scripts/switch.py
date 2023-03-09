import requests
import base64
import hashlib
import re
import sys
import os


CLIENT_ID = '5c38e31cd085304b'


class NintendoSwitch:

    def __init__(self, *, client_id=CLIENT_ID, session_token='') -> None:
        self.session = requests.Session()
        self.client_id = client_id
        self.ua = 'com.nintendo.znej/1.13.0 (Android/7.1.2)'

        self.session_token = session_token
        self.access_token = {}

    def log_in(self):
        """Logs in to a Nintendo Account and returns a session_token."""

        auth_code_verifier = base64.urlsafe_b64encode(os.urandom(32))
        auth_cv_hash = hashlib.sha256()
        auth_cv_hash.update(auth_code_verifier.replace(b"=", b""))
        auth_code_challenge = base64.urlsafe_b64encode(auth_cv_hash.digest())

        headers = {
            'Host': 'accounts.nintendo.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/94.0.4606.61 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8n',
            'DNT': '1',
            'Accept-Encoding': 'gzip,deflate,br',
        }
        params = {
            'state': '',
            'client_id': self.client_id,
            'redirect_uri': 'npf{}://auth'.format(self.client_id),
            'scope': 'openid user user.mii user.email user.links[].id',
            'response_type': 'session_token_code',
            'session_token_code_challenge': auth_code_challenge.replace(b"=", b""),
            'session_token_code_challenge_method': 'S256',
            'theme': 'login_form'
        }

        url = 'https://accounts.nintendo.com/connect/1.0.0/authorize'
        response = self.session.get(url, headers=headers, params=params, allow_redirects=False)
        print(f"""
Make sure you have fully read the \"Cookie generation\" section of the readme before proceeding.
To manually input a cookie instead, enter \"skip\" at the prompt below.
Navigate to this URL in your browser: {response.url}
Log in, right click the \"Select this account\" button, copy the link address, and paste it below:
        """)
        while True:
            try:
                user_account_url = input("")
                if user_account_url == "skip":
                    break
                session_token_code = re.search('de=(.*)&', user_account_url)
                self.get_session_token(session_token_code.group(1), auth_code_verifier)
                break
            except KeyboardInterrupt:
                print("Bye!")
                sys.exit(1)
            except AttributeError:
                print("Malformed URL. Please try again, or press Ctrl+C to exit.")
                print("URL:", end=' ')
            except KeyError:  # session_token not found
                print("The URL has expired. Please log out and back into your Nintendo Account and try again.")
                sys.exit(1)

    def get_session_token(self, session_token_code, auth_code_verifier):
        """Helper function for log_in()."""

        headers = {
            'User-Agent': self.ua,
            'Accept-Language': 'en-US',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'accounts.nintendo.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }

        body = {
            'client_id': self.client_id,
            'session_token_code': session_token_code,
            'session_token_code_verifier': auth_code_verifier.replace(b"=", b"")
        }

        url = 'https://accounts.nintendo.com/connect/1.0.0/api/session_token'

        response = self.session.post(url, headers=headers, data=body)
        self.session_token = response.json()["session_token"]
        print(f'Your session_token: {self.session_token}')

    def get_access_token(self):
        body = {
            "client_id": self.client_id,
            "session_token": self.session_token,
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer-session-token"
        }
        url = 'https://accounts.nintendo.com/connect/1.0.0/api/token'

        response = self.session.post(url, headers={'Content-Type': 'application/json'}, json=body)
        self.access_token = response.json()
        print(f'Your access_token: {self.access_token}')

    def get_history(self):
        authorization = "{} {}".format(
            self.access_token['token_type'],
            self.access_token['access_token']
        )
        url = 'https://mypage-api.entry.nintendo.co.jp/api/v1/users/me/play_histories'
        header = {
            'Authorization': authorization,
            'User-Agent': self.ua,
        }
        response = self.session.get(url, headers=header)
        return response


if __name__ == '__main__':
    ns = NintendoSwitch()
    ns.log_in()
    ns.get_access_token()

    r = ns.get_history()
    print(r.json())
