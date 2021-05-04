import os
import time

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from pfsense_config_backup import config

BACKUP_DIALOG_PAGE_NAME = "diag_backup.php"


def _extract_csrf_from_html(html_data: str) -> str:
    parsed_data = BeautifulSoup(html_data, "html")
    csrf_tag: Tag
    csrf_tag = parsed_data.find_all("input", attrs=dict(name='__csrf_magic'))[0]
    return csrf_tag.attrs["value"]


class PfsenseClient:
    def __init__(self, base_url, username, password, *, verify_requests=True):
        self._base_url = base_url
        self._username = username
        self._password = password
        self._verify = verify_requests
        self._session = requests.session()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def __del__(self):
        self._session.close()

    @property
    def _backup_dialog_url(self):
        return self._base_url + BACKUP_DIALOG_PAGE_NAME

    def _fetch_csrf(self, fetch_url=None) -> str:
        if not fetch_url:
            fetch_url = self._base_url

        response = self._session.get(fetch_url, verify=self._verify)
        response.raise_for_status()

        return _extract_csrf_from_html(response.text)

    def login(self):
        csrf_token = self._fetch_csrf()
        response = self._session.post(self._base_url, verify=self._verify,
                                      data=dict(login="Login",
                                                __csrf_magic=csrf_token,
                                                usernamefld=self._username,
                                                passwordfld=self._password))
        response.raise_for_status()

    def get_current_backup(self, *, skip_rrd_backup_field="yes"):
        csrf_token = self._fetch_csrf(fetch_url=self._backup_dialog_url)
        response = self._session.post(self._backup_dialog_url, verify=self._verify,
                                      data=dict(download="download",
                                                donotbackuprrd=skip_rrd_backup_field,
                                                __csrf_magic=csrf_token))
        response.raise_for_status()
        return response.text


def _get_new_backup_path(backup_directory):
    return os.path.join(backup_directory, f"config_backup_{str(time.time())}.xml")


def main():
    with PfsenseClient(config.base_url, username=config.username, password=config.password,
                       verify_requests=config.verify_requests) as client:
        backup_data = client.get_current_backup(skip_rrd_backup_field=config.skip_backup_rrd)

    backup_path = _get_new_backup_path(config.backups_path)
    with open(backup_path, "w") as backup_file:
        backup_file.write(backup_data)


if __name__ == '__main__':
    main()
