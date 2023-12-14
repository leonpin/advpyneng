import pytest
import yaml
import socket
import re
from scrapli.exceptions import ScrapliException
from paramiko.ssh_exception import SSHException
from scrapli import Scrapli
from task_1_3 import send_show

with open("devices.yaml") as f:
    devices = yaml.safe_load(f)
reachable = devices['reachable_ssh_telnet']
wrong_pass = devices['reachable_ssh_telnet_wrong_auth_password']
telnet = devices['reachable_telnet_only']
unreachable = devices['unreachable']

correct_return_value = (
    {'sh version | i BOOTLDR': 'BOOTLDR: 7200 Software (C7200-ADVENTERPRISEK9-M), Version '
                               '15.2(4)M11, RELEASE SOFTWARE (fc2)'},
    {'sh version | i BOOTLDR': 'BOOTLDR: 7200 Software (C7200-ADVENTERPRISEK9-M), Version 15.2(4)M11, '
                               'RELEASE SOFTWARE (fc2)',
     'sh ip int bri | b Fast': 'FastEthernet0/0            192.168.100.1   YES NVRAM  up                    up\n'
                               'FastEthernet0/1            unassigned      YES NVRAM  administratively down down'}
)


def test_return_type():
    result = send_show(reachable[0], 'sh clock')
    assert isinstance(result, dict) or result is None


def test_error(capsys):
    send_show(wrong_pass[0], 'sh clock')
    correct = 'Error'
    out, err = capsys.readouterr()
    assert out != ''
    assert wrong_pass[0]['host'] in out and correct in out


@pytest.mark.parametrize('command, result', [
    ('sh version | i BOOTLDR', correct_return_value[0]),
    (['sh version | i BOOTLDR', 'sh ip int bri | b Fast'], correct_return_value[1])]
                         )
def test_result(command, result):
    assert result == send_show(reachable[0], command)
