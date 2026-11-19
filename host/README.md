# Host

Ansible that builds the lab host described in [docs/host-setup.md](../docs/host-setup.md). It is safe to run repeatedly and safe to point at a host that is already doing other work.

## Use

```sh
cd host
cp inventory/hosts.example.yml inventory/hosts.yml   # git-ignored; edit it
ansible-playbook site.yml --check --diff             # dry run: shows what would change
ansible-playbook site.yml                            # apply
ansible-playbook site.yml                            # again: reports changed=0
ansible-playbook site.yml --tags tools               # one feature only
```

Needs only `ansible-core` on the controller, and SSH with sudo on the host. Supported hosts: RedHat family (tested on Rocky 9) and Debian family (written for Ubuntu, not yet tested), x86_64 or aarch64.

## What it changes

| Feature | Variable | Tag | What happens |
| --- | --- | --- | --- |
| Snapshot | `lab_snapshot_enabled` | `snapshot` | Before the first change, saves a record of the host to `/var/lib/infra-labs/snapshot.tar.gz` |
| Base packages | `lab_base_packages_enabled` | `packages` | Installs tcpdump, tshark, ethtool, iperf3, jq, git where missing |
| inotify limits | `lab_sysctl_enabled` | `sysctl` | Raises values that are below the minimum, now and in `/etc/sysctl.d/90-infra-labs.conf` |
| MPLS | `lab_mpls_enabled` | `mpls` | Loads `mpls_router` and `mpls_iptunnel` now and at boot; sets the label space |
| KSM | `lab_ksm_enabled` | `ksm` | Turns kernel same-page merging on now and at boot |
| zram swap | `lab_zram_enabled` | `zram` | Installs zram-generator with an 8 GB device, unless the host already has zram |
| Docker CE | `lab_docker_enabled` | `docker` | Installs Docker from Docker's repository **only if no Docker is present** |
| libvirt | `lab_libvirt_enabled` | `libvirt` | Installs libvirt and QEMU; keeps the default NAT network off |
| Group membership | `lab_users` | `users` | Adds the listed users to `docker` |
| Tools | `lab_tools_enabled` | `tools` | Installs kind, kubectl, helm, cilium, hubble, containerlab and gnmic to `/usr/local/bin`, pinned by version and SHA-256 |

Settings are in [roles/lab_host/defaults/main.yml](roles/lab_host/defaults/main.yml) and describe a dedicated lab host. Turn features off per host in the inventory. A mistyped setting fails the run before anything changes.

Not automated: disk layout, unattended upgrades, the local registry, netlab, vrnetlab image builds and Edgeshark.

containerlab is installed as a plain binary and needs root. On RedHat-family hosts `sudo` does not search `/usr/local/bin`, so run it as `sudo /usr/local/bin/containerlab`.

## How it is built

One role, [roles/lab_host](roles/lab_host), with one task file per feature. Each feature file reads the state it needs, changes only what differs, and leaves the rest alone. The role keeps no state of its own between runs: what it should do is decided from the host and the settings every time.

Every file the role writes starts with the line `Managed by the infra-labs lab_host role`, so `grep -rl 'infra-labs lab_host' /etc` lists them.

Each feature ends by checking its own result, and fails the run if it is not as intended: the sysctl values are at least the minimum, Docker is running, every tool runs and reports a version.

## Shared and production hosts

- **An existing Docker is never modified.** No package changes, no `daemon.json`, no restart. The run fails at the end if the Docker daemon's start time changed or a container that was running has stopped.
- **Nothing is restarted or rebooted**, and no firewall rule is touched.
- **Sysctl values only go up.** A value the host already has at or above the minimum is not written anywhere.
- **Existing zram is left alone**, whether it comes from a zram-generator config the role did not write or from somewhere else.
- **Binaries in `/usr/local/bin` with the same names are replaced.** Check for your own `kubectl` or `helm` there first; the dry run lists each tool it would install.
- **Installing a package can upgrade another.** The package manager may upgrade something already on the host to satisfy a dependency (libvirt pulled in a newer systemd in testing). `dnf install --assumeno <package>` or `apt-get install -s <package>` shows this beforehand.

There is no automated revert. To back a change out by hand, the snapshot records what the host looked like before the first run: packages, sysctls, modules, addresses, routes, listening ports, running services, firewall rules and containers. It is readable by root only and is never rewritten.

Use the conservative settings in [inventory/hosts.example.yml](inventory/hosts.example.yml), and always start with `--check --diff`.

This repo is public. Keep real host names and addresses in `inventory/hosts.yml`, never in committed files.

## Upgrading a tool

Change `version`, `url` and both `sha256` values for the tool in the defaults file, then run `ansible-playbook site.yml --tags tools`. The old binary is replaced.
