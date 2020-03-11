# Overview

This charm provides the TrilioVault Horizon plugin for the OpenStack Dashboard
and forms part of the [TrilioVault Cloud Backup solution][trilio.io].

# Usage

TrilioVault Horizon Plugin is a subordinate charm of openstack-dashboard
and relies on services from openstack-dashboard.

Steps to deploy the charm:

    juju deploy trilio-horizon-plugin
    juju deploy openstack-dashboard
    juju add-relation trilio-horizon-plugin openstack-dashboard

# Bugs

Please report bugs on [Launchpad][lp-bugs-charm-trilio-horizon-plugin].

[lp-bugs-charm-trilio-horizon-plugin]: https://bugs.launchpad.net/charm-trilio-horizon-plugin/+filebug
[trilio.io]: https://www.trilio.io/triliovault/openstack

