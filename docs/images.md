# Getting the images

Only some of the network operating systems can be pulled without an account, so sort out access before the lab that needs it. Terms change; check each vendor's current download page.

| Image | How to get it | First needed |
| --- | --- | --- |
| FRR | Public container image, pulled directly | Lab 2 |
| Nokia SR Linux | Public container image, pulled directly; no licence for the default chassis types | Lab 3 |
| Arista cEOS | Free arista.com account; download the archive and `docker import` it | Lab 3 (if chosen over SR Linux) |
| VyOS | No ready-made containerlab image; build a container from a rolling-release ISO | Lab 14 |
| Juniper vJunos-router | Juniper account; download the VM image and package it with vrnetlab | Lab 19 |
| Juniper cRPD | Juniper account; a licence or trial for some features | Lab 19 (instead of vJunos) |
| Cisco XRd | Cisco account with a software entitlement | Lab 19, lab 20 (optional) |

A path that needs no vendor account at all: SR Linux for every switch and FRR for every router, which covers every lab except the vendor-specific parts of lab 19.
