# Ansible Firewalld Exercise

Ansible playbook that opens TCP port 80 on a remote host using `firewalld`.

## Files

- `inventory.ini` — inventory defining the `myhosts` group and target host.
- `firewalld_setup.yml` — playbook that opens port 80/tcp and reloads firewalld.
- `devops/ansible_firewall_project.md` — write-up of the exercise with explanation and verification.

## Prerequisites

- Target host is Linux with `firewalld` installed and running.
- SSH access to the target host from your control machine.
- `ansible.posix` collection installed:

```bash
ansible-galaxy collection install ansible.posix
```

## Usage

```bash
ansible -i inventory.ini myhosts -m ping
ansible-playbook -i inventory.ini firewalld_setup.yml
```

## Verify

```bash
sudo firewall-cmd --list-ports
```

Expected output includes `80/tcp`.
