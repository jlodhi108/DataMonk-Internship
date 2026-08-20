# Ansible Firewalld Project — Enable Port 80

## Objective
Use Ansible to open TCP port 80 on a remote host managed by `firewalld`, using
a playbook with a handler that reloads the firewall only when a change is made.

## Files
- `inventory.ini` — defines the `myhosts` group with target host(s).
- `firewalld_setup.yml` — the playbook that opens port 80/tcp.

## Playbook Explanation

```yaml
- name: Enable Port 80 Using Firewalld
  hosts: myhosts
  become: yes
```
Targets the `myhosts` group from the inventory and escalates privileges
(`become: yes` is equivalent to running tasks with `sudo`), since managing
firewalld requires root.

```yaml
  tasks:
    - name: Enable port 80/tcp in firewalld
      ansible.posix.firewalld:
        port: 80/tcp
        permanent: true
        state: enabled
      notify: Reload firewalld
```
Uses the `firewalld` module to open port 80/tcp.
- `permanent: true` writes the rule to firewalld's persistent config so it
  survives a reboot (without this, the rule only applies to the current
  runtime firewall state).
- `state: enabled` means "make sure this port is open."
- `notify: Reload firewalld` tells Ansible to trigger the `Reload firewalld`
  handler, but only if this task actually changes something.

```yaml
  handlers:
    - name: Reload firewalld
      service:
        name: firewalld
        state: reloaded
```
Handlers run once, at the end of the play, and only if notified. Here it
reloads the `firewalld` service so the new permanent rule takes effect
immediately in the running firewall.

## How to Run

```bash
ansible-playbook -i inventory.ini firewalld_setup.yml
```

## Verification

On the target host:

```bash
sudo firewall-cmd --list-ports
```

Expected output includes:

```
80/tcp
```

## Output Screenshot
_(insert screenshot of the `ansible-playbook` run and `firewall-cmd --list-ports` output here)_
