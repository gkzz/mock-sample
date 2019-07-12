# Mock-Sample

**This Project is created because I would like to learn how mock works.**

<img src="/docs/demo/system_status.gif " alt="Demo to execute systemctl status" style="max-width:100%;">

# Table of Contents
- Technologies Used
- How to setup
- Notes
- Sources


# Technologies Used
- Python 3.6.7
- paramiko==2.6.0
- PyYAML==5.1.1
- SAKURA Internet [Virtual Private Server SERVICE


# How to setup

```
$ sudo apt-get update -y
$ python2.7 -m virtualenv 27 && source 27/bin/activate
$ cd 27 && pip install --upgrade pip && pip install -r requirements_dev.txt
```

# How to run unittest
<img src="/docs/demo/develmock.gif " alt="Demo to run unittest with mock" style="max-width:100%;">
```
$ ls tests/ | grep test
test_ls_dir.py
$ python -m unittest tests.test_ls_dir
```

## Trobleshooting
`being prepared`



# Notes

```
$ cat /etc/os-release 
NAME="Ubuntu"
VERSION="19.04 (Disco Dingo)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 19.04"
VERSION_ID="19.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=disco
UBUNTU_CODENAME=disco

$ $ tree -L 3
.
├── common.py
├── common.pyc
├── docs
│   └── demo
│       └── system_status.gif
├── driver.py
├── __init__.py
├── __init__.pyc
├── input.yml
├── input.yml.dummy
├── logs
│   ├── log_xx_xx.json
│   ├── log_xx_xx.csv
├── ls_dir.py
├── ls_dir.pyc
├── ps_aux.pyc
├── README.md
├── requirements_dev.txt
├── requirements.txt
├── system_status.py
├── system_status.pyc
    ├── config
    │   ├── response.yml
    │   ├── response.yml.dummy
    │   ├── test_input.yml
    │   ├── test_input.yml.dummy
    │   ├── test_output.yml
    │   └── test_output.yml.dummy
    ├── __init__.py
    ├── __init__.pyc
    ├── test_ls_dir.py
    └── test_ls_dir.pyc

15 directories, 70 files
```