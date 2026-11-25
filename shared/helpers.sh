# Helpers for the Verify checks in each lab's README.
#
#   source shared/helpers.sh lab03
#
# The argument is the containerlab topology name, so the helpers address
# containers as clab-<name>-<node>. See docs/verify.md for the conventions.

if [ -n "${1:-}" ]; then
  LAB="$1"
fi
if [ -z "${LAB:-}" ]; then
  echo "usage: source shared/helpers.sh <containerlab name, e.g. lab03>" >&2
  return 1 2>/dev/null || exit 1
fi

# Run a command in a lab node:            on client curl -s http://10.0.0.1
on() {
  local node="$1"
  shift
  docker exec "clab-$LAB-$node" "$@"
}

# Run a CLI command on a switch or router:
#   srl leaf1 "show version"              Nokia SR Linux
#   eos leaf1 "show version"              Arista cEOS
#   frr client "show bgp summary"         FRR, and VyOS (which runs FRR)
#   xr  p1 "show mpls forwarding"         Cisco XRd
srl() { docker exec "clab-$LAB-$1" sr_cli "$2"; }
eos() { docker exec "clab-$LAB-$1" Cli -p 15 -c "$2"; }
frr() { docker exec "clab-$LAB-$1" vtysh -c "$2"; }
xr()  { docker exec "clab-$LAB-$1" /pkg/bin/xr_cli.sh "$2"; }

# Capture on a node's interface from the host, without tcpdump in the image:
#   cap leaf1 -i e1-49 udp port 4789 -c 5
cap() {
  local node="$1"
  shift
  sudo ip netns exec "clab-$LAB-$node" tcpdump -nn "$@"
}

# Run the Cilium agent's own CLI:         cil status
cil() {
  kubectl -n kube-system exec ds/cilium -c cilium-agent -- cilium-dbg "$@"
}

# Address of a LoadBalancer service:      SVC_IP=$(svc_ip demo web)
svc_ip() {
  kubectl -n "$1" get svc "$2" -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
}
