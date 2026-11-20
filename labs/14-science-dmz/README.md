# Lab 14: Science DMZ and data transfer

[All labs](../../README.md) · [Notes](NOTES.md)

Fit: national labs · 10–12 GB. Moving big experiment data fast is central to network work at NERSC and ESnet.

![Bulk science data bypasses the enterprise firewall](diagram.svg)

- **Build:** an FRR WAN peer, a border router (cEOS or VyOS), an SR Linux Science DMZ switch with stateless ACLs, a VyOS or nftables firewall in front of a campus network, plus a DTN and a perfSONAR container.
- **DTN as a VM:** run the DTN, and the far-end transfer host, as small libvirt VMs bridged into the topology, not as containers. Containers share the host's kernel, and some of the TCP settings this lab tunes (the `net.core` buffer limits, the congestion-control modules) are host-wide, so a container DTN would change the host and couldn't be tuned independently of its peer.
- **Learn:** Science DMZ design, why stateful firewalls hurt bulk TCP, TCP tuning for long, fast paths, and measuring paths with perfSONAR.
- **Automation:** like [ESnet's fasterdata guidance](https://fasterdata.es.net/science-dmz/science-dmz-performance-monitoring/): a perfSONAR host running continuous latency and loss tests, plus periodic iperf3 tests via pScheduler. Here: pSConfig templates in git and Ansible for DTN tuning.

1. Add 60 ms of delay on the WAN link with `tc netem` to mimic a cross-country path.
2. Move a large file to the DTN with default TCP settings, then with larger buffers and BBR; compare.
3. Send the same transfer through the firewall path and compare throughput.
4. Schedule perfSONAR tests, then add loss to the path and see what they catch.

**Verify:** one check per exercise, same numbers; load the helpers first with `source ../../shared/verify.sh lab14` (see [verifying a lab](../../docs/verify.md)). `dtn` and `far` are the two VMs; reach them with `ssh`.

1. `on wan tc qdisc show dev eth1` shows `netem delay 60ms`, and `ssh far ping -c 3 $DTN_IP` reports a round trip of about 60 ms.
2. `ssh dtn sysctl net.ipv4.tcp_congestion_control net.core.rmem_max` shows the tuned values, and `ssh far iperf3 -c $DTN_IP -t 30` gives the throughput. `NOTES.md` has it for default and tuned settings, and the tuned figure is higher.
3. `ssh far traceroute -n $CAMPUS_IP` lists the firewall as a hop, and the DTN path does not. `NOTES.md` has both throughputs, with the firewall path lower.
4. `on perfsonar pscheduler schedule` lists the recurring tests and their runs. After you add loss with netem, the next loss test's result reports it.

**Published labs:** the University of South Carolina's [perfSONAR 5 lab library](https://research.cec.sc.edu/files/cyberinfra/files/End-to-end%20monitoring%20with%20perfSONAR%2C%20NETLAB%20platform.pdf) runs perfSONAR in Docker over Mininet topologies, on hosted pods offered at its [Science DMZ workshops](https://research.cec.sc.edu/cyberinfra/dmz-p4-dpdk-workshop) with EPOC. Its labs cover pScheduler, pSConfig templates and Grafana dashboards. **Differs:** Mininet switches are generic; this lab uses real NOS images for the border, the DMZ switch and the firewall, so ACLs and the firewall path behave like production gear. Their pSConfig and Grafana exercises slot into exercise 4.
