# Published labs, platforms and alternatives

## Published labs and online platforms

Seventeen of the 23 labs have a published lab or quickstart close enough to start from; each one's **Published labs** note names it and says how this doc's version differs, and why. Six have no close match: labs 6, 9, 12, 15, 17 and 19 (supply-chain security, chaos measurement, storage networking, hybrid cloud, and the two HPC-center designs).

The differences follow one pattern. Published labs teach one product or protocol on its own topology; these labs share lab 3's fabric and one git repo, add Kubernetes to the network labs and the network to the Kubernetes labs, and follow environments the target employers describe.

| Platform | Where it runs | Cost and limits | Labs it helps with |
| --- | --- | --- | --- |
| [Isovalent and Cilium labs](https://isovalent.com/resource-library/labs/) | Browser, guided, with quizzes and an exam | Free; [badges](https://www.credly.com/org/isovalent/badge/cilium-cluster-mesh) | 1, 2, 5, 7, 21 |
| [Containerlab in GitHub Codespaces](https://containerlab.dev/manual/codespaces/) | Browser or VS Code | 120 core-hours and 15 GB storage free a month; 2-core 8 GB or 4-core 16 GB machines by default | Labs needing 12 GB or less; a 4-core machine uses the free hours in 30 hours |
| [Arista Community Labs](https://aclabs.arista.com/) | Codespaces with Ansible, AVD and containerlab preinstalled | Codespaces quota; some labs need bigger machines [requested from GitHub](https://aclabs.arista.com/codespaces-quickstart) | 4, 10 |
| [Arista Test Drive automation labs](https://labguides.testdrive.arista.com/2025.3/automation/overview/) | Arista-hosted lab instance | Through Arista; the [AVD Playground](https://ansible-avd-forked.readthedocs.io/en/latest/ansible_collections/arista/avd/examples/dual-dc-l3ls/index.html) is for customers with a support contract | 4, 10 |
| [iximiuz Labs](https://labs.iximiuz.com/docs/playgrounds/what-are-playgrounds) | Firecracker microVMs, browser or `labctl` CLI | Free tier; [paid tier](https://labs.iximiuz.com/pricing/tinkerer) adds persistent playgrounds and bigger VMs | 0, 1, 14, and labs that need separate kernels |
| [NVIDIA Air](https://www.nvidia.com/en-us/networking/network-simulation) | NVIDIA's cloud | Free; Cumulus Linux, SONiC and NetQ | 4, 20 |
| [USC NETLAB pods](https://research.cec.sc.edu/cyberinfra/dmz-aug-2025) | Hosted, through USC's Science DMZ workshops | Access given to workshop attendees | 13 |

## Alternatives to the tools used

Each lab names one tool per job so the steps stay concrete; most jobs have a well-known substitute. Swap one when a target employer runs it, when it is lighter on RAM, or to compare two in the same lab.

| Job | Used here | Alternatives | When to switch |
| --- | --- | --- | --- |
| Switch NOS | SR Linux, cEOS | FRR (lightest), SONiC-VS, Juniper cRPD, Cisco XRd | FRR to save RAM; SONiC for open-NOS AI fabrics; cRPD instead of vJunos VMs (lab 18) |
| Router and firewall | VyOS, nftables | FRR plus nftables, OPNsense or pfSense VMs | A GUI firewall for lab 13's enterprise path |
| Topology generation | netlab, AVD | Jinja with Nornir, NetBox config templates | AVD only fits Arista; NetBox when it is already the source of truth |
| Local Kubernetes | kind | k3d, minikube, kubeadm or k3s on libvirt VMs, Talos | VMs when nodes need their own kernel (labs 5 and 16) |
| CNI and BGP to the host | Cilium | Calico (BGP through BIRD), MetalLB with FRR-K8s, kube-router | Calico is the other common bare-metal choice; MetalLB is what srl-k8s-anycast-lab uses |
| Multi-cluster | Cilium Cluster Mesh | Submariner, Istio multicluster, Kubernetes MCS API | When the clusters don't all run Cilium |
| Admission and policy | Kyverno | OPA Gatekeeper, built-in ValidatingAdmissionPolicy | Gatekeeper if a team writes Rego; built-in policy for simple rules |
| Image signing | cosign | Notation (Notary Project) | Notation where registries use it |
| Secrets | Vault, SOPS | OpenBao, External Secrets Operator, sealed-secrets | OpenBao is the open fork of Vault; External Secrets for cloud secret stores |
| Workload identity | SPIRE | Cilium mutual authentication, cert-manager with csi-driver-spiffe, Istio ambient | Cilium mTLS for fewer moving parts; Istio if the target runs a mesh |
| Switch telemetry | gnmic | Telegraf gNMI input, SNMP exporter, OpenTelemetry Collector | SNMP for gear without gNMI; Telegraf for InfluxDB shops |
| Metrics and logs | Prometheus, Grafana, Loki | VictoriaMetrics, Thanos or Mimir, OpenSearch | Thanos or Mimir for long retention across clusters |
| Chaos | Chaos Mesh, tc netem | LitmusChaos, Pumba | Litmus is the other CNCF chaos project |
| CI | GitHub Actions | GitLab CI, Jenkins, Tekton | Whatever the target team runs; the checks stay the same |
| Network tests | Batfish, pytest | ANTA, SuzieQ, pyATS | ANTA on cEOS; pyATS for Cisco |
| GitOps | Argo CD | Flux | Flux for a lighter, CLI-first setup |
| Inference gateway | Istio or agentgateway | NGINX Gateway Fabric, GKE Inference Gateway, Envoy Gateway (not in the guide; check its support first) | Stay on the guide's supported list |
| Model server | vLLM simulator, llama.cpp | vLLM CPU, Ollama, Triton | vLLM CPU only if you can spare 9.5 GB and 12 CPUs per replica |
| Storage | Rook-Ceph | Longhorn, OpenEBS | Longhorn is lighter but has no separate replication network to study |
| HPC scheduler on Kubernetes | Slinky slurm-operator | slurm-bridge, Soperator (Nebius), Volcano | slurm-bridge when Slurm stays outside Kubernetes |
| Batch queueing | Kueue, JobSet | Armada, Volcano, YuniKorn | Armada for G-Research-style multi-cluster queues |
| Bare-metal provisioning | Tinkerbell, Cluster API | Metal3, MAAS, Ironic | Metal3 is the OpenShift and CNCF route; MAAS for Ubuntu fleets |
| Controller framework | kopf, controller-runtime | Kubebuilder, Operator SDK, Metacontroller | Kubebuilder scaffolds a controller-runtime project |
| Infrastructure as code | Terraform, Atlantis | OpenTofu, Pulumi, Crossplane | OpenTofu is the open fork; Crossplane keeps cloud resources in Kubernetes |
| Workflows | Argo Workflows | Temporal | Temporal for long-running, code-first workflows |
| Network intent | NetBox, Workflow Orchestrator | Nautobot, Nornir alone | Nautobot is NetBox's fork with built-in jobs |
