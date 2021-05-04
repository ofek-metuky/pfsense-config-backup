import os

import dotenv

dotenv.load_dotenv()

username = os.getenv("pfsense_username")
password = os.getenv("pfsense_password")
base_url = os.getenv("pfsense_base_url")

_skip_backup_rrd_var = os.getenv("skip_backup_rrd", "yes").lower()
skip_backup_rrd = None if _skip_backup_rrd_var != "yes" else _skip_backup_rrd_var

verify_requests = False if os.getenv("verify_requests", "True").lower() == "false" else True
backups_path = os.getenv("backups_path")
