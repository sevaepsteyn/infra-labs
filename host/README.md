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

Needs only `ansible-core` on the machine you run it from, and SSH with sudo on the host. Supported hosts: RedHat family (tested on Rocky 9 and AlmaLinux 10) and Debian family (written for Ubuntu, not yet tested), x86_64 or aarch64.

### Run it on the host itself

The playbook can also run on the host it builds, with no second machine. The role installs `ansible-core` as a base package, so a host built remotely can already do this; on a fresh host, install it by hand first.

```sh
sudo dnf install -y ansible-core git                 # Debian family: sudo apt-get install -y ansible-core git
git clone https://github.com/sevaepsteyn/infra-labs.git
cd infra-labs/host
cp inventory/hosts.example.yml inventory/hosts.yml   # use the localhost entry, remove the others
ansible-playbook site.yml --check --diff
ansible-playbook site.yml
```

The `localhost` entry sets `ansible_connection: local`, so nothing goes over SSH. Add `-K` to the `ansible-playbook` commands if `sudo` asks for a password.

## What it changes

| Feature | Variable | Tag | What happens |
| --- | --- | --- | --- |
| Base packages | `lab_base_packages_enabled` | `packages` | Installs tcpdump, tshark, ethtool, iperf3, jq, git and ansible-core where missing |
| inotify limits | `lab_sysctl_enabled` | `sysctl` | Raises values that are below the minimum, now and in `/etc/sysctl.d/90-infra-labs.conf` |
| MPLS | `lab_mpls_enabled` | `mpls` | Loads `mpls_router` and `mpls_iptunnel` now and at boot; sets the label space |
| KSM | `lab_ksm_enabled` | `ksm` | Turns kernel same-page merging on now and at boot |
| zram swap | `lab_zram_enabled` | `zram` | Installs zram-generator with an 8 GB device, unless the host already has zram |
| Docker CE | `lab_docker_enabled` | `docker` | Installs Docker from Docker's repository **only if no Docker is present** |
| libvirt | `lab_libvirt_enabled` | `libvirt` | Installs libvirt and QEMU; leaves the default NAT network as it is |
| Group membership | `lab_users` | `users` | Adds the listed users to `docker` |
| Tools | `lab_tools_enabled` | `tools` | Installs kind, kubectl, helm, cilium, hubble, containerlab and gnmic to `/opt/infra-lab/bin`, pinned by version and SHA-256, and adds that directory to `PATH` |

Settings are in [roles/lab_host/defaults/main.yml](roles/lab_host/defaults/main.yml) and describe a dedicated lab host. Turn features off per host in the inventory. A mistyped setting fails the run before anything changes.

Not automated: unattended upgrades, the local registry, netlab, vrnetlab image builds and Edgeshark.

Everything the role installs goes under `/opt/infra-lab`: binaries in `bin`, downloads in `cache`. Outside it the role writes only small config files under `/etc`. `/etc/profile.d/infra-labs.sh` appends the `bin` directory to `PATH`, so log in again after the first run.

containerlab is installed as a plain binary and needs root. `sudo` does not search `/opt/infra-lab/bin`, so run it as `sudo /opt/infra-lab/bin/containerlab`.

## How it is built

One role, [roles/lab_host](roles/lab_host), with one task file per feature. Each feature file reads the state it needs, changes only what differs, and leaves the rest alone. The role keeps no state of its own between runs: what it should do is decided from the host and the settings every time.

Every file the role writes starts with the line `Managed by the infra-labs lab_host role`, so `grep -rl 'infra-labs lab_host' /etc` lists them.

Each feature ends by checking its own result, and fails the run if it is not as intended: the sysctl values are at least the minimum, Docker is running, every tool runs and reports a version.

## Shared and production hosts

- **An existing Docker is never modified.** No package changes, no `daemon.json`, no restart. The run fails at the end if the Docker daemon's start time changed or a container that was running has stopped.
- **Nothing is restarted or rebooted**, and the role touches no firewall rule.
- **A new Docker install brings its own network changes.** On a host with no Docker, starting it for the first time creates `docker0`, turns on `net.ipv4.ip_forward`, adds Docker's NAT and filter rules, and sets the `FORWARD` chain policy to `drop`. Set `lab_docker_enabled: false` if the host routes other traffic and you have not planned for that.
- **Sysctl values only go up.** A value the host already has at or above the minimum is not written anywhere.
- **Existing zram is left alone**, whether it comes from a zram-generator config the role did not write or from somewhere else.
- **The host's own tools win.** `/opt/infra-lab/bin` goes at the end of `PATH`, so a `kubectl` or `helm` the host already has is the one that runs; call the lab's by full path.
- **Docker's and libvirt's default NAT networks are left alone**, on a new install as on an existing one. Set `lab_libvirt_default_network_off` to turn libvirt's off.
- **Installing a package can upgrade another.** The package manager may upgrade something already on the host to satisfy a dependency (libvirt pulled in a newer systemd in testing). `dnf install --assumeno <package>` or `apt-get install -s <package>` shows this beforehand.

There is no automated revert. Use the conservative settings in [inventory/hosts.example.yml](inventory/hosts.example.yml), and always start with `--check --diff`.

This repo is public. Keep real host names and addresses in `inventory/hosts.yml`, never in committed files.

## Upgrading a tool

Change `version`, `url` and both `sha256` values for the tool in the defaults file, then run `ansible-playbook site.yml --tags tools`. The old binary is replaced.
