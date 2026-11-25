# Lab 0: Kubernetes fundamentals

[All labs](../../README.md) · [Notes](NOTES.md)

Fit: both · about 4 GB · kind only, with kind's default CNI. Every later lab assumes you can read and debug ordinary Kubernetes objects; this lab covers them before any networking product is added.

- **Build:** a 3-node kind cluster (1 control plane, 2 workers) with nothing changed, metrics-server, and one small web app with a Redis database behind it.
- **Learn:** pods, Deployments and rollouts, Services and cluster DNS, ConfigMaps and Secrets, volumes and StatefulSets, requests, limits and probes, scheduling (node selectors, taints, affinity), namespaces and RBAC, and how the control plane and kubelet fit together.
- **Automation:** plain manifests in git, applied with `kubectl apply -k` (Kustomize). Helm starts in lab 1, once you know what a chart is generating.

This lab is written out in full: every command is here, and every file the commands use is in this folder. Each exercise ends with a **Check** that says what you should see.

## What is in this folder

| Path | What it holds |
| --- | --- |
| [`kind.yaml`](kind.yaml) | The cluster: one control plane and two workers |
| [`metrics-server/`](metrics-server/) | metrics-server, with the one flag kind needs |
| [`01-deployment/`](01-deployment/) to [`06-scheduling/`](06-scheduling/) | One Kustomize folder per exercise. Each includes the one before it and adds or patches something, so `kubectl apply -k` on a folder gives the state for that exercise |
| [`01-deployment/app.py`](01-deployment/app.py) | The web app: a page with a visit counter, about 100 lines of Python with no dependencies |
| [`07-rbac/`](07-rbac/) | A namespace, a ServiceAccount and a Role |
| [`08-broken/`](08-broken/) | Four workloads, each with one fault to find |

The app reaches its pods as a ConfigMap mounted over a stock `python` image, so there is no image to build. Read [`01-deployment/kustomization.yaml`](01-deployment/kustomization.yaml) and [`web-deployment.yaml`](01-deployment/web-deployment.yaml) before you start; they are short.

## Before you start

Run everything from this folder.

Files: [kind.yaml](kind.yaml) · [metrics-server/kustomization.yaml](metrics-server/kustomization.yaml)

```sh
cd labs/00-fundamentals
kind create cluster --config kind.yaml
kubectl get nodes
kubectl apply -k metrics-server
```

`kind create cluster` switches your kubectl context to `kind-lab00`. To go back to another cluster later, use `kubectl config use-context NAME`.

**Check:** `kubectl get nodes` shows `lab00-control-plane`, `lab00-worker` and `lab00-worker2`, all `Ready`. After a minute, `kubectl top nodes` prints CPU and memory for each.

## 1. Pod, Deployment, rollout

Run a single pod, look at it, and delete it. Nothing brings it back.

```sh
kubectl run hello --image=nginx:1.27-alpine
kubectl get pod hello -o wide
kubectl describe pod hello
kubectl delete pod hello
```

Now run the app as a Deployment, which keeps a set number of pods running.

Files: [01-deployment/kustomization.yaml](01-deployment/kustomization.yaml) · [01-deployment/namespace.yaml](01-deployment/namespace.yaml) · [01-deployment/web-deployment.yaml](01-deployment/web-deployment.yaml) · [01-deployment/app.py](01-deployment/app.py)

```sh
kubectl apply -k 01-deployment
kubectl -n demo rollout status deploy/web
kubectl -n demo get deploy,replicaset,pods -o wide
```

Delete one of its pods and watch the Deployment replace it. Then scale it.

```sh
kubectl -n demo delete pod "$(kubectl -n demo get pods -l app=web --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1:].metadata.name}')"
kubectl -n demo get pods
kubectl -n demo scale deploy/web --replicas=3
```

Roll out a new image, then roll it back.

```sh
kubectl -n demo set image deploy/web web=python:3.13-alpine
kubectl -n demo rollout status deploy/web
kubectl -n demo rollout undo deploy/web
kubectl -n demo rollout status deploy/web
kubectl -n demo rollout history deploy/web
```

**Check:** `rollout history` lists revisions 2 and 3: the new image, and the rollback, which reuses revision 1's template under a new number. `kubectl -n demo get deploy web -o jsonpath='{.spec.template.spec.containers[0].image}'` prints `python:3.12-alpine`.

## 2. Services and DNS

Add a ClusterIP Service and a NodePort Service, and a pod to test from.

Files: [02-services/kustomization.yaml](02-services/kustomization.yaml) · [02-services/web-service.yaml](02-services/web-service.yaml) · [02-services/web-nodeport.yaml](02-services/web-nodeport.yaml)

```sh
kubectl apply -k 02-services
kubectl -n demo run client --image=busybox:1.36 --restart=Never -- sleep 1d
kubectl -n demo wait --for=condition=Ready pod/client
```

Applying the folder also sets the Deployment back to two replicas, because that is what the file says. Reach the app by its Service name, and look at what the name resolves to.

```sh
kubectl -n demo exec client -- wget -qO- http://web
kubectl -n demo exec client -- nslookup web.demo.svc.cluster.local
kubectl -n demo get svc
kubectl -n demo get endpointslices -l kubernetes.io/service-name=web
```

Run the `wget` several times: the `pod:` line changes as the Service spreads requests. A NodePort opens the same port on every node; the nodes are containers, so test from inside one.

```sh
docker exec lab00-control-plane curl -s localhost:30080
```

**Check:** the page prints six lines, starting with `greeting: Hello`. `nslookup` returns the Service's cluster IP, which matches `kubectl -n demo get svc web`. The EndpointSlice lists one address per web pod.

## 3. ConfigMap and Secret

The ConfigMap reaches the app two ways: one key as an environment variable, another as a file. The Secret arrives as an environment variable.

Files: [03-config/kustomization.yaml](03-config/kustomization.yaml) · [03-config/web-config.yaml](03-config/web-config.yaml) · [03-config/db-secret.yaml](03-config/db-secret.yaml) · [03-config/web-patch.yaml](03-config/web-patch.yaml)

```sh
kubectl apply -k 03-config
kubectl -n demo rollout status deploy/web
kubectl -n demo exec client -- wget -qO- http://web
```

Change both ConfigMap keys on the running cluster.

```sh
kubectl -n demo patch configmap web-config --type merge \
  -p '{"data":{"GREETING":"Hello again","message":"Changed while running"}}'
```

Request the page every few seconds for up to a minute. The `message` line changes by itself, because the kubelet rewrites the mounted file. The `greeting` line does not, because a process's environment is fixed when it starts. Restart the pods to pick it up.

```sh
kubectl -n demo exec client -- wget -qO- http://web
kubectl -n demo rollout restart deploy/web
kubectl -n demo rollout status deploy/web
kubectl -n demo exec client -- wget -qO- http://web
```

Look at how the Secret is stored and what the pod sees.

```sh
kubectl -n demo get secret db-secret -o jsonpath='{.data.password}' | base64 -d; echo
kubectl -n demo exec deploy/web -- printenv GREETING REDIS_PASSWORD
```

**Check:** before the restart the page shows the new `message` and the old `greeting`; after it, both are new, and the `secret:` line says `set`. The Secret decodes to plain text with one command: base64 is an encoding, not encryption.

## 4. StatefulSet and persistent volume

Add Redis as a StatefulSet with a volume claim, and point the app at it.

Files: [04-database/kustomization.yaml](04-database/kustomization.yaml) · [04-database/db-service.yaml](04-database/db-service.yaml) · [04-database/db-statefulset.yaml](04-database/db-statefulset.yaml) · [04-database/web-patch.yaml](04-database/web-patch.yaml)

```sh
kubectl apply -k 04-database
kubectl -n demo rollout status statefulset/db
kubectl -n demo rollout status deploy/web
kubectl -n demo get pvc,pv
```

This apply also puts the ConfigMap back to what the file says, undoing the patch from exercise 3. Load the page a few times and watch the counter, then delete the database pod.

```sh
kubectl -n demo exec client -- wget -qO- http://web
kubectl -n demo exec client -- wget -qO- http://web
kubectl -n demo delete pod db-0
kubectl -n demo wait --for=condition=Ready pod/db-0 --timeout=120s
kubectl -n demo exec client -- wget -qO- http://web
```

A StatefulSet pod keeps its name, its volume and its DNS name.

```sh
kubectl -n demo exec client -- nslookup db-0.db.demo.svc.cluster.local
kubectl -n demo exec db-0 -- sh -c 'redis-cli -a "$REDIS_PASSWORD" --no-auth-warning get visits'
```

**Check:** the claim `data-db-0` is `Bound`. The `visits:` count carries on from where it was after `db-0` is deleted and recreated, and `redis-cli` prints the same number.

## 5. Requests, limits and probes

Add CPU and memory requests, a memory limit, and liveness and readiness probes to the web pods.

Files: [05-probes/kustomization.yaml](05-probes/kustomization.yaml) · [05-probes/web-patch.yaml](05-probes/web-patch.yaml)

```sh
kubectl apply -k 05-probes
kubectl -n demo rollout status deploy/web
kubectl -n demo describe deploy web
```

Fail the newest pod's readiness probe. The app reports not ready while the file `/tmp/unready` exists.

```sh
POD=$(kubectl -n demo get pods -l app=web --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1:].metadata.name}')
echo "$POD"
kubectl -n demo exec "$POD" -- touch /tmp/unready
sleep 20
kubectl -n demo get pods -l app=web
kubectl -n demo get endpointslices -l kubernetes.io/service-name=web \
  -o jsonpath='{range .items[*].endpoints[*]}{.targetRef.name}{" ready="}{.conditions.ready}{"\n"}{end}'
kubectl -n demo exec "$POD" -- rm /tmp/unready
```

The pod stays `Running` and is not restarted; it only stops receiving traffic. Compare each pod's memory use with its 96 MiB limit (figures for new pods take about a minute to appear), then push the same pod past the limit by asking the app to hold 200 MB.

```sh
kubectl -n demo top pods
kubectl -n demo exec "$POD" -- wget -qO- 'http://127.0.0.1:8080/hog?mb=200'
sleep 10
kubectl -n demo get pods -l app=web -o custom-columns='NAME:.metadata.name,READY:.status.containerStatuses[0].ready,RESTARTS:.status.containerStatuses[0].restartCount,LAST:.status.containerStatuses[0].lastState.terminated.reason'
kubectl -n demo describe pod "$POD"
```

**Check:** while the flag file exists, the pod shows `0/1` ready and its endpoint shows `ready=false`; about ten seconds after you remove the file it is `1/1` again. The `wget` to `/hog` ends with exit code 137, and the pod then shows one restart with `OOMKilled` as the last state.

## 6. Scheduling: taints, node selection, drain

Pick the worker that does not hold the database. Taint it so ordinary pods stay off it, and label it so the web pods can ask for it.

```sh
DB_NODE=$(kubectl -n demo get pod db-0 -o jsonpath='{.spec.nodeName}')
OTHER=$(kubectl get nodes -l '!node-role.kubernetes.io/control-plane' -o name | grep -vx "node/$DB_NODE" | cut -d/ -f2)
echo "database on $DB_NODE, using $OTHER"
kubectl taint node "$OTHER" dedicated=web:NoSchedule
kubectl label node "$OTHER" role=web
```

Give the web pods a node selector for that label and a toleration for that taint.

Files: [06-scheduling/kustomization.yaml](06-scheduling/kustomization.yaml) · [06-scheduling/web-patch.yaml](06-scheduling/web-patch.yaml)

```sh
kubectl apply -k 06-scheduling
kubectl -n demo rollout status deploy/web
kubectl -n demo get pods -o wide
```

A pod that selects the node but does not tolerate the taint can't be scheduled. Read the scheduler's reason, then delete it.

```sh
kubectl -n demo run notolerate --image=busybox:1.36 --restart=Never \
  --overrides='{"spec":{"nodeSelector":{"role":"web"}}}' -- sleep 1d
sleep 5
kubectl -n demo describe pod notolerate
kubectl -n demo delete pod notolerate --now
```

Undo the pinning, spread four web pods over both workers, and drain the same node.

Files: [05-probes/kustomization.yaml](05-probes/kustomization.yaml) · [05-probes/web-patch.yaml](05-probes/web-patch.yaml)

```sh
kubectl apply -k 05-probes
kubectl taint node "$OTHER" dedicated=web:NoSchedule-
kubectl label node "$OTHER" role-
kubectl -n demo scale deploy/web --replicas=4
kubectl -n demo rollout status deploy/web
kubectl -n demo get pods -o wide
kubectl drain "$OTHER" --ignore-daemonsets --delete-emptydir-data --force
kubectl get nodes
kubectl -n demo get pods -o wide
kubectl uncordon "$OTHER"
```

`--force` is needed only if the `client` pod is on that node: a pod with no controller behind it is deleted by a drain, not moved, which is the difference exercise 1 showed. The drain is on the node without the database for a reason: kind's volumes live on one node's disk, so `db-0` can't follow its data to another node and would stay `Pending`.

**Check:** with the patch applied, both web pods are on `$OTHER`. The `notolerate` pod is `Pending`, and its events say one node didn't match the selector and two had untolerated taints. After the drain, the node shows `Ready,SchedulingDisabled` and all four web pods run on the other worker.

## 7. Namespaces and RBAC

Create a namespace, a ServiceAccount, and a Role that can only read pods.

Files: [07-rbac/kustomization.yaml](07-rbac/kustomization.yaml) · [07-rbac/rbac.yaml](07-rbac/rbac.yaml)

```sh
kubectl apply -k 07-rbac
SA=system:serviceaccount:team-a:reader
kubectl auth can-i list pods -n team-a --as=$SA
kubectl auth can-i delete pods -n team-a --as=$SA
kubectl auth can-i list secrets -n team-a --as=$SA
kubectl auth can-i list pods -n demo --as=$SA
kubectl auth can-i --list -n team-a --as=$SA
```

Act as the ServiceAccount to see the refusal a real client gets.

```sh
kubectl -n team-a get pods --as=$SA
kubectl -n demo get pods --as=$SA
```

**Check:** the four `can-i` answers are `yes`, `no`, `no`, `no`. Listing pods in `team-a` works and finds none; in `demo` it fails with `Forbidden`, because a Role only grants access inside its own namespace.

## 8. Break things and diagnose them

Four workloads, each with one fault. Apply them, wait a minute, and find each fault before reading the answers.

Files: [08-broken/a.yaml](08-broken/a.yaml) · [08-broken/b.yaml](08-broken/b.yaml) · [08-broken/c.yaml](08-broken/c.yaml) · [08-broken/d.yaml](08-broken/d.yaml)

```sh
kubectl create namespace broken
kubectl apply -f 08-broken/
sleep 60
kubectl -n broken get pods,svc,endpointslices
```

The commands that find them:

```sh
kubectl -n broken describe pod -l app=a
kubectl -n broken describe pod -l app=b
kubectl -n broken logs -l app=b --previous
kubectl -n broken describe pod -l app=c
kubectl -n broken get events --sort-by=.lastTimestamp
kubectl -n broken get svc d -o jsonpath='{.spec.selector}'; echo
kubectl -n broken get pods --show-labels
kubectl -n broken debug -it "$(kubectl -n broken get pods -l app=shop -o name)" --image=busybox:1.36 --target=web -- wget -qO- localhost
```

<details>
<summary>Answers</summary>

- **a** is `ImagePullBackOff`: the image tag is misspelled (`alpnie`).
- **b** is `CrashLoopBackOff` though nginx is healthy: the liveness probe checks port 8081, nothing listens there, and the kubelet keeps killing the container.
- **c** is `Pending`: it requests 512 GiB of memory, and the scheduler's event says no node has it.
- **d** runs, but its Service has no endpoints: the Service selects `app=store` and the pods are labelled `app=shop`.

</details>

Fix each one in its file, apply it again, and then remove the namespace.

Files: [08-broken/a.yaml](08-broken/a.yaml) · [08-broken/b.yaml](08-broken/b.yaml) · [08-broken/c.yaml](08-broken/c.yaml) · [08-broken/d.yaml](08-broken/d.yaml)

```sh
kubectl apply -f 08-broken/
kubectl -n broken get pods,endpointslices
kubectl delete namespace broken
```

**Check:** after your fixes, all four pods are `1/1 Running` with no new restarts, and the EndpointSlice for `d` lists an address. [`NOTES.md`](NOTES.md) names the command that exposed each fault.

## 9. The control plane and the kubelet

The control plane runs as static pods: the kubelet on the control-plane node starts them from files on disk, with no Deployment behind them.

```sh
docker exec lab00-control-plane ls /etc/kubernetes/manifests
kubectl -n kube-system get pods -o wide
docker exec lab00-control-plane crictl ps
```

Stop the kubelet on a worker. The node stops reporting, and the control plane marks it `NotReady`.

```sh
docker exec lab00-worker systemctl stop kubelet
kubectl get nodes -w
```

Press Ctrl-C once the node shows `NotReady`. The containers on it keep running, because the kubelet only manages them; the container runtime runs them.

```sh
docker exec lab00-worker crictl ps
kubectl -n demo get pods -o wide
docker exec lab00-worker systemctl start kubelet
kubectl wait --for=condition=Ready node/lab00-worker --timeout=60s
kubectl get nodes
```

**Check:** the manifests folder holds four files: etcd, the API server, the controller manager and the scheduler. The worker turns `NotReady` about 45 seconds after its kubelet stops, `crictl ps` on it still lists running containers, and it is `Ready` again within seconds of the kubelet starting.

## Clean up

```sh
kind delete cluster --name lab00
```

**Published labs:** the official [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/) tutorial covers deploying, exposing, scaling and updating an app. The [iximiuz Kubernetes playground](https://labs.iximiuz.com/playgrounds/k8s-omni) gives a kubeadm cluster of real VMs in the browser. **Differs:** the tutorial stops before storage, scheduling, RBAC and debugging, which later labs lean on; this lab covers them on the same kind setup every later lab uses.
