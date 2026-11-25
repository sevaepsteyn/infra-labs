# Networking, Kubernetes and automation labs

Twenty-five hands-on labs, numbered 0 to 24, simplest first: Kubernetes itself, then Cilium, BGP fabrics, security, monitoring, and designs modeled on what national labs and frontier AI labs publish about their infrastructure. Everything runs on one x86 host with containerlab and kind.

Each lab has what to build, exercises and, where one exists, the closest published lab, plus a fit line: national labs, frontier AI labs (AI), or both. Labs 1 to 22 also have a design diagram.

## Start here

1. Build the host: [docs/host-setup.md](docs/host-setup.md).
2. Pick a short path below.
3. Work through each lab's README, and keep a dated log in its `NOTES.md`. Lab 0 is written out in full, with every command and file; the other labs are specs that say what to build and leave the building to you.
4. Confirm each exercise with the lab's **Verify** list; [docs/verify.md](docs/verify.md) explains the names and helper commands the checks use.

## Suggested path

Nobody needs all 25. Pick one short path to start; each is complete on its own, runs in order, and every one begins with labs 0 and 1.

| Short path | Labs | Peak RAM | What it gives you |
| --- | --- | --- | --- |
| Kubernetes essentials | 0, 1, 7 | about 6 GB | Kubernetes itself, a CNI with policy and flow visibility, admission control, RBAC and signed images. Kind only, so it also fits a free Codespace |
| Kubernetes networking | 0, 1, 2, 3, 6 | 13–15 GB | How a cluster joins a routed data center: BGP to the host, ECMP to service IPs, kube-proxy replacement, encryption, L7 policy |
| Operations | 0, 1, 2, 3, 9, 10, 11 | 16–18 GB | Running a fabric and cluster as one system: telemetry, alerting, measured failures, and changes tested in CI |
| AI lab sampler | 0, 1, 6, 7, 8, 12 | 13–15 GB | Cilium in depth, cluster security, tenant isolation and inference serving. Lab 6 needs lab 3's fabric; read lab 3 and deploy its topology without doing its exercises |
| National lab sampler | 0, 1, 2, 3, 14, 15 | 12–14 GB | BGP fabric basics, then a Science DMZ with data transfer tuning and Slurm beside Kubernetes |
| Fabric design and RDMA | 0, 1, 2, 3, 4, 5, 22 | 14–18 GB | The network under a training cluster: BGP fabrics, EVPN-VXLAN, three-tier fat-tree design, and lossless RoCE with its congestion control |

All six fit a host or VM with about 20 GB for labs. The first one is the place to start if the goal is Kubernetes itself and the networking can wait.

To go further, the full route is the core path and then branches by the kind of employer you are aiming at.

| Full route | Labs | What it gives you |
| --- | --- | --- |
| Core | 0, 1, 2, 3, 6, 7, 9, 11 | Kubernetes itself, Cilium, BGP to the host on a real fabric, cluster security, monitoring, and changes tested in CI |
| Either branch | 4, 5, 10, 13 | EVPN-VXLAN, fat-tree design and BGP at scale, measured failure practice, storage networking |
| AI labs | 8, 12, 16, 17, then 21, 22, 23, 24 | Tenant isolation, inference serving, cloud connectivity, node lifecycle, GPU fabrics, lossless RoCE, multi-cluster scheduling |
| National labs | 14, 15, then 18, 19, 20 | Science DMZ, Slurm beside Kubernetes, HPC-center network designs, WAN |

Dependencies outside the core: lab 5 needs 3, lab 8 needs 6 and 7 (their configuration, not the fabric), lab 10 needs 3 and 9, lab 23 needs 3 and 6, and lab 24 needs 21 and 23. Lab 22 stands alone but reads better after 5 and 21.

## Labs

Ordered simplest first. Each lab lists its fit and rough RAM, then a design diagram, what to build, exercises, and a check for each exercise.

| Lab | Title | Fit | RAM |
| --- | --- | --- | --- |
| 0 | [Kubernetes fundamentals](labs/00-fundamentals/README.md) | both | about 4 GB |
| 1 | [Kind and Cilium](labs/01-kind-cilium/README.md) | both | about 4 GB |
| 2 | [One router and kind](labs/02-one-router/README.md) | both | about 5 GB |
| 3 | [Leaf-spine with Cilium BGP](labs/03-leaf-spine/README.md) | both | 12–14 GB |
| 4 | [EVPN-VXLAN fabric](labs/04-evpn-vxlan/README.md) | both | 14–18 GB |
| 5 | [Fat-tree design and BGP at scale](labs/05-fat-tree-bgp/README.md) | both | about 6 GB |
| 6 | [Cilium in depth](labs/06-cilium-in-depth/README.md) | both | 13–15 GB |
| 7 | [Cluster security and supply chain](labs/07-cluster-security/README.md) | AI, useful for both | about 6 GB |
| 8 | [Multi-tenant isolation](labs/08-multi-tenant/README.md) | AI | about 8 GB |
| 9 | [Monitoring pipeline](labs/09-monitoring/README.md) | both | 16–18 GB |
| 10 | [Failure practice](labs/10-failure-practice/README.md) | both | 16–18 GB |
| 11 | [Network changes tested in CI](labs/11-network-ci/README.md) | both | 10–14 GB |
| 12 | [Inference serving](labs/12-inference-serving/README.md) | AI | about 12 GB |
| 13 | [Storage networking](labs/13-storage-networking/README.md) | both | 14–18 GB |
| 14 | [Science DMZ and data transfer](labs/14-science-dmz/README.md) | national labs | 10–12 GB |
| 15 | [Slurm and Kubernetes side by side](labs/15-slurm-k8s/README.md) | national labs | 10–12 GB |
| 16 | [Hybrid cloud connectivity](labs/16-hybrid-cloud/README.md) | AI | 4–6 GB locally plus a small cloud account |
| 17 | [Bare-metal node lifecycle](labs/17-node-lifecycle/README.md) | both | 16–20 GB |
| 18 | [Perlmutter-style network](labs/18-perlmutter/README.md) | national labs | 20–25 GB |
| 19 | [Multi-site WAN](labs/19-multi-site-wan/README.md) | national labs | 16–24 GB |
| 20 | [Doudna-style network](labs/20-doudna/README.md) | national labs | 22–26 GB |
| 21 | [GPU training cluster, two fabrics](labs/21-gpu-training-cluster/README.md) | AI | 24–26 GB |
| 22 | [Lossless Ethernet and RoCE congestion control](labs/22-lossless-roce/README.md) | AI, useful for both | about 6 GB |
| 23 | [Multi-cluster and multi-region](labs/23-multi-cluster/README.md) | AI | 16–20 GB |
| 24 | [Anthropic-style scheduling and fleet operations](labs/24-fleet-scheduling/README.md) | AI | 16–20 GB |

## Layout

| Path | What it holds |
| --- | --- |
| `docs/` | Host setup, image sourcing, verifying a lab, alternatives and published labs, sources |
| `host/` | Ansible playbook that builds the lab host |
| `shared/` | kind configs and Cilium Helm values reused across labs, and `verify.sh`, the helpers the checks use |
| `labs/NN-name/` | One folder per lab: `README.md` (the spec), `NOTES.md` (the log), `diagram.svg`, topology, configs and manifests |

Diagrams are hand-written SVG and are edited as text. For exact wiring, generate a graph from the topology file with `containerlab graph`.

## Not in this repo

Vendor images and licence files, kubeconfigs, Terraform state, cloud credentials and private keys are ignored by `.gitignore`. This repo is public: do not commit addresses or hostnames of real networks, and do not attach a self-hosted CI runner to it (see [host setup](docs/host-setup.md#automation)).

## License

[MIT](LICENSE). Copyright (c) 2026 Glivorem Technologies LLC.
