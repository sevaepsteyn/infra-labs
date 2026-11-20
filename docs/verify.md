# Verifying a lab

Each lab's README ends its exercises with a **Verify** list: one check per exercise, with the same numbers. An exercise is done when its check gives the result described. A lab that is written out in full, as lab 0 is, puts a **Check** at the end of each exercise instead. Where an exercise is a measurement or a design on paper, the check is what must be written in the lab's `NOTES.md`.

The labs are specs, so the checks assume the names below. Use the same names when you write a lab's topology and manifests, or substitute your own in the commands.

## Names the checks assume

| Thing | Convention | Example |
| --- | --- | --- |
| containerlab topology name | `labNN` | `lab03`, so containers are `clab-lab03-leaf1` |
| A lab that reuses lab 3's fabric | lab 3's name | labs 6 and 9 to 13 use `lab03` |
| Switches and routers | role and number | `spine1`, `leaf1`, `border`, `client`, `wan` |
| kind cluster in a kind-only lab | `labNN` | node container `lab00-control-plane` |
| kind cluster wired into containerlab | node `k8s` | node containers `k8s-control-plane`, `k8s-worker` (no `clab-` prefix, so use `docker exec`) |
| Two clusters | `c1` and `c2` | kubectl contexts `kind-c1`, `kind-c2` |
| Test application | namespace `demo`, Deployment and Service `web` | `kubectl -n demo get svc web` |
| Addresses | shell variables you set | `SVC_IP`, `H2_IP`, `DTN_IP` |

## Helpers

Checks on containerlab nodes use the functions in [shared/verify.sh](../shared/verify.sh). Load them once per shell, with the topology name:

```sh
source shared/verify.sh lab03
```

| Helper | What it runs | Example |
| --- | --- | --- |
| `on` | A command inside a node | `on client curl -s http://$SVC_IP` |
| `srl` | An SR Linux CLI command | `srl leaf1 "show version"` |
| `eos` | A cEOS CLI command | `eos leaf1 "show version"` |
| `frr` | A vtysh command on FRR or VyOS | `frr client "show bgp summary"` |
| `xr` | A Cisco XRd CLI command | `xr p1 "show mpls forwarding"` |
| `cap` | tcpdump on a node's interface, from the host | `cap leaf1 -i e1-49 udp port 4789 -c 5` |
| `cil` | The Cilium agent's CLI | `cil status` |
| `svc_ip` | A LoadBalancer service's address | `SVC_IP=$(svc_ip demo web)` |

Checks that need Hubble assume `cilium hubble port-forward &` is running. Checks that query Prometheus assume `kubectl -n monitoring port-forward svc/prometheus-operated 9090 &`.

## SR Linux, cEOS and FRR equivalents

The checks are written for SR Linux, the image that needs no vendor account. On cEOS or FRR, use the matching command.

| Check | SR Linux (`srl`) | cEOS (`eos`) | FRR (`frr`) |
| --- | --- | --- | --- |
| BGP sessions | `show network-instance default protocols bgp neighbor` | `show ip bgp summary` | `show bgp summary` |
| One route | `show network-instance default route-table ipv4-unicast prefix 10.0.0.1/32` | `show ip route 10.0.0.1/32` | `show ip route 10.0.0.1/32` |
| EVPN routes of one type | `show network-instance default protocols bgp routes evpn route-type 2 summary` | `show bgp evpn route-type mac-ip` | `show bgp l2vpn evpn route type macip` |
| BFD sessions | `info from state bfd` | `show bfd peers` | `show bfd peers` |
| One interface | `show interface ethernet-1/1` | `show interfaces Ethernet1` | `show interface eth1` |
| LACP bundle | `show interface lag1` | `show lacp neighbor` | `cat /proc/net/bonding/bond0` (with `on`) |

A route in a tenant VRF uses the VRF's name in place of `default` on SR Linux, and `vrf NAME` on cEOS and FRR.

## What a check does not prove

The checks confirm that the thing an exercise asks for exists and behaves as intended. They don't grade the explanation an exercise asks for; write that in `NOTES.md`. Lab 0's checks were run on a real cluster. The others were written from each lab's spec and the tools' documented commands, before those labs had topology files, so expect to adjust an interface name or a label when you build one. When you do, fix the check in the README in the same commit.
