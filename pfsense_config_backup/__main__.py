import os
import time

from pfsense_config_backup.pfsense_client import PfsenseClient
from pfsense_config_backup import config


def _get_new_backup_path(backup_directory):
    return os.path.join(backup_directory, f"config_backup_{str(time.time())}.xml")


def main():
    with PfsenseClient(config.base_url, username=config.username, password=config.password,
                       verify_requests=config.verify_requests) as client:
        backup_data = client.get_current_backup(skip_backup_rrd=config.skip_backup_rrd)

    backup_path = _get_new_backup_path(config.backups_path)
    with open(backup_path, "w") as backup_file:
        backup_file.write(backup_data)


if __name__ == '__main__':
    main()
