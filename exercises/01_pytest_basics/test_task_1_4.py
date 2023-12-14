import pytest
import yaml
from task_1_4 import CiscoTelnet

# with open('devices_reachable.yaml') as f:
#     devices_param = yaml.safe_load(f)
#     devices_telnet = []
#     dev_telnet = {}
#     for dev in devices_param:
#         dev_telnet['host'] = dev['host']
#         dev_telnet['username'] = dev['auth_username']
#         dev_telnet['password'] = dev['auth_password']
#         dev_telnet['secret'] = dev['auth_secondary']
#         devices_telnet.append(dev_telnet.copy())


r1_params = {
    "host": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}

r1_hostname = "R"


@pytest.fixture(params=["cisco", None])
def telnet_conn(request):
    r_params = {
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": request.param,
    }
    with CiscoTelnet(**r_params) as telnet:
        yield telnet


def test_class(telnet_conn):
    prompt = telnet_conn.prompt
    assert prompt in ('>', '#')


@pytest.mark.parametrize('command', ['sh clock', 'sh run | i hostname'])
def test_command(command):
    with CiscoTelnet(**r1_params) as telnet:
        assert r1_hostname in telnet.send_showa_command(command)

