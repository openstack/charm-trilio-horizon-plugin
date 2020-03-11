# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = "workloads_admin"
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = "admin"
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = "backups-admin"
# Python panel class of the PANEL to be added.
ADD_PANEL = "dashboards.workloads_admin.panel.Workloads_admin"
ADD_INSTALLED_APPS = ["dashboards"]
DISABLED = False
