import sys
import settings
import subprocess

ls = settings.INSTALLED_APPS
data = ""

for app in ls:
    if app != "dashboards":
        data += "-i " + str(app) + " "

cmd = (
    "{} /usr/share/openstack-dashboard/manage.py collectstatic"
    " --noinput {}".format(sys.executable, data)
)

subprocess.call(cmd, shell=True)
