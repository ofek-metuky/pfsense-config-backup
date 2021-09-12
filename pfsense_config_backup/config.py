import os

import dotenv

dotenv.load_dotenv()

username = os.getenv("pfsense_username")
password = os.getenv("pfsense_password")
base_url = os.getenv("pfsense_base_url")

skip_backup_rrd = True if os.getenv("skip_backup_rrd", "true").lower() == "true" else False

verify_requests = False if os.getenv("verify_requests", "true").lower() == "false" else True
backups_path = os.getenv("backups_path")
