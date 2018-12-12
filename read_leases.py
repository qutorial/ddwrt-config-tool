#!./venv/bin/python3

import json
from lease import Lease


def readLeases(leaseSettingsFile):
    with open(leaseSettingsFile) as f:
        leasesFileJson = json.load(f)

    lease_entries = leasesFileJson['static_leases']

    static_leases = []
    for static_lease in sorted(lease_entries):
        lease_dict = lease_entries[static_lease]
        static_leases.append(Lease(lease_dict))

    return static_leases
