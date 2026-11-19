# Lab 6: Cilium in depth

[All labs](../../README.md) · [Notes](NOTES.md)

Fit: both · 13–15 GB · builds on lab 3. This covers most of what interviewers ask about Cilium.

![Cilium replaces kube-proxy, encrypts node to node, and pins egress](diagram.svg)

- **Build:** reinstall Cilium on lab 3 with kube-proxy replacement and native routing, then turn on WireGuard encryption, an L7 policy and an egress gateway node, with a test external service behind lab 3's border leaf.
- **Learn:** how eBPF replaces kube-proxy, native routing vs VXLAN tunnels, identity-based and L7 policy, the cost of encryption, and fixed egress IPs for outside firewalls.
- **Automation:** like [Celonis](https://www.cncf.io/case-studies/celonis/), which runs L7 and FQDN policy, Cluster Mesh, Hubble and WireGuard across 150+ clusters (deployment tooling not published). Here: Argo CD syncing Cilium Helm values and policies from git.

1. Confirm there are no kube-proxy iptables rules and services still work.
2. Switch between native routing and VXLAN; compare MTU, packet captures and the BGP routes.
3. Write an L7 policy that allows only `GET /health` from frontend to backend.
4. Enable WireGuard and check in Edgeshark that node-to-node traffic is encrypted.
5. Send one namespace's outbound traffic through the egress gateway and check the source IP the external service sees.

**Extend:** add Tetragon for eBPF runtime security, and alert when a pod runs an unexpected binary or opens an unexpected connection.

**Published labs:** Isovalent's browser labs cover each feature alone: [Advanced BGP Features](https://isovalent.com/labs/cilium-bgp-advanced) (timers, graceful restart, MD5), the [Cloud Network Engineer discovery lab](https://isovalent.com/labs/discovery-cloud-network-engineer) (dual stack, BGP, LB-IPAM, egress gateway), and, for Extend, [Getting Started with Tetragon](https://isovalent.com/labs/tetragon-getting-started), whose free badge has you install Tetragon on kind and trace a lateral attack. **Differs:** each runs one feature on a fresh cluster. Here they run together on lab 3's routed fabric, so native routing depends on real BGP routes and the combined MTU and policy effects show up in captures. Do their labs first for the feature, then this one for the interactions.
