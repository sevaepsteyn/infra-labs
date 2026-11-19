# Lab 0: Kubernetes fundamentals

[All labs](../../README.md) · [Notes](NOTES.md)

Fit: both · about 4 GB · kind only, with kind's default CNI. Every later lab assumes you can read and debug ordinary Kubernetes objects; this lab covers them before any networking product is added.

- **Build:** a 3-node kind cluster (1 control plane, 2 workers) with nothing changed, metrics-server, and one small web app with a database behind it.
- **Learn:** pods, Deployments and rollouts, Services and cluster DNS, ConfigMaps and Secrets, volumes and StatefulSets, requests, limits and probes, scheduling (node selectors, taints, affinity), namespaces and RBAC, and how the control plane and kubelet fit together.
- **Automation:** plain manifests in git under `labs/00-fundamentals/`, applied with `kubectl apply -k` (Kustomize). Helm starts in lab 1, once you know what a chart is generating.

1. Run a pod, then put it in a Deployment; scale it, roll out a new image, and roll it back.
2. Expose it with ClusterIP and NodePort Services; resolve the Service name from another pod and look at its EndpointSlices.
3. Feed the app a ConfigMap and a Secret; change each and see which changes need a pod restart.
4. Run the database as a StatefulSet with a PersistentVolumeClaim; delete the pod and confirm the data survives.
5. Add requests, limits, and liveness and readiness probes; fail a readiness probe and watch the pod leave the Service; exceed a memory limit and find the OOM kill.
6. Taint a worker, then use a toleration and a node selector to control where pods land; drain a node and watch pods move.
7. Create a namespace, a ServiceAccount and a Role that can only read pods; test it with `kubectl auth can-i`.
8. Break things and diagnose them with `kubectl describe`, `logs`, `events` and `debug`: a wrong image name, a failing probe, an unschedulable pod, a Service whose selector matches nothing.
9. Find where the control plane runs: list the static pods on the control-plane node, stop the kubelet on a worker with `docker exec`, and watch the node go NotReady.

**Published labs:** the official [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/) tutorial covers deploying, exposing, scaling and updating an app. The [iximiuz Kubernetes playground](https://labs.iximiuz.com/playgrounds/k8s-omni) gives a kubeadm cluster of real VMs in the browser. **Differs:** the tutorial stops before storage, scheduling, RBAC and debugging, which later labs lean on; this lab covers them on the same kind setup every later lab uses.
