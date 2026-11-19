# Networking, Kubernetes and automation labs

Twenty-three hands-on labs, numbered 0 to 22, simplest first: Kubernetes itself, then Cilium, BGP fabrics, security, monitoring, and designs modeled on what national labs and frontier AI labs publish about their infrastructure. Everything runs on one x86 host with containerlab and kind.

Each lab has what to build, exercises and, where one exists, the closest published lab, plus a fit line: national labs, frontier AI labs (AI), or both. Labs 1 to 22 also have a design diagram.

## Start here

1. Build the host: [docs/host-setup.md](docs/host-setup.md).
2. Pick a short path below.
3. Work through each lab's README, and keep a dated log in its `NOTES.md`.

## Suggested path

Nobody needs all 23. Pick one short path to start; each is complete on its own, runs in order, and every one begins with labs 0 and 1.

| Short path | Labs | Peak RAM | What it gives you |
| --- | --- | --- | --- |
| Kubernetes essentials | 0, 1, 6 | about 6 GB | Kubernetes itself, a CNI with policy and flow visibility, admission control, RBAC and signed images. Kind only, so it also fits a free Codespace |
| Kubernetes networking | 0, 1, 2, 3, 5 | 13–15 GB | How a cluster joins a routed data center: BGP to the host, ECMP to service IPs, kube-proxy replacement, encryption, L7 policy |
| Operations | 0, 1, 2, 3, 8, 9, 10 | 16–18 GB | Running a fabric and cluster as one system: telemetry, alerting, measured failures, and changes tested in CI |
| AI lab sampler | 0, 1, 5, 6, 7, 11 | 13–15 GB | Cilium in depth, cluster security, tenant isolation and inference serving. Lab 5 needs lab 3's fabric; read lab 3 and deploy its topology without doing its exercises |
| National lab sampler | 0, 1, 2, 3, 13, 14 | 12–14 GB | BGP fabric basics, then a Science DMZ with data transfer tuning and Slurm beside Kubernetes |

All five fit a host or VM with about 20 GB for labs. The first one is the place to start if the goal is Kubernetes itself and the networking can wait.

To go further, the full route is the core path and then branches by the kind of employer you are aiming at.

| Full route | Labs | What it gives you |
| --- | --- | --- |
| Core | 0, 1, 2, 3, 5, 6, 8, 10 | Kubernetes itself, Cilium, BGP to the host on a real fabric, cluster security, monitoring, and changes tested in CI |
| Either branch | 4, 9, 12 | EVPN-VXLAN, measured failure practice, storage networking |
| AI labs | 7, 11, 15, 16, then 20, 21, 22 | Tenant isolation, inference serving, cloud connectivity, node lifecycle, GPU fabrics, multi-cluster scheduling |
| National labs | 13, 14, then 17, 18, 19 | Science DMZ, Slurm beside Kubernetes, HPC-center network designs, WAN |

Dependencies outside the core: lab 7 needs 5 and 6 (their configuration, not the fabric), lab 9 needs 3 and 8, lab 21 needs 3 and 5, and lab 22 needs 20 and 21.

## Labs

Ordered simplest first. Each lab lists its fit and rough RAM, then a design diagram, what to build, and exercises.

| Lab | Title | Fit | RAM | Status |
| --- | --- | --- | --- | --- |
| 0 | [Kubernetes fundamentals](labs/00-fundamentals/README.md) | both | about 4 GB | Not started |
| 1 | [Kind and Cilium](labs/01-kind-cilium/README.md) | both | about 4 GB | Not started |
| 2 | [One router and kind](labs/02-one-router/README.md) | both | about 5 GB | Not started |
| 3 | [Leaf-spine with Cilium BGP](labs/03-leaf-spine/README.md) | both | 12–14 GB | Not started |
| 4 | [EVPN-VXLAN fabric](labs/04-evpn-vxlan/README.md) | both | 14–18 GB | Not started |
| 5 | [Cilium in depth](labs/05-cilium-in-depth/README.md) | both | 13–15 GB | Not started |
| 6 | [Cluster security and supply chain](labs/06-cluster-security/README.md) | AI, useful for both | about 6 GB | Not started |
| 7 | [Multi-tenant isolation](labs/07-multi-tenant/README.md) | AI | about 8 GB | Not started |
| 8 | [Monitoring pipeline](labs/08-monitoring/README.md) | both | 16–18 GB | Not started |
| 9 | [Failure practice](labs/09-failure-practice/README.md) | both | 16–18 GB | Not started |
| 10 | [Network changes tested in CI](labs/10-network-ci/README.md) | both | 10–14 GB | Not started |
| 11 | [Inference serving](labs/11-inference-serving/README.md) | AI | about 12 GB | Not started |
| 12 | [Storage networking](labs/12-storage-networking/README.md) | both | 14–18 GB | Not started |
| 13 | [Science DMZ and data transfer](labs/13-science-dmz/README.md) | national labs | 10–12 GB | Not started |
| 14 | [Slurm and Kubernetes side by side](labs/14-slurm-k8s/README.md) | national labs | 10–12 GB | Not started |
| 15 | [Hybrid cloud connectivity](labs/15-hybrid-cloud/README.md) | AI | 4–6 GB locally plus a small cloud account | Not started |
| 16 | [Bare-metal node lifecycle](labs/16-node-lifecycle/README.md) | both | 16–20 GB | Not started |
| 17 | [Perlmutter-style network](labs/17-perlmutter/README.md) | national labs | 20–25 GB | Not started |
| 18 | [Multi-site WAN](labs/18-multi-site-wan/README.md) | national labs | 16–24 GB | Not started |
| 19 | [Doudna-style network](labs/19-doudna/README.md) | national labs | 22–26 GB | Not started |
| 20 | [GPU training cluster, two fabrics](labs/20-gpu-training-cluster/README.md) | AI | 24–26 GB | Not started |
| 21 | [Multi-cluster and multi-region](labs/21-multi-cluster/README.md) | AI | 16–20 GB | Not started |
| 22 | [Anthropic-style scheduling and fleet operations](labs/22-fleet-scheduling/README.md) | AI | 16–20 GB | Not started |

## Layout

| Path | What it holds |
| --- | --- |
| `docs/` | Host setup, image sourcing, alternatives and published labs, sources |
| `host/` | Ansible playbook and VM definition that build the lab host |
| `shared/` | kind configs and Cilium Helm values reused across labs |
| `labs/NN-name/` | One folder per lab: `README.md` (the spec), `NOTES.md` (the log), `diagram.svg`, topology, configs and manifests |

Diagrams are hand-written SVG and are edited as text. For exact wiring, generate a graph from the topology file with `containerlab graph`.

## Not in this repo

Vendor images and licence files, kubeconfigs, Terraform state, cloud credentials and private keys are ignored by `.gitignore`. This repo is public: do not commit addresses or hostnames of real networks, and do not attach a self-hosted CI runner to it (see [host setup](docs/host-setup.md#automation)).
