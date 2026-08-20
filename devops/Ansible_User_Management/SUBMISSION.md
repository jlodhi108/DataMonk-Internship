# Ansible User Management Role — Submission

## Task
Build a simple Ansible role (`user_manager`) that creates a Linux user, sets up
their home directory, and deploys a personalized welcome file, then run it
against a real target and re-run it with a different username to prove
reusability.

## Target host
- Provider: AWS EC2
- OS: Amazon Linux 2023
- SSH user: `ec2-user`
- Connected via key pair: `ansible-key.pem`

## Role structure
```
my-first-role/
├── inventory.ini
├── user-management.yml
└── roles/
    └── user_manager/
        ├── tasks/main.yml
        ├── templates/welcome.txt.j2
        └── defaults/main.yml
```

## Run 1 — username: ansible_student
```
$ ansible-playbook -i inventory.ini user-management.yml

TASK [user_manager : Create a new user] *****
changed: [13.233.121.73]

TASK [user_manager : Deploy welcome message to user's home] *****
changed: [13.233.121.73]

TASK [user_manager : Display success message] *****
ok: [13.233.121.73] => {
    "msg": "User ansible_student has been created successfully!"
}

PLAY RECAP *****
13.233.121.73  : ok=4  changed=2  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
```

`changed=2` — the user account and the README.txt did not exist yet, so
Ansible created both.

## Run 2 — username changed to devops_user
Changed `vars.username` in `user-management.yml` from `ansible_student` to
`devops_user`, then re-ran the same command.

```
$ ansible-playbook -i inventory.ini user-management.yml

TASK [user_manager : Create a new user] *****
ok: [13.233.121.73]

TASK [user_manager : Deploy welcome message to user's home] *****
ok: [13.233.121.73]

TASK [user_manager : Display success message] *****
ok: [13.233.121.73] => {
    "msg": "User devops_user has been created successfully!"
}

PLAY RECAP *****
13.233.121.73  : ok=4  changed=0  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
```

The first user (`ansible_student`) was left untouched — only `devops_user`
was created, showing the same role works for any username via `vars`.

## Generated README.txt (rendered from the Jinja2 template)
```
Congratulations! You successfully used an Ansible role!

Hello devops_user!

This file was created automatically by Ansible on 2026-08-19.

Your account details:
- Username: devops_user
- Shell: /bin/bash
- Home Directory: /home/devops_user
- Server: ip-172-31-1-185
- OS: Amazon

Happy learning!
```

## Key takeaways
- `defaults/main.yml` variables are overridden by the playbook's `vars:` block.
- The `template` module uses Jinja2 (`{{ }}`) and Ansible facts
  (`ansible_date_time`, `ansible_hostname`, `ansible_distribution`) gathered
  automatically from the target at playbook start.
- Ansible is idempotent: re-running an unchanged playbook reports
  `changed=0` because the desired state already matches reality.
- New home directories default to `0700` permissions, so verifying file
  contents from a different SSH user (`ec2-user`) requires `sudo`.
